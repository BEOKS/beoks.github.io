JPA(Java Persistence API)는 자바 애플리케이션에서 관계형 데이터를 관리하기 위한 표준 기술입니다. 그 중에서도 Criteria API는 타입 안전한(type-safe) 방식으로 쿼리를 구성할 수 있게 해주는 강력한 도구입니다. 이 글에서는 JPA Criteria API의 개념부터 실전 활용법까지 자세히 알아보겠습니다.

## Criteria API란 무엇인가?

Criteria API는 JPA 2.0부터 도입된 프로그래밍 방식의 쿼리 작성 방법입니다. 이는 JPQL(Java Persistence Query Language)의 대안으로, 문자열 기반의 쿼리 대신 자바 코드로 쿼리를 작성할 수 있게 해줍니다. 이를 통해 다음과 같은 이점을 얻을 수 있습니다:

1. **타입 안전성(Type Safety)**: 컴파일 시점에 오류를 확인할 수 있어 런타임 오류 가능성을 줄여줍니다.
2. **동적 쿼리 생성**: 조건에 따라 쿼리를 동적으로 구성하기 용이합니다.
3. **리팩토링 안전성**: 코드 리팩토링 시 IDE의 지원을 받을 수 있습니다.
4. **메타모델(Metamodel) 지원**: 엔티티 속성을 문자열이 아닌 정적 필드로 참조할 수 있습니다.

## Criteria API의 기본 구성요소

Criteria API를 사용하기 위해 알아야 할 주요 인터페이스는 다음과 같습니다:

1. **CriteriaBuilder**: 쿼리 구성을 위한 핵심 인터페이스로, 표현식, 조건, 파라미터 등을 생성합니다.
2. **CriteriaQuery**: 쿼리의 반환 타입, FROM 절, SELECT 절, WHERE 절 등을 지정합니다.
3. **Root**: 쿼리의 FROM 절을 나타내며, 엔티티의 속성을 참조하는 시작점입니다.
4. **Path**: 엔티티의 특정 속성에 대한 참조를 제공합니다.
5. **Predicate**: WHERE 절의 조건을 표현하며, 여러 조건을 AND, OR 등으로 결합할 수 있습니다.

## 기본 쿼리 작성하기

### 간단한 SELECT 쿼리

아래는 JPA Criteria API를 사용하여 간단한 SELECT 쿼리를 작성하는 예시입니다:

```java
// 엔티티 클래스
@Entity
public class Employee {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String name;
    private int salary;
    
    // Getter, Setter 생략
}

// 쿼리 작성
public List<Employee> findAllEmployees() {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
    Root<Employee> employee = query.from(Employee.class);
    query.select(employee);
    
    return entityManager.createQuery(query).getResultList();
}
```

### WHERE 조건 추가하기

특정 조건을 만족하는 데이터만 검색하고 싶을 경우:

```java
public List<Employee> findEmployeesBySalary(int minSalary) {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
    Root<Employee> employee = query.from(Employee.class);
    
    // WHERE 조건 추가
    Predicate salaryCondition = cb.greaterThanOrEqualTo(employee.get("salary"), minSalary);
    query.select(employee).where(salaryCondition);
    
    return entityManager.createQuery(query).getResultList();
}
```

### ORDER BY 절 추가하기

결과를 특정 순서로 정렬하고 싶을 경우:

```java
public List<Employee> findEmployeesOrderedBySalary() {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
    Root<Employee> employee = query.from(Employee.class);
    
    // ORDER BY 추가
    query.select(employee).orderBy(cb.desc(employee.get("salary")));
    
    return entityManager.createQuery(query).getResultList();
}
```

## 고급 쿼리 기능

### 다중 조건 결합하기

여러 조건을 AND 또는 OR로 결합할 수 있습니다:

