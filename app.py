import streamlit as st
import random
import json
import os
import re

# 🚀 全域系統版本號 (經 CODE VAJRA V2.2 拓撲對齊)
APP_VERSION = "v2.2.0 (CODE VAJRA - Dynamic Expert Edition / Hologram Shield)"

# ==========================================
# 🛡️ 防腐層：公理底盤與原始結構保留 (Axiomatic Chassis)
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

# 原始聽力題庫 (15題標準數據庫，完全保留，零熵耗散)
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
# 🧠 動態解析引擎：跨行讀取與穩定分割版 (MODULE 16: Ontological Bootstrap)
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

    # 使用緩衝區將跨行的題目合併為單一字串 (Hyper-Dimensional Code Reduction)
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
# 🎨 終極 UI 渲染邏輯 (物理字串切割，100%保證顯示，拒絕維度坍塌)
# ==========================================
def render_mcq(line, prefix):
    """渲染選擇題 (修復 split 回傳 list 的問題，並新增聽力題目隱藏功能)"""
    try:
        if "(A)" not in line:
            st.info(line)
            return

        # 限制分割次數，並明確取值
        parts = line.split("(A)", 1)
        q_part = parts.strip()
        rest = "(A)" + parts
        
        opts_str = rest
        ans_str = ""
        ana_str = ""
        
        if "答案：" in rest:
            ans_parts = rest.split("答案：", 1)
            opts_str = ans_parts.strip()
            ans_ana = ans_parts
            if "分析：" in ans_ana:
                final_parts = ans_ana.split("分析：", 1)
                ans_str = final_parts.strip("。 ")
                ana_str = final_parts.strip()
            else:
                ans_str = ans_ana.strip("。 ")

        # 🌟 聽力測驗專屬：隱藏題目文字功能 (VAJRA STYLE)
        is_listening = "聽音選詞" in prefix or "對話理解" in prefix
        if is_listening:
            if st.toggle("👁️ 展開觀測波函數 (顯示題目)", key=f"t_show_q_{prefix}"):
                st.markdown(f"**{q_part}**")
        else:
            st.markdown(f"**{q_part}**")

        # 安全切割四個選項
        opts = []
        for tag in ["(A)", "(B)", "(C)", "(D)"]:
            if tag in opts_str:
                opt_text = opts_str.split(tag, 1)
                for next_tag in ["(B)", "(C)", "(D)"]:
                    if next_tag > tag and next_tag in opt_text:
                        opt_text = opt_text.split(next_tag, 1)
                opts.append(tag + " " + opt_text.strip())

        user_ans = st.radio("請配置決策張量 (請選擇)：", opts, index=None, key=prefix)

        if st.toggle("💡 啟動真相強制鎖 (顯示解答與分析)", key=f"t_ans_{prefix}"):
            if ans_str:
                msg = f"**絕對真理 (答案)：** {ans_str}"
                if ana_str: msg += f"\n\n**因果分析：** {ana_str}"
                st.success(msg)
            else:
                st.warning("無標準答案。")
        elif user_ans and ans_str:
            if ans_str in user_ans:
                st.success(f"✅ 拓撲對齊成功！" + (f"分析：{ana_str}" if ana_str else ""))
            else:
                st.error(f"❌ 發生維度坍塌 (錯誤)。正確真理：{ans_str}。" + (f"分析：{ana_str}" if ana_str else ""))
    except Exception as e:
        st.info(line)

