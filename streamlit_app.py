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
import xlrd  # .xls 파일 처리를 위해 추가

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

# 메인 페이지 컨텐츠
def main():
    st.write("여기에 메인 컨텐츠가 들어갑니다.")
    
    # 파일 업로더 수정
    uploaded_file = st.file_uploader(
        "데이터 파일을 업로드하세요",
        type=['csv', 'xls', 'xlsx']  # 허용할 파일 확장자 목록
    )
    
    if uploaded_file is not None:
        try:
            # 파일 확장자 확인
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            if file_type == 'csv':
                df = pd.read_csv(uploaded_file)
            elif file_type == 'xls':
                df = pd.read_excel(uploaded_file, engine='xlrd')  # .xls 파일용 엔진
            elif file_type == 'xlsx':
                df = pd.read_excel(uploaded_file, engine='openpyxl')  # .xlsx 파일용 엔진
            
            st.write("데이터 미리보기:")
            st.dataframe(df.head())
            
        except Exception as e:
            st.error(f"파일 처리 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()