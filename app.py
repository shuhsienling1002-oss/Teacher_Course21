import streamlit as st
import random
import json
import os
import re  # 引入正則表達式，執行最強大的容錯解析

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

# 原始聽力題庫 (15題標準數據庫，完全保留)
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
# 🧠 動態解析引擎：無敵掃描容錯版
# ==========================================
def load_question_bank():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cwd_dir = os.getcwd()

    db = {
        "聽音選詞": [], "對話理解": [], "段落朗讀": [], "情境問答": [],
        "看圖表達": [], "詞彙語意": [], "語言結構": [], "句子聽寫": [], "問答": []
    }
    db["_debug_msg"] = []

    # 🌟 1. 自動掃描資料夾內所有的 .txt 檔案，不再管檔名叫做什麼
    scanned_files = []
    for d in [base_dir, cwd_dir]:
        if not os.path.exists(d): continue
        try:
            for f in os.listdir(d):
                if f.lower().endswith(".txt") and f.lower() not in ["app.txt", "requirements.txt", "提示詞.txt"]:
                    scanned_files.append(os.path.join(d, f))
        except Exception:
            pass

    # 🌟 2. 自動嘗試各種檔案編碼，防止雲端亂碼崩潰
    target_content = ""
    file_loaded = False
    encodings_to_try = ["utf-8", "utf-8-sig", "big5", "cp950"]

    for filepath in set(scanned_files):
        for enc in encodings_to_try:
            try:
                with open(filepath, "r", encoding=enc) as f:
                    text_data = f.read()
                    # 只要內容包含題庫特有字眼，就確定是目標題庫檔！
                    if "聽音選詞" in text_data and "對話理解" in text_data:
                        target_content = text_data
                        file_loaded = True
                        break
            except Exception:
                continue
        if file_loaded:
            break

    if not file_loaded:
        db["_debug_msg"].append(f"無法找到題庫內容。已掃描檔案清單：{set(scanned_files)}")
        return db

    # 🌟 3. Regex 正則表達式自動分類引擎
    current_section = None
    for line in target_content.split("\n"):
        line = line.strip()
        if not line: continue
        
        # 定位大題區塊
        if "聽音選詞" in line: current_section = "聽音選詞"
        elif "對話理解" in line: current_section = "對話理解"
        elif "段落朗讀" in line: current_section = "段落朗讀"
        elif "情境問答" in line: current_section = "情境問答"
        elif "看圖表達" in line: current_section = "看圖表達"
        elif "詞彙語意" in line: current_section = "詞彙語意"
        elif "語言結構" in line: current_section = "語言結構"
        elif "句子聽寫" in line: current_section = "句子聽寫"
        elif "問答" in line and "情境問答" not in line: current_section = "問答"
        
        # 只要字串開頭是「數字」配上「.」或「、」，就 100% 判定為題目抓入
        elif current_section and re.match(r'^\d+[\.、]', line):
            db[current_section].append(line)
            
    return db

# ==========================================
# 🎨 UI 元件渲染邏輯 (全面升級為 Regex 正規表達式，徹底防護格式錯誤)
# ==========================================
def render_mcq(line, prefix):
    """渲染選擇題"""
    try:
        q_match = re.search(r'^(.*?)(?=\(A\))', line)
        q_text = q_match.group(1).strip() if q_match else line

        opts_text_match = re.search(r'(\(A\).*?)(?=答案：)', line)
        opts_str = opts_text_match.group(1) if opts_text_match else ""

        opt_a = re.search(r'(\(A\).*?)(?=\(B\))', opts_str)
        opt_b = re.search(r'(\(B\).*?)(?=\(C\))', opts_str)
        opt_c = re.search(r'(\(C\).*?)(?=\(D\))', opts_str)
        opt_d = re.search(r'(\(D\).*?$)', opts_str)

        opts = []
        if opt_a: opts.append(opt_a.group(1).strip())
        if opt_b: opts.append(opt_b.group(1).strip())
        if opt_c: opts.append(opt_c.group(1).strip())
        if opt_d: opts.append(opt_d.group(1).strip())

        ans_match = re.search(r'答案：(.*?)(?=。?分析：|$)', line)
        ana_match = re.search(r'分析：(.*)', line)

        ans_text = ans_match.group(1).strip().strip("。 ") if ans_match else ""
        ana_text = ana_match.group(1).strip() if ana_match else "無"

        st.markdown(f"**{q_text}**")
        if opts:
            user_ans = st.radio("請選擇：", opts, index=None, key=prefix)
            if user_ans:
                if ans_text in user_ans:
                    st.success(f"✅ 正確！分析：{ana_text}")
                else:
                    st.error(f"❌ 錯誤。正確答案：{ans_text}。分析：{ana_text}")
        else:
            st.info(line)
    except:
        st.info(line) 