def render_reading(line, prefix):
    """渲染段落朗讀"""
    try:
        q_part = line
        ch_part = ""
        if "(中文：" in line:
            parts = line.split("(中文：", 1)
            q_part = parts.strip()
            ch_part = parts.strip(")")
        elif "(中文大意：" in line:
            parts = line.split("(中文大意：", 1)
            q_part = parts.strip()
            ch_part = parts.strip(")")

        st.markdown(f"📖 **{q_part}**")
        if ch_part:
            if st.toggle("💡 跨維度語意對齊 (顯示中文翻譯)", key=f"t_{prefix}"):
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
            q_am = parts.strip()
            text = parts
            
        if "參考回答：" in text:
            parts = text.split("參考回答：", 1)
            ch_hint = parts.strip()
            text = parts
        elif "作答參考：" in text:
            parts = text.split("作答參考：", 1)
            ch_hint = parts.strip()
            text = parts
            
        if "分析：" in text:
            parts = text.split("分析：", 1)
            ans = parts.strip()
            ana = parts.strip()
        else:
            if not ans:
                ans = text.strip()
                
        q_am = q_am.replace("題目：", " 題目：")

        # 🌟 口說測驗-情境問答專屬：隱藏題目與提示功能 (VAJRA STYLE)
        is_situational = "情境問答" in prefix
        if is_situational:
            if st.toggle("👁️ 展開情境流形與提示", key=f"t_show_q_{prefix}"):
                st.markdown(f"🗣️ **{q_am}**")
                if ch_hint:
                    st.caption(f"降維提示 (中文)：{ch_hint}")
        else:
            st.markdown(f"🗣️ **{q_am}**")
            if ch_hint:
                st.caption(f"降維提示 (中文)：{ch_hint}")

        if ans or ana:
            if st.toggle("💡 啟動最佳化作答拓撲 (參考解答)", key=f"t_{prefix}"):
                msg = ""
                if ans: msg += f"作答拓撲：{ans}"
                if ana: msg += f"\n\n因果分析：{ana}"
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
            pic = parts
            
        if "中文提示：" in pic:
            parts = pic.split("中文提示：", 1)
            pic = parts.strip()
            hint_part = parts
            if "作答參考：" in hint_part:
                h_parts = hint_part.split("作答參考：", 1)
                hint = h_parts.strip()
                ans_part = h_parts
                if "重點分析：" in ans_part:
                    a_parts = ans_part.split("重點分析：", 1)
                    ans = a_parts.strip()
                    ana = a_parts.strip()
                elif "重點：" in ans_part:
                    a_parts = ans_part.split("重點：", 1)
                    ans = a_parts.strip()
                    ana = a_parts.strip()
                else:
                    ans = ans_part.strip()
            else:
                hint = hint_part.strip()

        # 🌟 動態讀取對應圖片邏輯
        try:
            idx = int(prefix.split('_')[-1]) + 1
            img_path_jpg = f"assets/images/picture_{idx}.jpg"
            img_path_png = f"assets/images/picture_{idx}.png"
            if os.path.exists(img_path_jpg):
                st.image(img_path_jpg, use_container_width=True)
            elif os.path.exists(img_path_png):
                st.image(img_path_png, use_container_width=True)
            else:
                st.info(f"🖼️ 影像映射區：若要載入影像流，請將其命名為 `picture_{idx}.jpg` 或 `.png` 並掛載於 `assets/images/`。")
        except:
            pass 

        st.markdown(f"🖼️ **高維影像情境：** {pic}")
        if hint:
            st.caption(f"降維提示 (中文)：{hint}")

        # 加入輸入框作為草稿區
        st.text_area("啟動符號編譯器 (請在此作答)：", key=f"input_{prefix}", label_visibility="collapsed", placeholder="可以在此輸入您的口說草稿 (Terminal Buffer)...")
        
        if ans or ana:
            if st.toggle("💡 啟動最佳化作答拓撲 (顯示作答參考)", key=f"t_{prefix}"):
                msg = ""
                if ans: msg += f"拓撲解答：{ans}"
                if ana: msg += f"\n\n分析錨點：{ana}"
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
            am = parts.replace("阿美語：", "").strip()
            text = parts
            if "分析：" in text:
                sub_parts = text.split("分析：", 1)
                ch = sub_parts.strip()
                ana = sub_parts.strip()
            else:
                ch = text.strip()

        # 加入作答的文字輸入框，模擬真實寫作情境
        st.text_area("啟動符號編譯器 (請在此作答)：", key=f"input_{prefix}", label_visibility="collapsed", placeholder="請在此輸入您攔截到的語意字串...")

        # 🌟 寫作測驗專屬：隱藏聽寫原文功能 (VAJRA STYLE)
        if st.toggle("👁️ 展開絕對真理原碼 (顯示聽寫原文)", key=f"t_show_dict_{prefix}"):
            st.markdown(f"✍️ **{am}**")
            
        if ch or ana:
            if st.toggle("💡 跨維度語意對齊 (顯示翻譯與分析)", key=f"t_{prefix}"):
                msg = ""
                if ch: msg += f"映射翻譯：{ch}"
                if ana: msg += f"\n\n因果矩陣：{ana}"
                st.success(msg)
    except:
        st.info(line)