```java
public List<Employee> findEmployeesByNameAndSalary(String name, int minSalary) {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
    Root<Employee> employee = query.from(Employee.class);
    
    // 여러 조건 결합
    Predicate namePredicate = cb.equal(employee.get("name"), name);
    Predicate salaryPredicate = cb.greaterThan(employee.get("salary"), minSalary);
    Predicate finalPredicate = cb.and(namePredicate, salaryPredicate);
    
    query.select(employee).where(finalPredicate);
    
    return entityManager.createQuery(query).getResultList();
}
```

### JOIN 사용하기

관련 엔티티를 조인하여 데이터를 검색할 수 있습니다:

```java
public List<Employee> findEmployeesByDepartmentName(String departmentName) {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
    Root<Employee> employee = query.from(Employee.class);
    
    // JOIN 사용
    Join<Employee, Department> department = employee.join("department");
    
    // 조인된 엔티티의 속성으로 조건 설정
    Predicate condition = cb.equal(department.get("name"), departmentName);
    query.select(employee).where(condition);
    
    return entityManager.createQuery(query).getResultList();
}
```

### 그룹화와 집계 함수

GROUP BY와 집계 함수를 사용한 쿼리:

```java
public List<Object[]> findAverageSalaryByDepartment() {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Object[]> query = cb.createQuery(Object[].class);
    Root<Employee> employee = query.from(Employee.class);
    Join<Employee, Department> department = employee.join("department");
    
    // GROUP BY와 집계 함수
    query.multiselect(
        department.get("name"),
        cb.avg(employee.get("salary"))
    );
    query.groupBy(department.get("name"));
    
    return entityManager.createQuery(query).getResultList();
}
```

### 서브쿼리 사용하기

서브쿼리를 사용하여 복잡한 조건을 표현할 수 있습니다:

```java
public List<Employee> findEmployeesWithSalaryAboveAverage() {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
    Root<Employee> employee = query.from(Employee.class);
    
    // 서브쿼리 생성
    Subquery<Double> subquery = query.subquery(Double.class);
    Root<Employee> subEmployee = subquery.from(Employee.class);
    subquery.select(cb.avg(subEmployee.get("salary")));
    
    // 메인 쿼리에 서브쿼리 조건 추가
    query.select(employee)
         .where(cb.gt(employee.get("salary"), subquery));
    
    return entityManager.createQuery(query).getResultList();
}
```

## 메타모델(Metamodel) 활용

JPA Criteria API를 사용할 때 문자열로 속성을 참조하는 것은 타입 안전성을 보장하지 않습니다. 이를 해결하기 위해 메타모델을 활용할 수 있습니다.

### 메타모델 생성하기

메타모델 클래스는 자동 생성 도구를 통해 생성할 수 있습니다. Maven을 사용한다면 `hibernate-jpamodelgen` 의존성을 추가하면 됩니다:

```xml
<dependency>
    <groupId>org.hibernate</groupId>
    <artifactId>hibernate-jpamodelgen</artifactId>
    <version>5.6.3.Final</version>
    <scope>provided</scope>
</dependency>
```

이렇게 하면 엔티티 클래스에 대한 메타모델 클래스가 자동으로 생성됩니다:

```java
// 자동 생성된 메타모델 클래스
@Generated(value = "org.hibernate.jpamodelgen.JPAMetaModelEntityProcessor")
@StaticMetamodel(Employee.class)
public abstract class Employee_ {
    public static volatile SingularAttribute<Employee, Long> id;
    public static volatile SingularAttribute<Employee, String> name;
    public static volatile SingularAttribute<Employee, Integer> salary;
    public static volatile SingularAttribute<Employee, Department> department;
}
```

### 메타모델을 사용한 쿼리 작성

메타모델을 사용하면 타입 안전한 쿼리를 작성할 수 있습니다:

```java
public List<Employee> findEmployeesBySalaryWithMetamodel(int minSalary) {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
    Root<Employee> employee = query.from(Employee.class);
    
    // 메타모델을 사용한 타입 안전한 속성 참조
    Predicate salaryCondition = cb.greaterThanOrEqualTo(employee.get(Employee_.salary), minSalary);
    query.select(employee).where(salaryCondition);
    
    return entityManager.createQuery(query).getResultList();
}
```

