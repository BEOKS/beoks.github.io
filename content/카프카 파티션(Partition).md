파티션은 카프카 토픽을 물리적으로 분할한 단위입니다. 토픽은 논리적인 개념이며, 실제 데이터는 파티션이라는 물리적 단위에 저장됩니다. 각 파티션은 순서가 보장된 불변의 메시지 시퀀스이며, 카프카 클러스터의 여러 브로커에 분산되어 저장됩니다.

## 파티션의 주요 특징

1. **순차적 데이터 구조**: 각 파티션은 순차적으로 추가되는(append-only) 로그 구조입니다. 메시지는 항상 파티션의 끝에 추가되며, 각 메시지는 파티션 내에서 고유한 오프셋(offset)을 부여받습니다.
    
2. **분산 저장**: 파티션은 카프카 클러스터의 여러 브로커에 분산되어 저장될 수 있으며, 이를 통해 수평적 확장이 가능합니다.
    
3. **병렬 처리**: 토픽의 파티션 수는 컨슈머의 병렬 처리 능력을 결정합니다. 컨슈머 그룹 내의 각 컨슈머는 하나 이상의 파티션을 독점적으로 처리할 수 있습니다.
    
4. **오프셋(Offset)**: 파티션 내의 각 메시지는 0부터 시작하는 연속적인 오프셋을 가집니다. 오프셋은 파티션 내에서 메시지의 위치를 나타냅니다.
    
5. **복제(Replication)**: 고가용성을 위해 각 파티션은 여러 브로커에 복제될 수 있습니다. 복제 계수(replication factor)는 각 파티션이 몇 개의 복제본을 가질지 결정합니다.
    

## 파티션 할당 및 분배

### 프로듀서의 파티션 할당

프로듀서가 메시지를 토픽에 발행할 때, 어떤 파티션으로 메시지를 보낼지 결정해야 합니다. 파티션 할당 방식은 다음과 같습니다:

1. **명시적 파티션 지정**: 프로듀서가 메시지를 보낼 파티션을 직접 지정할 수 있습니다.
    
2. **키 기반 파티션 할당**: 메시지에 키가 있는 경우, 키의 해시 값을 기반으로 파티션이 결정됩니다. 동일한 키를 가진 메시지는 항상 같은 파티션으로 전송됩니다.
    
3. **라운드 로빈**: 메시지에 키가 없고 파티션을 명시적으로 지정하지 않은 경우, 기본적으로 라운드 로빈 방식으로 파티션이 선택됩니다.
    

### 컨슈머의 파티션 할당

컨슈머 그룹 내에서 파티션 할당은 다음과 같이 이루어집니다:

1. **그룹 코디네이터**: 카프카는 그룹 코디네이터를 통해 컨슈머 그룹의 멤버십과 파티션 할당을 관리합니다.
    
2. **리밸런싱(Rebalancing)**: 컨슈머 그룹에 컨슈머가 추가되거나 제거될 때, 파티션 할당이 재조정됩니다.
    
3. **할당 전략**: 기본적으로 Range, RoundRobin, Sticky 등의 할당 전략을 사용하여 파티션을 컨슈머에게 분배합니다.
    

## 파티션 수 결정 시 고려사항

토픽의 파티션 수를 결정할 때 고려해야 할 요소들:

1. **처리량(Throughput)**: 높은 처리량이 필요한 경우, 더 많은 파티션을 사용하여 병렬 처리 능력을 높일 수 있습니다.
    
2. **메시지 순서**: 메시지 순서가 중요한 경우, 관련 메시지가 동일한 파티션에 할당되도록 키를 설정해야 합니다.
    
3. **컨슈머 수**: 컨슈머 그룹의 최대 병렬 처리 능력은 파티션 수를 초과할 수 없습니다. 즉, 파티션 수보다 많은 컨슈머가 있다면 일부 컨슈머는 유휴 상태가 됩니다.
    
4. **브로커 자원**: 각 파티션은 브로커의 리소스(디스크, 메모리, CPU)를 소비합니다. 너무 많은 파티션은 브로커에 부담을 줄 수 있습니다.
    
5. **리밸런싱 비용**: 파티션 수가 많을수록 컨슈머 그룹의 리밸런싱 비용이 증가합니다.
    

## 파티션 관리

1. **토픽 생성 시 파티션 수 지정**:
    
    ```bash
    kafka-topics.sh --create --topic my-topic --partitions 3 --replication-factor 2 --bootstrap-server localhost:9092
    ```
    
2. **기존 토픽의 파티션 수 증가**:
    
    ```bash
    kafka-topics.sh --alter --topic my-topic --partitions 6 --bootstrap-server localhost:9092
    ```
    
3. **파티션 정보 확인**:
    
    ```bash
    kafka-topics.sh --describe --topic my-topic --bootstrap-server localhost:9092
    ```
    

주의할 점은 파티션 수는 증가만 가능하고 감소는 불가능하다는 것입니다. 또한 파티션 수를 증가시키면 메시지 키에 따른 파티션 매핑이 변경될 수 있으므로, 키 순서가 중요한 애플리케이션에서는 신중히 고려해야 합니다.

파티션은 카프카의 확장성과 고성능의 핵심 요소이며, 애플리케이션의 요구사항에 맞게 적절히 설계하는 것이 중요합니다.