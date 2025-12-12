import streamlit as st
import pandas as pd
import plotly.express as px
import time


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

def bubble_sort(data, key=None, reverse=False):
    """
    버블 정렬 알고리즘
    Args:
        data: 정렬할 리스트 또는 pandas DataFrame
        key: 정렬 기준이 되는 키 함수 (DataFrame의 경우 컬럼명)
        reverse: True면 내림차순, False면 오름차순
    Returns:
        정렬된 리스트 또는 DataFrame
    """
    if isinstance(data, pd.DataFrame):
        data_list = data.to_dict('records')
        n = len(data_list)

        for i in range(n - 1):
            for j in range(n - i - 1):
                if key:
                    current_val = data_list[j][key]
                    next_val = data_list[j + 1][key]
                else:
                    current_val = data_list[j]
                    next_val = data_list[j + 1]

                if reverse:
                    if current_val > next_val:
                        data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]
                else:
                    if current_val < next_val:
                        data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]
        return pd.DataFrame(data_list)
    else:
        data_list = list(data)
        n = len(data_list)

        for i in range(n - 1):
            for j in range(n - i - 1):
                if reverse:
                    if data_list[j] > data_list[j + 1]:
                        data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]
                else:
                    if data_list[j] < data_list[j + 1]:
                        data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]
        return data_list

def insertion_sort(data, key=None, reverse=False):
    """
    삽입 정렬 알고리즘
    Args:
        data: 정렬할 리스트 또는 pandas DataFrame
        key: 정렬 기준이 되는 키 함수 (DataFrame의 경우 컬럼명)
        reverse: True면 내림차순, False면 오름차순
    Returns:
        정렬된 리스트 또는 DataFrame
    """
    if isinstance(data, pd.DataFrame):
        data_list = data.to_dict('records')
        n = len(data_list)

        for i in range(1, n):
            for j in range(i, 0, -1):
                if key:
                    if reverse:
                        if data_list[j][key] > data_list[j - 1][key]:
                            data_list[j], data_list[j - 1] = data_list[j - 1], data_list[j]
                        else:
                            break
                    else:
                        if data_list[j][key] < data_list[j - 1][key]:
                            data_list[j], data_list[j - 1] = data_list[j - 1], data_list[j]
                        else:
                            break
                else:
                    if reverse:
                        if data_list[j] > data_list[j - 1]:
                            data_list[j], data_list[j - 1] = data_list[j - 1], data_list[j]
                        else:
                            break
                    else:
                        if data_list[j] < data_list[j - 1]:
                            data_list[j], data_list[j - 1] = data_list[j - 1], data_list[j]
                        else:
                            break
        return pd.DataFrame(data_list)
    else:
        data_list = list(data)
        n = len(data_list)

        for i in range(1, n):
            for j in range(i, 0, -1):
                if reverse:
                    if data_list[j] > data_list[j - 1]:
                        data_list[j], data_list[j - 1] = data_list[j - 1], data_list[j]
                    else:
                        break
                else:
                    if data_list[j] < data_list[j - 1]:
                        data_list[j], data_list[j - 1] = data_list[j - 1], data_list[j]
                    else:
                        break
        
        return data_list

