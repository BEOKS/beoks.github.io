# 기능 추가
1. 기획에서 신규 기능을 정의
2. 신규 기능을 개발에 전달
3. 개발에서 기능을 검토
	1. 기능 요구사항과 관련된 현황 정보를 수집
	2. 기능 요구사항에 아래 요소가 있는지 검토하고 없으면 부족한 점을 기획에 다시 전달
		1. 기능이 기존 정책을 어기는 등 물리적으로 구현이 불가능한지 검토
		2. 기능이 필요한 이유가 포함되어 있는지 검토(정확한 문제를 진단하기 위함)
		3. 문제를 해결하는데 기능에 불필요한 요소가 있는지 검토, 불필요한 요소가 있다면 다 빼야한다고 근거와 함께 기획에 전달
		4. 불필요한 요소를 다 제거 했으면, 기능을 단순화, 간소화 할 수 있는 방안을 검토, 역으로 제안
		5. 기능을 빠르게 수행할 수 있는 방안을 검토 역으로 제안
		6. 기능을 자동화할 수 있는 방안을 검토 역으로 제안
4. 검토된 기능을 바탕으로 테스트 코드와 인터페이스 작성
5. 개발 계획서를 작성
	1. 패키지/코드 등 기존 컨벤션을 고려해 계획 수립
	2. 해결방안을 구현할 수 있는 여러 구현 계획을 수립
	3. 구현 계획의 장단점을 비교
6. 개발 계획서를 jira 에 등록
```mermaid
architecture-beta
    group api(cloud)[API]

    service db(database)[Database] in api
    service disk1(disk)[Storage] in api
    service disk2(disk)[Storage] in api
    service server(server)[Server] in api

    db:L -- R:server
    disk1:T -- B:server
    disk2:T -- B:db

```
# 디버깅
1. 기획에서 ㄷ