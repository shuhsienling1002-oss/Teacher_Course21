抱歉！剛才為了呈現效果，省略了中間的邏輯程式碼，導致您直接複製時無法正常運作。
這次為您奉上完全獨立、可直接複製執行的完整程式碼。
這次改用「極簡暗黑科技風 (Minimal Cyber Noir)」，採用深灰底色（#121212）搭配冷冽的螢光藍、極光綠與電子紫色，並將原本的紙膠帶與點點手帳，全部替換成發光光暈邊框、數碼儀表板卡片與科技粒子風格。
請直接完整複製下方程式碼，貼入您的檔案中即可直接啟動：

import streamlit as stimport timeimport osimport randomfrom gtts import gTTSfrom io import BytesIO
# --- 0. 系統配置 ---
st.set_page_config(
    page_title="阿美語 - 日子與天氣 (Cyber)", 
    page_icon="⚡", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)
# --- CSS 視覺魔法 (極簡暗黑科技風) ---
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* 全局背景：深邃科幻黑與電子網格線 */
    .stApp { 
        background-color: #0D0E12;
        background-image: linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px);
        background-size: 25px 25px;
        font-family: 'Orbitron', 'Noto Sans TC', sans-serif;
        color: #E2E8F0;
    }
    
    .block-container { padding-top: 2rem !important; padding-bottom: 5rem !important; }
    
    /* --- Header (高科技能量核心風格) --- */
    .header-container {
        background: #14161D;
        border: 1px solid #00E5FF; /* 螢光藍邊框 */
        box-shadow: 0px 0px 15px rgba(0, 229, 255, 0.2);
        border-radius: 6px;
        padding: 25px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    /* 模擬邊角科技感飾條 */
    .header-container::before {
        content: '// SYSTEM READY';
        position: absolute;
        top: -12px;
        left: 15px;
        background: #0D0E12;
        padding: 0 8px;
        font-size: 11px;
        color: #00E5FF;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
    }
    
    .main-title {
        font-family: 'Orbitron', sans-serif;
        color: #00E5FF;
        font-size: 38px;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 8px rgba(0, 229, 255, 0.5);
        letter-spacing: 2px;
    }
    
    .sub-title { color: #94A3B8; font-size: 16px; margin-top: 5px; font-weight: 500; }
    
    .teacher-tag { 
        display: inline-block; 
        margin-top: 15px; 
        padding: 4px 12px; 
        background: rgba(168, 85, 247, 0.1); /* 電子紫 */
        color: #C084FC;
        border-radius: 4px; 
        font-size: 13px; 
        font-weight: bold; 
        border: 1px solid rgba(168, 85, 247, 0.3);
    }
    
    /* --- Cards (數據終端模組風) --- */
    .word-card {
        background: #14161D;
        border-radius: 4px;
        padding: 15px 10px;
        text-align: center;
        border: 1px solid #222530;
        border-left: 4px solid #10B981; /* 綠色側邊能量條 */
        height: 100%;
        margin-bottom: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        transition: all 0.2s ease;
    }
    
    .word-card h3 {
        color: #FFFFFF !important;
        font-weight: 700;
        margin: 0;
        padding-bottom: 5px;
        font-size: 18px;
    }
    .word-card:hover { 
        transform: translateY(-3px); 
        border-color: #10B981;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.3); 
    }
    
    .icon-box { font-size: 26px; margin-bottom: 5px; }
    .zh-word { font-size: 14px; color: #94A3B8; font-weight: 500; }
    
    /* --- Sentences (矩陣代碼面板風格) --- */
    .sentence-box {
        background: #14161D;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 6px;
        border: 1px solid #222530;
        border-bottom: 2px solid #A855F7; /* 紫色底線 */
    }
    .sentence-amis { font-size: 18px; color: #C084FC; font-weight: 700; margin-bottom: 5px; text-shadow: 0 0 5px rgba(192, 132, 252, 0.3); }
    .sentence-zh { font-size: 15px; color: #CBD5E1; }
    
    /* --- Buttons (電漿按鈕) --- */
    .stButton>button { 
        width: 100%; 
        border-radius: 4px; 
        background: #1E293B; 
        border: 1px solid #00E5FF; 
        color: #00E5FF !important; 
        font-weight: bold; 
        box-shadow: 0 2px 0 #00B3CC;
        font-family: 'Orbitron', 'Noto Sans TC', sans-serif;
    }
    .stButton>button:hover { background: #00E5FF; color: #0D0E12 !important; box-shadow: 0 0 10px rgba(0,229,255,0.5); }
    .stButton>button:active { transform: translateY(2px); box-shadow: none; }
    
    /* --- Tabs (系統切換卡) --- */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        color: #94A3B8 !important; 
        background-color: transparent !important;
        border-radius: 4px;
        padding: 5px 15px;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(0, 229, 255, 0.1) !important;
        color: #00E5FF !important;
        border: 1px solid #00E5FF;
        font-weight: bold;
    }
    
    /* 修正進度條樣式 */
    .stProgress > div > div > div {
        background-color: #00E5FF !important;
    }
    </style>""", unsafe_allow_html=True)
# --- 1. 資料設定 (主題：Remiad 日子與天氣) ---VOCABULARY = [
    {"amis": "kapahay", "zh": "好的", "emoji": "✨", "file": "v_kapahay"},
    {"amis": "remiad", "zh": "日子;天氣;白天", "emoji": "📅", "file": "v_remiad"},
    {"amis": "katangasaan", "zh": "到達的時間", "emoji": "⏳", "file": "v_katangasaan"},
    {"amis": "katangasaan tu","zh": "到期了", "emoji": "⏰", "file": "v_katangasaan_tu"},
    {"amis": "kasuvucan", "zh": "生日", "emoji": "🎂", "file": "v_kasuvucan"},
    {"amis": "maku", "zh": "我的", "emoji": "👤", "file": "v_maku"},
    {"amis": "anini a remiad","zh": "今天", "emoji": "📌", "file": "v_anini_a_remiad"},
    {"amis": "saremiad sa", "zh": "整天", "emoji": "🔄", "file": "v_saremiad_sa"},
    {"amis": "maurad", "zh": "下雨", "emoji": "🌧️", "file": "v_maurad"},
    {"amis": "pataluma’en", "zh": "送(帶)回家", "emoji": "🏠", "file": "v_patalumaen"},
    {"amis": "saremiaden", "zh": "需整天", "emoji": "⏳", "file": "v_saremiaden"},
    {"amis": "pawali", "zh": "曬著", "emoji": "☀️", "file": "v_pawali"},
    {"amis": "vuduy", "zh": "衣服", "emoji": "👕", "file": "v_vuduy"},
    {"amis": "misu", "zh": "你的", "emoji": "👉", "file": "v_misu"},
    {"amis": "katawalan", "zh": "忘記", "emoji": "❌", "file": "v_katawalan"},
    {"amis": "uradan", "zh": "下雨(天)", "emoji": "☔", "file": "v_uradan"},
    {"amis": "utiih", "zh": "不方便", "emoji": "⚠️", "file": "v_utiih"},
    {"amis": "dademak", "zh": "做工作", "emoji": "🛠️", "file": "v_dademak"},
]
SENTENCES = [
    {"amis": "Kapahay a remiad.", "zh": "好的天氣。", "emoji": "🌤️", "file": "s_kapahay_a_remiad"},
    {"amis": "Katangasaan tu ku remiad.", "zh": "到期了。", "emoji": "🛑", "file": "s_katangasaan_tu_ku_remiad"},
    {"amis": "Kasuvucan nu maku anini a remiad.", "zh": "今天是我的生日。", "emoji": "🎉", "file": "s_kasuvucan_nu_maku"},
    {"amis": "Saremiad sa a maurad anini.", "zh": "今天整天下著雨。", "emoji": "⛈️", "file": "s_saremiad_sa_a_maurad"},
    {"amis": "Kai remiad a pataluma’en kami.", "zh": "白天送我們回家。", "emoji": "🚌", "file": "s_kai_remiad"},
    {"amis": "Saremiaden a pawali ku vuduy.", "zh": "衣服需整天曬著。", "emoji": "🧺", "file": "s_saremiaden_a_pawali"},
    {"amis": "Katangasaan tu ku kasuvucan nu misu a remiad.", "zh": "你的生日到了。", "emoji": "🎁", "file": "s_katangasaan_tu_ku_kasuvucan"},
    {"amis": "Aya! Katawalan nu maku.", "zh": "哎呀! 我忘記了。", "emoji": "💡", "file": "s_aya_katawalan"},
    {"amis": "Uradan a remiad utiih a dademak.", "zh": "下雨天工作不方便。", "emoji": "💼", "file": "s_uradan_a_remiad"},
]
QUIZ_DATA = [
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
        st.markdown(f"<span style='color:#00E5FF; font-size:12px; background:rgba(0,229,255,0.1); padding:2px 5px; border-radius:4px; border: 1px solid #00E5FF;'> [MISSING AUDIO]: {filename_base}</span>", unsafe_allow_html=True)
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
    # 複製一份選項避免污染原資料
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
st.markdown("// VOCABULARY MODULE", unsafe_allow_html=True)
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
st.markdown("// SENTENCE MATRIX", unsafe_allow_html=True)
for item in SENTENCES:
st.markdown(f"""

{item['emoji']} {item['amis']}
{item['zh']}

""", unsafe_allow_html=True)
play_audio(item['amis'], filename_base=item['file'])
def show_quiz_mode():
st.markdown("// SYSTEM TERMINAL QUIZ", unsafe_allow_html=True)
st.progress((st.session_state.current_q) / 3)
st.write("")
if st.session_state.current_q == 0:
data = st.session_state.q1_data
target = data['target']
st.markdown(f"""

[聽力解碼] 聽聽看，這是哪個字？

""", unsafe_allow_html=True)
play_audio(target['amis'], filename_base=target['file'])
st.write("")
cols = st.columns(3)
for idx, opt in enumerate(data['options']):
with cols[idx]:
if st.button(f"{opt['zh']}", key=f"q1_{idx}"):
if opt['amis'] == target['amis']:
st.balloons()
st.success("解碼成功！ (Correct)")
time.sleep(1)
st.session_state.score += 1
st.session_state.current_q += 1
st.rerun()
else:
st.error("特徵不符，再試一次")
elif st.session_state.current_q == 1:
data = st.session_state.q2_data
st.markdown(f"""

[矩陣填空] 補全文本鏈條
{data['q'].replace('___', '')}

""", unsafe_allow_html=True)
cols = st.columns(3)
for i, opt in enumerate(data['opts']):
with cols[i]:
if st.button(opt, key=f"q2_{i}"):
if opt.lower() in data['ans'].lower() or data['ans'].lower() in opt.lower():
st.balloons()
st.success("校準正確！ (Great)")
time.sleep(1)
st.session_state.score += 1
st.session_state.current_q += 1
st.rerun()
else:
st.error("核心錯誤")
elif st.session_state.current_q == 2:
data = st.session_state.q3_data
target = data['target']
st.markdown(f"""

[語義分析] 這是什麼意思？
{target['amis']}

""", unsafe_allow_html=True)
for idx, opt in enumerate(data['options']):
if st.button(opt, key=f"q3_{idx}"):
if opt == target['zh']:
st.balloons()
st.success("同步完成！ (Perfect)")
time.sleep(1)
st.session_state.score += 1
st.session_state.current_q += 1
st.rerun()
else:
st.error("運算偏移，再想一下")
else:
st.markdown(f"""

評估完成！
系統同步率: {st.session_state.score} / 3

""", unsafe_allow_html=True)
if st.button("重新加載核心 (Restart)"):
init_quiz()
st.rerun()
def show_debug_info():
st.markdown("---")
files_audio = []
if os.path.exists("audio"):
files_audio = [f for f in os.listdir('audio') if f.endswith('.m4a') or f.endswith('.mp3')]
if not files_audio:
st.caption(" ⚡ SYSTEM NOTICE：檢測到本地音頻模組未加載。建立 audio 資料夾並放入音檔，即可啟用真人音訊。")
## --- 主程式 ---
def main():
st.markdown("""

Remiad // OS
日子、天氣與白晝·數碼數據庫
核心講師：胡美芳 | 數據提供：胡美芳

""", unsafe_allow_html=True)
tab1, tab2 = st.tabs([" 數據單元 (Learn)", " 終端測試 (Quiz)"])
with tab1:
show_learning_mode()
with tab2:
show_quiz_mode()
show_debug_info()
if name == "main":
main()


### 🛠️ 此版本修復與優化細節：
1. **完整結構交付**：包含原版所有的字典資料、隨機測驗狀態初始化邏輯，沒有任何程式碼省略。
2. **防崩潰修復**：針對原版測驗選項 shuffle 時，避免了直接改動原始全局 `QUIZ_DATA` 陣列而引發的執行期（Runtime）狀態錯誤。
3. **完美兼容 Streamlit 1.30+**：內建的 `st.rerun()` 均已採用最新標準，不需擔心棄用警告。

現在，您可以放心將這段程式碼直接覆蓋，並用終端機執行 `streamlit run 檔名.py` 來看新介面了！

若您想要調整特定的**發光顏色**或**區塊排列方式**，請隨時告訴我！


