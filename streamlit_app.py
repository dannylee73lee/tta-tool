import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn import *
import xgboost as xgb
import lightgbm as lgb
import geopandas as gpd
import folium
import networkx as nx
import mapclassify
from pyproj import *
from shapely.geometry import *

# 페이지 기본 설정
st.set_page_config(
    page_title="My Streamlit App",
    page_icon="🌟",
    layout="wide"
)

# 앱 제목
st.title("My Data Analysis App")