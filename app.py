import streamlit as st
import time
import os
import random
from gtts import gTTS
from io import BytesIO

# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣", 
    page_icon="🌃", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- CSS 視覺魔法 (賽博龐克霓虹風) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Noto+Sans+TC:wght@400;700&display=swap');

    /* 全局背景：暗黑科技網格 */
    .stApp {
        background-color: #090A0F;
        background-image: 
            linear-gradient(rgba(8, 247, 254, 0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(8, 247, 254, 0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        font-family: 'Noto Sans TC', sans-serif;
        color: #E0E0E0;
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }

    /* --- Header (霓虹招牌風格) --- */
    .header-container {
        background: linear-gradient(135deg, #111116 0%, #1A1A24 100%);
        border: 2px solid #08F7FE;
        box-shadow: 0 0 15px rgba(8, 247, 254, 0.4), inset 0 0 10px rgba(8, 247, 254, 0.2);
        padding: 30px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    /* 賽博龐克裝飾條 */
    .header-container::after {
        content: '';
        position: absolute;
        bottom: -2px;
        right: 20px;
        width: 80px;
        height: 4px;
        background: #FE53BB;
        box-shadow: 0 0 10px #FE53BB;
    }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #FE53BB;
        font-size: 46px;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 10px #FE53BB, 0 0 20px #FE53BB;
        letter-spacing: 4px;
        text-transform: uppercase;
    }
    
    .sub-title { 
        color: #08F7FE; 
        font-size: 20px; 
        margin-top: 10px; 
        font-weight: 700; 
        text-shadow: 0 0 8px rgba(8, 247, 254, 0.8);
        letter-spacing: 2px;
    }
    
    .teacher-tag {
        display: inline-block;
        margin-top: 20px;
        padding: 6px 18px;
        background: #090A0F;
        color: #F5D300;
        border: 1px solid #F5D300;
        box-shadow: 0 0 8px rgba(245, 211, 0, 0.6);
        font-size: 14px;
        font-weight: bold;
        font-family: 'Orbitron', 'Noto Sans TC', sans-serif;
    }

    /* --- Cards (全息投影面板風格) --- */
    .word-card {
        background: rgba(15, 15, 25, 0.85);
        border: 1px solid #2A2A35;
        border-left: 4px solid #08F7FE;
        padding: 20px 10px;
        text-align: center;
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.6);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        backdrop-filter: blur(4px);
    }
    
    .word-card h3 {
        color: #08F7FE !important;
        font-weight: 700;
        margin: 0;
        padding-bottom: 5px;
        font-size: 19px;
        text-shadow: 0 0 5px rgba(8, 247, 254, 0.5);
    }

    .word-card:hover { 
        transform: translateY(-5px); 
        border-left-color: #FE53BB;
        box-shadow: 0 0 20px rgba(254, 83, 187, 0.4); 
    }

    .icon-box { font-size: 34px; margin-bottom: 8px; filter: drop-shadow(0 0 8px rgba(255,255,255,0.3)); }
    .zh-word { font-size: 15px; color: #A0AAB5; font-weight: 500; }

    /* --- Sentences (數位數據列風格) --- */
    .sentence-box {
        background: rgba(20, 20, 30, 0.8);
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #2A2A35;
        border-right: 4px solid #F5D300;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        transition: all 0.3s;
    }
    .sentence-box:hover {
        border-color: #F5D300;
        box-shadow: 0 0 15px rgba(245, 211, 0, 0.3);
    }
    .sentence-amis { 
        font-size: 19px; 
        color: #FE53BB; 
        font-weight: 700; 
        margin-bottom: 8px; 
        text-shadow: 0 0 6px rgba(254, 83, 187, 0.6);
    }
    .sentence-zh { font-size: 16px; color: #B0BEC5; }

    /* --- Buttons (高科技控制終端) --- */
    .stButton>button {
        width: 100%;
        background-color: rgba(8, 247, 254, 0.05);
        border: 2px solid #08F7FE;
        color: #08F7FE !important;
        font-weight: bold;
        font-family: 'Orbitron', 'Noto Sans TC', sans-serif;
        font-size: 16px;
        padding: 10px 0;
        box-shadow: 0 0 10px rgba(8, 247, 254, 0.3), inset 0 0 5px rgba(8, 247, 254, 0.2);
        transition: all 0.2s;
        text-transform: uppercase;
        border-radius: 0;
    }
    .stButton>button:hover { 
        background-color: #08F7FE; 
        color: #090A0F !important;
        box-shadow: 0 0 20px #08F7FE; 
    }
    .stButton>button:active { transform: scale(0.98); }

    /* --- Tabs (電路板連線設計) --- */
    .stTabs [data-baseweb="tab-list"] { gap: 15px; justify-content: center; border-bottom: 1px solid #333; }
    .stTabs [data-baseweb="tab"] {
        color: #556677 !important;
        background-color: transparent !important;
        padding: 12px 20px;
        font-weight: 700;
        font-family: 'Orbitron', 'Noto Sans TC', sans-serif;
        border-radius: 0;
    }
    .stTabs [aria-selected="true"] {
        color: #F5D300 !important;
        border-bottom: 3px solid #F5D300;
        text-shadow: 0 0 10px rgba(245, 211, 0, 0.8);
        background-color: transparent !important;
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
        
        st.markdown(f"<span style='color:#090A0F; font-size:12px; background:#F5D300; padding:2px 5px; border-radius:4px; font-weight:bold;'>⚠️ 缺音檔: {filename_base}</span>", unsafe_allow_html=True)
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
    st.markdown("<h3 style='color:#08F7FE; text-shadow: 0 0 10px #08F7FE; text-align:center; margin-bottom:20px; font-family:Orbitron;'>⚡ 核心數據庫 (Vocabulary)</h3>", unsafe_allow_html=True)
    
    cols = st.columns(3)
    for idx, item in enumerate(VOCABULARY):
        with cols[idx % 3]:
            # 處理括號顯示
            display_amis = item['amis']
            if "kasuvucan" in display_amis:
                display_amis = "kasuvucan<br><span style='font-size:12px; color:#A0AAB5;'>(kasubucan)</span>"
            if "vuduy" in display_amis:
                display_amis = "vuduy<br><span style='font-size:12px; color:#A0AAB5;'>(buduy)</span>"

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
    st.markdown("<h3 style='color:#08F7FE; text-shadow: 0 0 10px #08F7FE; text-align:center; margin-bottom:20px; font-family:Orbitron;'>📡 頻率載波 (Sentences)</h3>", unsafe_allow_html=True)
    
    for item in SENTENCES:
        st.markdown(f"""
        <div class="sentence-box">
            <div class="sentence-amis">{item['emoji']} {item['amis']}</div>
            <div class="sentence-zh">{item['zh']}</div>
        </div>
        """, unsafe_allow_html=True)
        play_audio(item['amis'], filename_base=item['file'])

def show_quiz_mode():
    st.markdown("<h3 style='text-align: center; color: #F5D300; text-shadow: 0 0 10px #F5D300; font-family:Orbitron;'>🎯 系統入侵測試 (Quiz)</h3>", unsafe_allow_html=True)
    st.progress((st.session_state.current_q) / 3)
    st.write("")

    if st.session_state.current_q == 0:
        data = st.session_state.q1_data
        target = data['target']
        st.markdown(f"""
        <div class="word-card" style="border-left-color:#08F7FE; box-shadow: 0 0 15px rgba(8, 247, 254, 0.3);">
            <h3>🎧 音頻解析，匹配目標？</h3>
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
                        st.success("ACCESS GRANTED! (正確)")
                        time.sleep(1)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error("ACCESS DENIED! (再試一次)")

    elif st.session_state.current_q == 1:
        data = st.session_state.q2_data
        st.markdown(f"""
        <div class="word-card" style="border-left-color:#F5D300; box-shadow: 0 0 15px rgba(245, 211, 0, 0.3);">
            <h3 style="color:#F5D300 !important; text-shadow:0 0 5px #F5D300;">🧩 數據碎片修復</h3>
            <h2 style="color:#E0E0E0; margin-top:10px;">{data['q'].replace('______', '<span style="color:#FE53BB; text-shadow: 0 0 8px #FE53BB;">___</span>')}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, opt in enumerate(data['opts']):
            with cols[i]:
                if st.button(opt, key=f"q2_{i}"):
                    if opt.lower() in data['ans'].lower() or data['ans'].lower() in opt.lower():
                        st.balloons()
                        st.success("SYSTEM RESTORED! (正確)")
                        time.sleep(1)
                        st.session_state.score += 1
                        st.session_state.current_q += 1
                        st.rerun()
                    else:
                        st.error("ERROR! 匹配失敗")

    elif st.session_state.current_q == 2:
        data = st.session_state.q3_data
        target = data['target']
        st.markdown(f"""
        <div class="word-card" style="border-left-color:#FE53BB; box-shadow: 0 0 15px rgba(254, 83, 187, 0.3);">
            <h3 style="color:#FE53BB !important; text-shadow:0 0 5px #FE53BB;">🤔 原始碼解密</h3>
            <h3 style="color:#E0E0E0; margin-top:15px; font-weight:500;">{target['amis']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        play_audio(target['amis'], filename_base=target['file'])
        
        for opt in data['options']:
            if st.button(opt):
                if opt == target['zh']:
                    st.balloons()
                    st.success("DECRYPTED! (完全正確)")
                    time.sleep(1)
                    st.session_state.score += 1
                    st.session_state.current_q += 1
                    st.rerun()
                else:
                    st.error("RETRY! 重新解密")

    else:
        st.markdown(f"""
        <div class="word-card" style="border-left-color: #08F7FE; background: rgba(8, 247, 254, 0.1);">
            <h1 style='color: #08F7FE; text-shadow: 0 0 15px #08F7FE; font-family:Orbitron;'>MISSION COMPLETE</h1>
            <p style='color: #E0E0E0; font-size:20px; margin-top:10px;'>同步率 (SCORE): <span style='color:#FE53BB; font-weight:bold; font-size:24px;'>{st.session_state.score} / 3</span></p>
            <div style='font-size: 60px; filter: drop-shadow(0 0 10px #08F7FE);'>🤖</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("REBOOT SYSTEM (重新開始)"):
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
        <div class="sub-title">日子、天氣與白天 (DAY & WEATHER)</div>
        <div class="teacher-tag">SYS_ADMIN: 胡美芳 | DATA_PROVIDER: 胡美芳</div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📂 核心數據", "⚔️ 入侵測試"])
    
    with tab1:
        show_learning_mode()
    with tab2:
        show_quiz_mode()
        
    show_debug_info()

if __name__ == "__main__":
    main()