def quick_sort(data, key=None, reverse=False):
    """
    퀵 정렬 알고리즘
    Args:
        data: 정렬할 리스트 또는 pandas DataFrame
        key: 정렬 기준이 되는 키 함수 (DataFrame의 경우 컬럼명)
        reverse: True면 내림차순, False면 오름차순
    Returns:
        정렬된 리스트 또는 DataFrame
    """
    if isinstance(data, pd.DataFrame):
        def _quick_sort(data_list: dict, key=None, reverse=False) -> dict:
            n = len(data_list)

            if n <= 1:
                return data_list
            
            start = 0
            end = n - 1
            pivot = start
            
            left = start + 1
            right = end
            
            while left <= right:
                while left <= right and data_list[left][key] <= data_list[pivot][key]:
                    left += 1
                while left <= right and data_list[right][key] >= data_list[pivot][key]:
                    right -= 1
                if left <= right:
                    data_list[left], data_list[right] = data_list[right], data_list[left]
            
            data_list[pivot], data_list[right] = data_list[right], data_list[pivot]
            return _quick_sort(data_list[:right], key, reverse) + [data_list[right]] + _quick_sort(data_list[(right + 1):], key, reverse)

        return pd.DataFrame(_quick_sort(data.to_dict('records'), key, reverse))
    else: # TODO FIX ^^
        data_list = list(data)
        n = len(data_list)

        if n <= 1:
            return data_list

        start = 0
        end = n - 1
        pivot = start
        
        left = start + 1
        right = end

        # escape when left > right
        while left <= right:
            if reverse: # reverse
                # find MIN(less than pivot)
                while left <= right and data_list[left] >= data_list[pivot]:
                    left += 1
                
                # find MAX(greater than pivot)
                while left <= right and data_list[right] <= data_list[pivot]:
                    right -= 1
            else:
                # find MAX(greater than pivot)
                while left <= right and data_list[left] <= data_list[pivot]:
                    left += 1
                
                # find MIN(less than pivot)
                while left <= right and data_list[right] >= data_list[pivot]:
                    right -= 1
            
            # swap MAX and MIN
            if left <= right:
                data_list[left], data_list[right] = data_list[right], data_list[left]
            
        # swap pivot and MIN if reverse swap pivot and MAX
        data_list[pivot], data_list[right] = data_list[right], data_list[pivot]
        return quick_sort(data_list[:right], key, reverse) + [data_list[right]] + quick_sort(data_list[(right + 1):], key, reverse)

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

###############################

 ######  #####  ######  #######
#       #     # #     # #
#       #     # #     # #######
#       #     # #     # #
 ######  #####  ######  #######

###############################
# 메인 분석 섹션
st.title("범죄 지역 찾기")
st.write("이 사이트의 목적은 지역별 범죄 발생 건수를 분석하고 시각화하는 것입니다.")
st.write("이 범죄 데이터는 2023년 기준 경찰청에서 집계한 범죄 발생 지역별 통계를 제공하는 공공데이터입니다. \
    \n외국인 범죄자에 대해서는 국적별(중국, 베트남, 러시아 등) 범죄 발생 수치도 포함됩니다.")

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
    
    st.dataframe(top_combinations, width='stretch')
    
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
    st.plotly_chart(fig, width='stretch')
    
