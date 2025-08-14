소프트 딜리트([[Soft Delete]])는 데이터베이스에서 레코드를 실제로 삭제하지 않고, "삭제됨"을 나타내는 플래그를 설정하여 관련 데이터가 유지되도록 하는 기법입니다. 이렇게 하면 데이터 복구나 감사(audit)가 필요한 경우에도 데이터를 보존할 수 있습니다.

Hibernate에서는 소프트 딜리트를 구현하기 위한 다양한 방법을 제공합니다. 아래에서는 Hibernate를 사용하여 소프트 딜리트를 구현하는 방법을 설명합니다.

---

### 1. 엔티티에 삭제 플래그 필드 추가

엔티티에 레코드의 활성/삭제 상태를 나타내는 필드를 추가합니다. 보통 `isDeleted` 또는 `deleted`라는 Boolean 타입의 필드를 사용합니다.

```java
@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private String email;

    @Column(name = "is_deleted")
    private boolean isDeleted = false;

    // getters and setters
}
```

---

### 2. @SQLDelete 및 @Where 어노테이션 사용

`@SQLDelete` 어노테이션을 사용하면 Hibernate에서 엔티티를 삭제할 때 실행되는 SQL 명령을 재정의할 수 있습니다. 이를 이용하여 실제 삭제 대신 `is_deleted` 플래그를 `true`로 업데이트합니다.

또한 `@Where` 어노테이션을 사용하여 조회 시 삭제된 레코드를 제외할 수 있습니다.

```java
import org.hibernate.annotations.SQLDelete;
import org.hibernate.annotations.Where;

@Entity
@Table(name = "users")
@SQLDelete(sql = "UPDATE users SET is_deleted = true WHERE id = ?")
@Where(clause = "is_deleted = false")
public class User {
    //...
}
```

**설명:**

- `@SQLDelete`: 삭제 시 실행될 SQL을 지정합니다.
- `@Where`: 엔티티를 조회할 때 `is_deleted = false` 조건을 추가하여 삭제되지 않은 레코드만 조회합니다.

---

### 3. Repository 또는 DAO에서 삭제 메서드 수정

삭제 메서드에서 실제 삭제 대신 `isDeleted` 플래그를 `true`로 설정하도록 수정합니다.

```java
public void deleteUser(Long userId) {
    User user = entityManager.find(User.class, userId);
    if (user != null) {
        user.setIsDeleted(true);
        entityManager.merge(user);
    }
}
```

하지만, 위와 같이 수동으로 플래그를 설정하지 않아도 `@SQLDelete`를 설정하면 `entityManager.remove(user);`를 호출할 때 자동으로 `is_deleted` 필드가 `true`로 업데이트됩니다.

```java
public void deleteUser(Long userId) {
    User user = entityManager.find(User.class, userId);
    if (user != null) {
        entityManager.remove(user); // Soft delete가 적용됨
    }
}
```

---

### 4. 소프트 딜리트된 엔티티 제외하고 조회하기

`@Where` 어노테이션을 사용하면 별도의 조건을 붙이지 않아도 자동으로 `is_deleted = false` 조건이 적용됩니다.

```java
public List<User> getAllUsers() {
    return entityManager.createQuery("SELECT u FROM User u", User.class)
            .getResultList();
}
```

위의 조회 결과에는 삭제되지 않은 사용자만 포함됩니다.

### 주의 사항

- **성능 이슈:** `@Where` 어노테이션은 조회 시 항상 추가 조건을 적용하므로, 대용량 테이블에서는 **인덱스 설정 등 성능 최적화**가 필요합니다.
- **연관 관계 및 캐스케이드:** 소프트 딜리트를 적용할 때 연관된 엔티티나 캐스케이드 옵션을 주의해야 합니다. 물리적인 삭제가 발생하지 않도록 설정합니다.
- **실제 삭제가 필요한 경우:** 일정 기간 이후에 실제 삭제가 필요하다면 잡 스케줄러 등을 통해 물리적으로 삭제하도록 설계합니다.

---

**참고 자료**

- [Hibernate 공식 문서 - Soft Deletable Entities](https://docs.jboss.org/hibernate/orm/current/userguide/html_single/Hibernate_User_Guide.html#mapping-deleting-soft)
- [Baeldung - Soft Deletes with Hibernate](https://www.baeldung.com/hibernate-soft-delete)