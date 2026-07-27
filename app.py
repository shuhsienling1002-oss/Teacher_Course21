import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣", 
    page_icon="🌿", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (原民傳統編織風) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* 全局背景：傳統麻絲織品粗糙質感與米白底色 */
    .stApp { 
        background-color: #F5F2EB;
        background-image: 
            linear-gradient(90deg, rgba(211,47,47,0.03) 1px, transparent 1px),
            linear-gradient(rgba(26,26,26,0.03) 1px, transparent 1px);
        background-size: 8px 8px;
        font-family: 'Noto Sans TC', sans-serif;
        color: #1A1A1A;
    }
    
    .block-container { 
        padding-top: 2rem !important; 
        padding-bottom: 5rem !important; 
    }
    
    /* --- Header (傳統圖騰大禮堂風格) --- */
    .header-container {
        background: #1A1A1A;
        border-top: 8px solid #D32F2F;
        border-bottom: 8px solid #FBC02D;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.15);
        border-radius: 4px;
        padding: 30px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    .main-title {
        font-family: 'Cinzel', serif;
        color: #F5F2EB;
        font-size: 45px;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 0;
    }
    
    .sub-title { 
        color: #FBC02D; 
        font-size: 20px; 
        margin-top: 8px; 
        font-weight: 500;
        letter-spacing: 1px;
    }
    
    .teacher-tag { 
        display: inline-block; 
        margin-top: 18px; 
        padding: 6px 18px; 
        background: #D32F2F; 
        color: #F5F2EB;
        border-radius: 0px; 
        font-size: 14px; 
        font-weight: bold; 
        border: 2px solid #FBC02D;
    }
    
    /* --- Cards (幾何編織卡片風格) --- */
    .word-card {
        background: #FFFFFF;
        border-radius: 0px;
        padding: 20px 15px;
        text-align: center;
        border: 2px solid #1A1A1A;
        border-top: 6px solid #D32F2F;
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 4px 4px 0px #1A1A1A;
        transition: all 0.2s ease-in-out;
    }
    
    .word-card h3 {
        color: #1A1A1A !important;
        font-weight: 700;
        margin: 0;
        padding-bottom: 8px;
        font-size: 20px;
        letter-spacing: 0.5px;
    }
    
    .word-card:hover { 
        transform: translate(-2px, -2px); 
        box-shadow: 6px 6px 0px #D32F2F; 
    }
    
    .icon-box { 
        font-size: 32px; 
        margin-bottom: 8px; 
    }
    
    .zh-word { 
        font-size: 15px; 
        color: #555555; 
        font-weight: 500; 
    }
    
    /* --- Sentences (祖靈之線條紋風格) --- */
    .sentence-box {
        background: #FFFFFF;
        padding: 22px;
        margin-bottom: 18px;
        border-radius: 0px;
        border: 2px solid #1A1A1A;
        border-left: 8px solid #D32F2F;
        box-shadow: 3px 3px 0px rgba(0,0,0,0.05);
    }
    
    .sentence-amis { 
        font-size: 20px; 
        color: #D32F2F; 
        font-weight: 700; 
        margin-bottom: 6px; 
    }
    
    .sentence-zh { 
        font-size: 16px; 
        color: #1A1A1A; 
    }
    
    /* --- Buttons (部落勇士重裝風格) --- */
    .stButton>button { 
        width: 100%; 
        border-radius: 0px; 
        background: #1A1A1A; 
        border: 2px solid #1A1A1A; 
        color: #F5F2EB !important; 
        font-weight: bold; 
        padding: 10px 0px;
        letter-spacing: 1px;
        box-shadow: 3px 3px 0px #D32F2F;
        transition: all 0.1s;
    }
    
    .stButton>button:hover { 
        background: #D32F2F; 
        border-color: #D32F2F;
        color: #F5F2EB !important;
        box-shadow: 3px 3px 0px #1A1A1A;
    }
    
    .stButton>button:active { 
        transform: translate(2px, 2px); 
        box-shadow: none; 
    }
    
    /* --- Tabs (祭典舞台頁籤風格) --- */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 15px; 
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #1A1A1A !important; 
        background-color: #E8E4D8 !important;
        border: 2px solid #1A1A1A;
        border-radius: 0px;
        padding: 8px 22px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #D32F2F !important;
        color: #F5F2EB !important;
        border-color: #1A1A1A;
        font-weight: bold;
        box-shadow: 3px -3px 0px #FBC02D;
    }
    </style>
