import streamlit as st
import random
import json
import os
import re

# 🚀 全域系統版本號
APP_VERSION = "v2.1.4 (Build 20260727 - Kawaii Manga Edition ✨)"

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
# 🧠 動態解析引擎：跨行讀取與穩定分割版
# ==========================================
def load_question_bank():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cwd_dir = os.getcwd()

    db = {
        "聽音選詞": [], "對話理解": [], "段落朗讀": [], "情境問答": [],
        "看圖表達": [], "詞彙語意": [], "語言結構": [], "句子聽寫": [], "問答": []
    }
    
    scanned_files = []
    for d in [base_dir, cwd_dir]:
        if not os.path.exists(d): continue
        try:
            for f in os.listdir(d):
                if f.lower().endswith(".txt") and f.lower() not in ["app.txt", "requirements.txt", "提示詞.txt"]:
                    scanned_files.append(os.path.join(d, f))
        except:
            pass

    target_content = ""
    file_loaded = False
    encodings_to_try = ["utf-8", "utf-8-sig", "big5", "cp950"]

    for filepath in set(scanned_files):
        for enc in encodings_to_try:
            try:
                with open(filepath, "r", encoding=enc) as f:
                    text_data = f.read()
                    if "聽音選詞" in text_data and "對話理解" in text_data:
                        target_content = text_data
                        file_loaded = True
                        break
            except:
                continue
        if file_loaded:
            break

    if not file_loaded:
        return db

    # 使用緩衝區將跨行的題目合併為單一字串
    current_section = None
    current_question = []

    def save_question():
        if current_section and current_question:
            q_text = " ".join(current_question).strip()
            if re.match(r'^\d+[\.、]', q_text):
                db[current_section].append(q_text)
            current_question.clear()

    for line in target_content.split("\n"):
        line = line.strip()
        # 遇到空行代表題目結束，存入題庫
        if not line:
            save_question()
            continue
            
        # 判斷是否為題型切換標題
        if "一、選擇題（聽音選詞）" in line: save_question(); current_section = "聽音選詞"
        elif "二、選擇題（對話理解）" in line: save_question(); current_section = "對話理解"
        elif "三、段落朗讀" in line: save_question(); current_section = "段落朗讀"
        elif "四、情境問答" in line: save_question(); current_section = "情境問答"
        elif "五、看圖表達" in line: save_question(); current_section = "看圖表達"
        elif "六、選擇題（詞彙語意）" in line: save_question(); current_section = "詞彙語意"
        elif "七、選擇題（語言結構）" in line: save_question(); current_section = "語言結構"
        elif "八、句子聽寫" in line: save_question(); current_section = "句子聽寫"
        elif "九、問答" in line: save_question(); current_section = "問答"
        
        # 開頭為數字代表新題目的開始
        elif re.match(r'^\d+[\.、]', line):
            save_question()
            current_question.append(line)
        # 屬於目前題目的後續內容（選項或答案）
        else:
            if current_question:
                current_question.append(line)
                
    save_question() # 儲存最後一題
            
    return db

# ==========================================
# 🎨 終極 UI 渲染邏輯 (可愛漫畫風格 Kawaii Style)
# ==========================================
def render_mcq(line, prefix):
    """渲染選擇題 (修復 split 回傳 list 的問題，並新增聽力題目隱藏功能)"""
    try:
        if "(A)" not in line:
            st.info(line)
            return

        # 限制分割次數，並明確取值
        parts = line.split("(A)", 1)
        q_part = parts[0].strip()
        rest = "(A)" + parts[1]
        
        opts_str = rest
        ans_str = ""
        ana_str = ""
        
        if "答案：" in rest:
            ans_parts = rest.split("答案：", 1)
            opts_str = ans_parts[0].strip()
            ans_ana = ans_parts[1]
            
            if "分析：" in ans_ana:
                final_parts = ans_ana.split("分析：", 1)
                ans_str = final_parts[0].strip("。 ")
                ana_str = final_parts[1].strip()
            else:
                ans_str = ans_ana.strip("。 ")

        # 🌟 聽力測驗專屬：隱藏題目文字功能
        is_listening = "聽音選詞" in prefix or "對話理解" in prefix
        if is_listening:
            if st.toggle("👁️ 顯示題目文字", key=f"t_show_q_{prefix}"):
                st.markdown(f"**{q_part}**")
        else:
            st.markdown(f"**{q_part}**")
        
        # 安全切割四個選項
        opts = []
        for tag in ["(A)", "(B)", "(C)", "(D)"]:
            if tag in opts_str:
                opt_text = opts_str.split(tag, 1)[1]
                for next_tag in ["(B)", "(C)", "(D)"]:
                    if next_tag > tag and next_tag in opt_text:
                        opt_text = opt_text.split(next_tag, 1)[0]
                opts.append(tag + " " + opt_text.strip())

        user_ans = st.radio("✨ 請選擇正確答案：", opts, index=None, key=prefix)
        
        if st.toggle("💡 顯示解答與分析", key=f"t_ans_{prefix}"):
            if ans_str:
                msg = f"**🎉 正確答案：** {ans_str}"
                if ana_str: msg += f"\n\n🔍 **詳盡解析：** {ana_str}"
                st.success(msg)
            else:
                st.warning("🐾 暫無標準答案～")
        elif user_ans and ans_str:
            if ans_str in user_ans:
                st.success(f"🎉 答對了！太厲害啦！" + (f"\n\n🔍 **解析：**{ana_str}" if ana_str else ""))
            else:
                st.error(f"❌ 差一點點！加油！正確答案是：**{ans_str}**。" + (f"\n\n🔍 **解析：**{ana_str}" if ana_str else ""))
    except Exception as e:
        st.info(line) 

