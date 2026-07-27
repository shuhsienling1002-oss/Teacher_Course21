import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 海洋 Liyal", 
    page_icon="📜", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (天堂復古 MMORPG 風格) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@700&family=Noto+Serif+TC:wght@400;700&display=swap');

    /* 全局背景：地城暗色石板/羊皮紙氛圍 */
    .stApp { 
        background-color: #120e0a;
        background-image: radial-gradient(circle at 50% 0%, #2b1f16 0%, #0a0705 100%);
        font-family: 'Noto Serif TC', serif;
        color: #d4c4a9;
    }
    
    .block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; }

    /* --- Header (登入畫面/主標題) --- */
    .header-container {
        background: linear-gradient(to bottom, #2b1f16, #120e0a);
        border: 2px solid #8c734a;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.8), inset 0 0 20px rgba(0, 0, 0, 0.9);
        border-radius: 4px;
        padding: 30px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    .main-title {
        font-family: 'Cinzel', serif;
        color: #e6b800;
        font-size: 44px;
        font-weight: 700;
        letter-spacing: 4px;
        text-shadow: 2px 2px 4px #000, 0 0 15px #a67c00;
        margin: 0;
    }
    
    .sub-title { color: #d4c4a9; font-size: 20px; margin-top: 10px; letter-spacing: 2px; font-weight: bold; text-shadow: 1px 1px 2px #000; }
    .teacher-tag { display: inline-block; margin-top: 15px; padding: 5px 15px; border: 1px solid #8b0000; background: rgba(139, 0, 0, 0.2); color: #ff6666; border-radius: 2px; font-size: 13px; font-weight: bold; letter-spacing: 1px; }

    /* --- Cards (物品欄/技能圖示風格) --- */
    .word-card {
        background: linear-gradient(135deg, #1a1410 0%, #0a0705 100%);
        border-radius: 2px;
        padding: 20px 10px;
        text-align: center;
        border: 1px solid #5a4629;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.8), 2px 2px 5px rgba(0,0,0,0.5);
        height: 100%;
        margin-bottom: 15px;
    }
    .icon-box { font-size: 36px; margin-bottom: 10px; filter: drop-shadow(2px 2px 2px rgba(0,0,0,0.8)); }
    .amis-word { font-size: 18px; font-weight: 700; color: #e6b800; margin-bottom: 5px; font-family: 'Cinzel', serif; text-shadow: 1px 1px 2px #000; }
    .zh-word { font-size: 15px; color: #a99a80; }

    /* --- Sentences (任務卷軸風格) --- */
    .sentence-box {
        background: linear-gradient(90deg, #2a1f18 0%, #120e0a 100%);
        border: 1px solid #4a3622;
        border-left: 5px solid #8b0000;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.6);
    }
    .sentence-amis { font-size: 19px; color: #ff6666; font-weight: 700; margin-bottom: 8px; text-shadow: 1px 1px 1px #000; }
    .sentence-zh { font-size: 15px; color: #d4c4a9; }

    /* --- Buttons (復古木質/金屬按鈕) --- */
    .stButton>button { 
        width: 100%; 
        border-radius: 2px; 
        background: linear-gradient(to bottom, #4a3320, #2b1f16);
        border: 1px solid #8c734a; 
        color: #e6b800 !important; 
        font-weight: bold; 
        box-shadow: 1px 1px 3px #000;
        text-shadow: 1px 1px 1px #000;
        transition: all 0.2s;
    }
    .stButton>button:hover { 
        background: linear-gradient(to bottom, #8b0000, #4a0000); 
        color: #ffffff !important; 
        border-color: #ff3333; 
        box-shadow: 0 0 8px #ff3333;
    }

    /* --- Tab (分頁) 裝備欄/技能欄切換風格 --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        background-color: transparent;
        border-bottom: 2px solid #4a3622;
    }
    
    /* 未選中的狀態 */
    .stTabs [data-baseweb="tab"] {
        color: #8a7350 !important; 
        background-color: #1a1410 !important;
        border: 1px solid #4a3622 !important;
        border-bottom: none !important;
        border-radius: 4px 4px 0 0;
        padding: 10px 20px;
        font-weight: bold;
        opacity: 1 !important; 
    }

    /* 被選中的狀態 */
    .stTabs [aria-selected="true"] {
        background-color: #362417 !important;
        color: #e6b800 !important;
        border: 1px solid #e6b800 !important;
        border-bottom: none !important;
        box-shadow: inset 0 5px 10px rgba(230, 184, 0, 0.1);
    }
    
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    /* --- Debug Area (系統對話框頻道) --- */
    .debug-box { background: rgba(0,0,0,0.8); color: #55ff55; padding: 10px; font-family: monospace; font-size: 12px; border: 1px solid #333; margin-top: 50px; box-shadow: inset 0 0 5px #000; }
    
    /* --- Progress Bar (血條/經驗條) --- */
    .stProgress > div > div > div > div {
        background-color: #8b0000; /* 血紅色 */
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 資料設定 ---
VOCABULARY = [
    {"amis": "salawacan", "zh": "海岸", "emoji": "🏖️", "file": "v_salawacan"},
    {"amis": "kanatal",   "zh": "海島", "emoji": "🏝️", "file": "v_kanatal"},
    {"amis": "tapelik nu liyal/laying nu liyal", "zh": "海浪", "emoji": "🌊", "file": "v_tapelik"},
    {"amis": "cunami",    "zh": "海嘯", "emoji": "🌊🌪️", "file": "v_cunami"},
    {"amis": "rariyaran", "zh": "海上", "emoji": "🚢", "file": "v_rariyaran"},
]

SENTENCES = [
    {
        "amis": "Iraay ku valiyus, matungalay ku tapelik tu salawacan nu liyal.", 
        "zh": "有颱風，沿海地區的浪變高了。", 
        "emoji": "🌀", 
        "file": "s_valiyus"
    },
    {
        "amis": "Cacay ofad ku kasakanatal nu Ripun.", 
        "zh": "日本有一萬多個海島。", 
        "emoji": "🇯🇵", 
        "file": "s_ripun"
    },
    {
        "amis": "I rariyaran adihayay ku lunan a mivuting.", 
        "zh": "在海上有很多漁船捕魚。", 
        "emoji": "🛥️", 
        "file": "s_lunan"
    },
]

QUIZ_DATA = [
    {"q": "Iraay ku valiyus, matungalay ku ______ tu salawacan nu liyal.", "zh": "有颱風，沿海地區的浪變高了", "ans": "tapelik", "opts": ["tapelik", "kanatal", "cunami"]},
    {"q": "______ / 海嘯", "zh": "海嘯", "ans": "cunami", "opts": ["cunami", "salawacan", "rariyaran"]},
    {"q": "I ______ adihayay ku lunan a mivuting.", "zh": "在海上有很多漁船捕魚", "ans": "rariyaran", "opts": ["rariyaran", "kanatal", "salawacan"]},
    {"q": "______ / 海島", "zh": "海島", "ans": "kanatal", "opts": ["kanatal", "tapelik", "cunami"]},
    {"q": "______ / 海岸", "zh": "海岸", "ans": "salawacan", "opts": ["salawacan", "rariyaran", "kanatal"]},
]

# --- 1.5 強力語音核心 (診斷版) ---
def play_audio(text, filename_base=None):
    if filename_base:
        for ext in ['m4a', 'mp3', 'ma4', 'wav']: 
            path = f"audio/{filename_base}.{ext}"
            if os.path.exists(path):
                mime = 'audio/mp4' if ext in ['m4a', 'ma4'] else 'audio/mp3'
                st.audio(path, format=mime)
                return
        st.markdown(f"<span style='color:#ff3333; font-size:12px;'>⚠️ 系統提示：找不到音效檔案 {filename_base}.m4a</span>", unsafe_allow_html=True)

    try:
        speak_text = text.split('/')[0].strip()
        tts = gTTS(text=speak_text, lang='id') 
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    except:
        st.caption("🔇 (音效系統未命中)")

# --- 2. 隨機出題邏輯 ---
def init_quiz():
    st.session_state.score = 0
    st.session_state.current_q = 0
    
    q1_target = random.choice(VOCABULARY)
    others = [v for v in VOCABULARY if v['amis'] != q1_target['amis']]
    q1_options = random.sample(others, 2) + [q1_target]
    random.shuffle(q1_options)
    st.session_state.q1_data = {"target": q1_target, "options": q1_options}

    q2_data = random.choice(QUIZ_DATA)
    random.shuffle(q2_data['opts'])
    st.session_state.q2_data = q2_data

    q3_target = random.choice(SENTENCES)
    other_sentences = [s['zh'] for s in SENTENCES if s['zh'] != q3_target['zh']]
    if len(other_sentences) < 2:
        q3_options = other_sentences + [q3_target['zh']]
    else:
        q3_options = random.sample(other_sentences, 2) + [q3_target['zh']]
    random.shuffle(q3_options)
    st.session_state.q3_data = {"target": q3_target, "options": q3_options}

if 'q1_data' not in st.session_state:
    init_quiz()

# --- 3. 介面呈現 ---
def show_learning_mode():
    st.markdown("<h3 style='color:#e6b800; text-align:center; margin-bottom:20px; font-family:\"Cinzel\", serif;'>📖 魔法書：單字記憶</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, item in enumerate(VOCABULARY):
        with cols[idx % 3]:
            display_amis = item['amis'].replace(" nu ", "<br>nu ")
            st.markdown(f"""
            <div class="word-card">
                <div class="icon-box">{item['emoji']}</div>
                <div class="amis-word">{display_amis}</div>
                <div class="zh-word">{item['zh']}</div>
            </div>
            """, unsafe_allow_html=True)
            play_audio(item['amis'], filename_base=item['file'])
            st.write("")

    st.markdown("<hr style='border-top: 1px solid #4a3622;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#e6b800; text-align:center; margin-bottom:20px; font-family:\"Cinzel\", serif;'>📜 任務卷軸：語法研習</h3>", unsafe_allow_html=True)
    
    for item in SENTENCES:
        st.markdown(f"""
        <div class="sentence-box">
            <div class="sentence-amis">{item['emoji']} {item['amis']}</div>
            <div class="sentence-zh">{item['zh']}</div>
        </div>
        """, unsafe_allow_html=True)
        play_audio(item['amis'], filename_base=item['file'])

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #b30000; font-family:\"Cinzel\", serif;'>⚔️ 挑戰任務：知識檢定</h3>", unsafe_allow_html=True)
    st.progress((st.session_state.current_q) / 3)
    st.write("")

    if st.session_state.current_q == 0:
        data = st.session_state.q1_data
        target = data['target']
        st.markdown(f"""<div class="quiz-card" style="background:#1a0a0a; text-align:center; padding:20px; border:1px solid #8b0000; box-shadow: 0 0 10px rgba(139,0,0,0.5); border-radius:2px;">
            <h3 style="color:#e6b800;">🔊 魔法詠唱辨識 (聽力)</h3>
        </div>""", unsafe_allow_html=True)
        play_audio(target['amis'], filename_base=target['file'])
        st.write("")
        
        cols = st.columns(3)
        for idx, opt in enumerate(data['options']):
            with cols[idx]:
                if st.button(f"{opt['zh']}", key=f"q1_{idx}"):
                    if opt['amis'] == target['amis']:
                        st.balloons()
                        st.success("詠唱確認成功！")
                        time.sleep(1)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error("詠唱錯誤，受到反噬！")

    elif st.session_state.current_q == 1:
        data = st.session_state.q2_data
        st.markdown(f"""
        <div class="quiz-card" style="background:#1a0a0a; text-align:center; padding:20px; border:1px solid #8b0000; box-shadow: 0 0 10px rgba(139,0,0,0.5); border-radius:2px;">
            <h3 style="color:#e6b800;">🧩 殘缺的石板 (填空)</h3>
            <h2 style="color:#ff6666;">{data['q'].replace('______', '___?___')}</h2>
            <p style="color:#d4c4a9;">{data['zh']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, opt in enumerate(data['opts']):
            with cols[i]:
                if st.button(opt, key=f"q2_{i}"):
                    if opt == data['ans']:
                        st.balloons()
                        st.success("石板修復完成！")
                        time.sleep(1)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error("符文不吻合！")

    elif st.session_state.current_q == 2:
        data = st.session_state.q3_data
        target = data['target']
        st.markdown(f"""
        <div class="quiz-card" style="background:#1a0a0a; text-align:center; padding:20px; border:1px solid #8b0000; box-shadow: 0 0 10px rgba(139,0,0,0.5); border-radius:2px;">
            <h3 style="color:#e6b800;">📡 古老密語解碼 (句意解析)</h3>
            <h2 style="color:#ff6666;">{target['amis']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        play_audio(target['amis'], filename_base=target['file'])
        
        for opt in data['options']:
            if st.button(opt):
                if opt == target['zh']:
                    st.balloons()
                    st.success("解碼成功，獲得經驗值！")
                    time.sleep(1)
                    st.session_state.score += 1
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.error("解碼失敗！")

    else:
        st.markdown(f"""
        <div class="quiz-card" style="background:#1a0a0a; text-align:center; padding:30px; border:2px solid #e6b800; box-shadow: 0 0 20px rgba(230,184,0,0.4); border-radius:2px;">
            <h1 style='color: #e6b800; font-family:"Cinzel", serif;'>任務全數完成</h1>
            <p style='font-size: 20px; color: #d4c4a9;'>目前經驗積分: {st.session_state.score} / 3</p>
            <div style='font-size: 60px; margin: 20px 0;'>🏆</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 重新挑戰地城"):
            init_quiz()
            st.rerun()

# --- 4. 診斷工具 (系統對話框) ---
def show_debug_info():
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='debug-box'>", unsafe_allow_html=True)
    st.markdown(">[系統訊息] 正在掃描地城資源檔案...")
    
    if not os.path.exists("audio"):
        st.markdown("<span style='color:#ff3333;'>[系統錯誤] 找不到 'audio' 資源目錄，請回報 GM！</span>", unsafe_allow_html=True)
    else:
        files = os.listdir("audio")
        if not files:
            st.markdown("<span style='color:#ffcc00;'>[系統警告] audio 資源目錄為空！</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:#55ff55;'>[系統提示] audio 資源目錄載入成功，共 {len(files)} 個檔案。</span>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- 主程式 ---
def main():
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">O LIYAL</h1>
        <div class="sub-title">海洋之歌</div>
        <div class="teacher-tag">大賢者：孫秀蘭 | 卷軸提供者：孫秀蘭</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🛡️ 海洋筆記", "⚔️ 挑戰任務"])
    
    with tab1:
        show_learning_mode()
    with tab2:
        show_quiz_mode()
        
    show_debug_info()

if __name__ == "__main__":
    main()