def render_reading(line, prefix):
    """渲染段落朗讀"""
    try:
        am_match = re.search(r'^(.*?)(?=\(中文)', line)
        zh_match = re.search(r'\(中文(?:大意)?：(.*?)\)', line)

        if am_match and zh_match:
            st.markdown(f"📖 **{am_match.group(1).strip()}**")
            if st.toggle("顯示中文翻譯", key=f"t_{prefix}"):
                st.success(zh_match.group(1).strip())
        else:
            st.info(line)
    except:
        st.info(line)

def render_qa(line, prefix):
    """渲染問答與情境問答"""
    try:
        title_m = re.search(r'(?:題目：|^\d+[\.、])(.*?)(?=中文：)', line)
        zh_m = re.search(r'中文：(.*?)(?=參考回答：|作答參考：)', line)
        ans_m = re.search(r'(?:參考回答：|作答參考：)(.*?)(?=分析：|$)', line)
        ana_m = re.search(r'分析：(.*)', line)

        if title_m and zh_m:
            st.markdown(f"🗣️ **{title_m.group(1).strip()}**")
            st.caption(f"中文提示：{zh_m.group(1).strip()}")
            if st.toggle("顯示參考解答", key=f"t_{prefix}"):
                ans_text = ans_m.group(1).strip() if ans_m else ""
                ana_text = f"\n\n分析：{ana_m.group(1).strip()}" if ana_m else ""
                st.success(f"參考解答：{ans_text}{ana_text}")
        else:
            st.info(line)
    except:
        st.info(line)

def render_picture(line, prefix):
    """渲染看圖表達"""
    try:
        pic_m = re.search(r'圖片情境：(.*?)(?=中文提示：|作答參考：)', line)
        hint_m = re.search(r'中文提示：(.*?)(?=作答參考：)', line)
        ans_m = re.search(r'作答參考：(.*?)(?=重點(?:分析)?：|$)', line)
        ana_m = re.search(r'重點(?:分析)?：(.*)', line)

        if pic_m:
            st.markdown(f"🖼️ **圖片情境：** {pic_m.group(1).strip()}")
            if hint_m:
                st.caption(f"中文提示：{hint_m.group(1).strip()}")
            if st.toggle("顯示作答參考", key=f"t_{prefix}"):
                ans_text = ans_m.group(1).strip() if ans_m else ""
                ana_text = f"\n\n重點：{ana_m.group(1).strip()}" if ana_m else ""
                st.success(f"作答參考：{ans_text}{ana_text}")
        else:
            st.info(line)
    except:
        st.info(line)

def render_dictation(line, prefix):
    """渲染句子聽寫"""
    try:
        am_m = re.search(r'阿美語：(.*?)(?=中文：)', line)
        if not am_m:
            am_m = re.search(r'^\d+[\.、](.*?)(?=中文：)', line)
            
        zh_m = re.search(r'中文：(.*?)(?=分析：|$)', line)
        ana_m = re.search(r'分析：(.*)', line)

        if am_m and zh_m:
            st.markdown(f"✍️ **{am_m.group(1).strip()}**")
            if st.toggle("顯示翻譯與分析", key=f"t_{prefix}"):
                ana_text = f"\n\n分析：{ana_m.group(1).strip()}" if ana_m else ""
                st.success(f"中文：{zh_m.group(1).strip()}{ana_text}")
        else:
            st.info(line)
    except:
        st.info(line)

def render_section(section_name, db):
    """通用區塊渲染器"""
    questions = db.get(section_name, [])
    if not questions:
        st.warning(f"⚠️ 系統抓不到【{section_name}】的資料。")
        if "_debug_msg" in db and db["_debug_msg"]:
            st.error("🔍 **系統路徑與編碼偵錯報告**")
            for msg in db["_debug_msg"]:
                st.info(msg)
        return

    for i, line in enumerate(questions):
        with st.container():
            # 賦予卡片樣式
            st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
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
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🚀 應用程式主邏輯 (Main)
# ==========================================
def main():
    st.set_page_config(page_title="中高級認證", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")

    # 極簡北歐冷調風 (Minimalist Nordic Cold Tone) CSS
    st.markdown("""
    <style>
    /* 核心題目卡片式容器 */
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

    db = load_question_bank()

    ### ---- 第二層：根據選擇顯示對應架構 ----
    if current_tab == "📋 認證考試說明":
        st.subheader("📋 認證考試說明")
        st.divider()
        st.info("請透過上方導覽列選擇您要進行的測驗項目。系統將自動從資料庫載入完整題庫。")
        if "_debug_msg" in db and db["_debug_msg"]:
            st.error(f"⚠️ 系統異常：{db['_debug_msg']}。請切換至「閱讀」等測驗頁面查看詳細錯誤報告。")

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
