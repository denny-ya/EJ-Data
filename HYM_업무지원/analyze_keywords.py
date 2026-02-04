import pandas as pd

# v6 파일 로드
v6_df = pd.read_csv(r'정리된_수리데이터_키워드분석_v6.csv', encoding='utf-8-sig')

# COVER MAT-FOOTREST에서 실증상에 '마모'와 '파손'이 둘 다 있는 경우 확인
cover_mat = v6_df[v6_df['2.부품명 보정'] == 'COVER MAT-FOOTREST']

overlap_cases = []
for idx, row in cover_mat.iterrows():
    symptom = str(row['3.실증상']) if pd.notna(row['3.실증상']) else ''
    keyword = row['7.주요 키워드']
    
    has_mamo = '마모' in symptom
    has_byunhyung = '변형' in symptom  
    has_pason = '파손' in symptom
    
    # 마모+파손 또는 마모+변형 겹치는 경우
    if has_mamo and (has_pason or has_byunhyung):
        overlap_cases.append({
            '실증상': symptom[:50],
            '마모': has_mamo,
            '변형': has_byunhyung,
            '파손': has_pason,
            '결과키워드': keyword
        })

print(f'=== COVER MAT-FOOTREST: 유형 겹침 검증 ===')
print(f'전체 건수: {len(cover_mat)}')
print(f'마모+파손 or 마모+변형 겹치는 건수: {len(overlap_cases)}')
print()

if overlap_cases:
    print('겹침 사례 (최대 10건):')
    for i, case in enumerate(overlap_cases[:10]):
        print(f"{i+1}. 실증상: {case['실증상']}...")
        print(f"   마모:{case['마모']}, 변형:{case['변형']}, 파손:{case['파손']} → 결과: {case['결과키워드']}")
        
    # 겹칠 때 결과가 '마모'인지 확인
    correct = sum(1 for c in overlap_cases if c['결과키워드'] == '마모')
    print(f'\n겹침 사례 중 마모로 정확히 표시된 건수: {correct}/{len(overlap_cases)}')
else:
    print('마모와 파손/변형이 동시에 나타나는 경우가 없습니다.')
    print('=> 현재 결과는 우선순위가 정상 적용된 것입니다.')
