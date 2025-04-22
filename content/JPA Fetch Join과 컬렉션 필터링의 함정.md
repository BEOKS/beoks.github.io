
오늘은 개발 프로젝트를 진행하면서 [[JPA]]와 [[QueryDSL]]을 사용하다 마주쳤던 문제와 그 해결 과정을 공유하고자 합니다. 특히 [[Fetch Join]]을 사용하여 연관된 컬렉션을 함께 조회할 때, 특정 조건으로 필터링하면 예상과 다른 결과가 나오는 상황이었죠.

## 문제 상황: 사라진 IP 주소들

저희는 `Device`라는 엔티티와, 이 `Device`가 가질 수 있는 여러 개의 `IpAddress` 엔티티(1:N 관계)를 관리하고 있었습니다. 요구사항은 **특정 IP 주소를 가진 `Device`를 찾되, 찾아낸 `Device`가 가진 모든 IP 주소 정보를 함께 조회**하는 것이었습니다.

[[N+1 문제]]를 피하기 위해 자연스럽게 [[Fetch Join]]을 사용하여 `Device`를 조회하면서 연관된 `IpAddress` 목록도 한 번에 가져오려고 했습니다. QueryDSL 코드는 대략 아래와 같은 형태였습니다.

```java
// 개념적인 초기 접근 방식 (문제가 있는 코드)
QDevice device = QDevice.device;
QIpAddress ipAddress = QIpAddress.ipAddress;
String searchIp = "192.168.0.10"; // 예시 검색 IP

List<Device> devices = queryFactory
    .selectFrom(device)
    .leftJoin(device.ipAddresses, ipAddress).fetchJoin() // IpAddress 컬렉션을 Fetch Join
    .where(ipAddress.address.contains(searchIp)) // !!! IP 주소 조건 필터링 !!!
    .fetch();

// 이후 devices 리스트의 각 device 객체를 확인해보면...
for (Device d : devices) {
    System.out.println("Device ID: " + d.getId());
    // d.getIpAddresses()에는 searchIp와 일치하는 IP 객체만 들어있음!
    System.out.println("IPs: " + d.getIpAddresses());
}
````

쿼리 자체는 문제없이 실행되었지만, 결과가 이상했습니다. 예를 들어 ID가 1인 `Device`가 "192.168.0.10", "192.168.0.11", "192.168.0.12" 세 개의 IP를 가지고 있을 때, "192.168.0.10"으로 검색하면 결과 `Device` 객체의 `ipAddresses` 컬렉션에는 "192.168.0.10"에 해당하는 `IpAddress` 객체 _하나만_ 들어있었습니다. 나머지 ".11", ".12" IP 정보는 사라져 버렸죠. 저희가 원했던 것은 ID 1번 `Device`와 그에 속한 _모든_ IP 정보였습니다.

## 원인 분석: Fetch Join과 WHERE 절의 상호작용

이 문제의 원인은 [[ORM (Object-Relational Mapping)]]의 동작 방식, 특히 `Fetch Join`과 `WHERE` 절이 데이터베이스 쿼리 레벨에서 어떻게 상호작용하는지에 대한 이해 부족이었습니다.

1. **SQL 변환**: `WorkspaceJoin`을 사용하면 JPA는 `Device` 테이블과 `IpAddress` 테이블을 조인하는 SQL을 생성합니다. 예를 들면 `SELECT d.*, ip.* FROM device d LEFT OUTER JOIN ip_address ip ON d.id = ip.device_id ...` 와 같은 형태가 됩니다.
2. **WHERE 절 필터링**: 여기에 `where(ipAddress.address.contains(searchIp))` 조건이 추가되면, 데이터베이스는 조인된 결과 _로우(row)_ 중에서 `ip_address` 테이블의 `address` 컬럼 값이 `searchIp`를 포함하는 로우만 필터링합니다.
3. **객체 매핑**: JPA는 이렇게 필터링된 로우들을 기반으로 `Device` 객체와 그 안의 `ipAddresses` 컬렉션을 재구성합니다.

결과적으로, 데이터베이스 레벨에서 `searchIp`와 일치하지 않는 IP 주소 정보를 가진 로우는 이미 걸러졌기 때문에, 최종 `Device` 객체에는 검색 조건에 맞았던 `IpAddress` 정보만 남게 되는 것이었습니다. 즉, 쿼리는 "특정 IP를 가진 **Device-IP 조합 로우**"를 찾은 것이지, "특정 IP를 가진 **Device 엔티티**를 찾아서 그 엔티티의 모든 IP를 가져온 것"이 아니었던 거죠.

## 해결책: 서브쿼리(Subquery)의 도입

이 문제를 해결하기 위한 핵심 아이디어는 **"어떤 Device를 가져올지 결정하는 조건"** 과 **"가져올 Device의 데이터를 구성하는 방법"** 을 분리하는 것이었습니다. 즉, `WHERE` 절에서는 `Device`가 특정 IP를 가지고 있는지 _존재 여부_만 확인하고, `SELECT` 절과 `WorkspaceJoin`은 조건에 맞는 `Device`의 모든 `IpAddress`를 가져오도록 해야 했습니다.

이를 위해 [[QueryDSL]]의 [[Subquery]] 기능, 특히 `EXISTS` 연산자를 사용하기로 결정했습니다.

```java
// 개념적인 수정된 접근 방식 (서브쿼리 사용)
QDevice device = QDevice.device;
QIpAddress ipAddress = QIpAddress.ipAddress; // 메인 쿼리용
String searchIp = "192.168.0.10";

