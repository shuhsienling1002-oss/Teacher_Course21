import streamlit as st
import random
import json
import os
import re

# 🚀 全域系統版本號
APP_VERSION = "v2.1.4 (Build 20260727 - Lazy Boho Edition)"

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

# 原始聽力題庫 (完全保留)
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
# 🧠 動態解析引擎 (保留原始邏輯)
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
        if not line:
            save_question()
            continue
            
        if "一、選擇題（聽音選詞）" in line: save_question(); current_section = "聽音選詞"
        elif "二、選擇題（對話理解）" in line: save_question(); current_section = "對話理解"
        elif "三、段落朗讀" in line: save_question(); current_section = "段落朗讀"
        elif "四、情境問答" in line: save_question(); current_section = "情境問答"
        elif "五、看圖表達" in line: save_question(); current_section = "看圖表達"
        elif "六、選擇題（詞彙語意）" in line: save_question(); current_section = "詞彙語意"
        elif "七、選擇題（語言結構）" in line: save_question(); current_section = "語言結構"
        elif "八、句子聽寫" in line: save_question(); current_section = "句子聽寫"
        elif "九、問答" in line: save_question(); current_section = "問答"
        
        elif re.match(r'^\d+[\.、]', line):
            save_question()
            current_question.append(line)
        else:
            if current_question:
                current_question.append(line)
                
    save_question() 
            
    return db

# ==========================================
# 🎨 UI 渲染邏輯 (保留邏輯，僅微調 Icon 以配合風格)
# ==========================================
def render_mcq(line, prefix):
    """渲染選擇題"""
    try:
        if "(A)" not in line:
            st.info(line)
            return

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

        is_listening = "聽音選詞" in prefix or "對話理解" in prefix
        if is_listening:
            if st.toggle("🌙 顯示題目文字", key=f"t_show_q_{prefix}"):
                st.markdown(f"**{q_part}**")
        else:
            st.markdown(f"**{q_part}**")
        
        opts = []
        for tag in ["(A)", "(B)", "(C)", "(D)"]:
            if tag in opts_str:
                opt_text = opts_str.split(tag, 1)[1]
                for next_tag in ["(B)", "(C)", "(D)"]:
                    if next_tag > tag and next_tag in opt_text:
                        opt_text = opt_text.split(next_tag, 1)[0]
                opts.append(tag + " " + opt_text.strip())

        # 慵懶風不強迫回答，index=None 很棒
        user_ans = st.radio("✨ 請選擇：", opts, index=None, key=prefix)
        
        if st.toggle("💡 解答", key=f"t_ans_{prefix}"):
            if ans_str:
                msg = f"**正確答案：** {ans_str}"
                if ana_str: msg += f"\n\n**分析：** {ana_str}"
                st.success(msg)
            else:
                st.warning("無標準答案。")
        elif user_ans and ans_str:
            if ans_str in user_ans:
                st.success(f"🌻 正確！" + (f"分析：{ana_str}" if ana_str else ""))
            else:
                st.error(f"☁️ 錯誤。正確答案：{ans_str}。" + (f"分析：{ana_str}" if ana_str else ""))
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
            if st.toggle("🍃 中文翻譯", key=f"t_{prefix}"):
                st.success(ch_part)
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
        
        is_situational = "情境問答" in prefix
        if is_situational:
            if st.toggle("🌙 顯示題目與提示", key=f"t_show_q_{prefix}"):
                st.markdown(f"🗣️ **{q_am}**")
                if ch_hint:
                    st.caption(f"中文提示：{ch_hint}")
        else:
            st.markdown(f"🗣️ **{q_am}**")
            if ch_hint:
                st.caption(f"中文提示：{ch_hint}")
            
        if ans or ana:
            if st.toggle("💡 參考解答", key=f"t_{prefix}"):
                msg = ""
                if ans: msg += f"參考解答：{ans}"
                if ana: msg += f"\n\n分析：{ana}"
                st.success(msg)
    except:
        st.info(line)

