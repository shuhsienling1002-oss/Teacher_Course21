import streamlit as st
import random
import json
import os  # 引入 OS 模組，用於物理檔案路徑防禦性偵測

# 🚀 全域系統版本號
APP_VERSION = "v2.0.0 (Build 20260619)"

# ==========================================
# 🛡️ 防腐層：保留指定的原始結構與函數
# ==========================================
VOCABULARY = []
SENTENCES = []

def init_quiz(): 
    pass

def play_audio(): 
    pass

def show_learning_mode(): 
    pass

def show_quiz_mode(): 
    pass

def show_debug_info(): 
    pass

# 原始聽力題庫 (15題標準數據庫)
QUIZ_DATA = [
    {"id": 1, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-01.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["riyar", "'alo", "fanaw", "sa'owac"], "correct_text": "riyar"},
    {"id": 2, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-02.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["korkor", "rohayan", "romakat", "rotarot"], "correct_text": "romakat"},
    {"id": 3, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-03.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["hadhad", "hakhak", "hawan", "hafay"], "correct_text": "hafay"},
    {"id": 4, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-04.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["tefo'", "'okoy", "tafokod", "tafolod"], "correct_text": "tafokod"},
    {"id": 5, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-05.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["fakar", "tayhi", "pitaw", "tarakar"], "correct_text": "pitaw"},
    {"id": 6, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-06.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["sariri'", "riri'", "siri", "riyar"], "correct_text": "siri"},
    {"id": 7, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-07.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["koleto", "lokot", "kewaw", "kakorot"], "correct_text": "koleto"},
    {"id": 8, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-08.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["siwoy", "kodasing", "konga", "damay"], "correct_text": "konga"},
    {"id": 9, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-09.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["mali'", "tikami", "tilifi", "pawli"], "correct_text": "tilifi"},
    {"id": 10, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-10.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["picakay", "pitangtang", "picaliw", "pafeli'"], "correct_text": "picakay"},
    {"id": 11, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-11.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["'olaw", "'alo", "fao", "tao"], "correct_text": "tao"},
    {"id": 12, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-12.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["rorang", "kolong", "lotong", "ekong"], "correct_text": "lotong"},
    {"id": 13, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-13.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["Halitamako", "Haliradiw", "Haliepah", "Hali'ecaw"], "correct_text": "Haliepah"},
    {"id": 14, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-14.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["dafak", "a'ayad", "dadaya", "kamaya"], "correct_text": "dadaya"},
    {"id": 15, "audio_path": "assets/audio/01_listening/listening_words/tengil-a1-15.mp3", "question_text": "聆聽音檔，選出關聯的詞彙：", "options": ["sioy", "simal", "sinafel", "simico"], "correct_text": "sinafel"}
]