###############################################################################################

    # 2. 지역별 총 범죄 발생 건수
    st.subheader("📍 지역별 총 범죄 발생 건수")

    # (ㄱ) -> (ㄴ)는 내가 함. 그 외에도 Quick sort 내가 함. 그 외에는 거의 AI. (ㄱ)
    delta_time_list = [[[[0, list, False] for _ in range(4)], 'sort_name'] for _ in range(4)]
    # 위에 저 변수 도대체 무엇이냐? 아래에 설명하겠다. (이거 그냥 온공 제출용이고 누군가 이 프로젝트를 쓸지 모르겠지만 있어 보이니까)
    # level: 0 | var = [A, B, C, D] 이때 A, B, C, D는 각각 네 개(Q, S, I, B)의 정렬한 결과를 모으기 위함.
    # Level: 1 | A = [sort_result, sort_name] sort_result는 정렬 방법에서 정렬한 결과, sort_name은 정렬 방법 이름임.
    # Level: 2 | sort_result = [a, b, c, d] a, b, c, d는 한 정렬 방법으로 정렬한 정렬 결과임.
    # Level: 3 | a = [d_t, data_type, reverse] d_t는 정렬 시간, data_type은 정렬할 데이터의 종류가 무엇인지 reverse는 내림차순 또는오름차순으로 정렬하였는지 나타냄.

    delta_time_list[0][1] = 'quick'
    t0 = time.time()
    quick_sort(df['지역'].unique().tolist(), reverse = False)
    t1 = time.time()
    quick_sort(df['지역'].unique().tolist(), reverse = True)
    t2 = time.time()
    quick_sort(df.groupby('지역')['발생건수'].sum().reset_index(), key='발생건수', reverse = False)
    t3 = time.time()
    quick_sort(df.groupby('지역')['발생건수'].sum().reset_index(), key='발생건수', reverse = True)
    t4 = time.time()
    st.write(f"Quick sort\
        \nlist를 정렬할 때) 오름차순: {t1 - t0}, 내림차순: {t2 - t1}\
        \n작은 데이터를 정렬할 때) 오름차순: {t3 - t2}, 내림차순: {t4 - t3}")
    delta_time_list[0][0][0] = [t1 - t0, list, False]
    delta_time_list[0][0][1] = [t2 - t1, list, True]
    delta_time_list[0][0][2] = [t3 - t2, pd.DataFrame, False]
    delta_time_list[0][0][3] = [t4 - t3, pd.DataFrame, True]

    delta_time_list[1][1] = 'selection'
    t0 = time.time()
    selection_sort(df['지역'].unique().tolist(), reverse = False)
    t1 = time.time()
    selection_sort(df['지역'].unique().tolist(), reverse = True)
    t2 = time.time()
    selection_sort(df.groupby('지역')['발생건수'].sum().reset_index(), key='발생건수', reverse = False)
    t3 = time.time()
    selection_sort(df.groupby('지역')['발생건수'].sum().reset_index(), key='발생건수', reverse = True)
    t4 = time.time()
    st.write(f"Selection sort\
        \nlist를 정렬할 때) 오름차순: {t1 - t0}, 내림차순: {t2 - t1}\
        \n작은 데이터를 정렬할 때) 오름차순: {t3 - t2}, 내림차순: {t4 - t3}")
    delta_time_list[1][0][0] = [t1 - t0, list, False]
    delta_time_list[1][0][1] = [t2 - t1, list, True]
    delta_time_list[1][0][2] = [t3 - t2, pd.DataFrame, False]
    delta_time_list[1][0][3] = [t4 - t3, pd.DataFrame, True]
    
    delta_time_list[2][1] = 'insertion'
    t0 = time.time()
    insertion_sort(df['지역'].unique().tolist(), reverse = False)
    t1 = time.time()
    insertion_sort(df['지역'].unique().tolist(), reverse = True)
    t2 = time.time()
    insertion_sort(df.groupby('지역')['발생건수'].sum().reset_index(), key='발생건수', reverse = False)
    t3 = time.time()
    insertion_sort(df.groupby('지역')['발생건수'].sum().reset_index(), key='발생건수', reverse = True)
    t4 = time.time()
    st.write(f"Insertion sort\
        \nlist를 정렬할 때) 오름차순: {t1 - t0}, 내림차순: {t2 - t1}\
        \n작은 데이터를 정렬할 때) 오름차순: {t3 - t2}, 내림차순: {t4 - t3}")
    delta_time_list[2][0][0] = [t1 - t0, list, False]
    delta_time_list[2][0][1] = [t2 - t1, list, True]
    delta_time_list[2][0][2] = [t3 - t2, pd.DataFrame, False]
    delta_time_list[2][0][3] = [t4 - t3, pd.DataFrame, True]

    delta_time_list[3][1] = 'bubble'
    t0 = time.time()
    bubble_sort(df['지역'].unique().tolist(), reverse = False)
    t1 = time.time()
    bubble_sort(df['지역'].unique().tolist(), reverse = True)
    t2 = time.time()
    bubble_sort(df.groupby('지역')['발생건수'].sum().reset_index(), key='발생건수', reverse = False)
    t3 = time.time()
    bubble_sort(df.groupby('지역')['발생건수'].sum().reset_index(), key='발생건수', reverse = True)
    t4 = time.time()
    st.write(f"Bubble sort\
        \nlist를 정렬할 때) 오름차순: {t1 - t0}, 내림차순: {t2 - t1}\
        \n작은 데이터를 정렬할 때) 오름차순: {t3 - t2}, 내림차순: {t4 - t3}")
    delta_time_list[3][0][0] = [t1 - t0, list, False]
    delta_time_list[3][0][1] = [t2 - t1, list, True]
    delta_time_list[3][0][2] = [t3 - t2, pd.DataFrame, False]
    delta_time_list[3][0][3] = [t4 - t3, pd.DataFrame, True]

    sort_data = dict()

    for sort_type in delta_time_list: # sort_type = Level 1
        out_str = ''
        str_name = ''

        if sort_type[1] == 'quick':
            str_name = '퀵 정렬'
        elif sort_type[1] == 'selection':
            str_name = '선택 정렬'
        elif sort_type[1] == 'insertion':
            str_name = '삽입 정렬'
        elif sort_type[1] == 'bubble':
            str_name = '버블 정렬'
        else:
            str_name = '[정렬 이름 에러]'
        
        for which_what_sort in sort_type[0]: # which ~ = Level 3
            out_str += str_name
            if which_what_sort[1] is list:
                out_str += '로 ' + '긴 리스트를'
            elif which_what_sort[1] is pd.DataFrame:
                out_str += '로 ' + '짧은 데이터를'
            else:
                out_str += '[정렬 타입 에러]'
            
            if not which_what_sort[2]:
                out_str += ' 오름차순으로 정렬 할 때: '
            else:
                out_str += ' 내림차순으로 정렬 할 때: '

            out_str += str(which_what_sort[0])
            sort_data[which_what_sort[0]] = out_str
            out_str = ''
            
    # st.write(sort_data)
    for key in sorted(sort_data.keys()):
        st.write(sort_data[key])
    # (ㄴ) 힘들었다.

    region_grouped = df.groupby('지역')['발생건수'].sum().reset_index()
    region_sorted = selection_sort(region_grouped, key='발생건수', reverse=True)
    region_total = region_sorted.set_index('지역')['발생건수']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(region_total.reset_index(), width='stretch')
    
    with col2:
        fig2 = px.bar(
            x=region_total.index,
            y=region_total.values,
            title='지역별 총 범죄 발생 건수',
            labels={'x': '지역', 'y': '총 발생 건수'}
        )
        fig2.update_xaxes(tickangle=-45)
        st.plotly_chart(fig2, width='stretch')
    