## 동적 쿼리 구성하기

Criteria API의 큰 장점 중 하나는 동적 쿼리 구성이 용이하다는 점입니다. 다음은 검색 조건에 따라 동적으로 쿼리를 구성하는 예시입니다:

```java
public List<Employee> searchEmployees(EmployeeSearchCriteria criteria) {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
    Root<Employee> employee = query.from(Employee.class);
    
    List<Predicate> predicates = new ArrayList<>();
    
    // 조건에 따라 동적으로 Predicate 추가
    if (criteria.getName() != null && !criteria.getName().isEmpty()) {
        predicates.add(cb.like(employee.get(Employee_.name), "%" + criteria.getName() + "%"));
    }
    
    if (criteria.getMinSalary() != null) {
        predicates.add(cb.greaterThanOrEqualTo(employee.get(Employee_.salary), criteria.getMinSalary()));
    }
    
    if (criteria.getMaxSalary() != null) {
        predicates.add(cb.lessThanOrEqualTo(employee.get(Employee_.salary), criteria.getMaxSalary()));
    }
    
    if (criteria.getDepartmentId() != null) {
        Join<Employee, Department> department = employee.join(Employee_.department);
        predicates.add(cb.equal(department.get(Department_.id), criteria.getDepartmentId()));
    }
    
    // 모든 조건을 AND로 결합
    if (!predicates.isEmpty()) {
        query.where(cb.and(predicates.toArray(new Predicate[0])));
    }
    
    // 정렬 조건 추가
    if (criteria.getSortField() != null) {
        if (criteria.isSortAscending()) {
            query.orderBy(cb.asc(employee.get(criteria.getSortField())));
        } else {
            query.orderBy(cb.desc(employee.get(criteria.getSortField())));
        }
    }
    
    return entityManager.createQuery(query).getResultList();
}
```

위 예시에서 `EmployeeSearchCriteria`는 검색 조건을 담고 있는 클래스입니다:

```java
public class EmployeeSearchCriteria {
    private String name;
    private Integer minSalary;
    private Integer maxSalary;
    private Long departmentId;
    private String sortField;
    private boolean sortAscending = true;
    
    // Getter, Setter 생략
}
```

## 페이징 처리하기

대량의 데이터를 처리할 때는 페이징이 필수적입니다. Criteria API에서는 `setFirstResult`와 `setMaxResults` 메서드를 통해 페이징을 구현할 수 있습니다:

```java
public List<Employee> findEmployeesWithPaging(int page, int pageSize) {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
    Root<Employee> employee = query.from(Employee.class);
    query.select(employee);
    
    // 정렬 조건 추가 (페이징에는 정렬이 권장됨)
    query.orderBy(cb.asc(employee.get(Employee_.id)));
    
    // 페이징 처리
    TypedQuery<Employee> typedQuery = entityManager.createQuery(query);
    typedQuery.setFirstResult((page - 1) * pageSize); // 시작 위치
    typedQuery.setMaxResults(pageSize); // 페이지 크기
    
    return typedQuery.getResultList();
}
```

## 프로젝션과 DTO 매핑

특정 필드만 선택하여 결과를 가져오거나, 결과를 DTO(Data Transfer Object)에 매핑하는 것도 가능합니다:

### 특정 필드만 선택하기

```java
public List<Object[]> findEmployeeNamesAndSalaries() {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Object[]> query = cb.createQuery(Object[].class);
    Root<Employee> employee = query.from(Employee.class);
    
    // 특정 필드만 선택
    query.multiselect(employee.get(Employee_.name), employee.get(Employee_.salary));
    
    return entityManager.createQuery(query).getResultList();
}
```

### 생성자 표현식을 사용한 DTO 매핑