def render_reading(line, prefix):
    """渲染段落朗讀"""
    try:
        q_part = line
        ch_part = ""
        if "(中文：" in line:
            parts = line.split("(中文：", 1)
            q_part = parts[0].strip()
            ch_part = parts[1].strip(")")
        elif "(中文大意：" in line:
            parts = line.split("(中文大意：", 1)
            q_part = parts[0].strip()
            ch_part = parts[1].strip(")")
        
        st.markdown(f"📖 **{q_part}**")
        if ch_part:
            if st.toggle("💡 顯示中文翻譯", key=f"t_{prefix}"):
                st.success(f"🌸 **中文翻譯：** {ch_part}")
    except:
        st.info(line)

def render_qa(line, prefix):
    """渲染問答與情境問答"""
    try:
        text = line
        q_am = text
        ch_hint = ""
        ans = ""
        ana = ""
        
        if "中文：" in text:
            parts = text.split("中文：", 1)
            q_am = parts[0].strip()
            text = parts[1]
            
        if "參考回答：" in text:
            parts = text.split("參考回答：", 1)
            ch_hint = parts[0].strip()
            text = parts[1]
        elif "作答參考：" in text:
            parts = text.split("作答參考：", 1)
            ch_hint = parts[0].strip()
            text = parts[1]
            
        if "分析：" in text:
            parts = text.split("分析：", 1)
            ans = parts[0].strip()
            ana = parts[1].strip()
        else:
            if not ans: 
                ans = text.strip()
        
        q_am = q_am.replace("題目：", " 題目：")
        
        # 🌟 口說測驗-情境問答專屬：隱藏題目與提示功能
        is_situational = "情境問答" in prefix
        if is_situational:
            if st.toggle("👁️ 顯示題目與提示", key=f"t_show_q_{prefix}"):
                st.markdown(f"🗣️ **{q_am}**")
                if ch_hint:
                    st.caption(f"💭 中文提示：{ch_hint}")
        else:
            st.markdown(f"🗣️ **{q_am}**")
            if ch_hint:
                st.caption(f"💭 中文提示：{ch_hint}")
            
        if ans or ana:
            if st.toggle("💡 顯示參考解答", key=f"t_{prefix}"):
                msg = ""
                if ans: msg += f"✨ **參考解答：** {ans}"
                if ana: msg += f"\n\n🔍 **重點解析：** {ana}"
                st.success(msg)
    except:
        st.info(line)

def render_picture(line, prefix):
    """渲染看圖表達，並支援動態載入對應題號圖片"""
    try:
        text = line
        pic = text
        hint = ""
        ans = ""
        ana = ""
        
        if "圖片情境：" in text:
            parts = text.split("圖片情境：", 1)
            pic = parts[1]
            
        if "中文提示：" in pic:
            parts = pic.split("中文提示：", 1)
            pic = parts[0].strip()
            hint_part = parts[1]
            
            if "作答參考：" in hint_part:
                h_parts = hint_part.split("作答參考：", 1)
                hint = h_parts[0].strip()
                ans_part = h_parts[1]
                
                if "重點分析：" in ans_part:
                    a_parts = ans_part.split("重點分析：", 1)
                    ans = a_parts[0].strip()
                    ana = a_parts[1].strip()
                elif "重點：" in ans_part:
                    a_parts = ans_part.split("重點：", 1)
                    ans = a_parts[0].strip()
                    ana = a_parts[1].strip()
                else:
                    ans = ans_part.strip()
            else:
                hint = hint_part.strip()
        
        # 🌟 動態讀取對應圖片邏輯 (假設 prefix 格式為 "看圖表達_0")
        try:
            # 從 prefix 中解析題號 (index + 1)
            idx = int(prefix.split('_')[-1]) + 1
            img_path_jpg = f"assets/images/picture_{idx}.jpg"
            img_path_png = f"assets/images/picture_{idx}.png"
            
            if os.path.exists(img_path_jpg):
                st.image(img_path_jpg, use_container_width=True)
            elif os.path.exists(img_path_png):
                st.image(img_path_png, use_container_width=True)
            else:
                st.info(f"🖼️ **圖片佔位區：** 若要顯示圖片，請將圖片命名為 `picture_{idx}.jpg` 或 `.png`，並放置於 `assets/images/` 資料夾中。")
        except:
            pass # 若解析題號失敗則安全跳過

        st.markdown(f"🖼️ **圖片情境：** {pic}")
        
        if hint:
            st.caption(f"💭 中文提示：{hint}")
            
        # 加入輸入框作為草稿區
        st.text_area("✍️ 練練看筆記區：", key=f"input_{prefix}", label_visibility="collapsed", placeholder="可以在此輸入您的口說練習草稿唷...")
            
        if ans or ana:
            if st.toggle("💡 顯示作答參考", key=f"t_{prefix}"):
                msg = ""
                if ans: msg += f"✨ **作答參考：** {ans}"
                if ana: msg += f"\n\n🔍 **重點說明：** {ana}"
                st.success(msg)
    except:
        st.info(line)