def render_picture(line, prefix):
    """渲染看圖表達"""
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
        
        try:
            idx = int(prefix.split('_')[-1]) + 1
            img_path_jpg = f"assets/images/picture_{idx}.jpg"
            img_path_png = f"assets/images/picture_{idx}.png"
            
            if os.path.exists(img_path_jpg):
                st.image(img_path_jpg, use_container_width=True)
            elif os.path.exists(img_path_png):
                st.image(img_path_png, use_container_width=True)
            else:
                # 佔位區也溫柔一點
                st.caption(f"🎨 [ 圖片預留區：picture_{idx}.jpg ]")
        except:
            pass

        st.markdown(f"🖼️ **圖片情境：** {pic}")
        
        if hint:
            st.caption(f"中文提示：{hint}")
            
        st.text_area("✍️ 筆記 / 草稿：", key=f"input_{prefix}", label_visibility="collapsed", placeholder="可以在此輸入您的口說草稿...")
            
        if ans or ana:
            if st.toggle("💡 作答參考", key=f"t_{prefix}"):
                msg = ""
                if ans: msg += f"作答參考：{ans}"
                if ana: msg += f"\n\n重點：{ana}"
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
        
        st.text_area("✍️ 聽寫作答：", key=f"input_{prefix}", label_visibility="collapsed", placeholder="請在此輸入您聽寫的句子...")
        
        if st.toggle("🌙 顯示聽寫原文", key=f"t_show_dict_{prefix}"):
            st.markdown(f"🖋️ **{am}**")
            
        if ch or ana:
            if st.toggle("💡 翻譯與分析", key=f"t_{prefix}"):
                msg = ""
                if ch: msg += f"中文：{ch}"
                if ana: msg += f"\n\n分析：{ana}"
                st.success(msg)
    except:
        st.info(line)

