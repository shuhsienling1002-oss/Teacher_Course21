import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣", 
    page_icon="📅", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (極簡北歐冷調風) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* 全局背景：北歐極簡冷調灰底 */
    .stApp { 
        background-color: #F8F9FA;
        font-family: 'Inter', 'Noto Sans TC', sans-serif;
        color: #2D3748;
    }
    
    .block-container { padding-top: 3rem !important; padding-bottom: 5rem !important; }
    
    /* --- Header (北歐洗練風) --- */
    .header-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border-radius: 12px;
        padding: 35px 25px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }
    
    /* 左側冷調冰川藍現代裝飾條 */
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: #90CDF4;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        color: #1A202C; 
        font-size: 42px;
        font-weight: 600;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    .sub-title { 
        color: #718096; 
        font-size: 16px; 
        margin-top: 8px; 
        font-weight: 400; 
        letter-spacing: 0.5px;
    }
    
    .teacher-tag { 
        display: inline-block; 
        margin-top: 20px; 
        padding: 4px 14px; 
        background: #EDF2F7; 
        color: #4A5568;
        border-radius: 6px; 
        font-size: 13px; 
        font-weight: 500; 
        border: 1px solid #CBD5E0;
    }
    
    /* --- Cards (冷調平板風格) --- */
    .word-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 24px 16px;
        text-align: center;
        border: 1px solid #E2E8F0;
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: all 0.25s ease-in-out;
    }
    
    .word-card h3 {
        color: #1A202C !important;
        font-weight: 600;
        margin: 0;
        padding-bottom: 8px;
        font-size: 18px;
        letter-spacing: -0.3px;
    }
    
    .word-card:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border-color: #CBD5E0;
    }
    
    .icon-box { font-size: 28px; margin-bottom: 8px; filter: grayscale(20%); }
    .zh-word { font-size: 14px; color: #718096; font-weight: 400; }
    
    /* --- Sentences (極簡橫欄風格) --- */
    .sentence-box {
        background: #FFFFFF;
        padding: 20px 24px;
        margin-bottom: 15px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    .sentence-amis { font-size: 18px; color: #2B6CB0; font-weight: 600; margin-bottom: 6px; }
    .sentence-zh { font-size: 14px; color: #4A5568; }
    
    /* --- Buttons --- */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        background: #4A5568; 
        border: 1px solid #4A5568; 
        color: #FFFFFF !important; 
        font-weight: 500; 
        font-size: 14px;
        padding: 8px 16px;
        letter-spacing: 0.5px;
        box-shadow: none;
        transition: all 0.2s;
    }
    .stButton>button:hover { background: #2D3748; border-color: #2D3748; color: #FFFFFF !important; }
    .stButton>button:active { transform: scale(0.98); background: #1A202C; }
    
    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #EDF2F7; padding: 4px; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] {
        color: #718096 !important; 
        background-color: transparent !important;
        border-radius: 6px;
        padding: 6px 18px;
        font-size: 14px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* 修正內建水平線樣式 */
    hr { margin: 2rem 0 !important; border-color: #E2E8F0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 1. 資料設定 (主題：Remiad 日子與天氣) ---
VOCABULARY = [
    {"amis": "kapahay", "zh": "好的", "emoji": "👍", "file": "v_kapahay"},
    {"amis": "remiad", "zh": "日子;天氣;白天", "emoji": "📅", "file": "v_remiad"},
    {"amis": "katangasaan", "zh": "到達的時間", "emoji": "⏱️", "file": "v_katangasaan"},
    {"amis": "katangasaan tu", "zh": "到期了", "emoji": "🔴", "file": "v_katangasaan_tu"},
    {"amis": "kasuvucan", "zh": "生日", "emoji": "🎂", "file": "v_kasuvucan"},
    {"amis": "maku", "zh": "我的", "emoji": "🙋", "file": "v_maku"},
    {"amis": "anini a remiad", "zh": "今天", "emoji": "📅", "file": "v_anini_a_remiad"},
    {"amis": "saremiad sa", "zh": "整天", "emoji": "🔄", "file": "v_saremiad_sa"},
    {"amis": "maurad", "zh": "下雨", "emoji": "🌧️", "file": "v_maurad"},
    {"amis": "pataluma’en", "zh": "送(帶)回家", "emoji": "🏠", "file": "v_patalumaen"},
    {"amis": "saremiaden", "zh": "需整天", "emoji": "⏳", "file": "v_saremiaden"},
    {"amis": "pawali", "zh": "曬著", "emoji": "☀️", "file": "v_pawali"},
    {"amis": "vuduy", "zh": "衣服", "emoji": "👕", "file": "v_vuduy"},
    {"amis": "misu", "zh": "你的", "emoji": "👊", "file": "v_misu"},
    {"amis": "katawalan", "zh": "忘記", "emoji": "😫", "file": "v_katawalan"},
    {"amis": "uradan", "zh": "下雨(天)", "emoji": "☔", "file": "v_uradan"},
    {"amis": "utiih", "zh": "不方便", "emoji": "😣", "file": "v_utiih"},
    {"amis": "dademak", "zh": "做工作", "emoji": "🛠️", "file": "v_dademak"},
]

SENTENCES = [
    {"amis": "Kapahay a remiad.", "zh": "好的天氣。", "emoji": "🌤️", "file": "s_kapahay_a_remiad"},
    {"amis": "Katangasaan tu ku remiad.", "zh": "到期了。", "emoji": "🔚", "file": "s_katangasaan_tu_ku_remiad"},
    {"amis": "Kasuvucan nu maku anini a remiad.", "zh": "今天是我的生日。", "emoji": "🎂", "file": "s_kasuvucan_nu_maku"},
    {"amis": "Saremiad sa a maurad anini.", "zh": "今天整天下著雨。", "emoji": "🌧️", "file": "s_saremiad_sa_a_maurad"},
    {"amis": "Kai remiad a pataluma’en kami.", "zh": "白天送我們回家。", "emoji": "🚘", "file": "s_kai_remiad"},
    {"amis": "Saremiaden a pawali ku vuduy.", "zh": "衣服需整天曬著。", "emoji": "👕", "file": "s_saremiaden_a_pawali"},
    {"amis": "Katangasaan tu ku kasuvucan nu misu a remiad.", "zh": "你的生日到了。", "emoji": "🎉", "file": "s_katangasaan_tu_ku_kasuvucan"},
    {"amis": "Aya! Katawalan nu maku.", "zh": "哎呀! 我忘記了。", "emoji": "🤦", "file": "s_aya_katawalan"},
    {"amis": "Uradan a remiad utiih a dademak.", "zh": "下雨天工作不方便。", "emoji": "😥", "file": "s_uradan_a_remiad"},
]

# 測驗題庫
QUIZ_DATA = [
    {"q": "______ a remiad / 好的天氣", "zh": "好的", "ans": "Kapahay", "opts": ["Kapahay", "Utiih", "Maurad"]},
    {"q": "______ nu maku anini / 今天是我的生日", "zh": "生日", "ans": "Kasuvucan", "opts": ["Kasuvucan", "Remiad", "Vuduy"]},
    {"q": "______ sa a maurad / 整天下雨", "zh": "整天", "ans": "Saremiad", "opts": ["Saremiad", "Anini", "Pawali"]},
    {"q": "Aya! ______ nu maku / 哎呀! 我忘記了", "zh": "忘記", "ans": "Katawalan", "opts": ["Katawalan", "Katangasaan", "Dademak"]},
    {"q": "pawali ku ______ / 曬衣服", "zh": "衣服", "ans": "vuduy", "opts": ["vuduy", "remiad", "utiih"]},
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
        st.markdown(f"<span style='color:#718096; font-size:12px; background:#EDF2F7; padding:2px 6px; border-radius:4px; border: 1px solid #E2E8F0;'> 缺音檔: {filename_base}</span>", unsafe_allow_html=True)
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
    st.markdown("<h3 style='color:#1A202C; font-weight:600; text-align:center; margin-bottom:25px; letter-spacing:-0.3px;'> 單字筆記 (Vocabulary)</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, item in enumerate(VOCABULARY):
        with cols[idx % 3]:
            # 處理括號顯示
            display_amis = item['amis']
            if "kasuvucan" in display_amis:

這是一份將原本程式碼徹底改造為 「極簡北歐冷調風」 (Nordic Minimalist Style) 的完整 Streamlit 程式碼。
我為您進行了以下前端與視覺的調整：

   1. 色彩計畫 (Color Palette)：全面棄用暖橘與米色，改用極簡的冷調灰、冰川藍與碳黑。背景使用純淨的 #F8F9FA，搭配微細的冷調線條，展現斯堪地那維亞的寧靜感。
   2. 字體與排版 (Typography)：全局導入現代感與高可讀性的英文字體 Inter 與中文字體 Noto Sans TC，字體線條簡練乾淨。
   3. 區塊設計 (Components)：
   * 標頭 (Header)：取消紙膠帶與厚重陰影，改用無邊框、精緻微陰影與左側冰川藍「現代裝飾條」的洗練洗頭。
      * 卡片與區塊 (Cards & Boxes)：卡片改為低調的極簡細邊框與柔和懸停（Hover）淡入放大效果。
      * 按鈕與標籤 (Buttons & Tabs)：按鈕與選擇標籤全面換上帶有現代感的低飽和度灰藍色系。
   
以下為 100% 完整無刪減 的 Python 程式碼，您可以直接複製並執行：

import streamlit as stimport timeimport osimport randomfrom gtts import gTTSfrom io import BytesIO
# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣", 
    page_icon="📅", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)
# --- CSS 視覺魔法 (極簡北歐冷調風) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* 全局背景：北歐極簡冷調灰底 */
    .stApp { 
        background-color: #F8F9FA;
        font-family: 'Inter', 'Noto Sans TC', sans-serif;
        color: #2D3748;
    }
    
    .block-container { padding-top: 3rem !important; padding-bottom: 5rem !important; }
    
    /* --- Header (北歐洗練風) --- */
    .header-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border-radius: 12px;
        padding: 35px 25px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }
    
    /* 左側冷調冰川藍現代裝飾條 */
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: #90CDF4;
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        color: #1A202C; 
        font-size: 42px;
        font-weight: 600;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    .sub-title { 
        color: #718096; 
        font-size: 16px; 
        margin-top: 8px; 
        font-weight: 400; 
        letter-spacing: 0.5px;
    }
    
    .teacher-tag { 
        display: inline-block; 
        margin-top: 20px; 
        padding: 4px 14px; 
        background: #EDF2F7; 
        color: #4A5568;
        border-radius: 6px; 
        font-size: 13px; 
        font-weight: 500; 
        border: 1px solid #CBD5E0;
    }
    
    /* --- Cards (冷調平板風格) --- */
    .word-card {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 24px 16px;
        text-align: center;
        border: 1px solid #E2E8F0;
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        transition: all 0.25s ease-in-out;
    }
    
    .word-card h3 {
        color: #1A202C !important;
        font-weight: 600;
        margin: 0;
        padding-bottom: 8px;
        font-size: 18px;
        letter-spacing: -0.3px;
    }
    
    .word-card:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border-color: #CBD5E0;
    }
    
    .icon-box { font-size: 28px; margin-bottom: 8px; filter: grayscale(20%); }
    .zh-word { font-size: 14px; color: #718096; font-weight: 400; }
    
    /* --- Sentences (極簡橫欄風格) --- */
    .sentence-box {
        background: #FFFFFF;
        padding: 20px 24px;
        margin-bottom: 15px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    .sentence-amis { font-size: 18px; color: #2B6CB0; font-weight: 600; margin-bottom: 6px; }
    .sentence-zh { font-size: 14px; color: #4A5568; }
    
    /* --- Buttons --- */
    .stButton>button { 
        width: 100%; 
        border-radius: 8px; 
        background: #4A5568; 
        border: 1px solid #4A5568; 
        color: #FFFFFF !important; 
        font-weight: 500; 
        font-size: 14px;
        padding: 8px 16px;
        letter-spacing: 0.5px;
        box-shadow: none;
        transition: all 0.2s;
    }
    .stButton>button:hover { background: #2D3748; border-color: #2D3748; color: #FFFFFF !important; }
    .stButton>button:active { transform: scale(0.98); background: #1A202C; }
    
    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: #EDF2F7; padding: 4px; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] {
        color: #718096 !important; 
        background-color: transparent !important;
        border-radius: 6px;
        padding: 6px 18px;
        font-size: 14px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* 修正內建水平線樣式 */
    hr { margin: 2rem 0 !important; border-color: #E2E8F0 !important; }
    </style>""", unsafe_allow_html=True)
# --- 1. 資料設定 (主題：Remiad 日子與天氣) ---VOCABULARY = [
    {"amis": "kapahay", "zh": "好的", "emoji": "👍", "file": "v_kapahay"},
    {"amis": "remiad", "zh": "日子;天氣;白天", "emoji": "📅", "file": "v_remiad"},
    {"amis": "katangasaan", "zh": "到達的時間", "emoji": "⏱️", "file": "v_katangasaan"},
    {"amis": "katangasaan tu", "zh": "到期了", "emoji": "🔴", "file": "v_katangasaan_tu"},
    {"amis": "kasuvucan", "zh": "生日", "emoji": "🎂", "file": "v_kasuvucan"},
    {"amis": "maku", "zh": "我的", "emoji": "🙋", "file": "v_maku"},
    {"amis": "anini a remiad", "zh": "今天", "emoji": "📅", "file": "v_anini_a_remiad"},
    {"amis": "saremiad sa", "zh": "整天", "emoji": "🔄", "file": "v_saremiad_sa"},
    {"amis": "maurad", "zh": "下雨", "emoji": "🌧️", "file": "v_maurad"},
    {"amis": "pataluma’en", "zh": "送(帶)回家", "emoji": "🏠", "file": "v_patalumaen"},
    {"amis": "saremiaden", "zh": "需整天", "emoji": "⏳", "file": "v_saremiaden"},
    {"amis": "pawali", "zh": "曬著", "emoji": "☀️", "file": "v_pawali"},
    {"amis": "vuduy", "zh": "衣服", "emoji": "👕", "file": "v_vuduy"},
    {"amis": "misu", "zh": "你的", "emoji": "👊", "file": "v_misu"},
    {"amis": "katawalan", "zh": "忘記", "emoji": "😫", "file": "v_katawalan"},
    {"amis": "uradan", "zh": "下雨(天)", "emoji": "☔", "file": "v_uradan"},
    {"amis": "utiih", "zh": "不方便", "emoji": "😣", "file": "v_utiih"},
    {"amis": "dademak", "zh": "做工作", "emoji": "🛠️", "file": "v_dademak"},
]
SENTENCES = [
    {"amis": "Kapahay a remiad.", "zh": "好的天氣。", "emoji": "🌤️", "file": "s_kapahay_a_remiad"},
    {"amis": "Katangasaan tu ku remiad.", "zh": "到期了。", "emoji": "🔚", "file": "s_katangasaan_tu_ku_remiad"},
    {"amis": "Kasuvucan nu maku anini a remiad.", "zh": "今天是我的生日。", "emoji": "🎂", "file": "s_kasuvucan_nu_maku"},
    {"amis": "Saremiad sa a maurad anini.", "zh": "今天整天下著雨。", "emoji": "🌧️", "file": "s_saremiad_sa_a_maurad"},
    {"amis": "Kai remiad a pataluma’en kami.", "zh": "白天送我們回家。", "emoji": "🚘", "file": "s_kai_remiad"},
    {"amis": "Saremiaden a pawali ku vuduy.", "zh": "衣服需整天曬著。", "emoji": "👕", "file": "s_saremiaden_a_pawali"},
    {"amis": "Katangasaan tu ku kasuvucan nu misu a remiad.", "zh": "你的生日到了。", "emoji": "🎉", "file": "s_katangasaan_tu_ku_kasuvucan"},
    {"amis": "Aya! Katawalan nu maku.", "zh": "哎呀! 我忘記了。", "emoji": "🤦", "file": "s_aya_katawalan"},
    {"amis": "Uradan a remiad utiih a dademak.", "zh": "下雨天工作不方便。", "emoji": "😥", "file": "s_uradan_a_remiad"},
]
# 測驗題庫QUIZ_DATA = [
    {"q": "______ a remiad / 好的天氣", "zh": "好的", "ans": "Kapahay", "opts": ["Kapahay", "Utiih", "Maurad"]},
    {"q": "______ nu maku anini / 今天是我的生日", "zh": "生日", "ans": "Kasuvucan", "opts": ["Kasuvucan", "Remiad", "Vuduy"]},
    {"q": "______ sa a maurad / 整天下雨", "zh": "整天", "ans": "Saremiad", "opts": ["Saremiad", "Anini", "Pawali"]},
    {"q": "Aya! ______ nu maku / 哎呀! 我忘記了", "zh": "忘記", "ans": "Katawalan", "opts": ["Katawalan", "Katangasaan", "Dademak"]},
    {"q": "pawali ku ______ / 曬衣服", "zh": "衣服", "ans": "vuduy", "opts": ["vuduy", "remiad", "utiih"]},
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
        st.markdown(f"<span style='color:#718096; font-size:12px; background:#EDF2F7; padding:2px 6px; border-radius:4px; border: 1px solid #E2E8F0;'> 缺音檔: {filename_base}</span>", unsafe_allow_html=True)
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
    st.markdown("<h3 style='color:#1A202C; font-weight:600; text-align:center; margin-bottom:25px; letter-spacing:-0.3px;'> 單字筆記 (Vocabulary)</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, item in enumerate(VOCABULARY):
        with cols[idx % 3]:
            # 處理括號顯示
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
st.markdown(" 例句練習 (Sentences)", unsafe_allow_html=True)
for item in SENTENCES:
st.markdown(f"""

{item['emoji']} {item['amis']}
{item['zh']}

""", unsafe_allow_html=True)
play_audio(item['amis'], filename_base=item['file'])
def show_quiz_mode():
st.markdown(" 小測驗 (Quiz)", unsafe_allow_html=True)
st.progress((st.session_state.current_q) / 3)
st.write("")
if st.session_state.current_q == 0:
data = st.session_state.q1_data
target = data['target']
st.markdown(f"""

聽聽看，這是哪個字？

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

句子填空
{data['q'].replace('___', '')}

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

這是什麼意思？
{target['amis']}

""", unsafe_allow_html=True)
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

測驗完成
您的最終得分為: {st.session_state.score} / 3

""", unsafe_allow_html=True)
if st.button("重新開始"):
init_quiz()
st.rerun()
## --- 4. 診斷工具 ---
def show_debug_info():
st.markdown("---")
files_audio = []
if os.path.exists("audio"):
files_audio = [f for f in os.listdir('audio') if f.endswith('.m4a') or f.endswith('.mp3')]
if not files_audio:
st.markdown("提示：建立 audio 資料夾並放入音檔，即可聽到發音。", unsafe_allow_html=True)
## --- 主程式 ---
def main():
st.markdown("""

Remiad
日子、天氣與白天
講師：胡美芳 | 教材提供者：胡美芳

""", unsafe_allow_html=True)
tab1, tab2 = st.tabs(["學習筆記", "小測驗"])
with tab1:
show_learning_mode()
with tab2:
show_quiz_mode()
show_debug_info()
if name == "main":
main()
