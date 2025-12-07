import streamlit as st
import pandas as pd
import plotly.express as px

st.title("범죄 지역 찾기")
st.write("이 사이트의 목적은 지역별 범죄 발생 건수를 분석하고 시각화하는 것입니다.")
st.write("이 범죄 데이터는 2023년 기준 경찰청에서 집계한 범죄 발생 지역별 통계를 제공하는 공공데이터입니다. 외국인 범죄자에 대해서는 국적별(중국, 베트남, 러시아 등) 범죄 발생 수치도 포함됩니다.")

# 선택 정렬 알고리즘 구현
def selection_sort(data, key=None, reverse=False):
    """
    선택 정렬 알고리즘
    Args:
        data: 정렬할 리스트 또는 pandas DataFrame
        key: 정렬 기준이 되는 키 함수 (DataFrame의 경우 컬럼명)
        reverse: True면 내림차순, False면 오름차순
    Returns:
        정렬된 리스트 또는 DataFrame
    """
    if isinstance(data, pd.DataFrame):
        # DataFrame인 경우
        data_list = data.to_dict('records')
        n = len(data_list)
        
        for i in range(n - 1):
            # 현재 위치부터 끝까지 최소값(또는 최대값) 찾기
            extreme_idx = i
            for j in range(i + 1, n):
                if key:
                    current_val = data_list[j][key]
                    extreme_val = data_list[extreme_idx][key]
                else:
                    current_val = data_list[j]
                    extreme_val = data_list[extreme_idx]
                
                if reverse:
                    # 내림차순: 더 큰 값을 찾음
                    if current_val > extreme_val:
                        extreme_idx = j
                else:
                    # 오름차순: 더 작은 값을 찾음
                    if current_val < extreme_val:
                        extreme_idx = j
            
            # 최소값(또는 최대값)을 현재 위치로 이동
            data_list[i], data_list[extreme_idx] = data_list[extreme_idx], data_list[i]
        
        return pd.DataFrame(data_list)
    else:
        # 리스트인 경우
        data_list = list(data)
        n = len(data_list)
        
        for i in range(n - 1):
            extreme_idx = i
            for j in range(i + 1, n):
                if reverse:
                    if data_list[j] > data_list[extreme_idx]:
                        extreme_idx = j
                else:
                    if data_list[j] < data_list[extreme_idx]:
                        extreme_idx = j
            
            data_list[i], data_list[extreme_idx] = data_list[extreme_idx], data_list[i]
        
        return data_list

# Top K 찾기 (선택 정렬 기반)
def get_top_k(data, k, key=None, reverse=True):
    """
    선택 정렬을 사용하여 Top K 항목 찾기
    Args:
        data: pandas DataFrame
        k: 상위 k개
        key: 정렬 기준 컬럼명
        reverse: True면 내림차순
    Returns:
        상위 k개 DataFrame
    """
    if isinstance(data, pd.DataFrame):
        sorted_data = selection_sort(data, key=key, reverse=reverse)
        return sorted_data.head(k)
    return data

# 데이터 파일 경로
data_path = "data/경찰청_범죄 발생 지역별 통계_20231231.csv"

# 데이터 로드 함수
@st.cache_data
def load_data():
    """CSV 파일을 읽고 변환하는 함수"""
    encodings = ['cp949', 'euc-kr', 'utf-8', 'utf-8-sig']
    
    for encoding in encodings:
        try:
            # CSV 파일 읽기
            df_raw = pd.read_csv(data_path, encoding=encoding)
            
            # 첫 번째 컬럼: 범죄대분류, 두 번째 컬럼: 범죄중분류
            # 나머지 컬럼들: 각 지역별 발생 건수
            crime_category_col = df_raw.columns[0]  # 범죄대분류
            crime_type_col = df_raw.columns[1]      # 범죄중분류
            
            # 데이터 변환: 피벗 테이블을 long format으로 변환
            data_list = []
            
            for idx, row in df_raw.iterrows():
                crime_category = row[crime_category_col]
                crime_type = row[crime_type_col]
                
                # 범죄 유형: 범죄대분류 + 범죄중분류 (또는 범죄중분류만)
                crime_name = f"{crime_category} - {crime_type}" if pd.notna(crime_category) else str(crime_type)
                
                # 나머지 컬럼들을 순회하며 지역별 발생 건수 수집
                for col in df_raw.columns[2:]:
                    region_name = str(col).strip()
                    
                    if pd.notna(row[col]) and str(row[col]).strip() != '':
                        try:
                            count = int(row[col])
                            if count > 0:  # 0보다 큰 값만 저장
                                data_list.append({
                                    '지역': region_name,
                                    '범죄유형': crime_name,
                                    '발생건수': count
                                })
                        except (ValueError, TypeError):
                            continue
            
            df = pd.DataFrame(data_list)
            
            if len(df) > 0:
                return df
        except Exception as e:
            continue
    
    return pd.DataFrame()

