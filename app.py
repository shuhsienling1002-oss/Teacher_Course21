import streamlit as st
import random
import json
import os
import re

# 🚀 全域系統版本號
APP_VERSION = "v2.2.0 (Build 20260727 - Form-Based Interactive Mode)"

# ==========================================
# 🛡️ 防腐層：已解除封印，啟動動態狀態記憶
# ==========================================
VOCABULARY = []
SENTENCES = []

def init_quiz():
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
# 🎨 終極 UI 渲染邏輯 (導入真實互動表單沙盒)
# ==========================================
def render_mcq(line, prefix):
    """渲染選擇題 (真實互動表單模式：作答後鎖定並顯示解答)"""
    try:
        if "(A)" not in line:
            st.info(line)
            return

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

        opts = []
        for tag in ["(A)", "(B)", "(C)", "(D)"]:
            if tag in opts_str:
                opt_text = opts_str.split(tag, 1)
                for next_tag in ["(B)", "(C)", "(D)"]:
                    if next_tag > tag and next_tag in opt_text:
                        opt_text = opt_text.split(next_tag, 1)
                opts.append(tag + " " + opt_text.strip())

        # 🌟 建立獨立的表單沙盒
        with st.form(key=f"form_mcq_{prefix}"):
            is_listening = "聽音選詞" in prefix or "對話理解" in prefix
            if is_listening:
                if st.toggle("👁️ 顯示題目文字 (聽力輔助)", key=f"t_show_q_{prefix}"):
                    st.markdown(f"**{q_part}**")
                else:
                    st.caption("🎧 請聆聽音檔後作答 (點擊上方按鈕可顯示題目文字)")
            else:
                st.markdown(f"**{q_part}**")

            # 使用者在此作答
            user_ans = st.radio("請選擇：", opts, index=None)
            
            # 送出按鈕
            submitted = st.form_submit_button("💡 送出作答並查看解答")
            
            # 檢查送出狀態
            if submitted:
                if user_ans is None:
                    st.warning("⚠️ 請先選擇一個選項再送出！")
                else:
                    st.session_state[f"locked_ans_{prefix}"] = user_ans

        # 表單外部：根據 session_state 顯示結果，防止頁面刷新導致答案消失
        if f"locked_ans_{prefix}" in st.session_state:
            locked_ans = st.session_state[f"locked_ans_{prefix}"]
            st.info(f"您的選擇： {locked_ans}")
            
            if ans_str:
                if ans_str in locked_ans:
                    st.success(f"✅ 正確！" + (f"\n\n**分析：** {ana_str}" if ana_str else ""))
                else:
                    st.error(f"❌ 錯誤。正確答案：{ans_str}。" + (f"\n\n**分析：** {ana_str}" if ana_str else ""))
            else:
                st.warning("本題無標準答案。")
    except Exception as e:
        st.info(line)

def render_reading(line, prefix):
    """渲染段落朗讀 (真實互動表單模式)"""
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
        
        with st.form(key=f"form_read_{prefix}"):
            st.markdown(f"📖 **{q_part}**")
            
            # 確保使用者有進行互動才顯示翻譯
            submitted = st.form_submit_button("👁️ 朗讀完畢，顯示中文翻譯")
            if submitted:
                st.session_state[f"locked_read_{prefix}"] = True
                
        if st.session_state.get(f"locked_read_{prefix}", False) and ch_part:
            st.success(f"**中文翻譯：** {ch_part}")
    except:
        st.info(line)

def render_qa(line, prefix):
    """渲染問答與情境問答 (真實互動表單模式)"""
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

        with st.form(key=f"form_qa_{prefix}"):
            is_situational = "情境問答" in prefix
            if is_situational:
                if st.toggle("👁️ 顯示題目與提示", key=f"t_show_q_{prefix}"):
                    st.markdown(f"🗣️ **{q_am}**")
                    if ch_hint: st.caption(f"中文提示：{ch_hint}")
                else:
                    st.caption("🎧 請聆聽情境後作答 (點擊上方按鈕可顯示提示)")
            else:
                st.markdown(f"🗣️ **{q_am}**")
                if ch_hint: st.caption(f"中文提示：{ch_hint}")
                
            user_input = st.text_area("請在此作答：", placeholder="請輸入您的答案...", label_visibility="collapsed")
            submitted = st.form_submit_button("💡 送出作答並查看解答")
            
            if submitted:
                if not user_input.strip():
                    st.warning("⚠️ 請先輸入您的答案再送出！")
                else:
                    st.session_state[f"locked_qa_ans_{prefix}"] = user_input

        if f"locked_qa_ans_{prefix}" in st.session_state:
            st.info(f"您的作答：\n{st.session_state[f'locked_qa_ans_{prefix}']}")
            if ans or ana:
                msg = ""
                if ans: msg += f"**參考解答：** {ans}"
                if ana: msg += f"\n\n**分析：** {ana}"
                st.success(msg)
    except:
        st.info(line)

