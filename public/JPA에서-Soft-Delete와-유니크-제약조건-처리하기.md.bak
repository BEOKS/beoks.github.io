JPA를 사용하면서 **[[Soft Delete]]** 를 구현할 때, 유니크 제약조건을 가진 필드 때문에 새로운 데이터를 삽입할 때 문제가 발생할 수 있습니다. 특히, 이미 Soft Delete된 엔티티가 동일한 유니크 키를 가지고 있을 경우, 새로운 데이터를 삽입하려고 하면 데이터베이스는 여전히 유니크 키 제약조건 위반을 발생시킵니다.

이번 글에서는 이러한 문제를 해결하기 위한 간단한 방법을 소개하겠습니다. 기존의 Soft Delete된 엔티티를 다시 활성화하면서 유니크 제약조건 오류를 우회하는 방법입니다.

## 문제 상황

- **[[Soft Delete]]**: 엔티티를 삭제할 때 실제로 데이터베이스에서 삭제하지 않고, `isDeleted`와 같은 플래그를 `true`로 설정하여 논리적으로 삭제 처리합니다.
- **유니크 제약조건**: 특정 필드(예: `uniqueField`)에 유니크 제약조건이 설정되어 있어 중복된 값을 허용하지 않습니다.
- **문제점**: Soft Delete된 엔티티가 동일한 유니크 키를 가지고 있을 때, 새로운 엔티티를 삽입하면 유니크 제약조건 위반이 발생합니다. 데이터베이스는 `isDeleted` 플래그를 고려하지 않고 유니크 키 중복을 검사하기 때문입니다.

## 해결 방법

1. **Soft Delete된 엔티티를 포함하여 동일한 유니크 키를 가진 엔티티를 검색합니다.**
2. **만약 존재한다면, 해당 엔티티의 `isDeleted` 플래그를 `false`로 변경하여 다시 활성화합니다.**
3. **필요한 필드를 업데이트하고 엔티티를 저장합니다.**
4. **존재하지 않는다면, 새로운 엔티티를 생성하여 저장합니다.**

## 구현 방법

### 1. 엔티티 설정

우선, Soft Delete를 구현하기 위해 엔티티에 `isDeleted` 플래그를 추가합니다.

```java
@Entity
@Table(name = "your_entity")
@SQLDelete(sql = "UPDATE your_entity SET is_deleted = true WHERE id = ?")
@Where(clause = "is_deleted = false")
public class YourEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(unique = true)
    private String uniqueField;

    // 기타 필드들...

    @Column(name = "is_deleted")
    private boolean isDeleted = false;

    // getter, setter...
}
```

- `@SQLDelete`를 사용하여 삭제 시 `is_deleted` 필드를 `true`로 설정합니다.
- `@Where`를 사용하여 조회 시 `is_deleted = false`인 엔티티만 가져오도록 합니다.

### 2. 리포지토리에 커스텀 메서드 추가

Soft Delete된 엔티티를 포함하여 유니크 키로 엔티티를 검색하는 메서드를 추가합니다.

```java
public interface YourEntityRepository extends JpaRepository<YourEntity, Long> {

    @Query(value = "SELECT * FROM your_entity WHERE unique_field = :uniqueField", nativeQuery = true)
    Optional<YourEntity> findByUniqueFieldIncludeDeleted(@Param("uniqueField") String uniqueField);
}
```

- `nativeQuery`를 사용하여 직접 SQL로 조회하면 `@Where` 조건을 무시하고 모든 엔티티를 가져올 수 있습니다.

### 3. 서비스 레이어에서 로직 구현

엔티티를 저장하거나 업데이트하는 로직을 서비스에서 구현합니다.

```java
@Service
public class YourEntityService {

    private final YourEntityRepository yourEntityRepository;

    public YourEntityService(YourEntityRepository yourEntityRepository) {
        this.yourEntityRepository = yourEntityRepository;
    }

	@Transactional
    public YourEntity saveOrUpdate(YourEntity newEntity) {
        Optional<YourEntity> existingEntityOpt = yourEntityRepository.findByUniqueFieldIncludeDeleted(newEntity.getUniqueField());

        if (existingEntityOpt.isPresent()) {
            YourEntity existingEntity = existingEntityOpt.get();
            if (existingEntity.isDeleted()) {
                // Soft Delete된 엔티티를 다시 활성화
                existingEntity.setDeleted(false);
                // 필요한 필드 업데이트
                existingEntity.setOtherField(newEntity.getOtherField());
                // 엔티티 저장
                return yourEntityRepository.save(existingEntity);
            } else {
                // 이미 존재하는 엔티티 처리 (예: 오류 발생)
                throw new RuntimeException("이미 존재하는 엔티티입니다.");
            }
        } else {
            // 새로운 엔티티 저장
            return yourEntityRepository.save(newEntity);
        }
    }
}
```

- 기존 엔티티가 존재하는지 확인합니다.
- Soft Delete된 엔티티라면 `isDeleted`를 `false`로 변경하고 필요한 필드를 업데이트합니다.
- 엔티티를 저장합니다.
- 존재하지 않는다면 새로운 엔티티를 생성하여 저장합니다.

## 주의사항

- **네이티브 쿼리 사용 시 데이터베이스 종속성**: 네이티브 쿼리는 특정 데이터베이스에 종속적일 수 있으므로 주의해야 합니다.
- **트랜잭션 처리**: 서비스 레이어에서 트랜잭션 처리를 적절히 설정하여 데이터 일관성을 유지해야 합니다.
- **동시성 문제**: 다중 스레드 환경에서 동일한 유니크 키로 동시 요청이 발생할 수 있으므로 필요에 따라 락을 고려해야 합니다.

## 마치며

JPA에서 Soft Delete를 사용하면서 유니크 제약조건으로 인해 발생하는 문제를 간단하게 해결하는 방법을 알아보았습니다. 핵심은 Soft Delete된 데이터를 포함하여 기존 데이터를 확인하고, 필요에 따라 재활성화하는 것입니다.

이 방법을 통해 유니크 제약조건 위반을 방지하고 데이터의 무결성을 유지할 수 있습니다. 프로젝트에 맞게 예시 코드를 일반화하여 적용해보시기 바랍니다.