#############################################################################################

    # 3. 범죄 유형별 총 발생 건수
    st.subheader("⚖️ 범죄 유형별 총 발생 건수")
    crime_grouped = df.groupby('범죄유형')['발생건수'].sum().reset_index()
    crime_sorted = selection_sort(crime_grouped, key='발생건수', reverse=True)
    crime_total = crime_sorted.set_index('범죄유형')['발생건수']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.dataframe(crime_total.reset_index(), width='stretch')
    
    with col2:
        fig3 = px.pie(
            values=crime_total.values,
            names=crime_total.index,
            title='범죄 유형별 비율'
        )
        st.plotly_chart(fig3, width='stretch')
    
########################################################################################

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
    
    st.dataframe(pivot_table, width='stretch')
    
#########################################################################################

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
        st.dataframe(sorted_filtered, width='stretch')
        
        if len(filtered_df) > 1:
            fig5 = px.bar(
                filtered_df,
                x='지역' if selected_region == '전체' else '범죄유형',
                y='발생건수',
                color='범죄유형' if selected_region != '전체' else '지역',
                title=f'검색 결과: {selected_region} - {selected_crime}'
            )
            st.plotly_chart(fig5, width='stretch')
    else:
        st.info("검색 결과가 없습니다.")
    
else:
    st.error("데이터에 필요한 컬럼('지역', '범죄유형', '발생건수')이 없습니다.")
    st.write("데이터 구조:")
    st.dataframe(df.head())

