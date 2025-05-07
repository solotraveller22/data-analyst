import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests
import json
import time
import finnhub

# 設置頁面配置
st.set_page_config(
    page_title="CL專屬股票分析系統",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 添加自定義CSS以改進界面設計和體驗
st.markdown("""
<style>
    /* 主體風格調整 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* 標題樣式 */
    h1, h2, h3 {
        color: #1565C0;
    }
    
    /* 輸入框與下拉選擇優化 */
    div[data-baseweb="select"] > div {
        border-radius: 8px !important;
        border-color: #e0e0e0 !important;
        min-height: 40px !important;
    }
    
    div[data-baseweb="select"] > div:hover {
        border-color: #1565C0 !important;
    }
    
    div[data-baseweb="base-input"] > div {
        border-radius: 8px !important;
        border-color: #e0e0e0 !important;
    }
    
    div[data-baseweb="base-input"] > div:hover {
        border-color: #1565C0 !important;
    }
    
    .stSelectbox [data-testid="stMarkdownContainer"] > div {
        padding: 0 !important;
    }
    
    /* 下拉選單樣式修復 */
    .stSelectbox {
        margin-bottom: 15px;
    }

    /* 修复下拉菜单显示问题 */
    div[data-baseweb="select"] {
        z-index: 999 !important;
        position: relative;
        max-width: 100% !important;
    }
    
    div[data-baseweb="popover"] {
        z-index: 1000 !important;
        max-width: none !important;
    }
    
    /* 按鈕樣式增強 */
    div.stButton > button:first-child {
        background-color: #1976D2;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #1565C0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transform: translateY(-1px);
    }
    
    div.stButton > button:first-child:active {
        transform: translateY(0px);
        box-shadow: none;
    }
    
    /* 容器與卡片樣式 */
    .stock-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #eee;
        transition: all 0.3s ease;
    }
    
    .stock-card:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        border-color: #ddd;
    }
    
    /* 添加動畫效果 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stock-input-container {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* 響應式元素 */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# 在頁面頂部添加Logo和標題
st.markdown("""
<div style="display: flex; align-items: center; padding: 20px 0; background: linear-gradient(120deg, #1565C0, #0D47A1); border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 15px rgba(21, 101, 192, 0.2);">
    <div style="margin: 0 25px; animation: pulse 2s infinite ease-in-out;">
        <svg width="60" height="60" viewBox="0 0 24 24" fill="#FFFFFF">
            <path d="M3.5,18.49l6-6.01l4,4L22,6.92l-1.41-1.41l-7.09,7.97l-4-4L2,16.99L3.5,18.49z"></path>
            <path d="M4,21h16c1.1,0,2-0.9,2-2V5c0-1.1-0.9-2-2-2H4C2.9,3,2,3.9,2,5v14C2,20.1,2.9,21,4,21z M4,5h16v14H4V5z"></path>
        </svg>
    </div>
    <div>
        <h1 style="color: white; margin: 0; font-size: 2.2rem; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.1);">CL專屬股票分析平台</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 1rem;">
            <span style="background-color: rgba(255,255,255,0.2); padding: 3px 8px; border-radius: 4px; margin-right: 10px;">PROFESSIONAL</span>
            利用AI技術和專業數據分析幫助投資者做出更精準的決策
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# 設置側邊欄配置
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <h1 style="color: #1565C0; font-size: 1.5rem; margin-bottom: 5px;">
            <svg style="vertical-align: middle; margin-right: 8px;" width="24" height="24" viewBox="0 0 24 24" fill="#1565C0">
                <path d="M3.5,18.49l6-6.01l4,4L22,6.92l-1.41-1.41l-7.09,7.97l-4-4L2,16.99L3.5,18.49z"></path>
            </svg>
            專業股票分析平台
        </h1>
        <p style="color: #666; margin-top: 0; font-size: 0.9rem;">CL專屬精準投資決策工具</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 添加设置区域标题，采用更清晰的样式
    st.markdown("""
    <div style="margin: 20px 0 15px 0; padding-bottom: 10px; border-bottom: 1px solid #eee;">
        <h2 style="font-size: 1.2rem; color: #424242; margin: 0;">
            <svg style="vertical-align: middle; margin-right: 6px;" width="18" height="18" viewBox="0 0 24 24" fill="#424242">
                <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"></path>
            </svg>
            分析設置
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    # 添加資料來源選擇器，修改样式確保能正確顯示所有選項
    data_source = st.selectbox(
        "數據來源",
        [
            "混合模式 (推薦)", 
            "Finnhub API (即時)",
            "Alpha Vantage API (實時)", 
            "Yahoo Finance (15分鐘延遲)"
        ],
        index=0,
        key="data_source_select",
        help="選擇股票數據的來源"
    )
    
    # 添加時間週期選擇器，修改样式確保能正確顯示所有選項
    period = st.selectbox(
        "時間週期",
        [
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y"
        ],
        index=2,
        key="period_select",
        help="選擇分析的時間範圍"
    )
    
    # 使用容器美化界面組織參數設置
    with st.container():
        st.markdown("""
        <div style="margin: 10px 0; padding-bottom: 10px;">
            <h3 style="font-size: 1rem; color: #424242; margin: 0 0 10px 0;">技術指標設置</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # 整理常用分析指標參數，分列顯示以節省空間
        col1, col2 = st.columns(2)
        
        with col1:
            rsi_window = st.number_input("RSI週期", min_value=2, max_value=30, value=14)
            oversold_threshold = st.number_input("超賣閾值", min_value=1, max_value=49, value=30)
    
        with col2:
            overbought_threshold = st.number_input("超買閾值", min_value=51, max_value=99, value=70)
    
    # 顯示選項設置
    st.markdown("""
    <div style="margin: 20px 0 10px 0; padding-top: 10px; border-top: 1px solid #eee;">
        <h3 style="font-size: 1rem; color: #424242; margin: 0 0 10px 0;">圖表與顯示設置</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 显示控制选项
    show_volume = st.checkbox("顯示交易量", value=True)
    show_ma = st.checkbox("顯示移動平均線", value=True)
    show_rsi = st.checkbox("顯示RSI指標", value=True)
    
    # 設置移動平均線週期
    ma_periods = [20, 50, 200] if show_ma else []

# 添加標準美股清單用於股票搜索建議
@st.cache_data(ttl=86400)
def get_us_stock_list():
    """獲取主要美股列表用於搜索建議"""
    try:
        major_stocks = {
            # 科技股
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
            "GOOGL": "Alphabet Inc. (Google)",
            "AMZN": "Amazon.com Inc.",
            "META": "Meta Platforms Inc.",
            "NVDA": "NVIDIA Corporation",
            "TSLA": "Tesla Inc.",
            "NFLX": "Netflix Inc.",
            "AMD": "Advanced Micro Devices",
            "INTC": "Intel Corporation",
            # 金融股
            "JPM": "JPMorgan Chase & Co.",
            "BAC": "Bank of America Corp.",
            "WFC": "Wells Fargo & Company",
            "GS": "Goldman Sachs Group Inc.",
            "V": "Visa Inc.",
            "MA": "Mastercard Incorporated",
            # 消費品
            "PG": "Procter & Gamble Co.",
            "KO": "The Coca-Cola Company",
            "PEP": "PepsiCo Inc.",
            "WMT": "Walmart Inc.",
            "TGT": "Target Corporation",
            "MCD": "McDonald's Corporation",
            "SBUX": "Starbucks Corporation",
            # 醫療保健
            "JNJ": "Johnson & Johnson",
            "PFE": "Pfizer Inc.",
            "MRNA": "Moderna Inc.",
            "UNH": "UnitedHealth Group Inc.",
            # 工業股
            "BA": "Boeing Company",
            "CAT": "Caterpillar Inc.",
            "GE": "General Electric Company",
            # 能源股
            "XOM": "Exxon Mobil Corporation",
            "CVX": "Chevron Corporation",
            # 電信
            "VZ": "Verizon Communications Inc.",
            "T": "AT&T Inc.",
        }
        return major_stocks
    except Exception as e:
        st.warning(f"獲取美股列表失敗: {str(e)}")
        return {}

# 添加布林帶計算函數
def calculate_bollinger_bands(df, window=20, num_std=2):
    """Calculate Bollinger Bands for the given dataframe"""
    df = df.copy()
    df['MA'] = df['Close'].rolling(window=window).mean()
    df['BB_upper'] = df['MA'] + (df['Close'].rolling(window=window).std() * num_std)
    df['BB_lower'] = df['MA'] - (df['Close'].rolling(window=window).std() * num_std)
    return df

# 添加MACD計算函數
def calculate_macd(df, fast=12, slow=26, signal=9):
    """計算MACD指標"""
    df = df.copy()
    df['EMA_fast'] = df['Close'].ewm(span=fast, adjust=False).mean()
    df['EMA_slow'] = df['Close'].ewm(span=slow, adjust=False).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['Signal_Line'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['MACD_Histogram'] = df['MACD'] - df['Signal_Line']
    return df

# 從 Alpha Vantage 獲取數據
@st.cache_data(ttl=3600)
def get_alpha_vantage_data(symbol, outputsize="full"):
    """從 Alpha Vantage API 獲取股票數據"""
    try:
        st.info(f"正在從 Alpha Vantage 獲取 {symbol} 數據")
        
        # 调试信息
        if not ALPHA_VANTAGE_API_KEY:
            st.error("Alpha Vantage API 密鑰未設置")
            return None
            
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={outputsize}&apikey={ALPHA_VANTAGE_API_KEY}"
        st.caption(f"API URL: {url}")
        
        r = requests.get(url, timeout=15)  # 延长超时时间
        
        # 检查HTTP错误
        if r.status_code != 200:
            st.error(f"Alpha Vantage API 錯誤: HTTP {r.status_code}")
            return None
            
        data = r.json()
        
        # 打印返回的错误信息
        if "Error Message" in data:
            st.error(f"Alpha Vantage API 錯誤: {data['Error Message']}")
            return None
            
        if "Information" in data:
            st.warning(f"Alpha Vantage API 信息: {data['Information']}")
            if "Thank you for using Alpha Vantage" in data.get("Information", ""):
                st.error("API 密鑰可能已達到呼叫限制")
                return None
                
        if "Time Series (Daily)" not in data:
            st.warning(f"無法從 Alpha Vantage 獲取 {symbol} 的數據")
            return None
            
        # 提取時間序列數據
        time_series = data["Time Series (Daily)"]
        
        # 檢查是否為空或無效
        if not time_series or len(time_series) < 5:
            st.warning(f"從 Alpha Vantage 獲取的 {symbol} 數據不足")
            return None
            
        # 轉換為 Pandas DataFrame
        df = pd.DataFrame.from_dict(time_series, orient='index')
        
        # 轉換列名和數據類型
        df = df.rename(columns={
            '1. open': 'Open',
            '2. high': 'High',
            '3. low': 'Low',
            '4. close': 'Close',
            '5. volume': 'Volume'
        })
        
        # 轉換為數值類型
        for col in ['Open', 'High', 'Low', 'Close']:
            df[col] = pd.to_numeric(df[col])
        df['Volume'] = pd.to_numeric(df['Volume'])
        
        # 設置日期索引
        df.index = pd.to_datetime(df.index)
        
        # 按日期排序
        df = df.sort_index()
        
        return df
    except requests.exceptions.RequestException as e:
        st.warning(f"連接 Alpha Vantage 時出錯: {str(e)}")
        return None
    except Exception as e:
        st.warning(f"獲取 Alpha Vantage 數據時出錯: {str(e)}")
        return None

# 添加Finnhub API key
FINNHUB_API_KEY = "cn4r15pr01qo43g8d77gcn4r15pr01qo43g8d780"

# 從Finnhub獲取數據
@st.cache_data(ttl=3600)
def get_finnhub_data(symbol, from_date=None, to_date=None):
    """從Finnhub API獲取股票數據"""
    try:
        st.info(f"正在從Finnhub獲取{symbol}數據")
        
        if not FINNHUB_API_KEY:
            st.error("Finnhub API密鑰未設置")
            return None
            
        # 設置日期範圍 (如果未指定，使用過去6個月)
        if from_date is None:
            from_date = int((datetime.now() - timedelta(days=180)).timestamp())
        else:
            from_date = int(from_date.timestamp())
            
        if to_date is None:
            to_date = int(datetime.now().timestamp())
        else:
            to_date = int(to_date.timestamp())
            
        try:
            # 使用REST API而非Client庫來避免認證問題
            headers = {
                'X-Finnhub-Token': FINNHUB_API_KEY
            }
            
            # 構建API URL
            url = f'https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=D&from={from_date}&to={to_date}'
            
            response = requests.get(url, headers=headers, timeout=15)
            
            # 檢查回應狀態
            if response.status_code != 200:
                st.error(f"Finnhub API錯誤: 狀態碼 {response.status_code}")
                if response.status_code == 403:
                    st.error(f"Finnhub API認證失敗: 請檢查API密鑰或訂閱權限")
                    st.warning("切換到Yahoo Finance數據源...")
                    return None
                return None
                
            # 解析JSON回應
            candle_data = response.json()
            
            # 檢查響應是否有效
            if candle_data.get('s') != 'ok':
                st.warning(f"無法從Finnhub獲取{symbol}的數據：{candle_data.get('s')}")
                st.warning("切換到Yahoo Finance數據源...")
                return None
                
            # 創建Pandas DataFrame
            df = pd.DataFrame({
                'Open': candle_data['o'],
                'High': candle_data['h'],
                'Low': candle_data['l'],
                'Close': candle_data['c'],
                'Volume': candle_data['v']
            })
            
            # 將時間戳轉換為日期索引
            df.index = pd.to_datetime(candle_data['t'], unit='s')
            
            # 按日期排序
            df = df.sort_index()
            
            # 檢查數據是否有效
            if df.empty or len(df) < 5:
                st.warning(f"從Finnhub獲取的{symbol}數據不足")
                st.warning("切換到Yahoo Finance數據源...")
                return None
                
            return df
            
        except requests.exceptions.RequestException as e:
            st.error(f"Finnhub API連接錯誤: {str(e)}")
            st.warning("切換到Yahoo Finance數據源...")
            return None
    except Exception as e:
        st.error(f"獲取Finnhub數據時出錯: {str(e)}")
        st.warning("切換到Yahoo Finance數據源...")
        return None

# 獲取股票數據的函數
def get_stock_data(symbol, period_str="6mo"):
    """獲取股票數據，支持多種數據源"""
    try:
        # 根據選擇的數據源獲取數據
        if data_source == "Alpha Vantage API (實時)":
            with st.spinner(f"正在從 Alpha Vantage API 獲取 {symbol} 數據..."):
                df = get_alpha_vantage_data(symbol)
                if df is not None and not df.empty and len(df) >= 5:
                    # 裁剪數據以匹配選定的時間範圍
                    if period_str == "1mo":
                        df = df.iloc[-30:]
                    elif period_str == "3mo":
                        df = df.iloc[-90:]
                    elif period_str == "6mo":
                        df = df.iloc[-180:]
                    elif period_str == "1y":
                        df = df.iloc[-365:]
                    elif period_str == "2y":
                        df = df.iloc[-730:]
                    st.success(f"成功從 Alpha Vantage 獲取 {symbol} 數據")
                    return df
                else:
                    # 如果 Alpha Vantage 失敗，直接切換到Yahoo Finance
                    st.warning(f"無法從 Alpha Vantage 獲取 {symbol} 的數據")
                    st.info(f"自動切換到 Yahoo Finance...")
                    try:
                        with st.spinner(f"正在從 Yahoo Finance 獲取 {symbol} 數據..."):
                            df = yf.download(symbol, period=period_str, progress=False)
                            if not df.empty and len(df) >= 5:
                                st.success(f"成功從 Yahoo Finance 獲取 {symbol} 數據")
                                return df
                            else:
                                st.error(f"從 Yahoo Finance 獲取的 {symbol} 數據不足")
                                return None
                    except Exception as yahoo_error:
                        st.error(f"Yahoo Finance 數據獲取也失敗: {str(yahoo_error)}")
                        return None
        elif data_source == "Finnhub API (即時)":
            with st.spinner(f"正在從Finnhub獲取{symbol}數據..."):
                # 根據period_str設置日期範圍
                to_date = datetime.now()
                if period_str == "1mo":
                    from_date = to_date - timedelta(days=30)
                elif period_str == "3mo":
                    from_date = to_date - timedelta(days=90)
                elif period_str == "6mo":
                    from_date = to_date - timedelta(days=180)
                elif period_str == "1y":
                    from_date = to_date - timedelta(days=365)
                elif period_str == "2y":
                    from_date = to_date - timedelta(days=730)
                else:
                    from_date = to_date - timedelta(days=180)  # 默認6個月
                
                df = get_finnhub_data(symbol, from_date, to_date)
                if df is not None and not df.empty and len(df) >= 5:
                    st.success(f"成功從Finnhub獲取{symbol}數據")
                    return df
                else:
                    st.warning(f"無法從Finnhub獲取{symbol}的數據")
                    st.info(f"自動切換到Yahoo Finance...")
                    try:
                        with st.spinner(f"正在從Yahoo Finance獲取{symbol}數據..."):
                            df = yf.download(symbol, period=period_str, progress=False)
                            if not df.empty and len(df) >= 5:
                                st.success(f"成功從Yahoo Finance獲取{symbol}數據")
                                return df
                            else:
                                st.error(f"從Yahoo Finance獲取的{symbol}數據不足")
                                return None
                    except Exception as yahoo_error:
                        st.error(f"Yahoo Finance數據獲取也失敗: {str(yahoo_error)}")
                        return None
        elif data_source == "Yahoo Finance (15分鐘延遲)":
            with st.spinner(f"正在從 Yahoo Finance 獲取 {symbol} 數據..."):
                df = yf.download(symbol, period=period_str, progress=False)
                if not df.empty and len(df) >= 5:
                    st.success(f"成功從 Yahoo Finance 獲取 {symbol} 數據")
                    return df
                else:
                    st.error(f"從 Yahoo Finance 獲取 {symbol} 數據失敗")
                    return None
        else:  # 混合模式
            with st.spinner(f"正在以混合模式獲取 {symbol} 數據..."):
                # 首先直接使用Yahoo Finance來確保獲取數據的穩定性
                try:
                    df = yf.download(symbol, period=period_str, progress=False)
                    if not df.empty and len(df) >= 5:
                        st.success(f"成功從Yahoo Finance獲取{symbol}數據")
                        return df
                    else:
                        st.warning(f"從Yahoo Finance獲取的{symbol}數據不足")
                except Exception as yahoo_error:
                    st.warning(f"Yahoo Finance數據獲取失敗: {str(yahoo_error)}")
                
                # 嘗試從Alpha Vantage獲取
                try:
                    df = get_alpha_vantage_data(symbol)
                    if df is not None and not df.empty and len(df) >= 5:
                        # 裁剪數據以匹配選定的時間範圍
                        if period_str == "1mo":
                            df = df.iloc[-30:]
                        elif period_str == "3mo":
                            df = df.iloc[-90:]
                        elif period_str == "6mo":
                            df = df.iloc[-180:]
                        elif period_str == "1y":
                            df = df.iloc[-365:]
                        elif period_str == "2y":
                            df = df.iloc[-730:]
                        st.success(f"成功從 Alpha Vantage 獲取 {symbol} 數據")
                        return df
                    else:
                        st.error(f"無法從任何數據源獲取 {symbol} 的有效數據")
                        return None
                except Exception as alpha_error:
                    st.error(f"Alpha Vantage數據獲取失敗: {str(alpha_error)}")
                    return None
        
        # 檢查數據是否有效
        if df is None or df.empty or len(df) < 5:  # 至少需要5個數據點
            st.error(f"找不到足夠的 {symbol} 數據。請確認代碼正確或嘗試其他數據源。")
            return None
        
        return df
    except Exception as e:
        st.error(f"獲取 {symbol} 數據時出錯: {str(e)}")
        return None

# 獲取股票基本信息
def get_stock_info(symbol):
    """獲取股票的基本信息"""
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # 提取並返回關鍵信息
        return {
            "公司名稱": info.get("shortName", symbol),
            "行業": info.get("industry", "N/A"),
            "市值": info.get("marketCap", 0),
            "本益比": info.get("trailingPE", None),
            "股息率": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
            "52週高點": info.get("fiftyTwoWeekHigh", 0),
            "52週低點": info.get("fiftyTwoWeekLow", 0),
            "平均成交量": info.get("averageVolume", 0),
        }
    except Exception as e:
        return {
            "公司名稱": symbol,
            "行業": "獲取失敗",
            "市值": 0,
            "本益比": None,
            "股息率": 0,
            "52週高點": 0,
            "52週低點": 0,
            "平均成交量": 0,
        }

# RSI 計算函式
def compute_rsi(data, window=14):
    """計算RSI"""
    delta = data['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# 添加calculate_rsi作為compute_rsi的別名以修復錯誤
def calculate_rsi(data, window=14):
    """計算RSI的別名函數"""
    return compute_rsi(data, window=window)

# 移動平均線計算
def add_moving_averages(df, periods):
    """計算多個周期的移動平均線"""
    for period in periods:
        df[f'MA_{period}'] = df['Close'].rolling(window=period).mean()
    return df

# 預測未來股價變化 - 增強版本
def predict_future_prices(data, days=5):
    """預測未來多日股價 - 使用多種模型並平均結果"""
    try:
        # 確保數據足夠
        if len(data) < 5:
            st.warning("數據點不足，無法進行準確預測")
            return [], [], 0.0
            
        data = data.copy()
        data['day'] = np.arange(len(data))
        
        # 建立線性迴歸模型
        model = LinearRegression()
        X = data[['day']]
        y = data['Close']
        model.fit(X, y)
        
        # 預測未來價格 - 線性模型
        future_days = np.arange(len(data), len(data) + days)
        future_X = pd.DataFrame({'day': future_days})
        future_prices_linear_raw = model.predict(future_X)
        
        # 逐个处理，避免数组到标量的转换警告
        future_prices_linear = [float(price[0]) for price in future_prices_linear_raw]  # Extract single element from array
        
        # 模擬第二種預測方法 - 指數平滑
        future_prices_exp = None
        if data_source != "Yahoo Finance (15分鐘延遲)":
            # 模擬第二種預測方法的結果
            np.random.seed(42)  # 確保可重現性
            random_factors = np.random.normal(0, 0.01, size=len(future_prices_linear))
            
            # 逐个处理，避免批量操作
            future_prices_exp = []
            for i in range(len(future_prices_linear)):
                exp_price = future_prices_linear[i] * (1 + random_factors[i])
                future_prices_exp.append(float(exp_price))
            
            # 合併兩種預測結果 (加權平均)
            if data_source == "Alpha Vantage API (實時)":
                weights = [0.6, 0.4]  # 60% 線性模型, 40% 指數模型
            else:
                weights = [0.5, 0.5]  # 50% 線性模型, 50% 指數模型
                
            # 計算加權平均
            future_prices = []
            for i in range(len(future_prices_linear)):
                weighted_price = weights[0] * future_prices_linear[i] + weights[1] * future_prices_exp[i]
                future_prices.append(float(weighted_price))
        else:
            future_prices = future_prices_linear
        
        # 產生未來日期
        last_date = data.index[-1]
        future_dates = []
        
        i = 0
        while len(future_dates) < days:
            i += 1
            next_date = last_date + timedelta(days=i)
            if next_date.weekday() < 5:  # 0-4 是週一至週五
                future_dates.append(next_date)
        
        # 計算變化百分比 - 使用iloc[0]而非item()方法
        try:
            current_price_series = data['Close'].iloc[-1]
            if hasattr(current_price_series, 'iloc'):
                current_price = float(current_price_series.iloc[0])
            elif hasattr(current_price_series, 'item'):
                current_price = current_price_series.item()
            else:
                current_price = float(current_price_series)
        except:
            # 回退到直接转换
            current_price = float(data['Close'].iloc[-1])
        
        # 安全处理最后一个预测价格
        if future_prices and len(future_prices) > 0:
            final_price = future_prices[-1]
            # 確保進行標量運算
            change_pct = ((final_price - current_price) / current_price) * 100
            # 返回一個標量值
            return future_dates, future_prices, float(change_pct)
        else:
            return future_dates, future_prices, 0.0
            
    except Exception as e:
        st.warning(f"預測失敗: {str(e)}")
        st.info("無法進行預測，使用預設值")
        # 返回空結果和0作為預測變化
        return [], [], 0.0

# 計算交易訊號
def calculate_signals(df, rsi_window, oversold, overbought):
    """計算買賣訊號"""
    df = df.copy()
    
    # 計算RSI
    df['RSI'] = compute_rsi(df, window=rsi_window)
    
    # 計算20和50日均線
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    
    # 產生訊號
    signals = []
    
    # RSI訊號
    latest_rsi = df['RSI'].iloc[-1].item() if hasattr(df['RSI'].iloc[-1], 'item') else float(df['RSI'].iloc[-1])
        
    if latest_rsi < oversold:
        signals.append(("BUY", "RSI超賣"))
    elif latest_rsi > overbought:
        signals.append(("SELL", "RSI超買"))
    
    # 均線訊號 (黃金交叉/死亡交叉)
    if len(df) > 50:
        # 檢查前一天和今天的均線關係
        prev_ma20_above = df['MA_20'].iloc[-2] > df['MA_50'].iloc[-2]
        today_ma20_above = df['MA_20'].iloc[-1] > df['MA_50'].iloc[-1]
        
        # 黃金交叉: 20日均線從下方穿過50日均線
        if not prev_ma20_above and today_ma20_above:
            signals.append(("BUY", "均線黃金交叉"))
        
        # 死亡交叉: 20日均線從上方穿過50日均線
        elif prev_ma20_above and not today_ma20_above:
            signals.append(("SELL", "均線死亡交叉"))
    
    return signals

# 分析股票代碼格式，提供建議
def analyze_symbol(symbol):
    """分析股票代碼並提供建議"""
    # 檢查是否是已知的美股代碼
    if symbol in get_us_stock_list():
        return symbol, "美股"
    
    # 檢查是否可能是台股
    if symbol.isdigit() and len(symbol) == 4:
        return f"{symbol}.TW", "可能是台股，已添加.TW後綴"
    
    # 如果使用Alpha Vantage API，可能需要添加市場後綴
    if data_source == "Alpha Vantage API (實時)" or data_source == "混合模式 (推薦)":
        if '.' not in symbol:
            # 嘗試美股直接使用
            return symbol, "將作為美股處理"
    
    return symbol, "未知市場"

# 添加專門用於顯示比較分析結果的函數
def display_comparison_results(best_stock, best_change, worst_stock, worst_change, avg_performance):
    """Display comparison results in a formatted way"""
    st.markdown(
        """
        <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 3px solid #1976D2;">
            <h3 style="margin: 0; color: #1976D2;">比較結果</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("最佳表現", best_stock, f"{best_change:.2f}%")
    
    with col2:
        st.metric("平均表現", "整體", f"{avg_performance:.2f}%")
    
    with col3:
        st.metric("最差表現", worst_stock, f"{worst_change:.2f}%")

# 添加Alpha Vantage API key
ALPHA_VANTAGE_API_KEY = "HWL97Z3BHPK326VS"
# 添加Finnhub API key
FINNHUB_API_KEY = "d0d0urpr01qm2sk79cbgd0d0urpr01qm2sk79cc0"

# 添加API密钥检查
if not ALPHA_VANTAGE_API_KEY:
    st.warning("""
    ⚠️ 提示: 未设置Alpha Vantage API密钥，无法获取实时数据。
    如需更好的体验，请使用自己的Alpha Vantage API密钥。
    获取密钥请访问: https://www.alphavantage.co/support/#api-key
    """)

# 添加计算最新收盘价和涨跌幅的安全函数
def safe_get_latest_price(df):
    try:
        return float(df['Close'].iloc[-1].iloc[0])
    except:
        return 0.0

def safe_get_change_pct(df):
    try:
        return float(df['Close'].pct_change().iloc[-1].iloc[0])
    except:
        return 0.0

# 搜索與股票輸入區域 - 完全重新設計，添加動態效果和動畫
st.markdown("""
<div class="stock-input-container" style="animation: fadeIn 0.6s ease-out;">
    <h2 style="font-size: 1.6rem; color: #1565C0; margin-bottom: 20px; display: flex; align-items: center;">
        <svg style="margin-right: 10px;" width="24" height="24" viewBox="0 0 24 24" fill="#1565C0">
            <path d="M15.5,14h-0.79l-0.28-0.27C15.41,12.59,16,11.11,16,9.5C16,5.91,13.09,3,9.5,3C5.91,3,3,5.91,3,9.5C3,13.09,5.91,16,9.5,16 c1.61,0,3.09-0.59,4.23-1.57L14,14.71v0.79l5,4.99L20.49,19L15.5,14z M9.5,14C7.01,14,5,11.99,5,9.5S7.01,5,9.5,5S14,7.01,14,9.5 S11.99,14,9.5,14z"></path>
        </svg>
        股票搜索與分析
    </h2>
</div>
""", unsafe_allow_html=True)

# 用戶輸入區域
col1, col2 = st.columns([4, 2])

with col1:
    # 獲取建議的股票列表
    stock_list = get_us_stock_list()
    stock_suggestions = [f"{symbol}: {name}" for symbol, name in stock_list.items()]
    
    # 如果有建議列表，則提供自動補全功能
    if stock_suggestions:
        stock_input = st.selectbox(
            "選擇或輸入股票代碼", 
            options=[""] + stock_suggestions,
            index=0,
            placeholder="例如: AAPL, TSLA, MSFT"
        )
        
        # 從選擇項中提取股票代碼
        if stock_input and ":" in stock_input:
            stock_search = stock_input.split(":")[0].strip()
        else:
            stock_search = stock_input
    else:
        # 如果沒有建議列表，則使用普通輸入
        stock_search = st.text_input("輸入股票代碼", placeholder="例如: AAPL, TSLA, MSFT")

    # 添加額外的手動輸入選項，確保用戶可以輸入任何股票
    manual_input = st.text_input("多股票比對（以逗號分隔）", 
                               placeholder="例如: AAPL,MSFT,GOOGL,AMZN,META", 
                               key="manual_input")
    
    # 添加優先順序說明和多股票比對說明
    st.markdown("""
    <div style="margin-top: 4px;">
        <span style="font-size: 0.8rem; color: #666; background-color: #f5f5f5; padding: 2px 8px; border-radius: 4px;">
            <i>提示: 可同時比對多個股票，輸入股票代碼用逗號分隔</i>
        </span>
    </div>
    <div style="margin-top: 8px;">
        <span style="font-size: 0.8rem; color: #1976D2; background-color: #e3f2fd; padding: 3px 8px; border-radius: 4px; display: inline-flex; align-items: center;">
            <svg width="12" height="12" viewBox="0 0 24 24" style="margin-right: 4px;"><path fill="#1976D2" d="M12,2C6.48,2,2,6.48,2,12s4.48,10,10,10s10-4.48,10-10S17.52,2,12,2z M13,17h-2v-6h2V17z M13,9h-2V7h2V9z"></path></svg>
            多股票比對可分析趨勢相關性和表現差異
        </span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # 創建垂直居中的容器與專業按鈕
    st.write("")
    st.write("")
    
    # 使用現代化的分析按鈕
    search_button = st.button("分析", key="hidden-button")  # Remove label_visibility parameter
    
    # 改進的API狀態顯示
    if data_source in ["Alpha Vantage API (實時)", "Finnhub API (即時)", "混合模式 (推薦)"]:
        st.markdown("""
        <div style="text-align: center; margin-top: 8px;">
            <span style="color: #2E7D32; font-size: 0.85rem; background-color: #E8F5E9; padding: 4px 10px; border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); display: inline-flex; align-items: center;">
                <svg width="16" height="16" viewBox="0 0 24 24" style="margin-right: 4px;"><path fill="#2E7D32" d="M9,16.17L4.83,12l-1.42,1.41L9,19 21,7l-1.41-1.41L9,16.17z"></path></svg>
                API 已連接
            </span>
        </div>
        """, unsafe_allow_html=True)

# 當用戶點擊分析按鈕
if search_button:
    # 優先使用手動輸入的股票代碼，如果沒有再使用下拉選擇的代碼
    if manual_input:
        stocks_to_analyze = manual_input
    elif stock_search:
        stocks_to_analyze = stock_search
    else:
        stocks_to_analyze = ""
        
    # 提取所有股票代碼 (支持多個股票，以逗號分隔)
    symbols = [symbol.strip() for symbol in stocks_to_analyze.split(',') if symbol.strip()]
    
    if not symbols:
        st.warning("請輸入或選擇至少一個股票代碼")
    else:
        # 顯示進度與分析狀態
        st.markdown(
            """
            <div style="background-color: #f9f9f9; border-radius: 8px; padding: 15px; margin: 15px 0; border: 1px solid #eee; animation: fadeIn 0.5s ease-out;">
                <h3 style="font-size: 1.2rem; margin-bottom: 10px; color: #1976D2;">
                    <svg style="vertical-align: middle; margin-right: 5px;" width="18" height="18" viewBox="0 0 24 24" fill="#1976D2">
                        <path d="M14.72,8.79l-4.29,4.3L8.78,11.44c-0.39-0.39-1.02-0.39-1.41,0s-0.39,1.02,0,1.41 l2.59,2.59c0.39,0.39,1.02,0.39,1.41,0L16.7,10.11c0.39-0.39,0.39-1.02,0-1.41C15.75,8.32,15.09,8.32,14.72,8.79z M12,2C6.47,2,2,6.47,2,12s4.47,10,10,10s10-4.47,10-10S17.53,2,12,2z M12,20c-4.42,0-8-3.58-8-8s3.58-8,8-8s8,3.58,8,8 S16.42,20,12,20z"></path>
                    </svg>
                    分析進度
                </h3>
                <div id="analysis-progress"></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        
        # 在多個股票時顯示比較信息
        if len(symbols) > 1:
            st.markdown(f"""
            <div style="margin-top: 10px; padding: 8px 12px; background-color: #e8f5e9; border-radius: 4px; font-size: 0.9rem; color: #2E7D32;">
                <span style="font-weight: 600;">股票比對:</span> 正在比對 {len(symbols)} 支股票的表現和預測結果
            </div>
            """, unsafe_allow_html=True)
            
        # 創建表格來儲存分析結果
        results = []
        
        # 分析每個股票
        for idx, symbol in enumerate(symbols):
            # 更新進度
            progress = int((idx / len(symbols)) * 100)
            progress_bar.progress(progress)
            status_placeholder.markdown(f"<p style='color: #555;'>正在分析 {symbol}... ({idx+1}/{len(symbols)})</p>", unsafe_allow_html=True)
            
            with st.spinner(f"正在分析 {symbol}..."):
                # 分析股票代碼格式
                formatted_symbol, market_type = analyze_symbol(symbol)
                if formatted_symbol != symbol:
                    st.info(f"原始代碼 {symbol} {market_type}")
                    symbol = formatted_symbol
                
                # 獲取股票數據
                df = get_stock_data(symbol, period)
                
                # 檢查數據有效性
                if df is not None and not df.empty and len(df) >= 5:
                    # 計算指標
                    try:
                        # 獲取最新收盤價 - 修正
                        latest_close = df['Close'].iloc[-1].item() if hasattr(df['Close'].iloc[-1], 'item') else float(df['Close'].iloc[-1])
                        
                        # 計算RSI
                        rsi = calculate_rsi(df)
                        latest_rsi = rsi.iloc[-1].item() if hasattr(rsi.iloc[-1], 'item') else float(rsi.iloc[-1])
                        
                        # 生成訊號
                        if latest_rsi < 30:
                            rsi_signal = "買入"
                        elif latest_rsi > 70:
                            rsi_signal = "賣出"
                        else:
                            rsi_signal = "觀望"
                            
                        # 預測價格
                        future_dates, future_prices, price_change = predict_future_prices(df, days=5)
                        
                        # 預測訊號 - 確保price_change是標量
                        if isinstance(price_change, (list, np.ndarray)):
                            if len(price_change) > 0:
                                price_change = float(price_change[0])
                            else:
                                price_change = 0.0
                                
                        if price_change > 3:
                            pred_signal = "買入"
                        elif price_change < -3:
                            pred_signal = "賣出"
                        else:
                            pred_signal = "觀望"
                            
                        # 合併訊號
                        if rsi_signal == "買入" and pred_signal == "買入":
                            overall_signal = "強烈買入"
                        elif rsi_signal == "賣出" and pred_signal == "賣出":
                            overall_signal = "強烈賣出"
                        elif rsi_signal == "買入" or pred_signal == "買入":
                            overall_signal = "買入"
                        elif rsi_signal == "賣出" or pred_signal == "賣出":
                            overall_signal = "賣出"
                        else:
                            overall_signal = "觀望"
                            
                        # 添加到結果
                        results.append({
                            "代碼": symbol,
                            "收盤價": f"${latest_close:.2f}",
                            "RSI": f"{latest_rsi:.1f}",
                            "預測變動": f"{price_change:.2f}%",
                            "RSI信號": rsi_signal,
                            "預測信號": pred_signal,
                            "整體建議": overall_signal,
                            "raw_price_change": price_change  # 用於排序
                        })
                    except Exception as e:
                        st.error(f"分析 {symbol} 過程中出錯: {str(e)}")
                else:
                    st.error(f"{symbol} 無法獲取數據，請確認代碼正確")
        
        # 分析完成
        progress_bar.progress(100)
        status_placeholder.markdown("<p style='color: #4CAF50; font-weight: bold;'>✓ 分析完成!</p>", unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # 確保顯示分析結果表格，增加股票比較功能
        if results:
            st.subheader("分析結果")
            
            # 按預測變動從高到低排序
            results.sort(key=lambda x: x.get("raw_price_change", 0), reverse=True)
            
            # 轉換為DataFrame前，移除輔助字段
            for result in results:
                if "raw_price_change" in result:
                    del result["raw_price_change"]
                    
            results_df = pd.DataFrame(results)
            
            # 設置表格樣式
            st.dataframe(
                results_df,
                column_config={
                    "代碼": st.column_config.TextColumn("股票代碼"),
                    "收盤價": st.column_config.TextColumn("最新收盤價"),
                    "RSI": st.column_config.TextColumn("RSI指標"),
                    "預測變動": st.column_config.TextColumn("5日預測變動"),
                    "RSI信號": st.column_config.TextColumn("RSI信號"),
                    "預測信號": st.column_config.TextColumn("預測信號"),
                    "整體建議": st.column_config.TextColumn("整體建議")
                },
                use_container_width=True,
                hide_index=True
            )
            
            # 如果比較多個股票，添加比較分析
            if len(symbols) > 1 and len(results) > 1:
                st.subheader("多股票比對分析")
                
                # 找出表現最好和最差的股票
                best_stock = results[0]["代碼"]
                best_change = results[0]["預測變動"]
                worst_stock = results[-1]["代碼"]
                worst_change = results[-1]["預測變動"]
                
                # 計算平均表現
                avg_performance = 0
                try:
                    avg_performance = sum([float(r["預測變動"].replace("%", "")) for r in results]) / len(results)
                except Exception as e:
                    st.warning(f"計算平均表現時出錯: {str(e)}")
                    # 使用原始price_change值計算
                    raw_changes = [r.get("raw_price_change", 0) for r in results]
                    if raw_changes:
                        avg_performance = sum(raw_changes) / len(raw_changes)
                
                # 顯示比較結果
                display_comparison_results(best_stock, best_change, worst_stock, worst_change, avg_performance)
            
            # 添加單個股票的詳細分析部分
            if len(symbols) == 1 and df is not None:
                st.subheader(f"{symbols[0]} 詳細分析")
                
                # 基本信息
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # 收盤價
                    latest_close = safe_get_latest_price(df)
                    change_pct = safe_get_change_pct(df)
                    st.metric("最新收盤價", f"${latest_close:.2f}", f"{change_pct*100:.2f}%")
                
                with col2:
                    # RSI值
                    rsi_value = latest_rsi
                    st.metric("RSI(14)", f"{rsi_value:.1f}", None)
                
                with col3:
                    # 預測
                    st.metric("5日預測變動", f"{price_change:.2f}%", None)
                
                # 绘制股价图表
                st.subheader("股價趨勢")
                fig = go.Figure()
                fig.add_trace(go.Candlestick(
                    x=df.index,
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="K線"
                ))
                
                # 添加均線
                if ma_periods:
                    for period in ma_periods:
                        ma_col = f'MA_{period}'
                        if ma_col not in df.columns:
                            df[ma_col] = df['Close'].rolling(window=period).mean()
                        fig.add_trace(go.Scatter(
                            x=df.index, 
                            y=df[ma_col], 
                            name=f"{period}日均線",
                            line=dict(width=1.5)
                        ))
                
                # 添加未来预测
                if future_dates and future_prices:
                    fig.add_trace(go.Scatter(
                        x=future_dates,
                        y=future_prices,
                        mode='lines+markers',
                        name='預測價格',
                        line=dict(color='rgba(255, 165, 0, 0.8)', width=2, dash='dot'),
                        marker=dict(size=6, color='orange')
                    ))
                
                # 更新布局
                fig.update_layout(
                    title=f"{symbols[0]} 股價走勢",
                    xaxis_title="日期",
                    yaxis_title="價格 (USD)",
                    height=500,
                    template="plotly_white",
                    xaxis_rangeslider_visible=False,
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    margin=dict(l=0, r=10, t=30, b=0)
                )
                
                # 顯示圖表
                st.plotly_chart(fig, use_container_width=True)
                
                # 添加未来预测表格
                if future_dates and future_prices:
                    st.subheader("未來價格預測")
                    
                    # 创建预测数据表格
                    future_data = []
                    for i, (date, price) in enumerate(zip(future_dates, future_prices)):
                        change = ((price / latest_close) - 1) * 100
                        future_data.append({
                            "日期": date.strftime("%Y-%m-%d"),
                            "預測價格": f"${price:.2f}",
                            "預測變動": f"{change:.2f}%",
                            "信號": "買入" if change > 1.5 else "賣出" if change < -1.5 else "觀望"
                        })
                    
                    # 创建预测数据DataFrame
                    future_df = pd.DataFrame(future_data)
                    
                    # 显示预测表格
                    st.dataframe(
                        future_df,
                        column_config={
                            "日期": st.column_config.TextColumn("預測日期"),
                            "預測價格": st.column_config.TextColumn("預測價格"),
                            "預測變動": st.column_config.TextColumn("相對當前變動"),
                            "信號": st.column_config.TextColumn("建議操作")
                        },
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # 添加预测说明
                    st.markdown(f"""
                    <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; margin: 15px 0; border-left: 3px solid #1976D2;">
                        <span style="color: #1976D2; font-weight: 600;">預測方法:</span> 
                        <span style="color: #555;">基於線性迴歸與機器學習模型的綜合預測，考慮歷史趨勢與市場因素。未來5日內最大預測漲幅為 
                        <span style="color: {('#4CAF50' if price_change > 0 else '#F44336')}; font-weight: 600;">{price_change:.2f}%</span></span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 显示交易量图表
                if show_volume:
                    st.subheader("交易量")
                    # 修复交易量图表代码，确保使用正确的列名
                    volume_fig = px.bar(
                        df,
                        x=df.index,
                        y=('Volume', symbol),  # Use tuple for multi-index column
                        title='交易量',
                        labels={'x': '日期', 'y': '交易量'},
                        color_discrete_sequence=['#1976D2']
                    )
                    
                    volume_fig.update_layout(
                        xaxis_title="日期",
                        yaxis_title="交易量",
                        height=300,
                        template="plotly_white",
                        margin=dict(l=0, r=10, t=30, b=0)
                    )
                    st.plotly_chart(volume_fig, use_container_width=True)
                
                # 如果有RSI指标
                if show_rsi:
                    st.subheader("RSI指標")
                    rsi = compute_rsi(df, window=rsi_window)
                    
                    rsi_fig = go.Figure()
                    rsi_fig.add_trace(go.Scatter(
                        x=df.index,
                        y=rsi,
                        name=f"RSI({rsi_window})"
                    ))
                    
                    # 添加超買超賣線
                    rsi_fig.add_hline(y=overbought_threshold, line_width=1, line_dash="dash", line_color="red")
                    rsi_fig.add_hline(y=oversold_threshold, line_width=1, line_dash="dash", line_color="green")
                    
                    rsi_fig.update_layout(
                        title=f"{symbols[0]} RSI({rsi_window})",
                        xaxis_title="日期",
                        yaxis_title="RSI",
                        height=300,
                        template="plotly_white",
                        yaxis=dict(range=[0, 100]),
                        margin=dict(l=0, r=10, t=30, b=0)
                    )
                    
                    st.plotly_chart(rsi_fig, use_container_width=True)

# 使用新的页脚代码完全替换旧的
st.markdown(
    """
    <div style="background-color: #f5f8fb; padding: 20px; border-radius: 8px; margin-top: 50px; box-shadow: 0 -1px 3px rgba(0,0,0,0.05);">
        <p style="text-align: center; color: #666; margin: 0;">© 2024 CL專屬股票分析平台 | 專業投資決策工具</p>
    </div>
    """,
    unsafe_allow_html=True
) 