""", unsafe_allow_html=True)

# --- 1. 資料設定 (主題：Remiad 日子與天氣) ---
VOCABULARY = [
    {"amis": "kapahay", "zh": "好的", "emoji": "☀️", "file": "v_kapahay"},
    {"amis": "remiad", "zh": "日子;天氣;白天", "emoji": "📅", "file": "v_remiad"},
    {"amis": "katangasaan", "zh": "到達的時間", "emoji": "⏳", "file": "v_katangasaan"},
    {"amis": "katangasaan tu", "zh": "到期了", "emoji": "🔔", "file": "v_katangasaan_tu"},
    {"amis": "kasuvucan", "zh": "生日", "emoji": "🎂", "file": "v_kasuvucan"},
    {"amis": "maku", "zh": "我的", "emoji": "🙋‍♂️", "file": "v_maku"},
    {"amis": "anini a remiad", "zh": "今天", "emoji": "📌", "file": "v_anini_a_remiad"},
    {"amis": "saremiad sa", "zh": "整天", "emoji": "🔄", "file": "v_saremiad_sa"},
    {"amis": "maurad", "zh": "下雨", "emoji": "🌧️", "file": "v_maurad"},
    {"amis": "pataluma’en", "zh": "送(帶)回家", "emoji": "🏡", "file": "v_patalumaen"},
    {"amis": "saremiaden", "zh": "需整天", "emoji": "⏳", "file": "v_saremiaden"},
    {"amis": "pawali", "zh": "曬著", "emoji": "🧺", "file": "v_pawali"},
    {"amis": "vuduy", "zh": "衣服", "emoji": "👕", "file": "v_vuduy"},
    {"amis": "misu", "zh": "你的", "emoji": "👉", "file": "v_misu"},
    {"amis": "katawalan", "zh": "忘記", "emoji": "❓", "file": "v_katawalan"},
    {"amis": "uradan", "zh": "下雨(天)", "emoji": "☔", "file": "v_uradan"},
    {"amis": "utiih", "zh": "不方便", "emoji": "⚠️", "file": "v_utiih"},
    {"amis": "dademak", "zh": "做工作", "emoji": "🛠️", "file": "v_dademak"}
]

SENTENCES = [
    {"amis": "Kapahay a remiad.", "zh": "好的天氣。", "emoji": "🌈", "file": "s_kapahay_a_remiad"},
    {"amis": "Katangasaan tu ku remiad.", "zh": "到期了。", "emoji": "⏰", "file": "s_katangasaan_tu_ku_remiad"},
    {"amis": "Kasuvucan nu maku anini a remiad.", "zh": "今天是我的生日。", "emoji": "🎉", "file": "s_kasuvucan_nu_maku"},
    {"amis": "Saremiad sa a maurad anini.", "zh": "今天整天下著雨。", "emoji": "🌧️", "file": "s_saremiad_sa_a_maurad"},
    {"amis": "Kai remiad a pataluma’en kami.", "zh": "白天送我們回家。", "emoji": "🚌", "file": "s_kai_remiad"},
    {"amis": "Saremiaden a pawali ku vuduy.", "zh": "衣服需整天曬著。", "emoji": "☀️", "file": "s_saremiaden_a_pawali"},
    {"amis": "Katangasaan tu ku kasuvucan nu misu a remiad.", "zh": "你的生日到了。", "emoji": "🎁", "file": "s_katangasaan_tu_ku_kasuvucan"},
    {"amis": "Aya! Katawalan nu maku.", "zh": "哎呀! 我忘記了。", "emoji": "💡", "file": "s_aya_katawalan"},
    {"amis": "Uradan a remiad utiih a dademak.", "zh": "下雨天工作不方便。", "emoji": "🚶‍♂️", "file": "s_uradan_a_remiad"}
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
        st.markdown(f"<span style='color:#FFFFFF; font-size:12px; background:#D32F2F; padding:2px 6px; border-radius:0px;'> 🪶 缺音檔: {filename_base}</span>", unsafe_allow_html=True)
    else:
        try:
            speak_text = text.split('/')[0].strip()
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
    random.shuffle(q2_data['opts'])
    st.session_state.q2_data = q2_data
    
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

# --- 3. 介面呈現 ---
def show_learning_mode():
    st.markdown("<h3 style='color:#D32F2F; text-align:center; margin-bottom:25px; font-weight:700;'>❖ 單字筆記 (Vocabulary) ❖</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, item in enumerate(VOCABULARY):


import streamlit as stimport timeimport osimport randomfrom gtts import gTTSfrom io import BytesIO
# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣", 
    page_icon="🌿", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)
# --- CSS 視覺魔法 (原民傳統編織風) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* 全局背景：傳統麻絲織品粗糙質感與米白底色 */
    .stApp { 
        background-color: #F5F2EB;
        background-image: 
            linear-gradient(90deg, rgba(211,47,47,0.03) 1px, transparent 1px),
            linear-gradient(rgba(26,26,26,0.03) 1px, transparent 1px);
        background-size: 8px 8px;
        font-family: 'Noto Sans TC', sans-serif;
        color: #1A1A1A;
    }
    
    .block-container { 
        padding-top: 2rem !important; 
        padding-bottom: 5rem !important; 
    }
    
    /* --- Header (傳統圖騰大禮堂風格) --- */
    .header-container {
        background: #1A1A1A;
        border-top: 8px solid #D32F2F;
        border-bottom: 8px solid #FBC02D;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.15);
        border-radius: 4px;
        padding: 30px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    .main-title {
        font-family: 'Cinzel', serif;
        color: #F5F2EB;
        font-size: 45px;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 0;
    }
    
    .sub-title { 
        color: #FBC02D; 
        font-size: 20px; 
        margin-top: 8px; 
        font-weight: 500;
        letter-spacing: 1px;
    }
    
    .teacher-tag { 
        display: inline-block; 
        margin-top: 18px; 
        padding: 6px 18px; 
        background: #D32F2F; 
        color: #F5F2EB;
        border-radius: 0px; 
        font-size: 14px; 
        font-weight: bold; 
        border: 2px solid #FBC02D;
    }
    
    /* --- Cards (幾何編織卡片風格) --- */
    .word-card {
        background: #FFFFFF;
        border-radius: 0px;
        padding: 20px 15px;
        text-align: center;
        border: 2px solid #1A1A1A;
        border-top: 6px solid #D32F2F;
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 4px 4px 0px #1A1A1A;
        transition: all 0.2s ease-in-out;
    }
    
    .word-card h3 {
        color: #1A1A1A !important;
        font-weight: 700;
        margin: 0;
        padding-bottom: 8px;
        font-size: 20px;
        letter-spacing: 0.5px;
    }
    
    .word-card:hover { 
        transform: translate(-2px, -2px); 
        box-shadow: 6px 6px 0px #D32F2F; 
    }
    
    .icon-box { 
        font-size: 32px; 
        margin-bottom: 8px; 
    }
    
    .zh-word { 
        font-size: 15px; 
        color: #555555; 
        font-weight: 500; 
    }
    
    /* --- Sentences (祖靈之線條紋風格) --- */
    .sentence-box {
        background: #FFFFFF;
        padding: 22px;
        margin-bottom: 18px;
        border-radius: 0px;
        border: 2px solid #1A1A1A;
        border-left: 8px solid #D32F2F;
        box-shadow: 3px 3px 0px rgba(0,0,0,0.05);
    }
    
    .sentence-amis { 
        font-size: 20px; 
        color: #D32F2F; 
        font-weight: 700; 
        margin-bottom: 6px; 
    }
    
    .sentence-zh { 
        font-size: 16px; 
        color: #1A1A1A; 
    }
    
    /* --- Buttons (部落勇士重裝風格) --- */
    .stButton>button { 
        width: 100%; 
        border-radius: 0px; 
        background: #1A1A1A; 
        border: 2px solid #1A1A1A; 
        color: #F5F2EB !important; 
        font-weight: bold; 
        padding: 10px 0px;
        letter-spacing: 1px;
        box-shadow: 3px 3px 0px #D32F2F;
        transition: all 0.1s;
    }
    
    .stButton>button:hover { 
        background: #D32F2F; 
        border-color: #D32F2F;
        color: #F5F2EB !important;
        box-shadow: 3px 3px 0px #1A1A1A;
    }
    
    .stButton>button:active { 
        transform: translate(2px, 2px); 
        box-shadow: none; 
    }
    
    /* --- Tabs (祭典舞台頁籤風格) --- */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 15px; 
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #1A1A1A !important; 
        background-color: #E8E4D8 !important;
        border: 2px solid #1A1A1A;
        border-radius: 0px;
        padding: 8px 22px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #D32F2F !important;
        color: #F5F2EB !important;
        border-color: #1A1A1A;
        font-weight: bold;
        box-shadow: 3px -3px 0px #FBC02D;
    }
    </style>""", unsafe_allow_html=True)