def render_dictation(line, prefix):
    """渲染句子聽寫"""
    try:
        text = line
        am = text
        ch = ""
        ana = ""
        
        if "中文：" in text:
            parts = text.split("中文：", 1)
            am = parts[0].replace("阿美語：", "").strip()
            text = parts[1]
            
            if "分析：" in text:
                sub_parts = text.split("分析：", 1)
                ch = sub_parts[0].strip()
                ana = sub_parts[1].strip()
            else:
                ch = text.strip()
        
        # 加入作答的文字輸入框，模擬真實寫作情境
        st.text_area("✍️ 聽寫作答區：", key=f"input_{prefix}", label_visibility="collapsed", placeholder="請在此輸入您聽到的句子答案...")
        
        # 🌟 寫作測驗專屬：隱藏聽寫原文功能
        if st.toggle("👁️ 顯示聽寫原文", key=f"t_show_dict_{prefix}"):
            st.markdown(f"✍️ **{am}**")
            
        if ch or ana:
            if st.toggle("💡 顯示翻譯與分析", key=f"t_{prefix}"):
                msg = ""
                if ch: msg += f"🌸 **中文意涵：** {ch}"
                if ana: msg += f"\n\n🔍 **詳細解析：** {ana}"
                st.success(msg)
    except:
        st.info(line)

