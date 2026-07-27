import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣 (部落風)", 
    page_icon="🪵", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (原民傳統部落風) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* 全局背景：木紋紙質質感與傳統織布紋理幾何底紋 */
    .stApp { 
        background-color: #F4EBE1; /* 暖陶土木質色 */
        background-image: linear-gradient(45deg, #EDE0D4 25%, transparent 25%), 
                          linear-gradient(-45deg, #EDE0D4 25%, transparent 25%), 
                          linear-gradient(45deg, transparent 75%, #EDE0D4 75%), 
                          linear-gradient(-45deg, transparent 75%, #EDE0D4 75%);
        background-size: 40px 40px; /* 原民幾何編織暗紋 */
        font-family: 'Noto Serif TC', 'Noto Sans TC', sans-serif;
        color: #4A2810; /* 深樹皮褐 */
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }
    
    /* --- Header (傳統瞭望台與圖騰織帶風格) --- */
    .header-container {
        background: #FFFFFF;
        border: 4px solid #8B263E; /* 祖靈祭典紅 */
        box-shadow: 0px 6px 0px #D9A05B; /* 豐收金黃黃銅陰影 */
        border-radius: 4px; /* 沉穩方形木雕結構 */
        padding: 25px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    /* 模擬傳統編織圖騰織帶裝飾 (紅黑黃相間鋸齒) */
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: repeating-linear-gradient(
            90deg,
            #8B263E, #8B263E 10px,
            #1A1A1A 10px, #1A1A1A 20px,
            #D9A05B 20px, #D9A05B 30px
        );
    }
    
    .main-title {
        font-family: 'Noto Serif TC', serif;
        color: #8B263E; /* 織布硃砂紅 */
        font-size: 38px;
        font-weight: 700;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .sub-title { color: #5C3D2E; font-size: 18px; margin-top: 5px; font-weight: 700; }
    
    .teacher-tag { 
        display: inline-block; 
        margin-top: 15px; 
        padding: 6px 18px; 
        background: #1A1A1A; /* 儀式黑 */
        color: #FFFFFF;
        border-radius: 0px; /* 木雕直角 */
        font-size: 14px; 
        font-weight: bold; 
        border-left: 4px solid #D9A05B;
        border-right: 4px solid #D9A05B;
    }
    
    /* --- Cards (石板屋與木雕山形便利卡) --- */
    .word-card {
        background: #FFFFFF;
        border-radius: 0px; /* 堅硬石板質體 */
        padding: 18px 10px;
        text-align: center;
        border: 1px solid #DDB892;
        border-top: 5px solid #8B263E; /* 頂部圖騰橫帶 */
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 4px 4px 0px rgba(92, 61, 46, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .word-card h3 {
        color: #1A1A1A !important;
        font-weight: 700;
        margin: 0;
        padding-bottom: 5px;
        font-size: 19px;
        font-family: 'Noto Serif TC', serif;
    }
    .word-card:hover { 
        transform: translateY(-4px); 
        box-shadow: 6px 6px 0px #D9A05B; 
        border-color: #8B263E;
    }
    
    .icon-box { font-size: 30px; margin-bottom: 5px; filter: grayscale(10%); }
    .zh-word { font-size: 14px; color: #5C3D2E; font-weight: 500; }
    
    /* --- Sentences (篝火集會橫木風格) --- */
    .sentence-box {
        background: #FFFFFF;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 0px;
        border-left: 6px solid #D9A05B; /* 黃銅土地色側線 */
        border-bottom: 1px solid #E6CCB2;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.02);
    }
    .sentence-amis { font-size: 19px; color: #8B263E; font-weight: 700; margin-bottom: 5px; font-family: 'Noto Serif TC', serif; }
    .sentence-zh { font-size: 15px; color: #332211; font-weight: 500; }
    
    /* --- Buttons (部落集體出征獸骨按鈕) --- */
    .stButton>button { 
        width: 100%; 
        border-radius: 0px; 
        background: #8B263E; 
        border: none; 
        color: #FFFFFF !important; 
        font-weight: bold; 
        font-size: 16px;
        box-shadow: 0px 4px 0px #1A1A1A;
        font-family: 'Noto Serif TC', serif;
        transition: all 0.1s ease;
    }
    .stButton>button:hover { background: #A3334D; color: #FFFFFF !important; }
    .stButton>button:active { transform: translateY(3px); box-shadow: 0px 1px 0px #1A1A1A; }
    
    /* --- Tabs (祭典分區) --- */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] {
        color: #5C3D2E !important; 
        background-color: #E6CCB2 !important;
        border-radius: 0px;
        padding: 8px 22px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #8B263E !important;
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* 修正進度條為山林綠 */
    .stProgress > div > div > div {
        background-color: #D9A05B !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. 資料設定 (主題：Remiad 日子與天氣) ---
VOCABULARY = [
    {"amis": "kapahay", "zh": "好的", "emoji": "🦅", "file": "v_kapahay"},
    {"amis": "remiad", "zh": "日子;天氣;白天", "emoji": "☀️", "file": "v_remiad"},
    {"amis": "katangasaan", "zh": "到達的時間", "emoji": "🏹", "file": "v_katangasaan"},
    {"amis": "katangasaan tu","zh": "到期了", "emoji": "⏳", "file": "v_katangasaan_tu"},
    {"amis": "kasuvucan", "zh": "生日", "emoji": "🔥", "file": "v_kasuvucan"},
    {"amis": "maku", "zh": "我的", "emoji": "🪵", "file": "v_maku"},
    {"amis": "anini a remiad","zh": "今天", "emoji": "🐾", "file": "v_anini_a_remiad"},
    {"amis": "saremiad sa", "zh": "整天", "emoji": "🔄", "file": "v_saremiad_sa"},
    {"amis": "maurad", "zh": "下雨", "emoji": "🌧️", "file": "v_maurad"},
    {"amis": "pataluma’en", "zh": "送(帶)回家", "emoji": "🏡", "file": "v_patalumaen"},
    {"amis": "saremiaden", "zh": "需整天", "emoji": "🌿", "file": "v_saremiaden"},
    {"amis": "pawali", "zh": "曬著", "emoji": "🌾", "file": "v_pawali"},
    {"amis": "vuduy", "zh": "衣服", "emoji": "☲", "file": "v_vuduy"},
    {"amis": "misu", "zh": "你的", "emoji": "🤝", "file": "v_misu"},
    {"amis": "katawalan", "zh": "忘記", "emoji": "🍃", "file": "v_katawalan"},
    {"amis": "uradan", "zh": "下雨(天)", "emoji": "☔", "file": "v_uradan"},
    {"amis": "utiih", "zh": "不方便", "emoji": "⚠️", "file": "v_utiih"},
    {"amis": "dademak", "zh": "做工作", "emoji": "🔨", "file": "v_dademak"}
]

SENTENCES = [
    {"amis": "Kapahay a remiad.", "zh": "好的天氣。", "emoji": "🌈", "file": "s_kapahay_a_remiad"},
    {"amis": "Katangasaan tu ku remiad.", "zh": "到期了。", "emoji": "🛑", "file": "s_katangasaan_tu_ku_remiad"},
    {"amis": "Kasuvucan nu maku anini a remiad.", "zh": "今天是我的生日。", "emoji": "✨", "file": "s_kasuvucan_nu_maku"},
    {"amis": "Saremiad sa a maurad anini.", "zh": "今天整天下著雨。", "emoji": "⛈️", "file": "s_saremiad_sa_a_maurad"},
    {"amis": "Kai remiad a pataluma’en kami.", "zh": "白天送我們回家。", "emoji": "🐗", "file": "s_kai_remiad"},
    {"amis": "Saremiaden a pawali ku vuduy.", "zh": "衣服需整天曬著。", "emoji": "🧺", "file": "s_saremiaden_a_pawali"},
    {"amis": "Katangasaan tu ku kasuvucan nu misu a remiad.", "zh": "你的生日到了。", "emoji": "🎁", "file": "s_katangasaan_tu_ku_kasuvucan"},
    {"amis": "Aya! Katawalan nu maku.", "zh": "哎呀! 我忘記了。", "emoji": "🍁", "file": "s_aya_katawalan"},
    {"amis": "Uradan a remiad utiih a dademak.", "zh": "下雨天工作不方便。", "emoji": "⛏️", "file": "s_uradan_a_remiad"}
]

# 測驗題庫
QUIZ_DATA = [
    {"q": "______ a remiad / 好的天氣", "zh": "好的", "ans": "Kapahay", "opts": ["Kapahay", "Utiih", "Maurad"]},
    {"q": "______ nu maku anini / 今天是我的生日", "zh": "生日", "ans": "Kasuvucan", "opts": ["Kasuvucan", "Remiad", "Vuduy"]},
    {"q": "______ sa a maurad / 整天下雨", "zh": "整天", "ans": "Saremiad", "opts": ["Saremiad", "Anini", "Pawali"]},
    {"q": "Aya! ______ nu maku / 哎呀! 我忘記了", "zh": "忘記", "ans": "Katawalan", "opts": ["Katawalan", "Katangasaan", "Dademak"]},
    {"q": "pawali ku ______ / 曬衣服", "zh": "衣服", "ans": "vuduy", "opts": ["vuduy", "remiad", "utiih"]}
]

# --- 1.5 語音核心 ---
def play_audio(text, filename_base=None):
    if filename_base:
        extensions = ['m4a', 'mp3', 'wav']
        folders = ['audio', '.'] 
        for folder in folders:
            for ext in extensions:
                path = os.path.join(folder, f"{filename_base}.{ext}")
                if os.path.exists(path):
                    mime = 'audio/mp4' if ext == 'm4a' else 'audio/mp3'
                    st.audio(path, format=mime)
                    return 
        st.markdown(f"<span style='color:#FFFFFF; font-size:12px; background:#8B263E; padding:2px 6px; border-radius:0px;'> 🪘 本地呼喚音檔缺失: {filename_base}</span>", unsafe_allow_html=True)
    else:
        try:
            speak_text = text.split('/').strip()
            tts = gTTS(text=speak_text, lang='id') 
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')
        except:
            st.caption(" ")

# --- 2. 測驗邏輯 ---
def init_quiz():
    st.session_state.score = 0
    st.session_state.current_q = 0
    
    # Q1: 聽力
    q1_target = random.choice(VOCABULARY)
    others = [v for v in VOCABULARY if v['amis'] != q1_target['amis']]
    q1_options = random.sample(others, 2) + [q1_target]
    random.shuffle(q1_options)
    st.session_state.q1_data = {"target": q1_target, "options": q1_options}
    
    # Q2: 填空
    q2_data = random.choice(QUIZ_DATA)
    opts_copy = list(q2_data['opts'])
    random.shuffle(opts_copy)
    st.session_state.q2_data = {
        "q": q2_data['q'],
        "zh": q2_data['zh'],
        "ans": q2_data['ans'],
        "opts": opts_copy
    }
    
    # Q3: 句子翻譯
    q3_target = random.choice(SENTENCES)
    other_sentences = [s['zh'] for s in SENTENCES if s['zh'] != q3_target['zh']]


import streamlit as stimport timeimport osimport randomfrom gtts import gTTSfrom io import BytesIO
# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣 (部落風)", 
    page_icon="🪵", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)
# --- CSS 視覺魔法 (原民傳統部落風) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* 全局背景：木紋紙質質感與傳統織布紋理幾何底紋 */
    .stApp { 
        background-color: #F4EBE1; /* 暖陶土木質色 */
        background-image: linear-gradient(45deg, #EDE0D4 25%, transparent 25%), 
                          linear-gradient(-45deg, #EDE0D4 25%, transparent 25%), 
                          linear-gradient(45deg, transparent 75%, #EDE0D4 75%), 
                          linear-gradient(-45deg, transparent 75%, #EDE0D4 75%);
        background-size: 40px 40px; /* 原民幾何編織暗紋 */
        font-family: 'Noto Serif TC', 'Noto Sans TC', sans-serif;
        color: #4A2810; /* 深樹皮褐 */
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }
    
    /* --- Header (傳統瞭望台與圖騰織帶風格) --- */
    .header-container {
        background: #FFFFFF;
        border: 4px solid #8B263E; /* 祖靈祭典紅 */
        box-shadow: 0px 6px 0px #D9A05B; /* 豐收金黃黃銅陰影 */
        border-radius: 4px; /* 沉穩方形木雕結構 */
        padding: 25px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    /* 模擬傳統編織圖騰織帶裝飾 (紅黑黃相間鋸齒) */
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: repeating-linear-gradient(
            90deg,
            #8B263E, #8B263E 10px,
            #1A1A1A 10px, #1A1A1A 20px,
            #D9A05B 20px, #D9A05B 30px
        );
    }
    
    .main-title {
        font-family: 'Noto Serif TC', serif;
        color: #8B263E; /* 織布硃砂紅 */
        font-size: 38px;
        font-weight: 700;
        margin: 0;
        letter-spacing: 1px;
    }
    
    .sub-title { color: #5C3D2E; font-size: 18px; margin-top: 5px; font-weight: 700; }
    
    .teacher-tag { 
        display: inline-block; 
        margin-top: 15px; 
        padding: 6px 18px; 
        background: #1A1A1A; /* 儀式黑 */
        color: #FFFFFF;
        border-radius: 0px; /* 木雕直角 */
        font-size: 14px; 
        font-weight: bold; 
        border-left: 4px solid #D9A05B;
        border-right: 4px solid #D9A05B;
    }
    
    /* --- Cards (石板屋與木雕山形便利卡) --- */
    .word-card {
        background: #FFFFFF;
        border-radius: 0px; /* 堅硬石板質體 */
        padding: 18px 10px;
        text-align: center;
        border: 1px solid #DDB892;
        border-top: 5px solid #8B263E; /* 頂部圖騰橫帶 */
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 4px 4px 0px rgba(92, 61, 46, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .word-card h3 {
        color: #1A1A1A !important;
        font-weight: 700;
        margin: 0;
        padding-bottom: 5px;
        font-size: 19px;
        font-family: 'Noto Serif TC', serif;
    }
    .word-card:hover { 
        transform: translateY(-4px); 
        box-shadow: 6px 6px 0px #D9A05B; 
        border-color: #8B263E;
    }
    
    .icon-box { font-size: 30px; margin-bottom: 5px; filter: grayscale(10%); }
    .zh-word { font-size: 14px; color: #5C3D2E; font-weight: 500; }
    
    /* --- Sentences (篝火集會橫木風格) --- */
    .sentence-box {
        background: #FFFFFF;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 0px;
        border-left: 6px solid #D9A05B; /* 黃銅土地色側線 */
        border-bottom: 1px solid #E6CCB2;
        box-shadow: 2px 2px 0px rgba(0,0,0,0.02);
    }
    .sentence-amis { font-size: 19px; color: #8B263E; font-weight: 700; margin-bottom: 5px; font-family: 'Noto Serif TC', serif; }
    .sentence-zh { font-size: 15px; color: #332211; font-weight: 500; }
    
    /* --- Buttons (部落集體出征獸骨按鈕) --- */
    .stButton>button { 
        width: 100%; 
        border-radius: 0px; 
        background: #8B263E; 
        border: none; 
        color: #FFFFFF !important; 
        font-weight: bold; 
        font-size: 16px;
        box-shadow: 0px 4px 0px #1A1A1A;
        font-family: 'Noto Serif TC', serif;
        transition: all 0.1s ease;
    }
    .stButton>button:hover { background: #A3334D; color: #FFFFFF !important; }
    .stButton>button:active { transform: translateY(3px); box-shadow: 0px 1px 0px #1A1A1A; }
    
    /* --- Tabs (祭典分區) --- */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] {
        color: #5C3D2E !important; 
        background-color: #E6CCB2 !important;
        border-radius: 0px;
        padding: 8px 22px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #8B263E !important;
        color: #FFFFFF !important;
        font-weight: bold;
    }
    
    /* 修正進度條為山林綠 */
    .stProgress > div > div > div {
        background-color: #D9A05B !important;
    }
    </style>""", unsafe_allow_html=True)
# --- 1. 資料設定 (主題：Remiad 日子與天氣) ---VOCABULARY = [
    {"amis": "kapahay", "zh": "好的", "emoji": "🦅", "file": "v_kapahay"},
    {"amis": "remiad", "zh": "日子;天氣;白天", "emoji": "☀️", "file": "v_remiad"},
    {"amis": "katangasaan", "zh": "到達的時間", "emoji": "🏹", "file": "v_katangasaan"},
    {"amis": "katangasaan tu","zh": "到期了", "emoji": "⏳", "file": "v_katangasaan_tu"},
    {"amis": "kasuvucan", "zh": "生日", "emoji": "🔥", "file": "v_kasuvucan"},
    {"amis": "maku", "zh": "我的", "emoji": "🪵", "file": "v_maku"},
    {"amis": "anini a remiad","zh": "今天", "emoji": "🐾", "file": "v_anini_a_remiad"},
    {"amis": "saremiad sa", "zh": "整天", "emoji": "🔄", "file": "v_saremiad_sa"},
    {"amis": "maurad", "zh": "下雨", "emoji": "🌧️", "file": "v_maurad"},
    {"amis": "pataluma’en", "zh": "送(帶)回家", "emoji": "🏡", "file": "v_patalumaen"},
    {"amis": "saremiaden", "zh": "需整天", "emoji": "🌿", "file": "v_saremiaden"},
    {"amis": "pawali", "zh": "曬著", "emoji": "🌾", "file": "v_pawali"},
    {"amis": "vuduy", "zh": "衣服", "emoji": "☲", "file": "v_vuduy"},
    {"amis": "misu", "zh": "你的", "emoji": "🤝", "file": "v_misu"},
    {"amis": "katawalan", "zh": "忘記", "emoji": "🍃", "file": "v_katawalan"},
    {"amis": "uradan", "zh": "下雨(天)", "emoji": "☔", "file": "v_uradan"},
    {"amis": "utiih", "zh": "不方便", "emoji": "⚠️", "file": "v_utiih"},
    {"amis": "dademak", "zh": "做工作", "emoji": "🔨", "file": "v_dademak"}
]
SENTENCES = [
    {"amis": "Kapahay a remiad.", "zh": "好的天氣。", "emoji": "🌈", "file": "s_kapahay_a_remiad"},
    {"amis": "Katangasaan tu ku remiad.", "zh": "到期了。", "emoji": "🛑", "file": "s_katangasaan_tu_ku_remiad"},
    {"amis": "Kasuvucan nu maku anini a remiad.", "zh": "今天是我的生日。", "emoji": "✨", "file": "s_kasuvucan_nu_maku"},
    {"amis": "Saremiad sa a maurad anini.", "zh": "今天整天下著雨。", "emoji": "⛈️", "file": "s_saremiad_sa_a_maurad"},
    {"amis": "Kai remiad a pataluma’en kami.", "zh": "白天送我們回家。", "emoji": "🐗", "file": "s_kai_remiad"},
    {"amis": "Saremiaden a pawali ku vuduy.", "zh": "衣服需整天曬著。", "emoji": "🧺", "file": "s_saremiaden_a_pawali"},
    {"amis": "Katangasaan tu ku kasuvucan nu misu a remiad.", "zh": "你的生日到了。", "emoji": "🎁", "file": "s_katangasaan_tu_ku_kasuvucan"},
    {"amis": "Aya! Katawalan nu maku.", "zh": "哎呀! 我忘記了。", "emoji": "🍁", "file": "s_aya_katawalan"},
    {"amis": "Uradan a remiad utiih a dademak.", "zh": "下雨天工作不方便。", "emoji": "⛏️", "file": "s_uradan_a_remiad"}
]
# 測驗題庫QUIZ_DATA = [
    {"q": "______ a remiad / 好的天氣", "zh": "好的", "ans": "Kapahay", "opts": ["Kapahay", "Utiih", "Maurad"]},
    {"q": "______ nu maku anini / 今天是我的生日", "zh": "生日", "ans": "Kasuvucan", "opts": ["Kasuvucan", "Remiad", "Vuduy"]},
    {"q": "______ sa a maurad / 整天下雨", "zh": "整天", "ans": "Saremiad", "opts": ["Saremiad", "Anini", "Pawali"]},
    {"q": "Aya! ______ nu maku / 哎呀! 我忘記了", "zh": "忘記", "ans": "Katawalan", "opts": ["Katawalan", "Katangasaan", "Dademak"]},
    {"q": "pawali ku ______ / 曬衣服", "zh": "衣服", "ans": "vuduy", "opts": ["vuduy", "remiad", "utiih"]}
]
# --- 1.5 語音核心 ---def play_audio(text, filename_base=None):
    if filename_base:
        extensions = ['m4a', 'mp3', 'wav']
        folders = ['audio', '.'] 
        for folder in folders:
            for ext in extensions:
                path = os.path.join(folder, f"{filename_base}.{ext}")
                if os.path.exists(path):
                    mime = 'audio/mp4' if ext == 'm4a' else 'audio/mp3'
                    st.audio(path, format=mime)
                    return 
        st.markdown(f"<span style='color:#FFFFFF; font-size:12px; background:#8B263E; padding:2px 6px; border-radius:0px;'> 🪘 本地呼喚音檔缺失: {filename_base}</span>", unsafe_allow_html=True)
    else:
        try:
            speak_text = text.split('/').strip()
            tts = gTTS(text=speak_text, lang='id') 
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')
        except:
            st.caption(" ")
# --- 2. 測驗邏輯 ---def init_quiz():
    st.session_state.score = 0
    st.session_state.current_q = 0
    
    # Q1: 聽力
    q1_target = random.choice(VOCABULARY)
    others = [v for v in VOCABULARY if v['amis'] != q1_target['amis']]
    q1_options = random.sample(others, 2) + [q1_target]
    random.shuffle(q1_options)
    st.session_state.q1_data = {"target": q1_target, "options": q1_options}
    
    # Q2: 填空
    q2_data = random.choice(QUIZ_DATA)
    opts_copy = list(q2_data['opts'])
    random.shuffle(opts_copy)
    st.session_state.q2_data = {
        "q": q2_data['q'],
        "zh": q2_data['zh'],
        "ans": q2_data['ans'],
        "opts": opts_copy
    }
    
    # Q3: 句子翻譯
    q3_target = random.choice(SENTENCES)
    other_sentences = [s['zh'] for s in SENTENCES if s['zh'] != q3_target['zh']]

if len(other_sentences) < 2:
q3_options = other_sentences + [q3_target['zh']] + ["天氣很好"]
q3_options = q3_options[:3]
else:
q3_options = random.sample(other_sentences, 2) + [q3_target['zh']]
random.shuffle(q3_options)
st.session_state.q3_data = {"target": q3_target, "options": q3_options}
if 'q1_data' not in st.session_state:
init_quiz()
## --- 3. 介面呈現 ---
def show_learning_mode():
st.markdown("🪵 部落單字筆記 (Vocabulary)", unsafe_allow_html=True)
cols = st.columns(3)
for idx, item in enumerate(VOCABULARY):
with cols[idx % 3]:
display_amis = item['amis']
if "kasuvucan" in display_amis:
display_amis = "kasuvucan
(kasubucan)"
if "vuduy" in display_amis:
display_amis = "vuduy
(buduy)"
st.markdown(f"""

{item['emoji']}
{display_amis}
{item['zh']}

""", unsafe_allow_html=True)
play_audio(item['amis'], filename_base=item['file'])
st.write("")
st.markdown("---")
st.markdown("🔥 篝火例句練習 (Sentences)", unsafe_allow_html=True)
for item in SENTENCES:
st.markdown(f"""

{item['emoji']} {item['amis']}
{item['zh']}

""", unsafe_allow_html=True)
play_audio(item['amis'], filename_base=item['file'])
def show_quiz_mode():
st.markdown("🏹 部落小獵場 (Quiz)", unsafe_allow_html=True)
st.progress((st.session_state.current_q) / 3)
st.write("")
if st.session_state.current_q == 0:
data = st.session_state.q1_data
target = data['target']
st.markdown(f"""

🪵 [聽力辨靈] 聽聽看，這是哪個字？

""", unsafe_allow_html=True)
play_audio(target['amis'], filename_base=target['file'])
st.write("")
cols = st.columns(3)
for idx, opt in enumerate(data['options']):
with cols[idx]:
if st.button(f"{opt['zh']}", key=f"q1_{idx}"):
if opt['amis'] == target['amis']:
st.balloons()
st.success("答對了！ (Correct)")
time.sleep(1)
st.session_state.score += 1
st.session_state.current_q += 1
st.rerun()
else:
st.error("再試一次 (Try again)")
elif st.session_state.current_q == 1:
data = st.session_state.q2_data
st.markdown(f"""

🪵 [織網填空] 句子填空
<h2 style="color:#4A2810; font-size:22px; font-family:"Noto Serif TC";">{data['q'].replace('___', '')}

""", unsafe_allow_html=True)
cols = st.columns(3)
for i, opt in enumerate(data['opts']):
with cols[i]:
if st.button(opt, key=f"q2_{i}"):
if opt.lower() in data['ans'].lower() or data['ans'].lower() in opt.lower():
st.balloons()
st.success("太棒了！ (Great)")
time.sleep(1)
st.session_state.score += 1
st.session_state.current_q += 1
st.rerun()
else:
st.error("不對喔")
elif st.session_state.current_q == 2:
data = st.session_state.q3_data
target = data['target']
st.markdown(f"""

🪵 [圖騰譯義] 這是什麼意思？
{target['amis']}

""", unsafe_allow_html=True)
for idx, opt in enumerate(data['options']):
if st.button(opt, key=f"q3_{idx}"):
if opt == target['zh']:
st.balloons()
st.success("全對！ (Perfect)")
time.sleep(1)
st.session_state.score += 1
st.session_state.current_q += 1
st.rerun()
else:
st.error("再想一下")
else:
st.markdown(f"""

出獵歸來！
榮譽得分: {st.session_state.score} / 3

""", unsafe_allow_html=True)
if st.button("重新出征"):
init_quiz()
st.rerun()
## --- 4. 診斷工具 ---
def show_debug_info():
st.markdown("---")
files_audio = []
if os.path.exists("audio"):
files_audio = [f for f in os.listdir('audio') if f.endswith('.m4a') or f.endswith('.mp3')]
if not files_audio:
st.caption(" 🐾 提示：建立 audio 資料夾並放入音檔，即可聽到真人發音。")
## --- 主程式 ---
def main():
st.markdown("""

Remiad
日子、天氣與白天 (部落文化篇)
部落講師：胡美芳 | 智慧提供者：胡美芳

""", unsafe_allow_html=True)
tab1, tab2 = st.tabs([" 🪵 學習筆記", " 🏹 獵場測驗"])
with tab1:
show_learning_mode()
with tab2:
show_quiz_mode()
show_debug_info()
if name == "main":
main()


