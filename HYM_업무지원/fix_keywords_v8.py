import pandas as pd

# v7 파일 로드
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

# 일반 키워드 목록 - 마모를 파손보다 앞으로 이동!
general_keywords = ['마모', '파손', '변형', '충돌', '충전', '분실', '작동불량', '소음', '누유', 
                   '고장', '깨짐', '오염', '교체', '불량', '부풀', '늘어남', '휘어짐', '크랙', 
                   '안됨', '안들어옴', '단선', '버튼', '유격', '베어링', '운행', '이탈', '멈춤',
                   '셀', '에러', '고무', '누설', '온도']

# 각 행별 키워드 재분석
def get_keyword_for_row(row):
    part_name = row['2.부품명 보정']
    symptom = str(row['3.실증상']) if pd.notna(row['3.실증상']) else ''
    
    if pd.isna(part_name):
        return ''
    
    # 1. 사전 정의된 부품: 유형1→유형2→유형3 순서 엄격 적용
    if part_name in predefined_parts:
        type_keywords = predefined_parts[part_name]
        for kw in type_keywords:
            if kw in symptom:
                return kw
        return type_keywords[0]
    
    # 2. 나머지 부품: 일반 키워드 분석 (마모 우선)
    for kw in general_keywords:
        if kw in symptom:
            return kw
    return ''

# 키워드 재적용
print('일반 키워드 순서 수정하여 재처리 중...')
v7_df['7.주요 키워드'] = v7_df.apply(get_keyword_for_row, axis=1)

# v8 저장
v7_df.to_csv('정리된_수리데이터_키워드분석_v8.csv', index=False, encoding='utf-8-sig')

# 결과 확인: WHEEL CAP A 검증
print('\n=== WHEEL CAP A 수정 확인 ===')
wheel_cap = v7_df[v7_df['2.부품명 보정'] == 'WHEEL CAP A']
print(f'전체 건수: {len(wheel_cap)}')
print(wheel_cap['7.주요 키워드'].value_counts())

# 마모+파손 겹침 검증
problem_fixed = 0
for idx, row in wheel_cap.iterrows():
    symptom = str(row['3.실증상']) if pd.notna(row['3.실증상']) else ''
    keyword = row['7.주요 키워드']
    if '마모' in symptom and keyword == '마모':
        problem_fixed += 1
        
print(f'마모가 있을 때 마모로 표시된 건수: {problem_fixed}')

# 전체 키워드 분포
print('\n=== 전체 키워드 분포 (상위 10개) ===')
keyword_counts = v7_df['7.주요 키워드'].value_counts()
for kw, cnt in keyword_counts.head(10).items():
    if kw:
        print(f'{kw}: {cnt}건')

print(f'\n저장 파일: 정리된_수리데이터_키워드분석_v8.csv')
print(f'전체 데이터 건수: {len(v7_df)}')
