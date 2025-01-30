import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
import networkx as nx
from sklearn import metrics
import xgboost as xgb
import lightgbm as lgb
import mapclassify
from shapely import geometry
import openpyxl
import xlrd

# 페이지 기본 설정
st.set_page_config(
    page_title="데이터 분석 앱",
    page_icon="📊",
    layout="wide",
    # 최대 업로드 크기 설정
    max_upload_size=200
)

# 앱 제목
st.title("데이터 분석 앱")

# 사이드바 설정
st.sidebar.header("설정")

def process_excel(df):
    try:
        # 기본 정보 표시
        st.write("ℹ️ 기본 정보:")
        st.write(f"- 행 수: {df.shape[0]}")
        st.write(f"- 열 수: {df.shape[1]}")
        
        # 데이터 미리보기
        st.write("📊 데이터 미리보기:")
        st.dataframe(df.head())
        
        # 컬럼별 기본 통계
        st.write("📈 컬럼별 통계:")
        st.write(df.describe())
        
        # 결측치 확인
        missing_values = df.isnull().sum()
        if missing_values.any():
            st.write("⚠️ 결측치 현황:")
            st.write(missing_values[missing_values > 0])
            
    except Exception as e:
        st.error(f"데이터 처리 중 오류가 발생했습니다: {str(e)}")

def main():
    st.write("여러 파일을 동시에 업로드할 수 있습니다. (파일당 최대 200MB)")
    
    # 다중 파일 업로더
    uploaded_files = st.file_uploader(
        "데이터 파일을 업로드하세요",
        type=['xls', 'xlsx'],  # xls, xlsx만 허용
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                st.markdown("---")
                st.subheader(f"📄 파일명: {uploaded_file.name}")
                
                # 파일 확장자 확인
                file_type = uploaded_file.name.split('.')[-1].lower()
                
                if file_type == 'xls':
                    df = pd.read_excel(uploaded_file, engine='xlrd')
                elif file_type == 'xlsx':
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                
                process_excel(df)
                
            except Exception as e:
                st.error(f"'{uploaded_file.name}' 파일 처리 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()