```java
// DTO 클래스
public class EmployeeDTO {
    private final String name;
    private final int salary;
    
    public EmployeeDTO(String name, int salary) {
        this.name = name;
        this.salary = salary;
    }
    
    // Getter 생략
}

// 쿼리 작성
public List<EmployeeDTO> findEmployeeDTOs() {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<EmployeeDTO> query = cb.createQuery(EmployeeDTO.class);
    Root<Employee> employee = query.from(Employee.class);
    
    // 생성자 표현식을 사용한 DTO 매핑
    query.select(cb.construct(
        EmployeeDTO.class,
        employee.get(Employee_.name),
        employee.get(Employee_.salary)
    ));
    
    return entityManager.createQuery(query).getResultList();
}
```

## 스프링 데이터 JPA와 함께 사용하기

스프링 데이터 JPA를 사용하는 경우, `JpaSpecificationExecutor` 인터페이스를 통해 Criteria API를 더 쉽게 활용할 수 있습니다:

```java
public interface EmployeeRepository extends JpaRepository<Employee, Long>, JpaSpecificationExecutor<Employee> {
    // 기본 메서드는 JpaRepository에서 제공
    // JpaSpecificationExecutor를 통해 Specification 기반 쿼리 지원
}
```

`Specification` 클래스를 사용하여 재사용 가능한 쿼리 조건을 정의할 수 있습니다:

```java
public class EmployeeSpecifications {
    
    public static Specification<Employee> nameLike(String name) {
        return (root, query, cb) -> {
            if (name == null || name.isEmpty()) {
                return cb.conjunction();
            }
            return cb.like(root.get(Employee_.name), "%" + name + "%");
        };
    }
    
    public static Specification<Employee> salaryGreaterThan(Integer salary) {
        return (root, query, cb) -> {
            if (salary == null) {
                return cb.conjunction();
            }
            return cb.greaterThan(root.get(Employee_.salary), salary);
        };
    }
    
    public static Specification<Employee> inDepartment(Long departmentId) {
        return (root, query, cb) -> {
            if (departmentId == null) {
                return cb.conjunction();
            }
            Join<Employee, Department> department = root.join(Employee_.department);
            return cb.equal(department.get(Department_.id), departmentId);
        };
    }
}
```

이제 리포지토리에서 이러한 Specification을 결합하여 사용할 수 있습니다:

```java
@Service
public class EmployeeService {
    
    private final EmployeeRepository employeeRepository;
    
    public EmployeeService(EmployeeRepository employeeRepository) {
        this.employeeRepository = employeeRepository;
    }
    
    public List<Employee> searchEmployees(EmployeeSearchCriteria criteria) {
        Specification<Employee> spec = Specification.where(null);
        
        if (criteria.getName() != null) {
            spec = spec.and(EmployeeSpecifications.nameLike(criteria.getName()));
        }
        
        if (criteria.getMinSalary() != null) {
            spec = spec.and(EmployeeSpecifications.salaryGreaterThan(criteria.getMinSalary()));
        }
        
        if (criteria.getDepartmentId() != null) {
            spec = spec.and(EmployeeSpecifications.inDepartment(criteria.getDepartmentId()));
        }
        
        return employeeRepository.findAll(spec);
    }
}
```

## Criteria API와 JPQL 비교

Criteria API와 JPQL은 각각 장단점이 있습니다. 다음은 간단한 비교입니다:

### JPQL 예시:

```java
String jpql = "SELECT e FROM Employee e WHERE e.salary > :minSalary ORDER BY e.name";
TypedQuery<Employee> query = entityManager.createQuery(jpql, Employee.class);
query.setParameter("minSalary", 50000);
List<Employee> employees = query.getResultList();
```

### 같은 쿼리의 Criteria API 예시:

```java
CriteriaBuilder cb = entityManager.getCriteriaBuilder();
CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
Root<Employee> employee = query.from(Employee.class);
query.select(employee)
     .where(cb.greaterThan(employee.get(Employee_.salary), 50000))
     .orderBy(cb.asc(employee.get(Employee_.name)));
List<Employee> employees = entityManager.createQuery(query).getResultList();
```

### 비교 결과:

1. **타입 안전성**: Criteria API가 우수함 (메타모델 사용 시)
2. **가독성**: JPQL이 일반적으로 더 간결하고 SQL과 유사하여 가독성이 좋음
3. **동적 쿼리**: Criteria API가 훨씬 우수함
4. **유지보수성**: Criteria API가 리팩토링에 안전함
5. **학습 곡선**: JPQL이 더 쉬움
6. **디버깅**: Criteria API가 컴파일 타임 오류 검출로 더 유리함

## 성능 최적화 팁

Criteria API를 사용할 때 성능을 최적화하기 위한 몇 가지 팁입니다:

1. **필요한 필드만 선택하기**: 전체 엔티티 대신 필요한 필드만 선택하면 메모리 사용량과 네트워크 트래픽을 줄일 수 있습니다.
    
2. **페치 조인(Fetch Join) 활용하기**: N+1 문제를 방지하기 위해 연관 엔티티를 함께 로드할 때 페치 조인을 사용합니다.
    
    ```java
    public List<Employee> findEmployeesWithDepartment() {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
        Root<Employee> employee = query.from(Employee.class);
        
        // 페치 조인으로 연관 엔티티 함께 로드
        employee.fetch(Employee_.department, JoinType.LEFT);
        query.select(employee);
        
        return entityManager.createQuery(query).getResultList();
    }
    ```
    
3. **Predicate 재사용하기**: 여러 쿼리에서 공통 조건을 재사용하여 코드 중복을 줄이세요.
    
4. **명시적인 힌트 사용하기**: 쿼리 힌트를 통해 데이터베이스에 특정 최적화 지시를 내릴 수 있습니다.
    
    ```java
    TypedQuery<Employee> typedQuery = entityManager.createQuery(query);
    typedQuery.setHint(QueryHints.HINT_CACHEABLE, true);
    ```
    
5. **배치 처리 활용하기**: 대량의 데이터를 처리할 때는 배치 처리를 사용하여 메모리 사용량을 줄이세요.
    

## Criteria API 응용 사례

### 복잡한 보고서 쿼리 생성

통계나 보고서용 복잡한 쿼리를 동적으로 생성할 수 있습니다:

```java
public List<DepartmentSalaryReport> generateDepartmentSalaryReport(ReportCriteria criteria) {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<DepartmentSalaryReport> query = cb.createQuery(DepartmentSalaryReport.class);
    Root<Department> department = query.from(Department.class);
    Join<Department, Employee> employees = department.join(Department_.employees, JoinType.LEFT);
    
    // 보고서용 표현식 생성
    Expression<Long> employeeCount = cb.count(employees.get(Employee_.id));
    Expression<Double> avgSalary = cb.avg(employees.get(Employee_.salary));
    Expression<Integer> maxSalary = cb.max(employees.get(Employee_.salary));
    Expression<Integer> minSalary = cb.min(employees.get(Employee_.salary));
    
    // 결과 매핑
    query.select(cb.construct(
        DepartmentSalaryReport.class,
        department.get(Department_.id),
        department.get(Department_.name),
        employeeCount,
        avgSalary,
        maxSalary,
        minSalary
    ));
    
    // 조건 추가
    List<Predicate> predicates = new ArrayList<>();
    if (criteria.getMinEmployeeCount() != null) {
        predicates.add(cb.greaterThanOrEqualTo(
            cb.size(department.get(Department_.employees)), 
            criteria.getMinEmployeeCount()
        ));
    }
    
    if (!predicates.isEmpty()) {
        query.where(cb.and(predicates.toArray(new Predicate[0])));
    }
    
    // 그룹화 및 정렬
    query.groupBy(department.get(Department_.id), department.get(Department_.name));
    query.orderBy(cb.desc(avgSalary));
    
    return entityManager.createQuery(query).getResultList();
}
```