def render_section(section_name, db):
    """通用區塊渲染器"""
    questions = db.get(section_name, [])
    if not questions:
        st.warning(f"⚠️ 系統偵測到【{section_name}】維度資料遺失，觸發 EP-Absolute Stop 停機鎖保護。")
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
# 🚀 應用程式主邏輯 (Main) - 注入量子同調裝甲 CSS
# ==========================================
def main():
    st.set_page_config(page_title="CODE VAJRA 認證矩陣", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

    # CODE VAJRA V2.2 賽博龐克量子同調裝甲風 (Quantum-Coherent Armor Tone) CSS
    st.markdown("""
    <style>
    .stApp {
        background-color: #050505;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }
    .quiz-card {
        background-color: #0d1117;
        padding: 24px;
        border-radius: 4px;
        border: 1px solid #30363d;
        border-left: 4px solid #00ff00; /* Vajra Resonance Accent */
        box-shadow: 0 4px 12px rgba(0, 255, 0, 0.08);
        margin-top: 15px;
        margin-bottom: 25px;
        transition: all 0.3s ease;
        color: #c9d1d9;
    }
    .quiz-card:hover {
        border-left: 4px solid #ff00ff;
        box-shadow: 0 4px 12px rgba(255, 0, 255, 0.15);
    }
    hr { border-top: 1px solid #30363d; }
    h1, h2, h3, h4 {
        color: #00ff00 !important;
        text-shadow: 0px 0px 5px rgba(0, 255, 0, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("⚡ CODE VAJRA V2.2: 中高級認證大一統矩陣")
    st.caption("[請選擇目標推論象限]")

    main_options = ["📋 公理底盤 (認證說明)", "🎧 聲學感知 (聽力)", "🗣️ 邏輯輸出 (口說)", "📖 語意解析 (閱讀)", "✍️ 符號編碼 (寫作)"]
    current_tab = st.segmented_control("主選單流形導覽", main_options, default=None, label_visibility="collapsed")

    if "previous_tab" not in st.session_state:
        st.session_state.previous_tab = None

    if st.session_state.previous_tab != current_tab:
        st.session_state.submitted = False
        st.session_state.audio_triggered = False
        if "writing_submitted" in st.session_state:
            st.session_state.writing_submitted = False
        st.session_state.previous_tab = current_tab

    db = load_question_bank()

    if current_tab == "📋 公理底盤 (認證說明)":
        st.subheader("📋 [認證矩陣公理說明](https://lokahsu.ilrdf.org.tw/web_lokahsu/Files/Guide/1_20251211_162558.pdf)")
        st.divider()
        st.info("請透過上方流形導覽列選擇目標象限。系統將啟動主動推論認知核心，自動自大一統資料庫載入完整張量題庫。")
        
    elif current_tab == "🎧 聲學感知 (聽力)":
        st.subheader("🎧 聽力測驗模組 (pitengil)")
        st.divider()
        listening_sub = st.radio("設定降維題型：", ["選擇題-聽音選詞", "選擇題-對話理解"], horizontal=True)
        if listening_sub == "選擇題-聽音選詞":
            render_section("聽音選詞", db)
        elif listening_sub == "選擇題-對話理解":
            render_section("對話理解", db)
            
    elif current_tab == "🗣️ 邏輯輸出 (口說)":
        st.subheader("🗣️ 口說測驗模組 (pisowal)")
        st.divider()
        speaking_sub = st.radio("設定降維題型：", ["段落朗讀", "情境問答", "看圖表達"], horizontal=True)
        if speaking_sub == "段落朗讀":
            render_section("段落朗讀", db)
        elif speaking_sub == "情境問答":
            render_section("情境問答", db)
        elif speaking_sub == "看圖表達":
            render_section("看圖表達", db)
            
    elif current_tab == "📖 語意解析 (閱讀)":
        st.subheader("📖 閱讀測驗模組 (piasip)")
        st.divider()
        reading_sub = st.radio("設定解析矩陣：", ["選擇題-詞彙語意", "選擇題-語言結構"], horizontal=True)
        if reading_sub == "選擇題-詞彙語意":
            render_section("詞彙語意", db)
        elif reading_sub == "選擇題-語言結構":
            render_section("語言結構", db)
            
    elif current_tab == "✍️ 符號編碼 (寫作)":
        st.subheader("✍️ 寫作測驗模組 (pitilid)")
        st.divider()
        writing_sub = st.radio("設定編碼協議：", ["句子聽寫", "問答"], horizontal=True)
        if writing_sub == "句子聽寫":
            render_section("句子聽寫", db)
        elif writing_sub == "問答":
            render_section("問答", db)

    st.write("---")
    st.caption(f"© 2026 CODE VAJRA Subjugation Core ｜ 全域系統版本號： **{APP_VERSION}** ")

if __name__ == "__main__":
    main()