# --- 1. 資料設定 (主題：Remiad 日子與天氣) ---VOCABULARY = [
    {"amis": "kapahay", "zh": "好的", "emoji": "☀️", "file": "v_kapahay"},
    {"amis": "remiad", "zh": "日子;天氣;白天", "emoji": "📅", "file": "v_remiad"},
    {"amis": "katangasaan", "zh": "到達的時間", "emoji": "⏳", "file": "v_katangasaan"},
    {"amis": "katangasaan tu", "zh": "到期了", "emoji": "🔔", "file": "v_katangasaan_tu"},
    {"amis": "kasuvucan", "zh": "生日", "emoji": "🎂", "file": "v_kasuvucan"},
    {"amis": "maku", "zh": "我的", "emoji": "🙋‍♂️", "file": "v_maku"},
    {"amis": "anini a remiad", "zh": "今天", "emoji": "📌", "file": "v_anini_a_remiad"},
    {"amis": "saremiad sa", "zh": "整天", "emoji": "🔄", "file": "v_saremiad_sa"},
    {"amis": "maurad", "zh": "下雨", "emoji": "🌧️", "file": "v_maurad"},
    {"amis": "pataluma’en", "zh": "送(帶)回家", "emoji": "🏡", "file": "v_patalumaen"},
    {"amis": "saremiaden", "zh": "需整天", "emoji": "⏳", "file": "v_saremiaden"},
    {"amis": "pawali", "zh": "曬著", "emoji": "🧺", "file": "v_pawali"},
    {"amis": "vuduy", "zh": "衣服", "emoji": "👕", "file": "v_vuduy"},
    {"amis": "misu", "zh": "你的", "emoji": "👉", "file": "v_misu"},
    {"amis": "katawalan", "zh": "忘記", "emoji": "❓", "file": "v_katawalan"},
    {"amis": "uradan", "zh": "下雨(天)", "emoji": "☔", "file": "v_uradan"},
    {"amis": "utiih", "zh": "不方便", "emoji": "⚠️", "file": "v_utiih"},
    {"amis": "dademak", "zh": "做工作", "emoji": "🛠️", "file": "v_dademak"}
]
SENTENCES = [
    {"amis": "Kapahay a remiad.", "zh": "好的天氣。", "emoji": "🌈", "file": "s_kapahay_a_remiad"},
    {"amis": "Katangasaan tu ku remiad.", "zh": "到期了。", "emoji": "⏰", "file": "s_katangasaan_tu_ku_remiad"},
    {"amis": "Kasuvucan nu maku anini a remiad.", "zh": "今天是我的生日。", "emoji": "🎉", "file": "s_kasuvucan_nu_maku"},
    {"amis": "Saremiad sa a maurad anini.", "zh": "今天整天下著雨。", "emoji": "🌧️", "file": "s_saremiad_sa_a_maurad"},
    {"amis": "Kai remiad a pataluma’en kami.", "zh": "白天送我們回家。", "emoji": "🚌", "file": "s_kai_remiad"},
    {"amis": "Saremiaden a pawali ku vuduy.", "zh": "衣服需整天曬著。", "emoji": "☀️", "file": "s_saremiaden_a_pawali"},
    {"amis": "Katangasaan tu ku kasuvucan nu misu a remiad.", "zh": "你的生日到了。", "emoji": "🎁", "file": "s_katangasaan_tu_ku_kasuvucan"},
    {"amis": "Aya! Katawalan nu maku.", "zh": "哎呀! 我忘記了。", "emoji": "💡", "file": "s_aya_katawalan"},
    {"amis": "Uradan a remiad utiih a dademak.", "zh": "下雨天工作不方便。", "emoji": "🚶‍♂️", "file": "s_uradan_a_remiad"}
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
        st.markdown(f"<span style='color:#FFFFFF; font-size:12px; background:#D32F2F; padding:2px 6px; border-radius:0px;'> 🪶 缺音檔: {filename_base}</span>", unsafe_allow_html=True)
    else:
        try:
            speak_text = text.split('/')[0].strip()
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
    random.shuffle(q2_data['opts'])
    st.session_state.q2_data = q2_data
    
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
# --- 3. 介面呈現 ---def show_learning_mode():
    st.markdown("<h3 style='color:#D32F2F; text-align:center; margin-bottom:25px; font-weight:700;'>❖ 單字筆記 (Vocabulary) ❖</h3>", unsafe_allow_html=True)
    
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
st.markdown("", unsafe_allow_html=True)
st.markdown("❖ 例句練習 (Sentences) ❖", unsafe_allow_html=True)
for item in SENTENCES:
st.markdown(f"""

{item['emoji']} {item['amis']}
{item['zh']}

""", unsafe_allow_html=True)
play_audio(item['amis'], filename_base=item['file'])
def show_quiz_mode():
st.markdown("❖ 部落小測驗 (Quiz) ❖", unsafe_allow_html=True)
st.progress((st.session_state.current_q) / 3)
st.write("")
if st.session_state.current_q == 0:
data = st.session_state.q1_data
target = data['target']
st.markdown(f"""

👂 聽聽看，這是哪個字？

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

📝 幾何填空挑戰

{data['q'].replace('___', '')}


""", unsafe_allow_html=True)
st.write("")
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

🏹 這是什麼意思？
{target['amis']}

""", unsafe_allow_html=True)
st.write("")
play_audio(target['amis'], filename_base=target['file'])
for opt in data['options']:
if st.button(opt):
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

✨ 織布完成！測驗結束 ✨
勇士得分: {st.session_state.score} / 3

""", unsafe_allow_html=True)
st.write("")
if st.button("重新挑戰 🔄"):
init_quiz()
st.rerun()
## --- 4. 診斷工具 ---
def show_debug_info():
st.markdown("

", unsafe_allow_html=True)
files_audio = []
if os.path.exists("audio"):
files_audio = [f for f in os.listdir('audio') if f.endswith('.m4a') or f.endswith('.mp3')]
if not files_audio:
st.caption("🌿 提示：建立 audio 資料夾並放入音檔，即可聽到真人發音。")
## --- 主程式 ---
def main():
st.markdown("""

Remiad
日子 ‧ 天氣 ‧ 白天
講師暨教材提供：胡美芳 老師

""", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["🌿 智慧學習筆記", "🏹 勇士小測驗"])
with tab1:
show_learning_mode()
with tab2:
show_quiz_mode()
show_debug_info()
if name == "main":
main()


