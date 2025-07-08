---
title: "Role 인터페이스 정의"
---

`Role` 인터페이스는 시스템 내에서 정의되는 역할의 기본 구조를 나타냅니다.

```java
public interface Role {
    Long getId();
    String getName();
    Set<Permission> getPermissions();

    void setId(Long id);
    void setName(String name);
    void setPermissions(Set<Permission> permissions);
}
```