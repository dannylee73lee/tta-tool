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
    layout="wide"
)

# 앱 제목
st.title("데이터 분석 앱")

# 사이드바 설정
st.sidebar.header("설정")

def main():
    st.write("여러 파일을 동시에 업로드할 수 있습니다.")
    
    # 다중 파일 업로더
    uploaded_files = st.file_uploader(
        "데이터 파일을 업로드하세요",
        type=['xls', 'xlsx'],
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
                
                # 데이터 정보 표시
                st.write("📊 데이터 미리보기:")
                st.dataframe(df.head())
                
                # 기본 정보 표시
                st.write("ℹ️ 기본 정보:")
                st.write(f"- 행 수: {df.shape[0]}")
                st.write(f"- 열 수: {df.shape[1]}")
                st.write(f"- 컬럼명: {', '.join(df.columns)}")
                
            except Exception as e:
                st.error(f"'{uploaded_file.name}' 파일 처리 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()