import pandas as pd

# v6 파일 로드
v6_df = pd.read_csv(r'정리된_수리데이터_키워드분석_v6.csv', encoding='utf-8-sig')

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

# 일반 키워드 목록 (나머지 부품용)
general_keywords = ['파손', '마모', '변형', '충돌', '충전', '분실', '작동불량', '소음', '누유', 
                   '고장', '깨짐', '오염', '교체', '불량', '부풀', '늘어남', '휘어짐', '크랙', 
                   '안됨', '안들어옴', '단선', '버튼', '유격', '베어링', '운행', '이탈', '멈춤',
                   '셀', '에러', '고무', '누설', '온도']

# 각 행별 키워드 재분석 (우선순위 엄격 적용)
def get_keyword_for_row(row):
    part_name = row['2.부품명 보정']
    symptom = str(row['3.실증상']) if pd.notna(row['3.실증상']) else ''
    
    if pd.isna(part_name):
        return ''
    
    # 1. 사전 정의된 부품: 유형1→유형2→유형3 순서 엄격 적용
    if part_name in predefined_parts:
        type_keywords = predefined_parts[part_name]
        for kw in type_keywords:  # 유형1부터 순서대로 확인
            if kw in symptom:
                return kw
        return type_keywords[0]  # 매칭 없으면 유형1 반환
    
    # 2. 나머지 부품: 일반 키워드 분석
    for kw in general_keywords:
        if kw in symptom:
            return kw
    return ''

# 키워드 재적용
print('모든 사전 정의 부품에 대해 유형1→2→3 우선순위 적용 중...')
v6_df['7.주요 키워드'] = v6_df.apply(get_keyword_for_row, axis=1)

# v7 저장
v6_df.to_csv('정리된_수리데이터_키워드분석_v7.csv', index=False, encoding='utf-8-sig')

# 모든 사전 정의 부품 검증
print('\n=== 모든 사전 정의 부품별 우선순위 검증 ===')
for part, types in predefined_parts.items():
    part_data = v6_df[v6_df['2.부품명 보정'] == part]
    if len(part_data) == 0:
        continue
    
    print(f'\n{part}')
    print(f'  유형 순서: {types}')
    
    # 겹침 검증
    overlap_count = 0
    correct_count = 0
    
    for idx, row in part_data.iterrows():
        symptom = str(row['3.실증상']) if pd.notna(row['3.실증상']) else ''
        keyword = row['7.주요 키워드']
        
        # 어떤 유형들이 있는지 확인
        found_types = [t for t in types if t in symptom]
        
        if len(found_types) > 1:  # 2개 이상 겹치는 경우
            overlap_count += 1
            if keyword == found_types[0]:  # 첫번째 유형(우선순위 높은)으로 됐는지
                correct_count += 1
    
    # 키워드 분포
    keyword_dist = part_data['7.주요 키워드'].value_counts()
    for kw, cnt in keyword_dist.items():
        print(f'  {kw}: {cnt}건')
    
    if overlap_count > 0:
        print(f'  [검증] 유형 겹침: {overlap_count}건, 올바른 우선순위 적용: {correct_count}건')

print(f'\n저장 파일: 정리된_수리데이터_키워드분석_v7.csv')
print(f'전체 데이터 건수: {len(v6_df)}')
