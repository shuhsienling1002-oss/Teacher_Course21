import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣", 
    page_icon="❄️", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (極簡北歐冷調風) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&family=Noto+Sans+TC:wght@300;400;500&display=swap');

    /* 全局背景：冷灰白質感 */
    .stApp {
        background-color: #F4F6F9;
        font-family: 'Inter', 'Noto Sans TC', sans-serif;
        color: #2E3440;
    }
    
    .block-container { padding-top: 3rem !important; padding-bottom: 5rem !important; }

    /* --- Header (極簡質感) --- */
    .header-container {
        background: #FFFFFF;
        border: 1px solid #E5E9F0;
        border-radius: 8px;
        padding: 40px 30px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
    }
    
    .main-title {
        font-family: 'Inter', sans-serif;
        color: #3B4252;
        font-size: 42px;
        font-weight: 300;
        letter-spacing: 6px;
        margin: 0;
        text-transform: uppercase;
    }
    
    .sub-title { 
        color: #4C566A; 
        font-size: 16px; 
        margin-top: 12px; 
        font-weight: 400; 
        letter-spacing: 2px;
    }
    
    .teacher-tag {
        display: inline-block;
        margin-top: 25px;
        padding: 6px 16px;
        background: transparent;
        color: #5E81AC;
        border: 1px solid #5E81AC;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 1px;
    }

    /* --- Cards (冷調方正卡片) --- */
    .word-card {
        background: #FFFFFF;
        border-radius: 6px;
        padding: 25px 15px;
        text-align: center;
        border: 1px solid #ECEFF4;
        border-top: 4px solid #81A1C1;
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .word-card h3 {
        color: #2E3440 !important;
        font-weight: 600;
        margin: 0;
        padding-bottom: 8px;
        font-size: 18px;
        letter-spacing: 1px;
    }

    .word-card:hover { 
        transform: translateY(-3px); 
        box-shadow: 0 8px 16px rgba(0,0,0,0.06); 
        border-top-color: #5E81AC; 
    }

    .icon-box { font-size: 28px; margin-bottom: 12px; filter: grayscale(30%); }
    .zh-word { font-size: 14px; color: #4C566A; font-weight: 400; }

    /* --- Sentences (冷冽線條) --- */
    .sentence-box {
        background: #FFFFFF;
        padding: 24px;
        margin-bottom: 16px;
        border-radius: 6px;
        border: 1px solid #ECEFF4;
        border-left: 4px solid #88C0D0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
        transition: border-left-color 0.3s ease;
    }
    .sentence-box:hover {
        border-left-color: #5E81AC;
    }
    .sentence-amis { font-size: 18px; color: #3B4252; font-weight: 600; margin-bottom: 8px; }
    .sentence-zh { font-size: 15px; color: #4C566A; }

    /* --- Buttons (扁平化) --- */
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        background-color: #ECEFF4;
        border: 1px solid #D8DEE9;
        color: #4C566A !important;
        font-weight: 500;
        font-size: 15px;
        padding: 8px 0;
        transition: all 0.2s ease;
        box-shadow: none;
    }
    .stButton>button:hover { 
        background-color: #5E81AC; 
        color: #FFFFFF !important;
        border-color: #5E81AC;
    }
    .stButton>button:active { transform: translateY(1px); }

    /* --- Tabs (無邊框底線設計) --- */
    .stTabs [data-baseweb="tab-list"] { gap: 30px; justify-content: center; border-bottom: 1px solid #E5E9F0; }
    .stTabs [data-baseweb="tab"] {
        color: #4C566A !important;
        background-color: transparent !important;
        border-radius: 0;
        padding: 10px 5px;
        font-weight: 400;
        letter-spacing: 1px;
    }
    .stTabs [aria-selected="true"] {
        color: #2E3440 !important;
        font-weight: 600;
        border-bottom: 2px solid #4C566A;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 資料設定 (主題：Remiad 日子與天氣) ---
VOCABULARY = [
    {"amis": "kapahay",       "zh": "好的",           "emoji": "👍", "file": "v_kapahay"},
    {"amis": "remiad",        "zh": "日子;天氣;白天",  "emoji": "🗓️", "file": "v_remiad"},
    {"amis": "katangasaan",   "zh": "到達的時間",      "emoji": "🕛", "file": "v_katangasaan"},
    {"amis": "katangasaan tu","zh": "到期了",         "emoji": "🛑", "file": "v_katangasaan_tu"},
    {"amis": "kasuvucan",     "zh": "生日",           "emoji": "🎂", "file": "v_kasuvucan"},
    {"amis": "maku",          "zh": "我的",           "emoji": "🙋", "file": "v_maku"},
    {"amis": "anini a remiad","zh": "今天",           "emoji": "📅", "file": "v_anini_a_remiad"},
    {"amis": "saremiad sa",   "zh": "整天",           "emoji": "🔄", "file": "v_saremiad_sa"},
    {"amis": "maurad",        "zh": "下雨",           "emoji": "🌧️", "file": "v_maurad"},
    {"amis": "pataluma’en",   "zh": "送(帶)回家",      "emoji": "🏠", "file": "v_patalumaen"},
    {"amis": "saremiaden",    "zh": "需整天",         "emoji": "⏳", "file": "v_saremiaden"},
    {"amis": "pawali",        "zh": "曬著",           "emoji": "🌕", "file": "v_pawali"},
    {"amis": "vuduy",         "zh": "衣服",           "emoji": "👕", "file": "v_vuduy"},
    {"amis": "misu",          "zh": "你的",           "emoji": "👉", "file": "v_misu"},
    {"amis": "katawalan",     "zh": "忘記",           "emoji": "😫", "file": "v_katawalan"},
    {"amis": "uradan",        "zh": "下雨(天)",       "emoji": "☔", "file": "v_uradan"},
    {"amis": "utiih",         "zh": "不方便",         "emoji": "😞", "file": "v_utiih"},
    {"amis": "dademak",       "zh": "做工作",         "emoji": "🛠️", "file": "v_dademak"},
]

SENTENCES = [
    {"amis": "Kapahay a remiad.",       "zh": "好的天氣。",       "emoji": "🌤️", "file": "s_kapahay_a_remiad"},      
    {"amis": "Katangasaan tu ku remiad.",       "zh": "到期了。",       "emoji": "🔚", "file": "s_katangasaan_tu_ku_remiad"},      
    {"amis": "Kasuvucan nu maku anini a remiad.",       "zh": "今天是我的生日。",       "emoji": "🎂", "file": "s_kasuvucan_nu_maku"},      
    {"amis": "Saremiad sa a maurad anini.",       "zh": "今天整天下著雨。",       "emoji": "🌧️", "file": "s_saremiad_sa_a_maurad"},      
    {"amis": "Kai remiad a pataluma’en kami.",       "zh": "白天送我們回家。",       "emoji": "🚗", "file": "s_kai_remiad"},      
    {"amis": "Saremiaden a pawali ku vuduy.",       "zh": "衣服需整天曬著。",       "emoji": "👕", "file": "s_saremiaden_a_pawali"},      
    {"amis": "Katangasaan tu ku kasuvucan nu misu a remiad.",       "zh": "你的生日到了。",       "emoji": "🎉", "file": "s_katangasaan_tu_ku_kasuvucan"},      
    {"amis": "Aya! Katawalan nu maku.",       "zh": "哎呀! 我忘記了。",       "emoji": "🤦", "file": "s_aya_katawalan"},      
    {"amis": "Uradan a remiad utiih a dademak.",       "zh": "下雨天工作不方便。",       "emoji": "☔", "file": "s_uradan_a_remiad"},
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
        
        st.markdown(f"<span style='color:#3B4252; font-size:12px; background:#ECEFF4; padding:2px 5px; border-radius:4px;'>⚠️ 缺音檔: {filename_base}</span>", unsafe_allow_html=True)
    else:
        try:
            speak_text = text.split('/').strip()
            tts = gTTS(text=speak_text, lang='id')
            
            fp = BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')
        except:
            st.caption("🔇")

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
    st.markdown("<h3 style='color:#4C566A; text-align:center; font-weight:300; letter-spacing:2px; margin-bottom:30px;'>▫️ 單字筆記 (Vocabulary) ▫️</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, item in enumerate(VOCABULARY):
        with cols[idx % 3]:
            # 處理括號顯示
            display_amis = item['amis']
            if "kasuvucan" in display_amis:
                display_amis = "kasuvucan<br><span style='font-size:12px'>(kasubucan)</span>"
            if "vuduy" in display_amis:
                display_amis = "vuduy<br><span style='font-size:12px'>(buduy)</span>"

            st.markdown(f"""
            <div class="word-card">
                <div class="icon-box">{item['emoji']}</div>
                <h3>{display_amis}</h3>
                <div class="zh-word">{item['zh']}</div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(item['amis'], filename_base=item['file'])
            st.write("")
            
    st.markdown("---")
    st.markdown("<h3 style='color:#4C566A; text-align:center; font-weight:300; letter-spacing:2px; margin-bottom:30px;'>▫️ 例句練習 (Sentences) ▫️</h3>", unsafe_allow_html=True)
    
    for item in SENTENCES:
        st.markdown(f"""
        <div class="sentence-box">
            <div class="sentence-amis">{item['emoji']} {item['amis']}</div>
            <div class="sentence-zh">{item['zh']}</div>
        </div>
        """, unsafe_allow_html=True)
        play_audio(item['amis'], filename_base=item['file'])

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #4C566A; font-weight:300; letter-spacing:2px; margin-bottom:20px;'>▫️ 測驗評量 (Quiz) ▫️</h3>", unsafe_allow_html=True)
    st.progress((st.session_state.current_q) / 3)
    st.write("")

    if st.session_state.current_q == 0:
        data = st.session_state.q1_data
        target = data['target']
        st.markdown(f"""
        <div class="word-card" style="border-top-color:#88C0D0;">
            <h3 style="color:#3B4252;">聽力測驗</h3>
            <p style="color:#4C566A; font-size:14px;">請聆聽語音並選擇對應的中文</p>
        </div>
        """, unsafe_allow_html=True)
        play_audio(target['amis'], filename_base=target['file'])
        st.write("")
        
        cols = st.columns(3)
        for idx, opt in enumerate(data['options']):
            with cols[idx]:
                if st.button(f"{opt['zh']}", key=f"q1_{idx}"):
                    if opt['amis'] == target['amis']:
                        st.balloons()
                        st.success("正確 (Correct)")
                        time.sleep(1)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error("請再試一次")

    elif st.session_state.current_q == 1:
        data = st.session_state.q2_data
        st.markdown(f"""
        <div class="word-card" style="border-top-color:#81A1C1;">
            <h3 style="color:#3B4252;">句子填空</h3>
            <h2 style="color:#2E3440; margin-top:15px; font-weight:400;">{data['q'].replace('______', '<span style="color:#5E81AC; text-decoration:underline;">___</span>')}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, opt in enumerate(data['opts']):
            with cols[i]:
                if st.button(opt, key=f"q2_{i}"):
                    if opt.lower() in data['ans'].lower() or data['ans'].lower() in opt.lower():
                        st.balloons()
                        st.success("正確 (Correct)")
                        time.sleep(1)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error("請再試一次")

    elif st.session_state.current_q == 2:
        data = st.session_state.q3_data
        target = data['target']
        st.markdown(f"""
        <div class="word-card" style="border-top-color:#5E81AC;">
            <h3 style="color:#3B4252;">句意翻譯</h3>
            <h3 style="color:#2E3440; margin-top:15px; font-weight:500;">{target['amis']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        play_audio(target['amis'], filename_base=target['file'])
        
        for opt in data['options']:
            if st.button(opt):
                if opt == target['zh']:
                    st.balloons()
                    st.success("完全正確 (Perfect)")
                    time.sleep(1)
                    st.session_state.score += 1
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.error("請再想一下")

    else:
        st.markdown(f"""
        <div class="word-card" style="border-top-color: #4C566A; background: #ECEFF4;">
            <h1 style='color: #2E3440; font-weight:300; letter-spacing:2px;'>測驗完成</h1>
            <p style='color: #4C566A; font-size:18px;'>得分: {st.session_state.score} / 3</p>
            <div style='font-size: 40px; filter: grayscale(100%); margin-top: 15px;'>🧊</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("重新開始"):
            init_quiz()
            st.rerun()

# --- 4. 診斷工具 ---
def show_debug_info():
    st.markdown("---")
    files_audio = []
    if os.path.exists("audio"):
        files_audio = [f for f in os.listdir('audio') if f.endswith('.m4a') or f.endswith('.mp3')]
        
    if not files_audio:
        st.caption("提示：建立 audio 資料夾並放入音檔，即可聽到真人發音。")

# --- 主程式 ---
def main():
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">Remiad</h1>
        <div class="sub-title">日子、天氣與白天</div>
        <div class="teacher-tag">講師：胡美芳 | 教材提供者：胡美芳</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["單字與例句", "評量測驗"])
    
    with tab1:
        show_learning_mode()
    with tab2:
        show_quiz_mode()
        
    show_debug_info()

if __name__ == "__main__":
    main()
