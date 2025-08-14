---
title: "RBAC 인터페이스 정의"
---

RBAC 시스템의 각 핵심 컴포넌트(역할, 권한, 사용자-역할 매핑, 역할-권한 매핑)는 명확한 인터페이스를 통해 상호작용하도록 설계하는 것이 좋습니다. 이는 시스템의 모듈성을 높이고, 향후 구현 변경에 유연하게 대응할 수 있도록 합니다.

역할(Role)과 권한(Permission)의 상세 인터페이스 정의는 각각 [[Role 인터페이스 정의]]와 [[Permission 인터페이스 정의]]를 참고해주세요.

## 1. RoleService 인터페이스

`RoleService`는 역할(Role) 관련 비즈니스 로직을 정의합니다.

```java
public interface RoleService {
    /**
     * 새로운 역할을 생성합니다.
     * @param roleName 생성할 역할의 이름
     * @return 생성된 역할 객체
     */
    Role createRole(String roleName);

    /**
     * ID로 역할을 조회합니다.
     * @param roleId 조회할 역할의 ID
     * @return 조회된 역할 객체 (없으면 null 또는 Optional.empty())
     */
    Role getRoleById(Long roleId);

    /**
     * 역할 이름으로 역할을 조회합니다.
     * @param roleName 조회할 역할의 이름
     * @return 조회된 역할 객체 (없으면 null 또는 Optional.empty())
     */
    Role getRoleByName(String roleName);

    /**
     * 모든 역할을 조회합니다.
     * @return 모든 역할 목록
     */
    List<Role> getAllRoles();

    /**
     * 역할을 업데이트합니다.
     * @param roleId 업데이트할 역할의 ID
     * @param newRoleName 새로운 역할 이름
     * @return 업데이트된 역할 객체
     */
    Role updateRole(Long roleId, String newRoleName);

    /**
     * 역할을 삭제합니다.
     * @param roleId 삭제할 역할의 ID
     */
    void deleteRole(Long roleId);

    /**
     * 사용자에게 역할을 부여합니다.
     * @param userId 역할을 부여할 사용자의 ID
     * @param roleId 부여할 역할의 ID
     */
    void assignRoleToUser(Long userId, Long roleId);

    /**
     * 사용자로부터 역할을 회수합니다.
     * @param userId 역할을 회수할 사용자의 ID
     * @param roleId 회수할 역할의 ID
     */
    void revokeRoleFromUser(Long userId, Long roleId);

    /**
     * 역할에 권한을 부여합니다.
     * @param roleId 권한을 부여할 역할의 ID
     * @param permissionId 부여할 권한의 ID
     */
    void addPermissionToRole(Long roleId, Long permissionId);

    /**
     * 역할로부터 권한을 회수합니다.
     * @param roleId 권한을 회수할 역할의 ID
     * @param permissionId 회수할 권한의 ID
     */
    void removePermissionFromRole(Long roleId, Long permissionId);
}
```

## 2. PermissionService 인터페이스

`PermissionService`는 권한(Permission) 관련 비즈니스 로직을 정의합니다.

```java
public interface PermissionService {
    /**
     * 새로운 권한을 생성합니다.
     * @param permissionName 생성할 권한의 이름 (예: PRODUCT:READ)
     * @return 생성된 권한 객체
     */
    Permission createPermission(String permissionName);

    /**
     * ID로 권한을 조회합니다.
     * @param permissionId 조회할 권한의 ID
     * @return 조회된 Permission 객체 (없으면 null 또는 Optional.empty())
     */
    Permission getPermissionById(Long permissionId);

    /**
     * 권한 이름으로 권한을 조회합니다.
     * @param permissionName 조회할 권한의 이름
     * @return 조회된 권한 객체 (없으면 null 또는 Optional.empty())
     */
    Permission getPermissionByName(String permissionName);

    /**
     * 모든 권한을 조회합니다.
     * @return 모든 권한 목록
     */
    List<Permission> getAllPermissions();

    /**
     * 권한을 업데이트합니다.
     * @param permissionId 업데이트할 권한의 ID
     * @param newPermissionName 새로운 권한 이름
     * @return 업데이트된 권한 객체
     */
    Permission updatePermission(Long permissionId, String newPermissionName);

    /**
     * 권한을 삭제합니다.
     * @param permissionId 삭제할 권한의 ID
     */
    void deletePermission(Long permissionId);
}
```

## 3. AuthorizationService 인터페이스

`AuthorizationService`는 실제 권한 부여 로직을 정의합니다.

```java
public interface AuthorizationService {
    /**
     * 특정 사용자가 특정 권한을 가지고 있는지 확인합니다.
     * @param userId 확인할 사용자의 ID
     * @param permissionName 확인할 권한의 이름 (예: PRODUCT:READ)
     * @return 권한이 있으면 true, 없으면 false
     */
    boolean hasPermission(Long userId, String permissionName);

    /**
     * 특정 사용자가 특정 역할을 가지고 있는지 확인합니다.
     * @param userId 확인할 사용자의 ID
     * @param roleName 확인할 역할의 이름 (예: ADMIN)
     * @return 역할이 있으면 true, 없으면 false
     */
    boolean hasRole(Long userId, String roleName);

    /**
     * 현재 인증된 사용자가 특정 권한을 가지고 있는지 확인합니다.
     * (Spring Security의 SecurityContextHolder를 활용하여 현재 사용자 정보를 가져옴)
     * @param permissionName 확인할 권한의 이름
     * @return 권한이 있으면 true, 없으면 false
     */
    boolean hasPermission(String permissionName);

    /**
     * 현재 인증된 사용자가 특정 역할을 가지고 있는지 확인합니다.
     * (Spring Security의 SecurityContextHolder를 활용하여 현재 사용자 정보를 가져옴)
     * @param roleName 확인할 역할의 이름
     * @return 역할이 있으면 true, 없으면 false
     */
    boolean hasRole(String roleName);
}
```
