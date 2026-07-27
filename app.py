沒問題！身為一位精通 Streamlit 與前端 CSS 的資深 Python 工程師，我已經為您將這個阿美語中高級認證 App 的前端設計，徹底改造成乾淨、專業的**「極簡北歐冷調風 (Minimalist Nordic Cold Tone)」**。

為了達到無刪減的承諾，以下程式碼**「完全保留」**了您提供的所有資料結構（包含 15 題聽力資料庫）、註解以及版面邏輯防腐層，絕不使用「...」或「略」，您可以直接複製並執行：

```python
import streamlit as st
import random
import json
import os  # 引入 OS 模組，用於物理檔案路徑防禦性偵測

### 🚀 新增：定義全域系統版本號 (每次更新只需修改這裡)
APP_VERSION = "v2.0.0 (Build 20260619)"

### ---- 1. 頁面佈局設定 (Code-CRF v9.0 運行時配置) ----
st.set_page_config( page_title="中高級認證", page_icon="🎓", layout="centered", initial_sidebar_state="collapsed" )

### ---- 2. 自動適應雙模式的 CSS 設計 (UIUX-CRF v9.0 視覺熵減) ----
st.markdown("""
<style>
/* 核心題目卡片式容器：只有顯式宣告的卡片才會擁有此風格 (極簡北歐冷調風) */
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
</style>
""", unsafe_allow_html=True)

### ---- App 頂部導覽列 ----
st.title("🎓 中高級認證")

### 🛠️ 修正 1：對齊您截圖中的文字
st.caption("[請選擇練習平台]")

### ---- 第一層：五個主要選項 (導覽選單) ----
main_options = ["📋 認證考試說明", "🎧 聽力", "🗣️ 口說", "📖 閱讀", "✍️ 寫作"]
current_tab = st.segmented_control(
    "主選單導覽", main_options, default=None,  # 🚀 修正 2：設為 None，代表一進來「不預設選取任何頁面」，保持畫面純淨
    label_visibility="collapsed"
)

### ---- 🧠 跨頁面狀態解耦防腐層 ----
if "previous_tab" not in st.session_state:
    # 🚀 修正 3：初始狀態同步設為 None
    st.session_state.previous_tab = None

if st.session_state.previous_tab != current_tab:
    st.session_state.submitted = False
    st.session_state.audio_triggered = False
    if "writing_submitted" in st.session_state:
        st.session_state.writing_submitted = False

### ---- 3. 原始聽力題庫 (15題標準數據庫) ----
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

### ---- 第二層：根據選擇顯示對應架構 ----
### 1. 📋 認證考試說明頁面
if current_tab == "📋 認證考試說明":
    st.subheader("📋 認證考試說明")
    st.divider()

### 2. 🎧 聽力測驗
elif current_tab == "🎧 聽力":
    st.subheader("🎧 聽力測驗 (pitengil)")
    st.divider()
    listening_sub = st.radio(
        "題型選擇：", ["選擇題-聽音選詞", "選擇題-對話理解"], horizontal=True
    )

### 3. 🗣️ 口說測驗
elif current_tab == "🗣️ 口說":
    st.subheader("🗣️ 口說測驗 (pisowal)")
    st.divider()
    speaking_sub = st.radio(
        "題型選擇：", ["段落朗讀", "情境問答", "看圖表達"], horizontal=True
    )

### 4. 📖 閱讀測驗
elif current_tab == "📖 閱讀":
    st.subheader("📖 閱讀測驗 (piasip)")
    st.divider()
    reading_sub = st.radio(
        "閱讀題型選擇：", ["選擇題-詞彙語意", "選擇題-語言結構"], horizontal=True
    )

### 5. ✍️ 寫作測驗
elif current_tab == "✍️ 寫作":
    st.subheader("✍️ 寫作測驗 (pitilid)")
    st.divider()
    writing_sub = st.radio(
        "寫作題型選擇：", ["句子聽寫", "問答"], horizontal=True
    )

### ---- App 底部註腳 ----
st.write("---")
st.caption(f"© 2026 中高級認證 App 三一開發團隊 ｜ 系統版本： **{APP_VERSION}** ")
```

以上的程式碼已為您確實還原並保留了原始專案提供的全域系統版本號、分頁導覽控制狀態、15 題聽力題庫結構以及第二層的頁面架構邏輯。並且，我依據您的提示詞指令對 CSS 部分進行了深度的重構，以偏冷的淺灰與高對比的深色字體打造出清爽無干擾的閱讀體驗。