### 다중 테이블 검색

여러 엔티티에 걸친 복합 검색도 구현할 수 있습니다:

```java
public List<Employee> findEmployeesByProjectAndSkill(Long projectId, String skillName) {
    CriteriaBuilder cb = entityManager.getCriteriaBuilder();
    CriteriaQuery<Employee> query = cb.createQuery(Employee.class);
    Root<Employee> employee = query.from(Employee.class);
    
    // 여러 조인 구성
    Join<Employee, Project> project = employee.join(Employee_.projects);
    Join<Employee, Skill> skill = employee.join(Employee_.skills);
    
    // 여러 테이블 조건 조합
    Predicate projectPredicate = cb.equal(project.get(Project_.id), projectId);
    Predicate skillPredicate = cb.equal(skill.get(Skill_.name), skillName);
    
    query.select(employee)
         .where(cb.and(projectPredicate, skillPredicate))
         .distinct(true); // 중복 제거
    
    return entityManager.createQuery(query).getResultList();
}
```

## 실전 적용: 스프링 부트 레포지토리 구현

이제 모든 개념을 종합하여 스프링 부트에서 완전한 레포지토리를 구현해보겠습니다:

```java
@Repository
public class EmployeeRepositoryImpl implements EmployeeRepositoryCustom {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    @Override
    public Page<EmployeeDTO> searchEmployees(EmployeeSearchCriteria criteria, Pageable pageable) {
        // 카운트 쿼리
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Long> countQuery = cb.createQuery(Long.class);
        Root<Employee> countRoot = countQuery.from(Employee.class);
        
        // 데이터 쿼리
        CriteriaQuery<EmployeeDTO> dataQuery = cb.createQuery(EmployeeDTO.class);
        Root<Employee> dataRoot = dataQuery.from(Employee.class);
        Join<Employee, Department> department = dataRoot.join(Employee_.department, JoinType.LEFT);
        
        // 조건 설정
        List<Predicate> predicates = buildPredicates(cb, dataRoot, department, criteria);
        
        // 카운트 쿼리 실행
        countQuery.select(cb.count(countRoot));
        if (!predicates.isEmpty()) {
            countQuery.where(predicates.toArray(new Predicate[0]));
        }
        long totalRecords = entityManager.createQuery(countQuery).getSingleResult();
        
        // 데이터 쿼리 실행
        dataQuery.select(cb.construct(
            EmployeeDTO.class,
            dataRoot.get(Employee_.id),
            dataRoot.get(Employee_.name),
            dataRoot.get(Employee_.salary),
            department.get(Department_.name)
        ));
        
        if (!predicates.isEmpty()) {
            dataQuery.where(predicates.toArray(new Predicate[0]));
        }
        
        // 정렬 설정
        if (pageable.getSort().isSorted()) {
            List<Order> orders = new ArrayList<>();
            pageable.getSort().forEach(order -> {
                if (order.isAscending()) {
                    orders.add(cb.asc(dataRoot.get(order.getProperty())));
                } else {
                    orders.add(cb.desc(dataRoot.get(order.getProperty())));
                }
            });
            dataQuery.orderBy(orders);
        }
        
        // 쿼리 실행 및 페이징 적용
        TypedQuery<EmployeeDTO> query = entityManager.createQuery(dataQuery);
        query.setFirstResult((int) pageable.getOffset());
        query.setMaxResults(pageable.getPageSize());
        
        List<EmployeeDTO> results = query.getResultList();
        
        return new PageImpl<>(results, pageable, totalRecords);
    }
    
    private List<Predicate> buildPredicates(CriteriaBuilder cb, Root<Employee> root, 
                                          Join<Employee, Department> department, 
                                          EmployeeSearchCriteria criteria)
```