// 서브쿼리용 Q-Type 별칭 (메인 쿼리와 구분)
QIpAddress subIpAddress = new QIpAddress("subIpAddress");

List<Device> devices = queryFactory
    .selectFrom(device)
    .leftJoin(device.ipAddresses, ipAddress).fetchJoin() // IpAddress 컬렉션을 Fetch Join (이제 안전함)
    .where(
        // 서브쿼리 시작: 이 Device에 연결된 IP 중 검색 조건에 맞는 것이 존재하는가?
        JPAExpressions.selectOne()
            .from(subIpAddress)
            .where(
                subIpAddress.device.id.eq(device.id) // 메인 쿼리의 device와 연결 (Correlated Subquery)
                .and(subIpAddress.address.contains(searchIp)) // 실제 IP 조건 확인
            )
            .exists() // 존재 여부만 확인
    )
    .fetch();

// 이제 devices 리스트의 각 device 객체는 모든 IP 주소 정보를 포함합니다.
for (Device d : devices) {
    System.out.println("Device ID: " + d.getId());
    // d.getIpAddresses()에는 해당 Device의 모든 IP 객체가 들어있음!
    System.out.println("IPs: " + d.getIpAddresses());
}
```

**변경된 부분:**

1. **`WHERE` 절 변경**: `ipAddress.address.contains(searchIp)`를 직접 사용하는 대신, `JPAExpressions.select(...).exists()`를 사용했습니다.
2. **서브쿼리**: 서브쿼리는 현재 메인 쿼리에서 평가 중인 `device`와 연결된(`subIpAddress.device.id.eq(device.id)`) `IpAddress` 중에서 `searchIp`를 포함하는 레코드가 있는지 확인합니다. 이 연결 방식은 [[Correlated Subquery]]라고 합니다.
3. **`exists()`**: 서브쿼리가 하나 이상의 로우를 반환하면 `true`를 반환하여 해당 `Device`를 결과에 포함시킵니다. 중요한 점은 서브쿼리가 `Device` 선택 여부만 결정하고, 메인 쿼리의 `WorkspaceJoin`은 여전히 모든 `IpAddress`를 로드한다는 것입니다.

이 수정 덕분에, 검색 조건에 맞는 IP를 가진 `Device`를 정확히 찾아내고, 해당 `Device`가 가진 모든 IP 주소 정보를 온전히 조회할 수 있게 되었습니다.

## 결론

이번 경험을 통해 몇 가지 중요한 점을 다시 한번 깨달았습니다.

1. **ORM 동작 방식 이해**: [[JPA]]나 [[Hibernate]]와 같은 [[ORM]] 프레임워크는 편리하지만, 내부적으로 SQL을 어떻게 생성하고 객체를 어떻게 매핑하는지 이해하는 것이 중요합니다. 특히 `WorkspaceJoin`과 같은 최적화 기능을 사용할 때는 더욱 그렇습니다.
2. **조건 필터링 위치**: 컬렉션의 내용을 기준으로 메인 엔티티를 필터링해야 할 때는 `WHERE` 절에서 직접 컬렉션 필드를 필터링하는 것의 부작용을 인지해야 합니다.
3. **서브쿼리의 유용성**: "관련된 무언가가 존재하는가?" 형태의 조건을 확인해야 할 때 [[Subquery]]와 [[EXISTS Operator]]는 매우 효과적인 해결책이 될 수 있습니다.