def render_section(section_name, db):
    """通用區塊渲染器"""
    questions = db.get(section_name, [])
    if not questions:
        st.warning(f"🐾 叮咚！系統暫時找不到【{section_name}】的資料庫內容～")
        return

    for i, line in enumerate(questions):
        with st.container():
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
    st.set_page_config(page_title="中高級認證 ‧ 萌萌學習寶典 ✨", page_icon="🎀", layout="centered", initial_sidebar_state="collapsed")

    # 🌸 可愛漫畫風格 (Kawaii Anime/Manga Style) CSS 造型設計
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Mamelon&family=Quicksand:wght@500;700&family=Zen+Maru+Gothic:wght@500;700;900&display=swap');

    /* 全局背景與字體設定 */
    .stApp {
        background-color: #FFF7F9;
        font-family: 'Zen Maru Gothic', 'Quicksand', 'Microsoft JhengHei', sans-serif;
        color: #4A3E4E;
    }

    /* 可愛標題裝飾 */
    h1 {
        color: #FF6B8B !important;
        text-shadow: 3px 3px 0px #FFD1DC;
        font-weight: 900 !important;
        text-align: center;
        letter-spacing: 1px;
        padding-bottom: 5px;
    }

    h2, h3 {
        color: #FF758C !important;
        font-weight: 700 !important;
    }

    /* 可愛漫畫卡片樣式 (Comic Speech Card) */
    .quiz-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 20px;
        border: 3.5px solid #FFC2D1;
        box-shadow: 6px 6px 0px #FFD1DC;
        margin-top: 20px;
        margin-bottom: 30px;
        transition: all 0.2s ease-in-out;
        position: relative;
    }

    .quiz-card:hover {
        transform: translateY(-3px);
        box-shadow: 8px 8px 0px #FFB6C1;
        border-color: #FF85A1;
    }

    /* 分割線樣式 */
    hr {
        border: none;
        border-top: 3px dashed #FFAAA5;
        margin: 20px 0;
    }

    /* 可愛按鈕與選項設計 */
    .stButton>button {
        background-color: #FF85A1;
        color: white !important;
        font-weight: bold;
        border-radius: 25px;
        border: 2px solid #FF6B8B;
        box-shadow: 0 4px 0 #D85772;
        transition: all 0.1s ease;
    }
    
    .stButton>button:hover {
        background-color: #FF6B8B;
        transform: translateY(2px);
        box-shadow: 0 2px 0 #D85772;
    }

    /* Toggle 開關樣式優化 */
    div[data-testid="stToggle"] {
        background-color: #FFF0F3;
        padding: 6px 12px;
        border-radius: 15px;
        border: 1.5px dashed #FFB6C1;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    /* 訊息提示框樣式 (Success, Warning, Info, Error) */
    .stAlert {
        border-radius: 18px !important;
        border: 2px solid !important;
        font-weight: bold !important;
    }

    /* Radio 選項包裝 */
    div[role="radiogroup"] {
        background-color: #FFF5F7;
        padding: 12px;
        border-radius: 16px;
        border: 2px solid #FFE3E8;
    }

    /* 文字輸入框樣式 */
    textarea, input {
        border-radius: 15px !important;
        border: 2px solid #FFC2D1 !important;
        background-color: #FAFAFA !important;
    }
    textarea:focus, input:focus {
        border-color: #FF85A1 !important;
        box-shadow: 0 0 8px rgba(255, 133, 161, 0.4) !important;
    }
    
    /* 頁尾標示 */
    .kawaii-footer {
        text-align: center;
        color: #B5838D;
        font-size: 0.9rem;
        padding: 15px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎓 中高級認證 ‧ 學習大冒險 ✨")
    st.caption("✨ 歡迎來到可愛漫畫風檢定教室～一起快樂學族語吧！🌸")

    main_options = ["📋 認證考試說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
    current_tab = st.segmented_control("🌟 主選單導覽 🌟", main_options, default=None, label_visibility="collapsed")

    if "previous_tab" not in st.session_state:
        st.session_state.previous_tab = None

    if st.session_state.previous_tab != current_tab:
        st.session_state.submitted = False
        st.session_state.audio_triggered = False
        if "writing_submitted" in st.session_state:
            st.session_state.writing_submitted = False
        st.session_state.previous_tab = current_tab

    db = load_question_bank()

    if current_tab == "📋 認證考試說明":
        st.subheader("📋 [認證考試說明點我開啟 PDF 📄](https://lokahsu.ilrdf.org.tw/web_lokahsu/Files/Guide/1_20251211_162558.pdf)")
        st.divider()
        st.info("💡 **可愛小提示：** 請點擊上方導覽按鈕選擇你想練習的測驗項目。系統會自動載入魔法題庫為你加油喔！✨")

    elif current_tab == "🎧 聽力":
        st.subheader("🎧 聽力測驗 ‧ 耳朵動一動 (pitengil)")
        st.divider()
        listening_sub = st.radio("✨ 請選擇試題類型：", ["選擇題-聽音選詞", "選擇題-對話理解"], horizontal=True)
        if listening_sub == "選擇題-聽音選詞":
            render_section("聽音選詞", db)
        elif listening_sub == "選擇題-對話理解":
            render_section("對話理解", db)

    elif current_tab == "🗣️ 口說":
        st.subheader("🗣️ 口說測驗 ‧ 大聲說族語 (pisowal)")
        st.divider()
        speaking_sub = st.radio("✨ 請選擇試題類型：", ["段落朗讀", "情境問答", "看圖表達"], horizontal=True)
        if speaking_sub == "段落朗讀":
            render_section("段落朗讀", db)
        elif speaking_sub == "情境問答":
            render_section("情境問答", db)
        elif speaking_sub == "看圖表達":
            render_section("看圖表達", db)

    elif current_tab == "📖 閱讀":
        st.subheader("📖 閱讀測驗 ‧ 智慧大躍進 (piasip)")
        st.divider()
        reading_sub = st.radio("✨ 請選擇閱讀題型：", ["選擇題-詞彙語意", "選擇題-語言結構"], horizontal=True)
        if reading_sub == "選擇題-詞彙語意":
            render_section("詞彙語意", db)
        elif reading_sub == "選擇題-語言結構":
            render_section("語言結構", db)

    elif current_tab == "✍️ 寫作":
        st.subheader("✍️ 寫作測驗 ‧ 小小妙筆生花 (pitilid)")
        st.divider()
        writing_sub = st.radio("✨ 請選擇寫作題型：", ["句子聽寫", "問答"], horizontal=True)
        if writing_sub == "句子聽寫":
            render_section("句子聽寫", db)
        elif writing_sub == "問答":
            render_section("問答", db)

    st.write("---")
    st.markdown(f'<div class="kawaii-footer">🐾 © 2026 中高級認證 App 三一開發團隊 ｜ 系統版本：{APP_VERSION} 💕</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
