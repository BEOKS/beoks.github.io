개발하면서 Hibernate를 사용하여 엔티티를 매핑할 때 `cascade="all-delete-orphan"` 설정을 사용하면 편리하게 참조되지 않는 엔티티를 자동으로 삭제할 수 있습니다. 그러나 이 설정을 사용할 때 컬렉션을 새로운 인스턴스로 교체하면 다음과 같은 예외가 발생할 수 있습니다:

```
org.hibernate.HibernateException: A collection with cascade="all-delete-orphan" was no longer referenced by the owning entity instance: com.example.domain.entity.SubAccount.networkDiagrams
```

이번 글에서는 이 오류의 원인과 해결 방법을 상세하게 알아보겠습니다.

## 오류의 원인 이해하기

`HibernateException` 오류 메시지를 보면 `cascade="all-delete-orphan"`이 설정된 컬렉션이 더 이상 소유 엔티티 인스턴스에서 참조되지 않는다고 명시하고 있습니다.

Hibernate는 엔티티의 상태 변화와 연관된 컬렉션을 추적하여 변경 사항을 데이터베이스에 반영합니다. 특히 `cascade="all-delete-orphan"` 또는 `orphanRemoval = true`로 설정된 컬렉션의 경우, 컬렉션에서 제거된 엔티티들을 고아 객체로 인식하여 자동으로 삭제합니다.

하지만 **컬렉션 자체를 새로운 인스턴스로 교체하면** Hibernate는 이전에 관리하던 **컬렉션과의 연관성을 잃게 되어 어떤 엔티티가 제거되었는지 추적할 수 없게 됩니다**. 이로 인해 예외가 발생하게 됩니다.

## 해결 방법

### 1. 기존 컬렉션 수정하기

컬렉션을 새로운 인스턴스로 교체하는 대신, **기존 컬렉션을 수정하는 방식**으로 변경해야 합니다.

```java
// 잘못된 방법
subAccount.setNetworkDiagrams(newNetworkDiagrams); // 새로운 컬렉션으로 교체하면 예외 발생

// 올바른 방법
subAccount.getNetworkDiagrams().clear(); // 기존 컬렉션 비우기
subAccount.getNetworkDiagrams().addAll(newNetworkDiagrams); // 새로운 요소 추가
```

Hibernate는 컬렉션의 인스턴스를 기준으로 변경 사항을 추적합니다. 기존 컬렉션 인스턴스를 유지하면서 그 안의 요소들을 변경하면 Hibernate는 어떤 엔티티가 추가되었고 제거되었는지 올바르게 인식할 수 있습니다.

### 2. 엔티티 매핑 확인하기

**엔티티 매핑이 올바르게 설정되었는지 확인**해야 합니다. 특히 `orphanRemoval = true`와 `cascade = CascadeType.ALL`이 설정되어 있어야 합니다.

```java
@Entity
public class SubAccount {

    @OneToMany(mappedBy = "subAccount", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<NetworkDiagram> networkDiagrams = new ArrayList<>();

    // getters and setters
}
```

위와 같이 매핑하면 `networkDiagrams` 컬렉션에서 제거된 `NetworkDiagram` 엔티티는 데이터베이스에서도 자동으로 삭제됩니다.

### 3. 엔티티 내에 컬렉션 교체 메서드 추가하기

컬렉션을 교체하는 작업을 엔티티 내부에서 처리하도록 메서드를 추가하는 것도 좋은 방법입니다.

```java
@Entity
public class SubAccount {

    // 기존 코드...

    public void replaceNetworkDiagrams(List<NetworkDiagram> newNetworkDiagrams) {
        this.networkDiagrams.clear();
        if (newNetworkDiagrams != null) {
            this.networkDiagrams.addAll(newNetworkDiagrams);
        }
    }
}
```

사용할 때는 다음과 같이 하면 됩니다:

```java
subAccount.replaceNetworkDiagrams(newNetworkDiagrams);
```

이렇게 하면 컬렉션의 내부 상태가 변경되므로 Hibernate는 변경 사항을 올바르게 감지할 수 있습니다.
## 주의 사항

- **컬렉션 인스턴스 교체 금지**: 컬렉션 자체를 새로운 인스턴스로 교체하면 안 됩니다.
- **컬렉션 초기화 확인**: 컬렉션이 `null`이 아닌지 확인하고, 초기화되지 않은 경우 `new ArrayList<>()`로 초기화해야 합니다.
- **양방향 매핑 관리**: 만약 `NetworkDiagram` 엔티티에도 `SubAccount`와의 연관관계가 매핑되어 있다면, 연관 관계의 일관성을 유지하도록 코드를 작성해야 합니다.

## 결론

Hibernate에서 `cascade="all-delete-orphan"` 또는 `orphanRemoval = true`를 사용하여 엔티티를 자동으로 삭제하려면 **컬렉션을 새로운 인스턴스로 교체하지 말고, 기존 컬렉션을 수정하는 방식으로 변경**해야 합니다.

컬렉션의 불변성 문제를 해결하고, 적절한 엔티티 매핑과 트랜잭션 관리를 통해 Hibernate가 엔티티의 상태 변화를 올바르게 추적할 수 있도록 해야 합니다.

## 추가 자료

- [[Hibernate 엔티티 상태 관리]]
- [[JPA 영속성 컨텍스트]]
- [[트랜잭션 관리 방법]]