# ==========================================
# 🧠 動態解析引擎：自動讀取並結構化題庫文字檔
# ==========================================
@st.cache_data
def load_question_bank(filepath="各類題目.txt"):
    # 🌟 關鍵修正：動態取得 app.py 當前所在的資料夾絕對路徑
    base_dir = os.path.dirname(os.path.abspath(__file__))
    actual_filepath = os.path.join(base_dir, filepath)

    db = {
        "聽音選詞": [], "對話理解": [], "段落朗讀": [], "情境問答": [],
        "看圖表達": [], "詞彙語意": [], "語言結構": [], "句子聽寫": [], "問答": []
    }
    
    # 🌟 改用 actual_filepath 進行防禦性偵測
    if not os.path.exists(actual_filepath):
        return db

    current_section = None
    # 🌟 改用 actual_filepath 開啟檔案
    with open(actual_filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            # 定位大題區塊
            if "選擇題（聽音選詞）" in line: current_section = "聽音選詞"
            elif "選擇題（對話理解）" in line: current_section = "對話理解"
            elif "三、段落朗讀" in line: current_section = "段落朗讀"
            elif "四、情境問答" in line: current_section = "情境問答"
            elif "五、看圖表達" in line: current_section = "看圖表達"
            elif "選擇題（詞彙語意）" in line: current_section = "詞彙語意"
            elif "選擇題（語言結構）" in line: current_section = "語言結構"
            elif "八、句子聽寫" in line: current_section = "句子聽寫"
            elif "九、問答" in line: current_section = "問答"
            # 擷取題目列 (以數字開頭)
            elif current_section and line.isdigit() and ("." in line[:4] or "、" in line[:4]):
                db[current_section].append(line)
    return db

# ==========================================
# 🎨 UI 元件渲染邏輯
# ==========================================
def render_mcq(line, prefix):
    """渲染選擇題 (自動切分選項與解答)"""
    try:
        q_part = line.split("(A)")
        opts_str = line.split("(A)").split("答案：")
        ans_part = line.split("答案：").split("分析：").strip("。 ")
        ana_part = line.split("分析：") if "分析：" in line else "無"

        st.markdown(f"**{q_part.strip()}**")
        
        o_a = "(A)" + opts_str.split("(B)")
        o_b = "(B)" + opts_str.split("(B)").split("(C)")
        o_c = "(C)" + opts_str.split("(C)").split("(D)")
        o_d = "(D)" + opts_str.split("(D)")

        opts = [o_a.strip(), o_b.strip(), o_c.strip(), o_d.strip()]
        user_ans = st.radio("請選擇：", opts, index=None, key=prefix)
        if user_ans:
            if ans_part in user_ans:
                st.success(f"✅ 正確！分析：{ana_part}")
            else:
                st.error(f"❌ 錯誤。正確答案：{ans_part}。分析：{ana_part}")
    except:
        st.info(line) 

def render_reading(line, prefix):
    """渲染段落朗讀"""
    try:
        q_part = line.split("(中文")
        ch_part = line.split("(中文").strip("：").strip(")")
        st.markdown(f"📖 **{q_part.strip()}**")
        if st.toggle("顯示中文翻譯", key=f"t_{prefix}"):
            st.success(ch_part)
    except:
        st.info(line)

def render_qa(line, prefix):
    """渲染問答與情境問答"""
    try:
        if "題目：" in line or "中文：" in line:
            title_part = line.split("題目：") if "題目：" in line else line
            q_am = title_part.split("中文：")
            ch_part = line.split("中文：").split("參考回答：")
            ans_part = line.split("參考回答：").split("分析：")
            ana_part = line.split("分析：") if "分析：" in line else ""
            
            st.markdown(f"🗣️ **{q_am.strip()}**")
            st.caption(f"中文提示：{ch_part.strip()}")
            if st.toggle("顯示參考解答", key=f"t_{prefix}"):
                st.success(f"參考解答：{ans_part.strip()}" + (f"\n\n分析：{ana_part.strip()}" if ana_part else ""))
        else:
            st.info(line)
    except:
        st.info(line)

def render_picture(line, prefix):
    """渲染看圖表達"""
    try:
        pic = line.split("圖片情境：").split("中文提示：") if "中文提示：" in line else line.split("圖片情境：").split("作答參考：")
        ans = line.split("作答參考：").split("重點")
        st.markdown(f"🖼️ **圖片情境：** {pic.strip()}")
        if st.toggle("顯示作答參考", key=f"t_{prefix}"):
            st.success(f"作答參考：{ans.strip()}")
    except:
        st.info(line)

def render_dictation(line, prefix):
    """渲染句子聽寫"""
    try:
        am = line.split("中文：").replace("阿美語：", "")
        ch = line.split("中文：").split("分析：")
        ana = line.split("分析：")
        st.markdown(f"✍️ **{am.strip()}**")
        if st.toggle("顯示翻譯與分析", key=f"t_{prefix}"):
            st.success(f"中文：{ch.strip()}\n\n分析：{ana.strip()}")
    except:
        st.info(line)

def render_section(section_name, db):
    """通用區塊渲染器"""
    questions = db.get(section_name, [])
    if not questions:
        st.warning(f"⚠️ 找不到題庫資料，請確認 **『各類題目.txt』** 是否與本程式放在同一個資料夾。")
        return

    for i, line in enumerate(questions):
        with st.container():
            if "聽音選詞" in section_name or "對話理解" in section_name or section_name in ["詞彙語意", "語言結構"]:
                render_mcq(line, f"{section_name}_{i}")
            elif section_name == "段落朗讀":
                render_reading(line, f"{section_name}_{i}")
            elif section_name in ["情境問答", "問答"]:
                render_qa(line, f"{section_name}_{i}")
            elif section_name == "看圖表達":
                render_picture(line, f"{section_name}_{i}")
            elif section_name == "句子聽寫":
                render_dictation(line, f"{section_name}_{i}")
            st.divider()

# ==========================================
# 🚀 應用程式主邏輯 (Main)
# ==========================================
def main():
    st.set_page_config(page_title="中高級認證", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

    # 極簡北歐冷調風 (Minimalist Nordic Cold Tone) CSS
    st.markdown("""
    <style>
    .quiz-card {
        background-color: #F8F9FA;
        padding: 24px;
        border-radius: 8px;
        border: 1px solid #E9ECEF;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        margin-top: 15px;
        margin-bottom: 25px;
        transition: all 0.3s ease;
        color: #343A40;
    }
    hr { border-top: 1px solid #E9ECEF; }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎓 中高級認證")
    st.caption("[請選擇練習平台]")

    main_options = ["📋 認證考試說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
    current_tab = st.segmented_control("主選單導覽", main_options, default=None, label_visibility="collapsed")

    if "previous_tab" not in st.session_state:
        st.session_state.previous_tab = None

    if st.session_state.previous_tab != current_tab:
        st.session_state.submitted = False
        st.session_state.audio_triggered = False
        if "writing_submitted" in st.session_state:
            st.session_state.writing_submitted = False
        st.session_state.previous_tab = current_tab

    # 載入動態題庫庫
    db = load_question_bank()

    ### ---- 第二層：根據選擇顯示對應架構 ----
    if current_tab == "📋 認證考試說明":
        st.subheader("📋 認證考試說明")
        st.divider()
        st.info("請透過上方導覽列選擇您要進行的測驗項目。系統將自動從 `各類題目.txt` 載入完整題庫。")

    elif current_tab == "🎧 聽力":
        st.subheader("🎧 聽力測驗 (pitengil)")
        st.divider()
        listening_sub = st.radio("題型選擇：", ["選擇題-聽音選詞", "選擇題-對話理解"], horizontal=True)
        if listening_sub == "選擇題-聽音選詞":
            render_section("聽音選詞", db)
        elif listening_sub == "選擇題-對話理解":
            render_section("對話理解", db)

    elif current_tab == "🗣️ 口說":
        st.subheader("🗣️ 口說測驗 (pisowal)")
        st.divider()
        speaking_sub = st.radio("題型選擇：", ["段落朗讀", "情境問答", "看圖表達"], horizontal=True)
        if speaking_sub == "段落朗讀":
            render_section("段落朗讀", db)
        elif speaking_sub == "情境問答":
            render_section("情境問答", db)
        elif speaking_sub == "看圖表達":
            render_section("看圖表達", db)

    elif current_tab == "📖 閱讀":
        st.subheader("📖 閱讀測驗 (piasip)")
        st.divider()
        reading_sub = st.radio("閱讀題型選擇：", ["選擇題-詞彙語意", "選擇題-語言結構"], horizontal=True)
        if reading_sub == "選擇題-詞彙語意":
            render_section("詞彙語意", db)
        elif reading_sub == "選擇題-語言結構":
            render_section("語言結構", db)

    elif current_tab == "✍️ 寫作":
        st.subheader("✍️ 寫作測驗 (pitilid)")
        st.divider()
        writing_sub = st.radio("寫作題型選擇：", ["句子聽寫", "問答"], horizontal=True)
        if writing_sub == "句子聽寫":
            render_section("句子聽寫", db)
        elif writing_sub == "問答":
            render_section("問答", db)

    st.write("---")
    st.caption(f"© 2026 中高級認證 App 三一開發團隊 ｜ 系統版本： **{APP_VERSION}** ")

if __name__ == "__main__":
    main()
