Apache Parquet는 Apache Hadoop 생태계에서 탄생한 열 지향(columnar) 저장 포맷이다. Google Dremel 논문(2010)의 중첩 데이터 표현 방식에서 영감을 받았으며, 분석 워크로드에 최적화된 이진 파일 포맷으로 설계되었다. 이 문서에서는 [apache/parquet-format](https://github.com/apache/parquet-format) 저장소의 공식 명세를 바탕으로 Parquet의 내부 구조를 바이트 수준까지 분석한다.

## 파일의 전체 레이아웃

Parquet 파일의 이진 레이아웃은 다음과 같다.

```
4바이트 매직 넘버 "PAR1"
<컬럼 1 청크 1>
<컬럼 2 청크 1>
...
<컬럼 N 청크 1>
<컬럼 1 청크 2>
<컬럼 2 청크 2>
...
<컬럼 N 청크 2>
...
<컬럼 1 청크 M>
<컬럼 2 청크 M>
...
<컬럼 N 청크 M>
파일 메타데이터 (Thrift TCompactProtocol로 직렬화)
파일 메타데이터의 바이트 길이 (4바이트, little-endian)
4바이트 매직 넘버 "PAR1"
```

N개의 컬럼이 M개의 로우 그룹으로 분할된 구조다. 핵심 설계 원칙은 **메타데이터가 데이터 뒤에 기록된다**는 것이다. 이 덕분에 단일 패스(single-pass)로 파일을 쓸 수 있다. 모든 데이터를 먼저 기록한 뒤 각 청크의 오프셋 정보를 메타데이터에 담아 마지막에 쓰면 되기 때문이다. 읽을 때는 파일 끝에서 메타데이터를 먼저 읽고, 거기에 기록된 오프셋으로 필요한 컬럼 청크만 찾아가서 읽는다.

암호화된 파일의 경우 매직 넘버가 `"PARE"`로 바뀌며, 이는 레거시 리더가 암호화된 파일을 일반 파일로 잘못 읽는 것을 방지한다.

## 계층 구조

Parquet 파일의 데이터는 4단계 계층으로 조직된다.

```
File
 └── Row Group (로우 그룹)
      └── Column Chunk (컬럼 청크)
           └── Page (페이지)
```

**파일(File)**: 하나의 HDFS 파일이며, 메타데이터를 반드시 포함한다. 데이터는 포함하지 않을 수도 있다(메타데이터만 있는 분할 파일 참조).

**로우 그룹(Row Group)**: 데이터를 행 단위로 수평 분할한 논리적 단위다. 하나의 로우 그룹은 데이터셋의 모든 컬럼에 대해 각각 하나의 컬럼 청크를 포함한다. 권장 크기는 512MB~1GB이며, HDFS 블록 하나에 맞추는 것이 이상적이다. MapReduce에서 병렬 처리의 기본 단위가 된다.

**컬럼 청크(Column Chunk)**: 특정 로우 그룹 내 특정 컬럼의 데이터 전체다. 파일 내에서 연속된 바이트로 보장된다. 이 연속성 덕분에 I/O 병렬화의 기본 단위가 된다. 하나의 컬럼 청크는 하나의 딕셔너리 페이지(선택)와 여러 데이터 페이지로 구성된다.

**페이지(Page)**: 압축과 인코딩의 최소 단위다. 권장 크기는 8KB이다. 페이지가 작을수록 단일 행 조회 같은 세밀한 읽기가 가능하지만 헤더 오버헤드가 늘어나고, 클수록 오버헤드는 줄지만 불필요한 데이터를 더 많이 읽게 된다.

## 원시 타입 (Physical Types)

Parquet는 7개의 원시 타입을 정의한다.

| 타입 | 크기 | 설명 |
|------|------|------|
| `BOOLEAN` | 1비트 | 참/거짓 |
| `INT32` | 4바이트 | 32비트 부호 있는 정수 |
| `INT64` | 8바이트 | 64비트 부호 있는 정수 |
| `INT96` | 12바이트 | 96비트 부호 있는 정수 (**사용 중단**) |
| `FLOAT` | 4바이트 | IEEE 754 32비트 부동소수점 |
| `DOUBLE` | 8바이트 | IEEE 754 64비트 부동소수점 |
| `BYTE_ARRAY` | 가변 | 임의 길이 바이트 배열 |
| `FIXED_LEN_BYTE_ARRAY` | 고정 | 고정 길이 바이트 배열 |

이 원시 타입들은 물리적 저장 단위이며, 논리적 의미(날짜, 시간, 문자열 등)는 별도의 논리 타입 어노테이션으로 부여된다.

## 인코딩 (Encodings)

Parquet는 데이터 특성에 따라 다양한 인코딩을 지원한다. 인코딩은 압축 이전 단계에서 데이터의 물리적 표현을 변환하여 압축 효율을 높인다.

### PLAIN 인코딩 (PLAIN = 0)

가장 기본적인 인코딩으로, 값을 연속으로 나열한다.

- **BOOLEAN**: 비트 패킹. LSB(Least Significant Bit) 우선 순서로 바이트에 채운다.
- **INT32**: 4바이트 little-endian.
- **INT64**: 8바이트 little-endian.
- **INT96**: 12바이트 little-endian (사용 중단).
- **FLOAT**: 4바이트 IEEE 754 little-endian.
- **DOUBLE**: 8바이트 IEEE 754 little-endian.
- **BYTE_ARRAY**: 4바이트 길이(little-endian) + 바이트 데이터.
- **FIXED_LEN_BYTE_ARRAY**: 바이트 데이터만 (길이 접두사 없음, 스키마에서 길이를 알 수 있으므로).

### 딕셔너리 인코딩 (RLE_DICTIONARY = 8)

컬럼 내 고유 값의 수가 적을 때 매우 효과적이다. 원리는 간단하다.

1. 컬럼 청크의 모든 고유 값을 수집하여 **딕셔너리 페이지**에 PLAIN 인코딩으로 저장한다.
2. 데이터 페이지에는 실제 값 대신 딕셔너리 인덱스(정수)를 저장한다.
3. 인덱스는 RLE/비트패킹 하이브리드 인코딩으로 압축한다.

데이터 페이지의 포맷은 `1바이트 비트 너비(최대 32)` + `RLE/비트패킹으로 인코딩된 인덱스 시퀀스`이다.

딕셔너리가 너무 커지면(고유 값이 많으면) PLAIN으로 폴백한다. 이전 식별자 `PLAIN_DICTIONARY(=2)`는 사용 중단되었으며, 딕셔너리 페이지는 `PLAIN`, 데이터 페이지는 `RLE_DICTIONARY`를 사용하도록 권장된다.

### RLE/비트패킹 하이브리드 (RLE = 3)

BOOLEAN 값과 딕셔너리 인덱스, 그리고 반복/정의 레벨에 사용되는 핵심 인코딩이다. 두 가지 런(run)을 섞어 쓴다.

```
rle-bit-packed-hybrid: <length: 4바이트 LE uint32> <encoded-data>
encoded-data := <run>*
run := <bit-packed-run> | <rle-run>
```

**RLE 런**: 같은 값이 반복될 때 사용한다.
```
rle-run := <rle-header> <repeated-value>
rle-header := varint-encode(반복 횟수 << 1)    // LSB가 0
repeated-value := ceil(bit-width / 8) 바이트로 인코딩된 값
```

**비트패킹 런**: 서로 다른 값이 연속될 때 사용한다.
```
bit-packed-run := <bit-packed-header> <bit-packed-values>
bit-packed-header := varint-encode((값의 수 / 8) << 1 | 1)  // LSB가 1
```

값은 LSB 우선으로 패킹된다. 예를 들어 비트 너비 3으로 1~7을 패킹하면:

```
값:     0       1       2       3       4       5       6       7
비트:   000     001     010     011     100     101     110     111
바이트: 10001000 11000110 11111010
```

varint 인코딩은 ULEB-128을 사용하며, 런 길이의 범위는 [1, 2^31 - 1]이다.

길이 접두사 규칙은 페이지 버전에 따라 다르다.

| 페이지 종류 | 데이터 종류 | 길이 접두사 여부 |
|------------|-----------|----------------|
| Data Page V1 | 정의/반복 레벨 | 있음 |
| Data Page V1 | 딕셔너리 인덱스 | 없음 |
| Data Page V1 | BOOLEAN 값 | 있음 |
| Data Page V2 | 정의/반복 레벨 | 없음 |
| Data Page V2 | 딕셔너리 인덱스 | 없음 |
| Data Page V2 | BOOLEAN 값 | 있음 |

### 델타 이진 패킹 (DELTA_BINARY_PACKED = 5)

INT32와 INT64에 사용된다. Lemire & Boytsov(2012)의 "Decoding billions of integers per second through vectorization" 논문을 기반으로 한다. 정렬되었거나 값의 변화폭이 작은 정수 시퀀스에 특히 효과적이다.

**구조**:
```
헤더: <블록 크기> <블록당 미니블록 수> <총 값 수> <첫 번째 값>
블록: <최소 델타> <각 미니블록의 비트 너비 목록> <미니블록들>
```

- 블록 크기: 128의 배수. ULEB128로 인코딩.
- 총 값 수: ULEB128.
- 첫 번째 값: 지그재그 + ULEB128.
- 최소 델타: 지그재그 + ULEB128.
- 각 미니블록의 비트 너비: 1바이트씩.

알고리즘:
1. 연속된 값들의 차이(델타)를 계산한다.
2. 블록 내 최소 델타를 구하고, 모든 델타에서 이를 뺀다(프레임 오브 레퍼런스).
3. 최소 델타를 지그재그 ULEB128로, 각 미니블록의 비트 너비를 1바이트로, 조정된 델타들을 비트 패킹으로 인코딩한다.

예를 들어 `[7, 5, 3, 1, 2, 3, 4, 5]`를 인코딩하면 델타는 `[-2, -2, -2, 1, 1, 1, 1]`이 되고, 최소 델타 `-2`를 빼면 `[0, 0, 0, 3, 3, 3, 3]`이 되어 각 값을 2비트로 표현할 수 있다.

### 델타 길이 바이트 배열 (DELTA_LENGTH_BYTE_ARRAY = 6)

BYTE_ARRAY 전용이다. 길이들을 DELTA_BINARY_PACKED로 인코딩하고, 바이트 데이터는 연접(concatenation)한다.

```
<델타 인코딩된 길이들> <바이트 배열 데이터 연접>
```

예시 — `"Hello"`, `"World"`, `"Foobar"`, `"ABCDEF"`:
- 길이: DeltaEncoding(5, 5, 6, 6)
- 데이터: `"HelloWorldFoobarABCDEF"`

### 델타 바이트 배열 (DELTA_BYTE_ARRAY = 7)

BYTE_ARRAY와 FIXED_LEN_BYTE_ARRAY에 사용된다. 사전식으로 정렬된 문자열에 매우 효과적인 **전방 압축(front compression)** 기법이다.

```
<델타 인코딩된 접두사 길이들> <접미사들 (DELTA_LENGTH_BYTE_ARRAY로 인코딩)>
```

예시 — `"axis"`, `"axle"`, `"babble"`, `"babyhood"`:
- 접두사 길이: DeltaEncoding(0, 2, 0, 3) — `"axis"`와 공통 접두사 0, `"axle"`은 `"ax"` 공유(2), `"babble"`은 0, `"babyhood"`는 `"bab"` 공유(3)
- 접미사: `"axis"`, `"le"`, `"babble"`, `"yhood"`
- 접미사 길이: DeltaEncoding(4, 2, 6, 5)
- 접미사 데이터: `"axislebabbleyhood"`

### 바이트 스트림 분할 (BYTE_STREAM_SPLIT = 9)

FLOAT, DOUBLE, INT32, INT64, FIXED_LEN_BYTE_ARRAY에 사용된다. 데이터 크기를 줄이지는 않지만, 후속 압축기(Snappy, Zstd 등)의 효율을 크게 높인다.

원리는 N개의 K-바이트 값에서 같은 위치의 바이트를 모아 K개의 스트림을 만드는 것이다.

```
원본 (3개의 float): AA BB CC DD | 00 11 22 33 | A3 B4 C5 D6
인코딩 후:          AA 00 A3 | BB 11 B4 | CC 22 C5 | DD 33 D6
```

부동소수점의 경우 같은 위치의 바이트(특히 지수부)가 유사한 패턴을 보이므로, 이 재배열만으로 압축률이 크게 향상된다. 총 크기는 K × N 바이트로 변하지 않으며, 메타데이터나 패딩도 없다.

## 중첩 데이터 인코딩 (Dremel 방식)

Parquet는 Google Dremel의 논문에서 가져온 **반복 레벨(Repetition Level)**과 **정의 레벨(Definition Level)**로 중첩 데이터를 평탄화한다.

### 정의 레벨 (Definition Level)

컬럼 경로 상의 선택적(optional) 필드 중 몇 개가 정의되었는지를 나타낸다. 최대 정의 레벨은 경로 상의 optional/repeated 필드 수와 같다.

예를 들어 스키마가 다음과 같을 때:
```
message Document {
  optional group links {
    repeated group forward {
      required string url;
    }
  }
}
```

`Document.links.forward.url`의 최대 정의 레벨은 3이다(links: optional → 1, forward: repeated → 2, url: required이지만 부모가 정의되어야 하므로 → 3).

- 정의 레벨 0: `links`가 null
- 정의 레벨 1: `links`는 있지만 `forward` 리스트가 비어있음
- 정의 레벨 2: `forward`는 있지만 `url`이 null (이 스키마에서는 url이 required이므로 불가)
- 정의 레벨 3: 값이 존재

### 반복 레벨 (Repetition Level)

경로 상의 어떤 반복 필드에서 값이 반복되는지를 나타낸다. 0이면 새로운 최상위 레코드(행)의 시작이다.

### NULL 인코딩

NULL 값은 데이터 자체에 인코딩되지 않는다. 정의 레벨만으로 표현된다. 예를 들어 1000개의 NULL이 연속되면 정의 레벨에 `(0, 1000회)`라는 RLE 런 하나만 기록되고, 데이터 영역은 비어있다. 이는 희소(sparse) 컬럼에 매우 효율적이다.

### 데이터 페이지의 내부 구조

데이터 페이지는 헤더 다음에 세 부분이 패딩 없이 연속으로 기록된다.

```
[반복 레벨 데이터] [정의 레벨 데이터] [인코딩된 값]
```

- 비중첩 컬럼(경로 길이 1)에서는 반복 레벨이 생략된다.
- 모든 값이 required인 컬럼에서는 정의 레벨이 생략된다.
- 헤더의 `uncompressed_page_size`는 세 부분의 합산 크기이다.

## 페이지 구조 상세

### Data Page V1

```thrift
struct DataPageHeader {
  1: required i32 num_values           // 페이지 내 값의 수 (NULL 포함)
  2: required Encoding encoding         // 값의 인코딩 방식
  3: required Encoding definition_level_encoding  // 정의 레벨 인코딩
  4: required Encoding repetition_level_encoding  // 반복 레벨 인코딩
  5: optional Statistics statistics      // 페이지 통계
}
```

V1에서는 반복/정의 레벨, 값 데이터 모두가 함께 압축된다.

### Data Page V2

```thrift
struct DataPageHeaderV2 {
  1: required i32 num_values                    // 값의 수
  2: required i32 num_nulls                     // NULL 수
  3: required i32 num_rows                      // 행의 수
  4: required Encoding encoding                  // 값의 인코딩
  5: required i32 definition_levels_byte_length  // 정의 레벨 바이트 길이
  6: required i32 repetition_levels_byte_length  // 반복 레벨 바이트 길이
  7: optional bool is_compressed = true          // 압축 여부
  8: optional Statistics statistics
}
```

V2의 중요한 차이점:
- 반복/정의 레벨은 **항상 RLE 인코딩**이며, 길이 접두사가 없다.
- 반복/정의 레벨은 **항상 비압축** 상태로 저장된다. 압축은 값 데이터에만 적용된다.
- 페이지는 반드시 **행 경계에서 시작**해야 한다.
- `num_nulls`와 `num_rows`가 명시되어 있어 레벨을 디코딩하지 않고도 페이지의 특성을 파악할 수 있다.

### 딕셔너리 페이지

```thrift
struct DictionaryPageHeader {
  1: required i32 num_values     // 딕셔너리 항목 수
  2: required Encoding encoding   // 항상 PLAIN
  3: optional bool is_sorted      // 정렬 여부
}
```

딕셔너리 페이지는 컬럼 청크의 **첫 번째 페이지**여야 하며, 컬럼 청크당 **최대 하나**만 존재할 수 있다.

### 페이지 헤더 래퍼

```thrift
struct PageHeader {
  1: required PageType type                          // 페이지 유형
  2: required i32 uncompressed_page_size             // 비압축 크기
  3: required i32 compressed_page_size               // 압축 후 크기
  4: optional i32 crc                                // CRC32 체크섬
  5: optional DataPageHeader data_page_header
  6: optional IndexPageHeader index_page_header
  7: optional DictionaryPageHeader dictionary_page_header
  8: optional DataPageHeaderV2 data_page_header_v2
}
```

페이지 유형은 `DATA_PAGE(0)`, `INDEX_PAGE(1)`, `DICTIONARY_PAGE(2)`, `DATA_PAGE_V2(3)`의 4종류다.

### 체크섬

각 페이지는 표준 CRC32(다항식 `0x04C11DB7`, GZip과 동일)로 개별 검증할 수 있다. CRC는 페이지 헤더를 제외한 직렬화된 바이너리 데이터에 대해 계산되며, 압축 및 암호화 **이후** 단계에서 산출된다.

## 메타데이터 구조

모든 메타데이터는 Apache Thrift의 **TCompactProtocol**로 직렬화된다.

### FileMetaData

```thrift
struct FileMetaData {
  1: required i32 version                            // 파일 버전 (항상 1로 기록)
  2: required list<SchemaElement> schema              // 스키마 트리의 DFS 평탄화
  3: required i64 num_rows                            // 전체 행 수
  4: required list<RowGroup> row_groups               // 로우 그룹 목록
  5: optional list<KeyValue> key_value_metadata       // 사용자 정의 키-값 메타데이터
  6: optional string created_by                       // 생성 라이브러리 정보
  7: optional list<ColumnOrder> column_orders         // 컬럼별 정렬 순서
  8: optional EncryptionAlgorithm encryption_algorithm
  9: optional binary footer_signing_key_metadata
}
```

`version` 필드에 대해: 작성자는 항상 `1`을 기록해야 하며, 독자는 `1`과 `2`를 동일하게 처리해야 한다.

### SchemaElement

```thrift
struct SchemaElement {
  1: optional Type type                    // 원시 타입 (리프 노드만)
  2: optional i32 type_length              // FIXED_LEN_BYTE_ARRAY의 길이
  3: optional FieldRepetitionType repetition_type  // REQUIRED/OPTIONAL/REPEATED
  4: required string name                  // 필드 이름
  5: optional i32 num_children             // 자식 수 (그룹 노드만)
  6: optional ConvertedType converted_type // 사용 중단된 논리 타입
  7: optional i32 scale                    // DECIMAL 스케일
  8: optional i32 precision                // DECIMAL 정밀도
  9: optional i32 field_id                 // Thrift/Protocol Buffer 필드 ID
  10: optional LogicalType logicalType     // 논리 타입
}
```

스키마는 트리 구조를 **깊이 우선 탐색(DFS)** 으로 평탄화한 리스트로 표현된다. 루트 노드에는 `repetition_type`이 없다. 리프 노드에는 `type`이 있고 `num_children`이 없으며, 그룹 노드에는 `type`이 없고 `num_children`이 있다.

### RowGroup

```thrift
struct RowGroup {
  1: required list<ColumnChunk> columns          // 컬럼 청크 목록
  2: required i64 total_byte_size                // 비압축 총 바이트 크기
  3: required i64 num_rows                       // 행 수
  4: optional list<SortingColumn> sorting_columns // 정렬 정보
  5: optional i64 file_offset                    // 파일 내 오프셋
  6: optional i64 total_compressed_size          // 압축 총 바이트 크기
  7: optional i16 ordinal                        // 로우 그룹 순번
}
```

### ColumnChunk과 ColumnMetaData

```thrift
struct ColumnChunk {
  1: optional string file_path                // 외부 파일 경로 (분할 저장 시)
  2: required i64 file_offset = 0             // 사용 중단
  3: optional ColumnMetaData meta_data        // 컬럼 메타데이터
  4: optional i64 offset_index_offset         // OffsetIndex 오프셋
  5: optional i32 offset_index_length         // OffsetIndex 길이
  6: optional i64 column_index_offset         // ColumnIndex 오프셋
  7: optional i32 column_index_length         // ColumnIndex 길이
  8: optional ColumnCryptoMetaData crypto_metadata
  9: optional binary encrypted_column_metadata
}

struct ColumnMetaData {
  1: required Type type                       // 원시 타입
  2: required list<Encoding> encodings        // 사용된 인코딩 목록
  3: required list<string> path_in_schema     // 스키마 내 경로
  4: required CompressionCodec codec          // 압축 코덱
  5: required i64 num_values                  // 값의 수
  6: required i64 total_uncompressed_size     // 비압축 총 크기
  7: required i64 total_compressed_size       // 압축 총 크기
  8: optional list<KeyValue> key_value_metadata
  9: required i64 data_page_offset            // 첫 번째 데이터 페이지 오프셋
  10: optional i64 index_page_offset
  11: optional i64 dictionary_page_offset     // 딕셔너리 페이지 오프셋
  12: optional Statistics statistics           // 컬럼 통계
  13: optional list<PageEncodingStats> encoding_stats
  14: optional i64 bloom_filter_offset        // 블룸 필터 오프셋
  15: optional i32 bloom_filter_length        // 블룸 필터 길이
  16: optional SizeStatistics size_statistics
}
```

### Statistics

```thrift
struct Statistics {
  1: optional binary max            // 사용 중단 (부호 있는 비교만 사용)
  2: optional binary min            // 사용 중단
  3: optional i64 null_count        // NULL 수
  4: optional i64 distinct_count    // 고유 값 수
  5: optional binary max_value      // 최댓값 (ColumnOrder에 따른 비교)
  6: optional binary min_value      // 최솟값
  7: optional bool is_max_value_exact  // 최댓값이 정확한지 (잘림 여부)
  8: optional bool is_min_value_exact  // 최솟값이 정확한지
}
```

`min`/`max` 필드가 사용 중단된 이유가 흥미롭다. 초기 구현에서는 부호 있는(signed) 바이트 비교만 사용했는데, 부호 없는(unsigned) 타입에서 잘못된 결과를 낳았다. `min_value`/`max_value`는 컬럼의 ColumnOrder를 따르도록 수정된 필드다.

값은 PLAIN 인코딩으로 직렬화되며, 가변 길이 바이트 배열의 경우 길이 접두사가 없다.

## 논리 타입 (Logical Types)

논리 타입은 원시 타입에 의미를 부여하는 어노테이션이다.

### 문자열 및 식별자

| 논리 타입 | 원시 타입 | 설명 |
|----------|----------|------|
| `STRING` | `BYTE_ARRAY` | UTF-8 인코딩 문자열 |
| `ENUM` | `BYTE_ARRAY` | UTF-8 인코딩 열거형 |
| `UUID` | `FIXED_LEN_BYTE_ARRAY(16)` | 빅엔디안 UUID |

### 숫자 타입

**정수**: `INT(bitWidth, isSigned)` — bitWidth는 {8, 16, 32, 64}. 8/16/32비트는 INT32에, 64비트는 INT64에 매핑된다.

**DECIMAL**: `unscaledValue × 10^(-scale)`. scale ≥ 0, precision > 0.

| 원시 타입 | 정밀도 범위 |
|----------|-----------|
| `INT32` | 1~9 |
| `INT64` | 1~18 (10 미만은 경고) |
| `FIXED_LEN_BYTE_ARRAY(n)` | ⌊log₁₀(2^(8n-1) - 1)⌋까지 |
| `BYTE_ARRAY` | 제한 없음 |

BYTE_ARRAY와 FIXED_LEN_BYTE_ARRAY의 경우 비스케일 값은 **2의 보수 빅엔디안**으로 인코딩된다.

**FLOAT16**: `FIXED_LEN_BYTE_ARRAY(2)`. IEEE 반정밀도, **little-endian**.

### 시간 타입

**DATE**: `INT32`. Unix 에포크(1970-01-01)로부터의 일 수. 부호 있는 비교.

**TIME**: 자정 이후 경과 시간.

| 단위 | 원시 타입 | 범위 |
|------|----------|------|
| MILLIS | `INT32` | 밀리초 |
| MICROS | `INT64` | 마이크로초 |
| NANOS | `INT64` | 나노초 |

`isAdjustedToUTC` 매개변수가 UTC 보정 여부를 나타낸다.

**TIMESTAMP**: `INT64`. Unix 에포크 이후 경과 시간.

- `isAdjustedToUTC=true`: UTC 기준 절대 시점. 모호하지 않은 순간(instant).
- `isAdjustedToUTC=false`: 로컬 타임스탬프. 1970-01-01 00:00:00 로컬 시간 기준 오프셋. DST 보정 없이 하루를 정확히 86,400초로 취급한다.
- NANOS 범위: 1677-09-21 00:12:43 ~ 2262-04-11 23:47:16.

**INTERVAL**: `FIXED_LEN_BYTE_ARRAY(12)`. 세 개의 little-endian unsigned 32비트 정수: 월(4바이트) + 일(4바이트) + 밀리초(4바이트). 정렬 순서가 정의되지 않아 min/max 통계를 기록하지 않는다.

### 내장 타입

- **JSON**: `BYTE_ARRAY`. UTF-8 JSON 문자열.
- **BSON**: `BYTE_ARRAY`. BSON 문서.
- **VARIANT**: 그룹 타입. required `metadata`(binary)와 optional/required `value`(binary) 필드로 구성. 분해된(shredded) variant 값을 지원한다.
- **GEOMETRY**: `BYTE_ARRAY`. WKB(Well-Known Binary) 포맷. 선형 에지. 기본 CRS는 `"OGC:CRS84"`.
- **GEOGRAPHY**: `BYTE_ARRAY`. WKB 포맷. 명시적 에지 보간. 알고리즘 매개변수(SPHERICAL/VINCENTY/THOMAS/ANDOYER/KARNEY).

### 중첩 타입

**LIST**:
```
<반복타입> group <이름> (LIST) {
  repeated group list {
    <요소반복타입> <요소타입> element;
  }
}
```

**MAP**:
```
<반복타입> group <이름> (MAP) {
  repeated group key_value {
    required <키타입> key;
    <값반복타입> <값타입> value;
  }
}
```

key는 반드시 `required`이며 첫 번째 필드여야 한다. 중복 키가 있으면 마지막 값이 우선한다.

## 정렬 순서 (Column Order)

통계의 min/max 비교에 사용되는 정렬 규칙이다.

| 논리 타입 | 비교 방식 |
|----------|----------|
| STRING, JSON, BSON, ENUM | 부호 없는 바이트 비교 |
| INT8/16/32/64 | 부호 있는 비교 |
| UINT8/16/32/64 | 부호 없는 비교 |
| DECIMAL | 표현 값의 부호 있는 비교 |
| DATE, TIME_*, TIMESTAMP_* | 부호 있는 비교 |
| FLOAT, DOUBLE, FLOAT16 | 표현 값의 부호 있는 비교 (NaN/영점 특수 처리) |
| BOOLEAN | false < true |
| BYTE_ARRAY, FIXED_LEN_BYTE_ARRAY | 부호 없는 바이트 비교 |
| INT96, INTERVAL, LIST, MAP, VARIANT, GEOMETRY, GEOGRAPHY | 미정의 |

**부동소수점 특수 규칙**: NaN은 min/max에 기록하지 않으며, 읽을 때 min이 NaN이면 무시한다. 최댓값이 0이면 `+0.0`을, 최솟값이 0이면 `-0.0`을 기록하여 IEEE 754의 부호 있는 영점 구분을 처리한다.

## 페이지 인덱스 (Page Index)

페이지 인덱스는 **페이지 스킵핑(page skipping)** 을 가능하게 하는 구조로, 정렬된 컬럼뿐 아니라 비정렬 컬럼에서도 작동한다.

### ColumnIndex

```thrift
struct ColumnIndex {
  1: required list<bool> null_pages         // 페이지가 전부 NULL인지
  2: required list<binary> min_values       // 페이지별 최솟값
  3: required list<binary> max_values       // 페이지별 최댓값
  4: required BoundaryOrder boundary_order  // UNORDERED/ASCENDING/DESCENDING
  5: optional list<i64> null_counts         // 페이지별 NULL 수
  6: optional list<i64> repetition_level_histograms
  7: optional list<i64> definition_level_histograms
}
```

- `null_pages[i]`가 true이면 i번째 페이지는 전부 NULL이고, min/max는 빈 바이트 배열로 설정된다.
- `min_values`/`max_values`는 **잘림(truncation)** 이 허용된다. 예를 들어 실제 최솟값이 `"Blart Versenwald III"`여도 `"B"`로 줄여 저장할 수 있다.
- `boundary_order`가 `ASCENDING`이나 `DESCENDING`이면 이진 검색이 가능하고, `UNORDERED`이면 순차 스캔해야 한다.
- 히스토그램 길이는 `페이지 수 × (최대 레벨 + 1)`이다.

### OffsetIndex

```thrift
struct OffsetIndex {
  1: required list<PageLocation> page_locations
  2: optional list<i64> unencoded_byte_array_data_bytes
}

struct PageLocation {
  1: required i64 offset                   // 페이지의 파일 내 오프셋
  2: required i32 compressed_page_size     // 압축된 페이지 크기
  3: required i64 first_row_index          // 페이지의 첫 번째 행 인덱스
}
```

`page_locations`는 오프셋 증가 순으로 정렬되며, `first_row_index`는 엄격하게 증가해야 한다. OffsetIndex가 존재하면 페이지는 반드시 행 경계(반복 레벨 = 0)에서 시작해야 한다.

### 파일 내 위치

ColumnIndex와 OffsetIndex는 로우 그룹과 별도로, 파일 푸터 근처에 저장된다. 이는 선택적 스캔을 하지 않는 경우 불필요한 I/O를 피하기 위한 설계다. 오프셋과 길이는 ColumnChunk의 `offset_index_offset`/`offset_index_length`, `column_index_offset`/`column_index_length` 필드에 기록된다.

### 사용 방식

- **정렬된 컬럼**: `boundary_order`를 이용한 이진 검색으로 관련 페이지만 식별한다.
- **비정렬 컬럼**: min/max를 순차적으로 스캔하여 술어(predicate)를 만족할 수 없는 페이지를 제외한다.

## 블룸 필터 (Bloom Filter)

Parquet는 **Split Block Bloom Filter(SBBF)** 를 사용한다. 포인트 쿼리(특정 값의 존재 여부)에 대해 false positive는 있지만 false negative는 없는 확률적 자료구조다.

### 블록 구조

블룸 필터는 z개의 블록으로 구성되며(1 ≤ z < 2^31), 각 블록은 256비트 = 8개의 32비트 워드이다.

### 솔트 상수

```
salt[8] = {
  0x47b6137b, 0x44974d91, 0x8824ad5b, 0xa2b7289d,
  0x705495c7, 0x2df1424b, 0x9efc4947, 0x5c6bfb31
}
```

### 마스크 연산

```
block mask(uint32 x):
  for i in [0..7]:
    uint32 y = x * salt[i]    // 하위 32비트만 유지
    result.word[i].setBit(y >> 27)  // 비트 인덱스 0~31
  return result
```

각 솔트와 입력의 곱에서 상위 5비트를 추출하여 8개 워드에 각각 1비트씩 설정한다.

### 필터 연산

64비트 해시 h에서 블록을 선택하는 방식:
```c
uint64 h_top = h >> 32;
uint32 block_index = (h_top * z) >> 32;
```

상위 32비트를 필터 크기와 곱하여 블록 인덱스를 산출한다. 그런 다음 하위 32비트를 마스크 연산에 사용한다.

### 해시 함수

**xxHash(XXH64)**, 시드 0, 명세 버전 0.1.1을 사용한다. 컬럼 값은 PLAIN 인코딩으로 직렬화한 후 해시한다.

### 크기와 오탐률

| 삽입당 비트 수 | 오탐 확률 |
|--------------|----------|
| 6.0 | 10% |
| 10.5 | 1% |
| 16.9 | 0.1% |
| 26.4 | 0.01% |
| 41 | 0.001% |

### 파일 내 배치

블룸 필터 = 헤더(Thrift) + 비트셋(바이너리). ColumnMetaData의 `bloom_filter_offset`과 `bloom_filter_length`로 참조된다. 모든 로우 그룹 이후에 페이지 인덱스 앞에 배치하거나, 로우 그룹 사이에 배치할 수 있다.

## 압축 코덱

| 코덱 | 열거값 | 비고 |
|------|-------|------|
| UNCOMPRESSED | 0 | 무압축 |
| SNAPPY | 1 | Google Snappy 포맷 |
| GZIP | 2 | RFC 1952 (zlib/deflate가 아님) |
| LZO | 3 | Oberhumer LZO 라이브러리 |
| BROTLI | 4 | RFC 7932. v2.4에서 추가 |
| LZ4 | 5 | **사용 중단**. Hadoop의 비표준 프레이밍 |
| ZSTD | 6 | RFC 8478. v2.4에서 추가 |
| LZ4_RAW | 7 | LZ4 블록 포맷 (프레이밍 없음). v2.9에서 추가 |

LZ4(=5)가 사용 중단된 이유는 Hadoop에서 사용한 비표준 프레이밍 때문에 구현 간 호환성 문제가 발생했기 때문이다. LZ4_RAW(=7)가 이를 대체한다.

모든 코덱은 추가 프레이밍이나 패딩 없이 데이터를 그대로 압축 라이브러리에 전달한다(사용 중단된 LZ4 제외).

## 암호화 (Parquet Modular Encryption)

Parquet 모듈식 암호화는 열 지향 프로젝션, 술어 푸시다운, 인코딩, 압축을 보존하면서 파일 데이터와 메타데이터를 암호화하고 인증한다.

### 암호화 모듈 단위

각각 독립적으로 암호화되는 모듈:
- 페이지와 페이지 헤더 (딕셔너리 및 데이터)
- 컬럼 인덱스
- 오프셋 인덱스
- 블룸 필터 헤더와 비트셋
- 푸터 (FileMetaData)
- 컬럼 메타데이터 (컬럼 키가 푸터 키와 다를 때)

### 암호화 알고리즘

AES 대칭 암호화 기반이며, 128/192/256비트 키를 지원한다.

**AES_GCM_V1**: 모든 모듈을 AES GCM으로 암호화한다. 출력은 `암호문(평문과 동일 길이) + 16바이트 인증 태그`이다.

**AES_GCM_CTR_V1**: 페이지를 제외한 모든 모듈은 AES GCM을 사용하고, 페이지만 AES CTR을 사용한다. CTR은 더 빠르지만 무결성 검증이 없다.

### 직렬화 포맷

GCM 모듈:
```
[길이: 4바이트 LE] [논스: 12바이트] [암호문: (길이-28)바이트] [태그: 16바이트]
```

CTR 모듈 (AES_GCM_CTR_V1의 페이지만):
```
[길이: 4바이트 LE] [논스: 12바이트] [암호문: (길이-12)바이트]
```

### AAD (추가 인증 데이터)

AAD = AAD 접두사 + AAD 접미사.

AAD 접미사 구성:
1. 내부 파일 식별자 (랜덤 바이트)
2. 모듈 유형 (1바이트) — Footer(0), ColumnMetaData(1), DataPage(2), DictionaryPage(3), DataPageHeader(4), DictionaryPageHeader(5), ColumnIndex(6), OffsetIndex(7), BloomFilterHeader(8), BloomFilterBitset(9)
3. 로우 그룹 순번 (2바이트 LE) — 푸터 제외
4. 컬럼 순번 (2바이트 LE) — 푸터 제외
5. 페이지 순번 (2바이트 LE) — 데이터/딕셔너리 페이지만

### 암호화 푸터 모드 vs 평문 푸터 모드

**암호화 푸터 모드**: 매직 바이트가 `"PARE"`로 변경된다. `FileCryptoMetaData`가 암호화된 푸터 앞에 기록된다.

**평문 푸터 모드**: 매직 바이트는 `"PAR1"`을 유지하여 레거시 리더와의 호환성을 확보한다. 푸터 자체는 암호화하지 않고 **서명**만 한다. FileMetaData를 AES GCM으로 암호화하되 암호문은 버리고 `논스(12바이트) + 태그(16바이트)` = 28바이트 서명만 저장한다. 암호화된 컬럼의 통계는 평문 푸터에서 제거되고, `encrypted_column_metadata` 필드를 통해 별도로 제공된다.

### 암호화 오버헤드

기본 1MB 페이지 기준으로 페이지당 32바이트의 암호화 오버헤드가 발생한다. 원본 데이터 약 30,000바이트당 1바이트 수준으로, 크기 영향은 무시할 수 있다.

### 키 호출 제한

NIST SP 800-38D 섹션 8.3에 따라 하나의 키로 최대 2^32회 호출이 가능하다. 실질적으로 하나의 키가 약 2^31개 이상의 페이지를 암호화해서는 안 된다.

## 오류 복구

Parquet의 오류 복구 전략은 계층 구조를 따른다.

| 손상 위치 | 영향 범위 |
|----------|----------|
| 파일 메타데이터 | 전체 파일 손실 |
| 컬럼 메타데이터 | 해당 컬럼 청크 손실 (다른 로우 그룹의 동일 컬럼은 무관) |
| 페이지 헤더 | 해당 청크의 나머지 페이지 전부 손실 |
| 페이지 데이터 | 해당 페이지만 손실 |

로우 그룹을 작게 만들면 손상 시 손실 범위가 줄어들지만, 메타데이터 오버헤드와 압축 효율 간의 트레이드오프가 있다.

## 확장성 설계

Parquet 포맷은 여러 확장 메커니즘을 갖추고 있다.

- **인코딩 열거형**: 새로운 인코딩을 번호로 추가할 수 있다.
- **페이지 유형**: 알 수 없는 페이지 유형은 안전하게 건너뛸 수 있다.
- **Thrift 예약 필드**: 모든 구조체에서 field-id `32767`이 이진 프로토콜 확장을 위해 예약되어 있다.
- **키-값 메타데이터**: FileMetaData와 ColumnMetaData에 임의의 키-값 쌍을 첨부할 수 있다.

## 읽기 흐름 요약

Parquet 파일을 읽는 전체 흐름을 정리하면 다음과 같다.

1. 파일 끝에서 4바이트 매직 넘버(`"PAR1"` 또는 `"PARE"`)를 확인한다.
2. 매직 넘버 바로 앞 4바이트에서 푸터 길이를 읽는다.
3. 푸터 길이만큼 앞으로 이동하여 FileMetaData를 TCompactProtocol로 역직렬화한다.
4. 스키마(SchemaElement 리스트)를 DFS 순서로 복원하여 트리를 재구성한다.
5. 쿼리에 필요한 컬럼과 로우 그룹을 식별한다.
6. (선택) ColumnIndex를 읽어 페이지 수준 술어 필터링을 수행한다.
7. (선택) 블룸 필터를 읽어 포인트 쿼리의 로우 그룹/페이지를 걸러낸다.
8. ColumnMetaData의 오프셋으로 이동하여 필요한 컬럼 청크만 읽는다.
9. 딕셔너리 페이지(있으면)를 먼저 디코딩한다.
10. 데이터 페이지의 반복/정의 레벨을 디코딩하여 중첩 구조와 NULL을 복원한다.
11. 값 데이터를 해당 인코딩에 따라 디코딩한다.

이 과정에서 열 지향 포맷의 핵심 이점이 드러난다. 100개 컬럼 중 3개만 필요한 쿼리는 전체 데이터의 3%만 I/O하면 된다. 페이지 인덱스와 블룸 필터를 활용하면 그 3%에서도 관련 없는 페이지를 추가로 건너뛸 수 있다.

#### 참고 자료
1. Apache Parquet Format Specification, [apache/parquet-format](https://github.com/apache/parquet-format)
2. Melnik et al. (2010), "Dremel: Interactive Analysis of Web-Scale Datasets", VLDB 2010
3. Lemire & Boytsov (2012), "Decoding billions of integers per second through vectorization"
4. NIST SP 800-38D, "Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC"
