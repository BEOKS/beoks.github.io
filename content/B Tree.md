B 트리(B Tree)는 B+ 트리와 마찬가지로 데이터베이스 및 파일 시스템에서 대량의 데이터를 효율적으로 저장하고 검색하기 위해 사용되는 자가 균형 이진 탐색 트리(Self-balancing Binary Search Tree)의 일반화된 형태입니다. B 트리는 특히 디스크와 같은 블록 지향 저장 장치에 최적화되어 있으며, 모든 노드에 데이터가 저장될 수 있다는 점에서 B+ 트리와 주요한 차이를 보입니다.

## B 트리의 구조

B 트리는 다음과 같은 주요 특징을 가집니다:

1.  **모든 노드에 데이터가 저장될 수 있습니다.**
    *   루트 노드, 내부 노드, 리프 노드 모두 키(Key)와 함께 실제 데이터 레코드에 대한 포인터(또는 실제 데이터)를 가질 수 있습니다.
    *   이는 B+ 트리가 모든 데이터를 리프 노드에만 저장하는 것과 대조됩니다.

2.  **리프 노드들은 연결 리스트로 연결되어 있지 않습니다.**
    *   B+ 트리와 달리, B 트리의 리프 노드들은 서로 연결되어 있지 않습니다.
    *   이로 인해 범위 검색(Range Query) 시 B+ 트리보다 효율성이 떨어질 수 있습니다.

3.  **균형 트리(Balanced Tree)입니다.**
    *   모든 리프 노드는 루트 노드로부터 같은 거리에 있습니다. 즉, 모든 검색 경로의 길이가 동일합니다.
    *   이는 어떤 데이터를 검색하더라도 일관된 검색 성능을 보장합니다.

### 노드의 종류



*   **루트 노드(Root Node)**: 트리의 최상단 노드입니다. 키와 데이터 포인터를 가집니다.
*   **내부 노드(Internal Node)**: 루트 노드와 리프 노드 사이에 있는 노드들입니다. 키, 데이터 포인터, 그리고 자식 노드 포인터를 가집니다.
*   **리프 노드(Leaf Node)**: 트리의 최하단 노드입니다. 키와 데이터 포인터를 가집니다.

## B 트리의 동작 방식

### 검색 (Search)

1.  루트 노드에서 시작하여 검색하려는 키 값과 노드의 키 값들을 비교합니다.
2.  키 값에 따라 적절한 자식 노드로 이동하거나, 현재 노드에서 키를 찾으면 데이터를 반환합니다.
3.  이 과정을 리프 노드에 도달할 때까지 반복합니다.
4.  리프 노드에서 해당 키 값을 찾아 데이터 레코드에 접근합니다.

```python
class Node:
    def __init__(self, is_leaf=False):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf
        self.data = {} # Stores key-value pairs for data

def search_b_tree(key, node):
    if node.is_leaf:
        if key in node.keys:
            return node.data[key] # Return data associated with the key
        return None # Key not found in leaf node
    else:
        # Find the smallest key_i such that key <= key_i
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        # If key is found in an internal node, return its data
        if i < len(node.keys) and key == node.keys[i]:
            return node.data[key]
        
        # Follow pointer to the appropriate child
        child_node = node.children[i]
        return search_b_tree(key, child_node)
```

### 삽입 (Insertion)

1.  새로운 키-값 쌍이 삽입될 노드를 검색합니다. (B+ 트리와 달리 내부 노드에도 삽입될 수 있습니다.)
2.  노드에 공간이 있으면 키-값 쌍을 삽입하고 정렬합니다.
3.  노드가 가득 찼다면, 노드를 분할(Split)합니다.
    *   분할된 노드의 중간 키를 부모 노드로 올립니다. (B+ 트리는 중간 키의 복사본을 올립니다.)
    *   부모 노드도 가득 찼다면, 부모 노드도 분할하고 그 부모의 부모 노드로 키를 올리는 과정이 재귀적으로 반복될 수 있습니다.
    *   최종적으로 루트 노드가 분할되면 트리의 높이가 증가합니다.

```python
# Simplified insertion logic for demonstration.
# A full B-Tree implementation requires careful handling of node capacity, splitting, and merging.

class BTree:
    def __init__(self, order):
        self.root = Node(is_leaf=True)
        self.order = order # Max number of children for internal nodes, max keys for any node

    def _find_node_for_insertion(self, key):
        node = self.root
        while not node.is_leaf:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            # If key already exists in an internal node, we might update its value or handle as duplicate
            if i < len(node.keys) and key == node.keys[i]:
                return node # Key found in internal node
            node = node.children[i]
        return node # Return leaf node

    def insert(self, key, value):
        node = self._find_node_for_insertion(key)
        
        # Check for duplicate key (simplified)
        if key in node.keys:
            node.data[key] = value # Update value if key exists
            return

        # Insert key and value into the node
        # This simplified version assumes keys are unique and handles only basic insertion
        # Real B-tree insertion involves finding the correct position and shifting elements
        
        # Find insertion point to maintain sorted order
        insert_idx = 0
        while insert_idx < len(node.keys) and key > node.keys[insert_idx]:
            insert_idx += 1
        
        node.keys.insert(insert_idx, key)
        node.data[key] = value

        if len(node.keys) > self.order - 1: # B-Tree nodes typically hold order-1 keys
            self._split_node(node)

    def _split_node(self, node):
        new_node = Node(is_leaf=node.is_leaf)
        mid_idx = len(node.keys) // 2
        
        # Key to promote to parent
        promoted_key = node.keys[mid_idx]
        promoted_data = node.data[promoted_key]

        # Move keys and data to new_node
        new_node.keys = node.keys[mid_idx+1:]
        for k in new_node.keys:
            new_node.data[k] = node.data[k]
        
        # Update original node's keys and data
        node.keys = node.keys[:mid_idx]
        for k in list(node.data.keys()): # Iterate over a copy to allow deletion
            if k >= promoted_key:
                del node.data[k]

        if not node.is_leaf:
            new_node.children = node.children[mid_idx+1:]
            node.children = node.children[:mid_idx+1]

        if node == self.root:
            new_root = Node()
            new_root.keys.append(promoted_key)
            new_root.data[promoted_key] = promoted_data
            new_root.children.append(node)
            new_root.children.append(new_node)
            self.root = new_root
        else:
            # In a real implementation, you'd insert promoted_key into the parent
            # and handle parent overflow recursively.
            # This part is highly simplified.
            pass # Placeholder for parent insertion and overflow handling
```