def render_picture(line, prefix):
    """渲染看圖表達 (真實互動表單模式)"""
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

        try:
            idx = int(prefix.split('_')[-1]) + 1
            img_path_jpg = f"assets/images/picture_{idx}.jpg"
            img_path_png = f"assets/images/picture_{idx}.png"
            
            if os.path.exists(img_path_jpg):
                st.image(img_path_jpg, use_container_width=True)
            elif os.path.exists(img_path_png):
                st.image(img_path_png, use_container_width=True)
            else:
                st.info(f"🖼️ 圖片佔位區：請將圖片命名為 `picture_{idx}.jpg` 並放置於 `assets/images/`。")
        except:
            pass 

        with st.form(key=f"form_pic_{prefix}"):
            st.markdown(f"🖼️ **圖片情境：** {pic}")
            if hint:
                st.caption(f"中文提示：{hint}")
                
            user_input = st.text_area("請在此作答草稿：", placeholder="可以在此輸入您的口說草稿...", label_visibility="collapsed")
            submitted = st.form_submit_button("💡 送出作答並查看參考")
            
            if submitted:
                if not user_input.strip():
                    st.warning("⚠️ 請先輸入您的草稿或答案再送出！")
                else:
                    st.session_state[f"locked_pic_ans_{prefix}"] = user_input

        if f"locked_pic_ans_{prefix}" in st.session_state:
            st.info(f"您的草稿：\n{st.session_state[f'locked_pic_ans_{prefix}']}")
            if ans or ana:
                msg = ""
                if ans: msg += f"**作答參考：** {ans}"
                if ana: msg += f"\n\n**重點：** {ana}"
                st.success(msg)
    except:
        st.info(line)

def render_dictation(line, prefix):
    """渲染句子聽寫 (真實互動表單模式)"""
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
        
        with st.form(key=f"form_dic_{prefix}"):
            st.caption("🎧 請聆聽音檔並進行聽寫。")
            user_input = st.text_area("請在此作答：", placeholder="請輸入您聽寫的句子...", label_visibility="collapsed")
            submitted = st.form_submit_button("👁️ 送出作答並查看原文")
            
            if submitted:
                if not user_input.strip():
                    st.warning("⚠️ 請先輸入聽寫內容再送出！")
                else:
                    st.session_state[f"locked_dic_ans_{prefix}"] = user_input

        if f"locked_dic_ans_{prefix}" in st.session_state:
            st.info(f"您的聽寫：\n{st.session_state[f'locked_dic_ans_{prefix}']}")
            st.markdown(f"✍️ **標準原文：** {am}")
            if ch or ana:
                msg = ""
                if ch: msg += f"**中文：** {ch}"
                if ana: msg += f"\n\n**分析：** {ana}"
                st.success(msg)
    except:
        st.info(line)

def render_section(section_name, db):
    """通用區塊渲染器"""
    questions = db.get(section_name, [])
    if not questions:
        st.warning(f"⚠️ 系統抓不到【{section_name}】的資料。")
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
    st.set_page_config(page_title="中高級認證", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed")
    
    # 🌊 深度海洋風格 (Deep Ocean Style) CSS
    st.markdown("""
    <style>
    .quiz-card {
        background-color: #E0F7FA;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #80DEEA;
        box-shadow: 0 4px 12px rgba(0, 96, 100, 0.15);
        margin-top: 15px;
        margin-bottom: 25px;
        transition: all 0.3s ease;
        color: #004D40;
    }
    .quiz-card:hover {
        box-shadow: 0 8px 24px rgba(0, 151, 167, 0.25);
        border-color: #4DD0E1;
    }
    hr { border-top: 1px solid #B2EBF2; }
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

    if current_tab == "📋 認證考試說明":
        st.subheader("📋 [認證考試說明](https://lokahsu.ilrdf.org.tw/web_lokahsu/Files/Guide/1_20251211_162558.pdf)")
        st.divider()
        st.info("請透過上方導覽列選擇您要進行的測驗項目。系統將自動從資料庫載入完整題庫。作答時，需點擊送出才會顯示解答。")

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
