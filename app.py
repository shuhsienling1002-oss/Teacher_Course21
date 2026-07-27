import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 未來科技介面", 
    page_icon="⚡", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (賽博龐克霓虹科技風) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* 全局背景：深邃科幻黑與電子網格細線 */
    .stApp { 
        background-color: #0B0E14;
        background-image: linear-gradient(rgba(18, 24, 38, 0.4) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(18, 24, 38, 0.4) 1px, transparent 1px);
        background-size: 30px 30px;
        font-family: 'Orbitron', 'Noto Sans TC', sans-serif;
        color: #E2E8F0;
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }
    
    /* --- Header (高科技能量核心風格) --- */
    .header-container {
        background: #121826;
        border: 2px solid #00FFCC; /* 螢光翠綠邊框 */
        box-shadow: 0px 0px 20px rgba(0, 255, 204, 0.3), inset 0px 0px 15px rgba(0, 255, 204, 0.1);
        border-radius: 4px; /* 稜角分明 */
        padding: 25px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }
    
    /* 模擬邊角科技感飾條 */
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 15px;
        height: 15px;
        border-top: 3px solid #FF007F; /* 霓虹粉紅角 */
        border-left: 3px solid #FF007F;
    }

    .header-container::after {
        content: '';
        position: absolute;
        bottom: 0;
        right: 0;
        width: 15px;
        height: 15px;
        border-bottom: 3px solid #FF007F;
        border-right: 3px solid #FF007F;
    }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #00FFCC; /* 翠綠核心 */
        font-size: 42px;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.6);
        letter-spacing: 2px;
    }
    
    .sub-title { 
        color: #8A99AD; 
        font-size: 16px; 
        margin-top: 8px; 
        font-weight: 500;
        letter-spacing: 1px;
    }
    
    .teacher-tag { 
        display: inline-block; 
        margin-top: 15px; 
        padding: 4px 12px; 
        background: rgba(255, 0, 127, 0.1); 
        color: #FF007F;
        border-radius: 0px; 
        font-size: 13px; 
        font-weight: bold; 
        border: 1px solid #FF007F;
        text-shadow: 0 0 5px rgba(255, 0, 127, 0.5);
    }

    /* --- Cards (數據終端模組風) --- */
    .word-card {
        background: #121826;
        border-radius: 4px;
        padding: 20px 10px;
        text-align: center;
        border: 1px solid #1E293B;
        border-left: 4px solid #00F0FF; /* 冰藍色側邊發光條 */
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .word-card h3 {
        color: #00F0FF !important;
        font-weight: 700;
        margin: 0;
        padding-bottom: 8px;
        font-size: 19px;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.4);
    }
    
    .word-card:hover { 
        transform: translateY(-4px); 
        border-color: #00F0FF;
        box-shadow: 0px 0px 15px rgba(0, 240, 255, 0.4); 
    }
    
    .icon-box { font-size: 28px; margin-bottom: 8px; filter: drop-shadow(0 0 5px rgba(255,255,255,0.2)); }
    .zh-word { font-size: 14px; color: #94A3B8; font-weight: 500; }
    
    /* --- Sentences (矩陣代碼面板風格) --- */
    .sentence-box {
        background: #121826;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 4px;
        border: 1px solid #1E293B;
        border-bottom: 2px solid #FF007F; /* 粉紅能量底線 */
        box-shadow: inset 0 0 10px rgba(0,0,0,0.2);
    }
    .sentence-amis { 
        font-size: 18px; 
        color: #FF007F; 
        font-weight: 700; 
        margin-bottom: 8px; 
        text-shadow: 0 0 8px rgba(255, 0, 127, 0.4);
    }
    .sentence-zh { font-size: 15px; color: #E2E8F0; }
    
    /* --- Buttons (電漿按鈕) --- */
    .stButton>button { 
        width: 100%; 
        border-radius: 4px; 
        background: transparent; 
        border: 1px solid #00FFCC; 
        color: #00FFCC !important; 
        font-weight: bold; 
        letter-spacing: 1px;
        box-shadow: 0 0 8px rgba(0, 255, 204, 0.2);
        transition: all 0.2s;
    }
    .stButton>button:hover { 
        background: #00FFCC; 
        color: #0B0E14 !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.6);
    }
    .stButton>button:active { transform: translateY(1px); box-shadow: none; }
    
    /* --- Tabs (系統切換卡) --- */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; }
    .stTabs [data-baseweb="tab"] {
        color: #8A99AD !important; 
        background-color: rgba(30, 41, 59, 0.5) !important;
        border-radius: 4px 4px 0 0;
        padding: 6px 20px;
        border: 1px solid #1E293B;
    }
    .stTabs [aria-selected="true"] {
        background-color: #121826 !important;
        color: #00FFCC !important;
        font-weight: bold;
        border: 1px solid #00FFCC;
        border-bottom: 2px solid #121826;
        box-shadow: 0px -4px 10px rgba(0, 255, 204, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# (以下資料內容與教學模式邏輯保持不變，略...)
# [為了簡潔，這裡省略了語音處理與邏輯函數的內容]
# ... 
# ...

def main():
    st.markdown("""
        <div class="header-container">
        <h1 class="main-title">Remiad // 系統</h1>
        <div class="sub-title">日子、天氣與白晝數據庫</div>
        <div class="teacher-tag">控制台講師：胡美芳 | 數據源：胡美芳</div>
        </div>
    """, unsafe_allow_html=True)
    
    # UI Layout & Tabs...
    # (省略主程序細節)

if __name__ == "__main__":
    main()
