import pandas as pd

# v7 파일 로드 (v8 이전 버전)
v7_df = pd.read_csv(r'정리된_수리데이터_키워드분석_v7.csv', encoding='utf-8-sig')

# 사진에서 제공된 부품별 유형 매핑 (유형1→유형2→유형3 우선순위)
predefined_parts = {
    '14 WHEEL&TIRE A': ['마모', '크랙', '파손'],
    'COVER MAT-FOOTREST': ['마모', '변형', '파손'],
    'BATTERY PACK ASSY (H3.0/H3.5)': ['멈춤', '셀', '에러'],
    'KNUCKLE ASSY,LH-REAR': ['파손', '유격', '이탈'],
    'KNUCKLE ASSY,RH-REAR': ['파손', '유격', '이탈'],
    '300,SLIDE RAIL-UPPER': ['파손'],
    'KNUCKLE ASSY,RH-FRONT': ['파손', '유격', '이탈'],
    'DRIVESHAFT ASSY, LH': ['고무', '누유', '이탈'],
    'KNUCKLE ASSY,LH-FRONT': ['파손', '유격', '이탈'],
    'DRIVESHAFT ASSY, RH': ['고무', '누유', '이탈'],
    'REFRIGERATOR ASSY': ['누설', '온도'],
}

# 일반 키워드 목록 - 원래 순서대로 (파손 우선)
general_keywords = ['파손', '마모', '변형', '충돌', '충전', '분실', '작동불량', '소음', '누유', 
                   '고장', '깨짐', '오염', '교체', '불량', '부풀', '늘어남', '휘어짐', '크랙', 
                   '안됨', '안들어옴', '단선', '버튼', '유격', '베어링', '운행', '이탈', '멈춤',
                   '셀', '에러', '고무', '누설', '온도']

# 각 행별 키워드 분석
def get_keyword_for_row(row):
    part_name = row['2.부품명 보정']
    symptom = str(row['3.실증상']) if pd.notna(row['3.실증상']) else ''
    
    if pd.isna(part_name):
        return ''
    
    # 1. 사전 정의된 부품만: 유형1→유형2→유형3 순서 엄격 적용
    if part_name in predefined_parts:
        type_keywords = predefined_parts[part_name]
        for kw in type_keywords:
            if kw in symptom:
                return kw
        return type_keywords[0]
    
    # 2. 나머지 부품: 일반 키워드 분석 (파손 우선 - 기존대로)
    for kw in general_keywords:
        if kw in symptom:
            return kw
    return ''

# 키워드 재적용
print('사전 정의 부품만 우선순위 적용, 나머지는 기존대로...')
v7_df['7.주요 키워드'] = v7_df.apply(get_keyword_for_row, axis=1)

# v9 저장
v7_df.to_csv('정리된_수리데이터_키워드분석_v9.csv', index=False, encoding='utf-8-sig')

# 사전 정의 부품 확인
print('\n=== 사전 정의 부품 키워드 분포 ===')
for part in ['14 WHEEL&TIRE A', 'COVER MAT-FOOTREST']:
    part_data = v7_df[v7_df['2.부품명 보정'] == part]
    print(f'\n{part}:')
    print(part_data['7.주요 키워드'].value_counts().head(5))

# WHEEL CAP A 확인 (기존대로 파손 우선)
print('\n=== WHEEL CAP A (유형 미지정 - 기존대로) ===')
wheel_cap = v7_df[v7_df['2.부품명 보정'] == 'WHEEL CAP A']
print(wheel_cap['7.주요 키워드'].value_counts().head(5))

print(f'\n저장 파일: 정리된_수리데이터_키워드분석_v9.csv')
