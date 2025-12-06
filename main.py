import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("범죄 지역 찾기")

st.write("이 사이트의 목적은 범죄가 가장 많이 발생한 곳과 가장 적게 발생한 곳을 찾는 것입니다.")

# 데이터 업로드 또는 샘플 데이터 사용
st.sidebar.header("데이터 설정")
uploaded_file = st.sidebar.file_uploader("범죄 데이터 CSV 파일 업로드", type=['csv'])

# 샘플 데이터 생성 함수
def create_sample_data():
    import random
    regions = ['서울 강남구', '서울 강북구', '서울 종로구', '서울 마포구', '부산 해운대구', 
               '부산 중구', '인천 남동구', '대구 수성구', '광주 광산구', '대전 유성구']
    crime_types = ['절도', '폭행', '사기', '살인', '강도', '성범죄', '마약', '교통범죄']
    
    data = []
    for region in regions:
        for crime_type in crime_types:
            count = random.randint(0, 150)
            if count > 0:
                data.append({
                    '지역': region,
                    '범죄유형': crime_type,
                    '발생건수': count
                })
    
    return pd.DataFrame(data)

# 데이터 로드
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        # 컬럼명 확인 및 표준화
        if '지역' not in df.columns or '범죄유형' not in df.columns or '발생건수' not in df.columns:
            st.error("CSV 파일은 '지역', '범죄유형', '발생건수' 컬럼을 포함해야 합니다.")
            st.info("샘플 데이터를 사용합니다.")
            df = create_sample_data()
    except Exception as e:
        st.error(f"파일 읽기 오류: {e}")
        st.info("샘플 데이터를 사용합니다.")
        df = create_sample_data()
else:
    st.info("📁 CSV 파일을 업로드하거나 샘플 데이터를 사용하세요.")
    df = create_sample_data()

# 데이터 확인
if st.sidebar.checkbox("데이터 미리보기"):
    st.subheader("원본 데이터")
    st.dataframe(df, use_container_width=True)

# 메인 분석 섹션
st.header("📊 지역별 범죄 발생 분석")

# 1. 가장 많이 발생한 지역-범죄 조합
st.subheader("🔥 가장 많이 발생한 지역-범죄 조합 Top 10")

# 지역별, 범죄 유형별 집계
if '지역' in df.columns and '범죄유형' in df.columns and '발생건수' in df.columns:
    # 가장 많이 발생한 조합 찾기
    top_combinations = df.nlargest(10, '발생건수')[['지역', '범죄유형', '발생건수']]
    
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
    region_total = df.groupby('지역')['발생건수'].sum().sort_values(ascending=False)
    
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
    crime_total = df.groupby('범죄유형')['발생건수'].sum().sort_values(ascending=False)
    
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
        selected_region = st.selectbox("지역 선택", ['전체'] + sorted(df['지역'].unique().tolist()))
    
    with col2:
        selected_crime = st.selectbox("범죄 유형 선택", ['전체'] + sorted(df['범죄유형'].unique().tolist()))
    
    filtered_df = df.copy()
    
    if selected_region != '전체':
        filtered_df = filtered_df[filtered_df['지역'] == selected_region]
    
    if selected_crime != '전체':
        filtered_df = filtered_df[filtered_df['범죄유형'] == selected_crime]
    
    if len(filtered_df) > 0:
        st.dataframe(filtered_df.sort_values('발생건수', ascending=False), use_container_width=True)
        
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

