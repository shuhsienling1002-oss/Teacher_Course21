import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣", 
    page_icon="🌊", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (海洋沖浪活力風) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&family=Nunito:wght@700;900&display=swap');

    /* 全局背景：海洋漸層與波浪感 */
    .stApp {
        background-color: #E0F7FA;
        background-image: linear-gradient(180deg, #E0F7FA 0%, #B2EBF2 100%);
        font-family: 'Noto Sans TC', sans-serif;
        color: #004D40;
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }

    /* --- Header (衝浪板風格) --- */
    .header-container {
        background: linear-gradient(135deg, #00BCD4 0%, #0288D1 100%);
        border: 3px solid #FFFFFF;
        box-shadow: 0px 10px 20px rgba(0, 131, 143, 0.2);
        border-radius: 30px 30px 60px 60px; /* 模擬衝浪板圓弧 */
        padding: 30px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        color: white;
    }
    
    /* 模擬浪花裝飾 */
    .header-container::before {
        content: '〰️〰️〰️';
        position: absolute;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 20px;
        opacity: 0.6;
    }
    
    .main-title {
        font-family: 'Nunito', sans-serif;
        color: #FFFFFF;
        font-size: 46px;
        font-weight: 900;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        letter-spacing: 2px;
    }
    
    .sub-title { 
        color: #E0F7FA; 
        font-size: 20px; 
        margin-top: 8px; 
        font-weight: 500; 
    }
    
    .teacher-tag {
        display: inline-block;
        margin-top: 20px;
        padding: 8px 20px;
        background: #FFCA28; /* 陽光黃 */
        color: #5D4037;
        border-radius: 20px;
        font-size: 14px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    /* --- Cards (浮潛海洋泡泡風格) --- */
    .word-card {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 16px;
        padding: 20px 10px;
        text-align: center;
        border: 2px solid #FFFFFF;
        border-bottom: 6px solid #00ACC1; /* 底部海洋色重點 */
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,188,212,0.15);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    
    .word-card h3 {
        color: #006064 !important;
        font-weight: 700;
        margin: 0;
        padding-bottom: 5px;
        font-size: 19px;
    }

    .word-card:hover { 
        transform: translateY(-8px); 
        box-shadow: 0 12px 20px rgba(0,188,212,0.3); 
        border-bottom-color: #FFCA28; 
    }

    .icon-box { font-size: 34px; margin-bottom: 8px; }
    .zh-word { font-size: 15px; color: #607D8B; font-weight: 500; }

    /* --- Sentences (海浪波紋風格) --- */
    .sentence-box {
        background: rgba(255, 255, 255, 0.85);
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 15px;
        border-left: 5px solid #00ACC1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: background 0.2s;
    }
    .sentence-box:hover {
        background: #FFFFFF;
    }
    .sentence-amis { font-size: 19px; color: #0288D1; font-weight: 700; margin-bottom: 8px; }
    .sentence-zh { font-size: 16px; color: #455A64; }

    /* --- Buttons --- */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(to right, #26C6DA, #00ACC1);
        border: none;
        color: #FFFFFF !important;
        font-weight: bold;
        font-size: 16px;
        padding: 10px 0;
        box-shadow: 0 4px 0 #00838F;
        transition: all 0.1s;
    }
    .stButton>button:hover { background: linear-gradient(to right, #4DD0E1, #26C6DA); }
    .stButton>button:active { transform: translateY(4px); box-shadow: none; }

    /* --- Tabs --- */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        color: #006064 !important;
        background-color: transparent !important;
        border-radius: 30px;
        padding: 8px 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00BCD4 !important;
        color: #FFFFFF !important;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,188,212,0.4);
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
        
        st.markdown(f"<span style='color:#004D40; font-size:12px; background:#B2EBF2; padding:2px 5px; border-radius:4px;'>⚠️ 缺音檔: {filename_base}</span>", unsafe_allow_html=True)
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
    st.markdown("<h3 style='color:#00838F; text-align:center; margin-bottom:20px;'>🌊 單字筆記 (Vocabulary)</h3>", unsafe_allow_html=True)
    
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
    st.markdown("<h3 style='color:#00838F; text-align:center; margin-bottom:20px;'>🏄 例句練習 (Sentences)</h3>", unsafe_allow_html=True)
    
    for item in SENTENCES:
        st.markdown(f"""
        <div class="sentence-box">
            <div class="sentence-amis">{item['emoji']} {item['amis']}</div>
            <div class="sentence-zh">{item['zh']}</div>
        </div>
        """, unsafe_allow_html=True)
        play_audio(item['amis'], filename_base=item['file'])

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #006064;'>🎯 小測驗 (Quiz)</h3>", unsafe_allow_html=True)
    st.progress((st.session_state.current_q) / 3)
    st.write("")

    if st.session_state.current_q == 0:
        data = st.session_state.q1_data
        target = data['target']
        st.markdown(f"""
        <div class="word-card" style="border-bottom-color:#0288D1;">
            <h3>🎧 聽聽看，這是哪個字？</h3>
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
        <div class="word-card" style="border-bottom-color:#FFCA28;">
            <h3>🧩 句子填空</h3>
            <h2 style="color:#004D40;">{data['q'].replace('______', '<span style="color:#00ACC1; text-decoration:underline;">___</span>')}</h2>
        </div>
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
        <div class="word-card" style="border-bottom-color:#4DD0E1;">
            <h3>🤔 這是什麼意思？</h3>
            <h3 style="color:#00695C;">{target['amis']}</h3>
        </div>
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
        <div class="word-card" style="border-bottom-color: #00BCD4; background: #E0F7FA;">
            <h1 style='color: #00838F;'>測驗完成！</h1>
            <p style='color: #006064; font-size:18px;'>得分: {st.session_state.score} / 3</p>
            <div style='font-size: 60px;'>🏄‍♂️</div>
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
        st.caption("💡 提示：建立 audio 資料夾並放入音檔，即可聽到真人發音。")

# --- 主程式 ---
def main():
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">Remiad</h1>
        <div class="sub-title">日子、天氣與白天</div>
        <div class="teacher-tag">🏄 講師：胡美芳 | 教材提供者：胡美芳 🏄</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🌊 學習筆記", "🎯 小測驗"])
    
    with tab1:
        show_learning_mode()
    with tab2:
        show_quiz_mode()
        
    show_debug_info()

if __name__ == "__main__":
    main()
```
