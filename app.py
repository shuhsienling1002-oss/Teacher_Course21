import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣", 
    page_icon="👾", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (復古 8 位元像素風) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DotGothic16&family=Press+Start+2P&display=swap');

    /* 全局背景：復古掃描線與深色街機背景 */
    .stApp {
        background-color: #000000;
        background-image: repeating-linear-gradient(0deg, #111, #111 2px, #000 2px, #000 4px);
        font-family: 'DotGothic16', monospace, sans-serif;
        color: #FFFFFF;
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }

    /* --- Header (遊戲標題畫面風格) --- */
    .header-container {
        background-color: #0000AA;
        border: 4px solid #FFFFFF;
        box-shadow: 6px 6px 0px #FF0055;
        padding: 30px;
        text-align: center;
        margin-bottom: 40px;
        image-rendering: pixelated;
    }
    
    .main-title {
        font-family: 'Press Start 2P', cursive;
        color: #FFFF00;
        font-size: 32px;
        text-shadow: 4px 4px 0 #000000;
        margin: 0;
        line-height: 1.5;
    }
    
    .sub-title { 
        color: #55FFFF; 
        font-size: 20px; 
        margin-top: 15px; 
        text-shadow: 2px 2px 0 #000000;
    }
    
    .teacher-tag {
        display: inline-block;
        margin-top: 20px;
        padding: 8px 15px;
        background: #AA0000;
        color: #FFFFFF;
        border: 2px solid #FFFFFF;
        box-shadow: 2px 2px 0 #000000;
        font-size: 16px;
    }

    /* --- Cards (遊戲選單方塊風格) --- */
    .word-card {
        background: #0000AA;
        border: 4px solid #FFFFFF;
        padding: 20px 10px;
        text-align: center;
        box-shadow: 4px 4px 0 #0055FF;
        height: 100%;
        margin-bottom: 15px;
        border-radius: 0;
        transition: transform 0.1s;
    }
    
    .word-card h3 {
        color: #FFFF00 !important;
        font-family: 'DotGothic16', monospace;
        font-weight: 700;
        margin: 0;
        padding-bottom: 5px;
        font-size: 22px;
        text-shadow: 2px 2px 0 #000000;
    }

    .word-card:hover { 
        transform: translate(-2px, -2px); 
        box-shadow: 6px 6px 0 #55FFFF; 
    }

    .icon-box { font-size: 34px; margin-bottom: 8px; image-rendering: pixelated; }
    .zh-word { font-size: 16px; color: #DDDDDD; }

    /* --- Sentences (對話框風格) --- */
    .sentence-box {
        background: #222222;
        padding: 20px;
        margin-bottom: 15px;
        border: 4px solid #555555;
        box-shadow: 4px 4px 0 #000000;
        border-radius: 0;
    }
    .sentence-box:hover {
        border-color: #55FF55;
    }
    .sentence-amis { 
        font-size: 20px; 
        color: #55FF55; 
        font-weight: bold; 
        margin-bottom: 8px; 
        text-shadow: 2px 2px 0 #000000;
    }
    .sentence-zh { font-size: 16px; color: #BBBBBB; }

    /* --- Buttons (大型機台按鈕) --- */
    .stButton>button {
        width: 100%;
        background-color: #AA0000;
        border: 4px solid #FFFFFF;
        color: #FFFFFF !important;
        font-family: 'DotGothic16', monospace;
        font-size: 18px;
        font-weight: bold;
        padding: 10px 0;
        box-shadow: 4px 4px 0 #FF0055;
        border-radius: 0;
        transition: none;
    }
    .stButton>button:hover { 
        background-color: #FF0055; 
        box-shadow: 4px 4px 0 #FFFFFF; 
    }
    .stButton>button:active { 
        transform: translate(4px, 4px); 
        box-shadow: none; 
    }

    /* --- Tabs (遊戲選單標籤) --- */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        color: #AAAAAA !important;
        background-color: transparent !important;
        border: 2px solid transparent;
        border-radius: 0;
        padding: 8px 20px;
        font-family: 'DotGothic16', monospace;
        font-size: 18px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0000AA !important;
        color: #FFFF00 !important;
        border: 4px solid #FFFFFF;
        box-shadow: 4px 4px 0 #000000;
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
        
        st.markdown(f"<span style='color:#FFFFFF; font-size:12px; background:#AA0000; padding:2px 5px; border:2px solid #FFF; box-shadow:2px 2px 0 #000;'>⚠️ 缺音檔: {filename_base}</span>", unsafe_allow_html=True)
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
    st.markdown("<h3 style='color:#55FF55; text-align:center; margin-bottom:20px; text-shadow:2px 2px 0 #000;'>👾 單字筆記 (Vocabulary)</h3>", unsafe_allow_html=True)
    
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
    st.markdown("<h3 style='color:#55FF55; text-align:center; margin-bottom:20px; text-shadow:2px 2px 0 #000;'>💬 例句練習 (Sentences)</h3>", unsafe_allow_html=True)
    
    for item in SENTENCES:
        st.markdown(f"""
        <div class="sentence-box">
            <div class="sentence-amis">{item['emoji']} {item['amis']}</div>
            <div class="sentence-zh">{item['zh']}</div>
        </div>
        """, unsafe_allow_html=True)
        play_audio(item['amis'], filename_base=item['file'])

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #FFFF00; text-shadow:2px 2px 0 #000;'>🎮 小測驗 (Quiz)</h3>", unsafe_allow_html=True)
    st.progress((st.session_state.current_q) / 3)
    st.write("")

    if st.session_state.current_q == 0:
        data = st.session_state.q1_data
        target = data['target']
        st.markdown(f"""
        <div class="word-card" style="border-color:#55FF55; box-shadow:4px 4px 0 #00AA00;">
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
                        st.success("STAGE CLEAR! 答對了！")
                        time.sleep(1)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error("MISS! 再試一次")

    elif st.session_state.current_q == 1:
        data = st.session_state.q2_data
        st.markdown(f"""
        <div class="word-card" style="border-color:#FF0055; box-shadow:4px 4px 0 #AA0000;">
            <h3>🧩 句子填空</h3>
            <h2 style="color:#FFFFFF; margin-top:15px; font-weight:400;">{data['q'].replace('______', '<span style="color:#FFFF00; border-bottom:4px solid #FFFF00;">___</span>')}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, opt in enumerate(data['opts']):
            with cols[i]:
                if st.button(opt, key=f"q2_{i}"):
                    if opt.lower() in data['ans'].lower() or data['ans'].lower() in opt.lower():
                        st.balloons()
                        st.success("LEVEL UP! 太棒了！")
                        time.sleep(1)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error("GAME OVER! 不對喔")

    elif st.session_state.current_q == 2:
        data = st.session_state.q3_data
        target = data['target']
        st.markdown(f"""
        <div class="word-card" style="border-color:#55FFFF; box-shadow:4px 4px 0 #0000AA;">
            <h3>🤔 這是什麼意思？</h3>
            <h3 style="color:#FFFFFF; margin-top:15px; font-weight:500;">{target['amis']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        play_audio(target['amis'], filename_base=target['file'])
        
        for opt in data['options']:
            if st.button(opt):
                if opt == target['zh']:
                    st.balloons()
                    st.success("YOU WIN! 全對！")
                    time.sleep(1)
                    st.session_state.score += 1
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.error("TRY AGAIN! 再想一下")

    else:
        st.markdown(f"""
        <div class="word-card" style="background: #222222; border-color: #FFFF00; box-shadow:4px 4px 0 #000000;">
            <h1 style='color: #FF0055; text-shadow:4px 4px 0 #FFFFFF;'>MISSION COMPLETE!</h1>
            <p style='color: #55FF55; font-size:24px; font-weight:bold;'>SCORE: {st.session_state.score} / 3</p>
            <div style='font-size: 60px; margin-top: 15px;'>🏆</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("INSERT COIN (重新開始)"):
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
        <h1 class="main-title">REMIAD</h1>
        <div class="sub-title">日子、天氣與白天</div>
        <div class="teacher-tag">PLAYER 1: 胡美芳 | MAP MAKER: 胡美芳</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["START 學習", "VS 測驗"])
    
    with tab1:
        show_learning_mode()
    with tab2:
        show_quiz_mode()
        
    show_debug_info()

if __name__ == "__main__":
    main()
