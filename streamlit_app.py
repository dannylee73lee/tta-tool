import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import zipfile
import glob
import openpyxl
from matplotlib import font_manager

# 페이지 설정
st.set_page_config(
    page_title="Data Analysis App",
    page_icon="📊",
    layout="wide"
)

# 한글 폰트 설정
def setup_korean_font():
    # 윈도우의 경우
    if os.path.exists('C:/Windows/Fonts/NanumBarunGothic.ttf'):
        font_path = 'C:/Windows/Fonts/NanumBarunGothic.ttf'
    # Linux의 경우
    elif os.path.exists('/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'):
        font_path = '/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf'
    else:
        st.warning("나눔바른고딕 폰트가 설치되어 있지 않습니다. 시스템 기본 폰트를 사용합니다.")
        return
    
    font_manager.fontManager.addfont(font_path)
    plt.rcParams['font.family'] = 'NanumBarunGothic'
    plt.rcParams['axes.unicode_minus'] = False

# 한글 폰트 설정 함수 호출
setup_korean_font()

# 앱 제목
st.title("데이터 분석 애플리케이션")

# 파일 업로더 추가
uploaded_file = st.file_uploader("분석할 파일을 업로드하세요", 
                               type=['csv', 'xlsx', 'zip'],
                               help="CSV, Excel, 또는 ZIP 파일을 업로드할 수 있습니다.")

if uploaded_file is not None:
    # 파일 확장자 확인
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension == 'xlsx':
            df = pd.read_excel(uploaded_file)
        elif file_extension == 'zip':
            # ZIP 파일 처리
            with zipfile.ZipFile(uploaded_file) as z:
                # ZIP 파일 내용 표시
                st.write("ZIP 파일 내용:")
                for filename in z.namelist():
                    st.write(filename)
                
                # 첫 번째 파일 처리 (예시)
                first_file = z.namelist()[0]
                if first_file.endswith('.csv'):
                    df = pd.read_csv(z.open(first_file))
                elif first_file.endswith('.xlsx'):
                    df = pd.read_excel(z.open(first_file))
                else:
                    st.error("지원되지 않는 파일 형식입니다.")
                    st.stop()
        
        # 데이터프레임 미리보기
        st.subheader("데이터 미리보기")
        st.dataframe(df.head())
        
        # 기본 정보 표시
        st.subheader("데이터 기본 정보")
        st.write(f"행 수: {df.shape[0]}")
        st.write(f"열 수: {df.shape[1]}")
        st.write("컬럼 목록:", df.columns.tolist())
        
        # 추가적인 분석 코드는 여기에 작성
        
    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {str(e)}")

# 사이드바에 추가 옵션 설정
with st.sidebar:
    st.header("분석 옵션")
    # 여기에 필요한 분석 옵션들을 추가할 수 있습니다