def render_section(section_name, db):
    """通用區塊渲染器 (保留)"""
    questions = db.get(section_name, [])
    if not questions:
        st.warning(f"⚠️ 找不到【{section_name}】的資料。")
        return

    for i, line in enumerate(questions):
        with st.container():
            # HTML 結構保留，透過 CSS 改變外觀
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
    # 修改 Page Icon 為更慵懶的符號
    st.set_page_config(page_title="中高級認證", page_icon="☕", layout="centered", initial_sidebar_state="collapsed")

    # ==========================================
    # 🎨 慵懶 Boho 風格 (Lazy Boho / Cozy Style) CSS
    # ==========================================
    st.markdown("""
    <style>
    /* 引入 Google Fonts: Handlee (手寫感) 與 Noto Sans TC */
    @import url('https://fonts.googleapis.com/css2?family=Handlee&family=Noto+Sans+TC:wght@400;500;700&display=swap');

    /* 全域字體設定 */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Noto Sans TC', sans-serif;
        background-color: #FDFCF5; /* 極淡的米奶油色背景 */
        color: #5D5046; /* 柔和的深褐，代替純黑 */
    }

    /* 標題設定 (h1, h2, h3) */
    h1, h2, h3 {
        font-family: 'Handlee', 'Noto Sans TC', cursive;
        color: #8E735B; /* 暖咖啡色 */
        font-weight: 400;
    }

    /* 慵懶風題目卡片 */
    .quiz-card {
        background-color: #FFFFFF; /* 純白卡片 */
        padding: 30px; /* 增加內距，更有呼吸感 */
        border-radius: 20px; /* 超大圓角 */
        border: 1px solid #F1E9D9; /* 極淡的暖色邊框 */
        
        /* 柔和擴散的陰影，營造漂浮感 */
        box-shadow: 0 10px 25px rgba(142, 115, 91, 0.08); 
        
        margin-top: 20px;
        margin-bottom: 30px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    /* 滑過卡片時有輕微互動 */
    .quiz-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(142, 115, 91, 0.12);
    }

    /* 修正 Streamlit 默認 hr 樣式 */
    hr { border-top: 1px solid #F1E9D9; }

    /* 自定義 Radio Button 樣式 (粗略模擬 Boho 感) */
    div[data-testid="stRadio"] > label {
        color: #5D5046;
        padding-bottom: 5px;
    }
    
    /* 讓 Segmented Control (主選單) 也變圓潤 */
    div[data-testid="stSegmentedControl"] button {
        border-radius: 15px !important;
        border: 1px solid #F1E9D9 !important;
        background-color: white !important;
        color: #8E735B !important;
    }
    div[data-testid="stSegmentedControl"] button[aria-selected="true"] {
        background-color: #E6DCCF !important; /* 選取時變為暖沙色 */
        color: #5D5046 !important;
        border: 1px solid #E6DCCF !important;
    }

    /* Input Box 與 Textarea 圓角 */
    .stTextArea textarea, .stTextInput input {
        border-radius: 15px !important;
        border: 1px solid #F1E9D9 !important;
        background-color: #FDFCF5 !important;
    }

    /* 隱藏預設的 Streamlit Header/Footer 以保持乾淨 */
    header, footer {visibility: hidden;}
    
    /* 讓 Caption 更淡更柔和 */
    .stCaption {
        color: #A39689 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 主標題使用預設 st.title，但 CSS 已將其改為 Handlee 字體
    st.title("☕ 中高級認證練習")
    st.caption("[ 找個舒服的位置，我們開始吧 ]")

    main_options = ["📋 考試說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
    # segmented_control 在 CSS 中已被美化
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

    if current_tab == "📋 考試說明":
        # Subheader 也會變成 Handlee 字體
        st.subheader("🍂 [認證考試說明](https://lokahsu.ilrdf.org.tw/web_lokahsu/Files/Guide/1_20251211_162558.pdf)")
        st.divider()
        st.info("請透過上方導覽列選擇項目。靜下心來練習，這不是考試，是一次學習的旅程。")

    elif current_tab == "🎧 聽力":
        st.subheader("🎧 聽力測驗")
        st.divider()
        listening_sub = st.radio("題型：", ["選擇題-聽音選詞", "選擇題-對話理解"], horizontal=True)
        if listening_sub == "選擇題-聽音選詞":
            render_section("聽音選詞", db)
        elif listening_sub == "選擇題-對話理解":
            render_section("對話理解", db)

    elif current_tab == "🗣️ 口說":
        st.subheader("🗣️ 口說測驗")
        st.divider()
        speaking_sub = st.radio("題型：", ["段落朗讀", "情境問答", "看圖表達"], horizontal=True)
        if speaking_sub == "段落朗讀":
            render_section("段落朗讀", db)
        elif speaking_sub == "情境問答":
            render_section("情境問答", db)
        elif speaking_sub == "看圖表達":
            render_section("看圖表達", db)

    elif current_tab == "📖 閱讀":
        st.subheader("📖 閱讀測驗")
        st.divider()
        reading_sub = st.radio("題型：", ["選擇題-詞彙語意", "選擇題-語言結構"], horizontal=True)
        if reading_sub == "選擇題-詞彙語意":
            render_section("詞彙語意", db)
        elif reading_sub == "選擇題-語言結構":
            render_section("語言結構", db)

    elif current_tab == "✍️ 寫作":
        st.subheader("✍️ 寫作測驗這是一個專為中高級認證練習設計的慵懶風格版面。整體採用了溫暖的米色和奶油色調，搭配莫蘭迪色系的導覽按鈕（土耳其藍、橄欖綠、柔沙色），呈現出輕鬆、不費力的氛圍。

卡片設計擁有柔軟的圓角和擴散陰影，營造出一種舒適的浮動感。標題字體更具人情味，與原本冷硬的樣式形成對比。在聽力測驗的示範中，您可以看到圓形的選項設計和簡單的切換開關，非常適合放鬆地進行學習。

如果您需要，我可以協助將現有的 CSS 樣式程式碼修改為這個版本，只需幾分鐘即可完成風格轉換。
