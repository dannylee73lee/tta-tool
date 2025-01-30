import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import zipfile
import io
import tempfile

# 페이지 설정 및 파일 크기 제한 증가
st.set_page_config(
    page_title="SKT 데이터 분석",
    page_icon="📊",
    layout="wide"
)

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# 메모리 사용량 관리를 위한 설정
@st.cache_data(ttl=3600)  # 1시간 캐시
def load_zip_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name

# 파일 업로드
uploaded_file = st.file_uploader(
    "ZIP 파일을 업로드하세요",
    type=['zip'],
    help="SKT 데이터 ZIP 파일을 업로드해주세요."
)

if uploaded_file is not None:
    try:
        # 임시 파일로 저장
        temp_file_path = load_zip_file(uploaded_file)
        
        with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
            # ZIP 파일 내용 표시
            file_list = zip_ref.namelist()
            st.write("ZIP 파일 내 포함된 파일들:")
            for file in file_list:
                st.write(f"- {file}")
            
            # 데이터 처리
            dfs = []  # 여러 파일의 데이터를 저장할 리스트
            
            for file in file_list:
                if file.endswith('.csv'):
                    with zip_ref.open(file) as f:
                        # 파일 내용을 읽어서 데이터프레임으로 변환
                        content = io.TextIOWrapper(f, encoding='cp949')  # 한글 인코딩 처리
                        df = pd.read_csv(content)
                        dfs.append(df)
            
            if dfs:
                # 모든 데이터프레임 합치기
                combined_df = pd.concat(dfs, ignore_index=True)
                
                # 데이터 미리보기
                st.subheader("데이터 미리보기")
                st.dataframe(combined_df.head())
                
                # 기본 통계 정보
                st.subheader("데이터 기본 정보")
                st.write(f"총 행 수: {combined_df.shape[0]:,}")
                st.write(f"총 열 수: {combined_df.shape[1]}")
                
                # 메모리 사용량 표시
                memory_usage = combined_df.memory_usage(deep=True).sum() / 1024**2  # MB 단위
                st.write(f"메모리 사용량: {memory_usage:.2f} MB")
                
                # 컬럼별 정보
                st.subheader("컬럼 정보")
                col_info = pd.DataFrame({
                    '데이터 타입': combined_df.dtypes,
                    '널값 수': combined_df.isnull().sum(),
                    '고유값 수': combined_df.nunique()
                })
                st.dataframe(col_info)
                
                # 사이드바에 분석 옵션 추가
                with st.sidebar:
                    st.header("분석 옵션")
                    if st.checkbox("데이터 타입 변환"):
                        # 날짜 컬럼 자동 변환
                        date_columns = combined_df.select_dtypes(include=['object']).columns
                        for col in date_columns:
                            if 'date' in col.lower() or 'time' in col.lower():
                                try:
                                    combined_df[col] = pd.to_datetime(combined_df[col])
                                    st.success(f"{col} 컬럼을 날짜 형식으로 변환했습니다.")
                                except:
                                    continue
                
        # 임시 파일 삭제
        os.unlink(temp_file_path)
        
    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {str(e)}")
        st.error("자세한 에러 정보:")
        st.exception(e)