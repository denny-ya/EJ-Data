import pandas as pd

# v7 파일 로드
v7_df = pd.read_csv(r'정리된_수리데이터_키워드분석_v7.csv', encoding='utf-8-sig')

# 문제 케이스 확인: 실증상에 '마모'가 있는데 '파손'으로 표시된 경우
print('=== 14 WHEEL 관련 부품명 확인 ===')
wheel_parts = v7_df[v7_df['2.부품명 보정'].str.contains('WHEEL', na=False)]['2.부품명 보정'].unique()
for p in wheel_parts:
    print(f"'{p}'")

print('\n=== 문제 케이스 확인: 마모가 있는데 파손으로 표시된 경우 ===')
wheel_data = v7_df[v7_df['2.부품명 보정'].str.contains('WHEEL', na=False)]

problem_cases = []
for idx, row in wheel_data.iterrows():
    symptom = str(row['3.실증상']) if pd.notna(row['3.실증상']) else ''
    keyword = row['7.주요 키워드']
    part = row['2.부품명 보정']
    
    has_mamo = '마모' in symptom
    has_pason = '파손' in symptom
    
    # 마모가 있는데 파손으로 표시된 경우
    if has_mamo and keyword == '파손':
        problem_cases.append({
            '부품명': part,
            '실증상': symptom[:60],
            '결과': keyword
        })

print(f'문제 케이스 수: {len(problem_cases)}')
for i, case in enumerate(problem_cases[:10]):
    print(f"\n{i+1}. 부품명: '{case['부품명']}'")
    print(f"   실증상: {case['실증상']}...")
    print(f"   결과: {case['결과']} (마모가 있는데 파손으로 됨)")