### 삭제 (Deletion)

1.  삭제할 키-값 쌍이 있는 노드를 검색합니다.
2.  해당 키-값 쌍을 노드에서 삭제합니다.
3.  삭제 후 노드의 키 개수가 최소 기준(보통 m/2)보다 적어지면, 재분배(Redistribution) 또는 병합(Merge)을 시도합니다.
    *   **재분배**: 인접한 형제 노드로부터 키를 빌려와 노드의 키 개수를 채웁니다.
    *   **병합**: 인접한 형제 노드와 병합하여 하나의 노드로 만듭니다. 이 경우 부모 노드에서 해당 키가 삭제됩니다.
    *   이 과정 또한 재귀적으로 루트 노드까지 전파될 수 있으며, 루트 노드의 자식이 하나만 남게 되면 트리의 높이가 감소할 수 있습니다.

```python
# Simplified deletion logic for demonstration.
# A full B-Tree implementation requires careful handling of node capacity, splitting, and merging.

    def delete(self, key):
        node = self._find_node_for_insertion(key) # Reusing find_node_for_insertion to locate the node

        if key not in node.keys:
            print(f"Key {key} not found for deletion.")
            return

        # Remove key and its associated data
        node.keys.remove(key)
        del node.data[key]

        # Simplified underflow handling. In a real B-tree, you'd check if the node
        # is below the minimum occupancy and then attempt redistribution or merging.
        # For this example, we'll just print a message if underflow occurs.
        min_keys = (self.order // 2) -1 # B-Tree minimum keys
        if len(node.keys) < min_keys and node != self.root:
            print(f"Node underflow after deleting {key}. (Simplified: No redistribution/merge implemented)")
            # In a full implementation, you would call a _handle_underflow method here
            # self._handle_underflow(node)

    # Placeholder for a more complete _handle_underflow method
    # def _handle_underflow(self, node):
    #     # Logic for redistribution with siblings or merging with siblings
    #     # and propagating changes up to the parent if parent underflows.
    #     pass
```

## B 트리와 B+ 트리의 차이점

| 특징         | B 트리                                     | B+ 트리                                        |
| :----------- | :----------------------------------------- | :--------------------------------------------- |
| **데이터 저장** | 모든 노드(내부, 리프)에 데이터 저장 가능    | 모든 데이터는 리프 노드에만 저장               |
| **리프 노드 연결** | 연결 리스트로 연결되어 있지 않음           | 연결 리스트로 순차적으로 연결되어 있음         |
| **내부 노드** | 키와 데이터 포인터 모두 가짐               | 키와 자식 노드 포인터만 가짐 (데이터 없음)     |
| **검색 효율성** | 특정 키 검색은 효율적이나, 범위 검색은 비효율적 | 특정 키 및 범위 검색 모두 효율적               |
| **디스크 I/O** | 내부 노드에 데이터가 있어 트리가 더 깊어질 수 있음 | 내부 노드가 작아 트리가 더 얕고 디스크 I/O 효율적 |

## B 트리의 장단점

### 장점

*   **빠른 특정 키 검색**: 데이터가 모든 노드에 존재할 수 있으므로, 검색 경로가 짧아질 수 있습니다.
*   **디스크 I/O 감소**: 특정 키를 찾을 때, 내부 노드에서 바로 데이터를 찾을 수 있다면 리프 노드까지 내려가지 않아도 되므로 디스크 I/O 횟수가 줄어들 수 있습니다.

### 단점

*   **비효율적인 범위 검색**: 리프 노드들이 연결되어 있지 않아 범위 검색 시 트리를 다시 탐색해야 하므로 비효율적입니다.
*   **복잡한 구현**: 삽입 및 삭제 시 노드 분할 및 병합 로직이 B+ 트리보다 더 복잡할 수 있습니다.
*   **낮은 캐시 효율성**: 내부 노드에 데이터가 포함되어 있어 B+ 트리에 비해 노드당 더 적은 키를 저장하게 되므로, 트리의 높이가 높아질 수 있고 캐시 효율성이 떨어질 수 있습니다.

## 참고 자료

*   데이터베이스 시스템 (Database System Concepts) - Abraham Silberschatz, Henry F. Korth, S. Sudarshan
*   운영체제 (Operating System Concepts) - Abraham Silberschatz, Peter B. Galvin, Greg Gagne
*   B-tree - Wikipedia: [https://en.wikipedia.org/wiki/B-tree](https://en.wikipedia.org/wiki/B-tree)
