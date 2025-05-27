import pandas as pd

# 파일명(경로), 시트명(필요시) 지정
filename = '이중화 장비 업데이트 요청_20250526_개발팀 공유(seqno) (1).xlsx'
sheet_name = 0  # 기본 0번 시트 (필요시 이름으로 변경)

# 엑셀 파일을 DataFrame으로 읽기
df = pd.read_excel(filename, sheet_name=sheet_name, header=0)

# 필요한 컬럼 추출 및 공백제거/문자변환
# seqno(정수), hw_sn, barcode
df = df[['A', 'J', 'M']]  # A=seqno, J=hw_sn, M=barcode
df.columns = ['seqno', 'hw_sn', 'barcode']

# 결측값(NaN)을 파이썬 None으로 변환
df = df.where(pd.notnull(df), None)

# CASE WHEN 문자열 생성
def to_case_when(col):
    lines = []
    for _, row in df.iterrows():
        seqno = row['seqno']
        value = row[col]
        if value is None or str(value).strip() == '' or str(value).upper() == 'NAN':
            value_str = 'NULL'
        else:
            value_str = f"'{str(value).replace("'", "''")}'"
        lines.append(f"WHEN {int(seqno)} THEN {value_str}")
    return "\n        ".join(lines)

# seqno 목록 추출 (IN절용)
seqnos = ', '.join(str(int(x)) for x in df['seqno'] if pd.notnull(x))

# 최종쿼리 조합
sql = f"""
UPDATE sec_equipment
SET
    hw_sn = CASE seqno
        {to_case_when('hw_sn')}
        ELSE hw_sn
    END,
    barcode = CASE seqno
        {to_case_when('barcode')}
        ELSE barcode
    END
WHERE seqno IN ({seqnos});
"""

print(sql)