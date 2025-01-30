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
    st.write("파일을 분할하여 업로드해주세요 (파일당 최대 200MB)")
    
    # 다중 파일 업로더
    uploaded_files = st.file_uploader(
        "데이터 파일을 업로드하세요",
        type=['xls'],  # xls만 허용
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files:
        all_dfs = []  # 모든 데이터프레임을 저장할 리스트
        
        for uploaded_file in uploaded_files:
            try:
                # 파일 읽기
                df = pd.read_excel(uploaded_file, engine='xlrd')
                all_dfs.append(df)
                
                # 개별 파일 정보 표시
                st.markdown(f"### 📄 {uploaded_file.name} 처리 완료")
                st.write(f"- 행 수: {df.shape[0]}")
                st.write(f"- 열 수: {df.shape[1]}")
                
            except Exception as e:
                st.error(f"'{uploaded_file.name}' 파일 처리 중 오류가 발생했습니다: {str(e)}")
        
        if all_dfs:
            try:
                # 모든 데이터프레임 합치기
                combined_df = pd.concat(all_dfs, ignore_index=True)
                
                st.markdown("---")
                st.markdown("### 📊 통합 데이터 미리보기")
                st.dataframe(combined_df.head())
                
                # 기본 정보 표시
                st.markdown("### ℹ️ 통합 데이터 정보")
                st.write(f"- 전체 행 수: {combined_df.shape[0]}")
                st.write(f"- 전체 열 수: {combined_df.shape[1]}")
                st.write(f"- 컬럼명: {', '.join(combined_df.columns)}")
                
                # 컬럼 선택 및 기초 통계
                if st.checkbox("컬럼별 기초 통계 보기"):
                    selected_columns = st.multiselect(
                        "분석할 컬럼을 선택하세요",
                        combined_df.columns
                    )
                    if selected_columns:
                        st.dataframe(combined_df[selected_columns].describe())
                
            except Exception as e:
                st.error(f"데이터 통합 중 오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()