# 데이터 로드
df = load_data()

if df.empty:
    st.error("데이터를 불러올 수 없습니다.")
    st.stop()

# 메인 분석 섹션
st.header("📊 지역별 범죄 발생 분석")

# 1. 가장 많이 발생한 지역-범죄 조합
st.subheader("🔥 가장 많이 발생한 지역-범죄 조합 Top 10")

# 지역별, 범죄 유형별 집계
if '지역' in df.columns and '범죄유형' in df.columns and '발생건수' in df.columns:
    # 가장 많이 발생한 조합 찾기 (선택 정렬 알고리즘 사용)
    top_combinations = get_top_k(df[['지역', '범죄유형', '발생건수']], k=10, key='발생건수', reverse=True)
    
    # 순위 추가
    top_combinations = top_combinations.reset_index(drop=True)
    top_combinations.index = top_combinations.index + 1
    
    st.dataframe(top_combinations, use_container_width=True)
    
    # 시각화
    fig = px.bar(
        top_combinations,
        x='발생건수',
        y='지역',
        color='범죄유형',
        orientation='h',
        title='지역별 범죄 발생 건수 (Top 10)',
        labels={'발생건수': '발생 건수', '지역': '지역', '범죄유형': '범죄 유형'},
        height=500
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)
    
    # 2. 지역별 총 범죄 발생 건수
    st.subheader("📍 지역별 총 범죄 발생 건수")
    region_grouped = df.groupby('지역')['발생건수'].sum().reset_index()
    region_sorted = selection_sort(region_grouped, key='발생건수', reverse=True)
    region_total = region_sorted.set_index('지역')['발생건수']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(region_total.reset_index(), use_container_width=True)
    
    with col2:
        fig2 = px.bar(
            x=region_total.index,
            y=region_total.values,
            title='지역별 총 범죄 발생 건수',
            labels={'x': '지역', 'y': '총 발생 건수'}
        )
        fig2.update_xaxes(tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
    
    # 3. 범죄 유형별 총 발생 건수
    st.subheader("⚖️ 범죄 유형별 총 발생 건수")
    crime_grouped = df.groupby('범죄유형')['발생건수'].sum().reset_index()
    crime_sorted = selection_sort(crime_grouped, key='발생건수', reverse=True)
    crime_total = crime_sorted.set_index('범죄유형')['발생건수']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(crime_total.reset_index(), use_container_width=True)
    
    with col2:
        fig3 = px.pie(
            values=crime_total.values,
            names=crime_total.index,
            title='범죄 유형별 비율'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # 4. 상세 분석 테이블
    st.subheader("📋 지역-범죄 유형별 상세 분석")
    
    # 피벗 테이블 생성
    pivot_table = df.pivot_table(
        values='발생건수',
        index='지역',
        columns='범죄유형',
        aggfunc='sum',
        fill_value=0
    )
    
    st.dataframe(pivot_table, use_container_width=True)
    
    # 히트맵 시각화
    fig4 = px.imshow(
        pivot_table.values,
        labels=dict(x="범죄 유형", y="지역", color="발생 건수"),
        x=pivot_table.columns,
        y=pivot_table.index,
        aspect="auto",
        color_continuous_scale="Reds",
        title="지역별 범죄 유형 히트맵"
    )
    st.plotly_chart(fig4, use_container_width=True)
    
    # 5. 검색 기능
    st.subheader("🔍 특정 지역 또는 범죄 유형 검색")
    
    col1, col2 = st.columns(2)
    
    with col1:
        regions = df['지역'].unique().tolist()
        sorted_regions = selection_sort(regions, reverse=False)
        selected_region = st.selectbox("지역 선택", ['전체'] + sorted_regions)
    
    with col2:
        crimes = df['범죄유형'].unique().tolist()
        sorted_crimes = selection_sort(crimes, reverse=False)
        selected_crime = st.selectbox("범죄 유형 선택", ['전체'] + sorted_crimes)
    
    filtered_df = df.copy()
    
    if selected_region != '전체':
        filtered_df = filtered_df[filtered_df['지역'] == selected_region]
    
    if selected_crime != '전체':
        filtered_df = filtered_df[filtered_df['범죄유형'] == selected_crime]
    
    if len(filtered_df) > 0:
        sorted_filtered = selection_sort(filtered_df, key='발생건수', reverse=True)
        st.dataframe(sorted_filtered, use_container_width=True)
        
        if len(filtered_df) > 1:
            fig5 = px.bar(
                filtered_df,
                x='지역' if selected_region == '전체' else '범죄유형',
                y='발생건수',
                color='범죄유형' if selected_region != '전체' else '지역',
                title=f'검색 결과: {selected_region} - {selected_crime}'
            )
            st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("검색 결과가 없습니다.")
    
else:
    st.error("데이터에 필요한 컬럼('지역', '범죄유형', '발생건수')이 없습니다.")
    st.write("데이터 구조:")
    st.dataframe(df.head())

