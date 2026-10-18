# 📊 WhatsApp Chat Analyzer

A Streamlit web app that turns an exported WhatsApp chat into interactive insights:
message stats, timelines, activity heatmaps, word clouds, top words and emoji analysis.

🔗 **Live demo:** (https://8y8zcyozk2baqt2sppcimv.streamlit.app/)

## ✨ Features
- Overall or per-user analysis
- Total messages, words, media and links shared
- Monthly and daily timelines
- Most busy day, month and weekly activity heatmap
- Most active users (group level)
- Word cloud and most common words (Hinglish stop-words supported)
- Emoji analysis with pie chart
- Supports 24-hour and AM/PM export formats

## 🛠 Tech Stack
Python · Pandas · Streamlit · Matplotlib · Seaborn · WordCloud · urlextract · emoji · Pytest

## 📂 Project Structure
| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI |
| `preprocessor.py` | Parses raw chat text into a DataFrame using regex |
| `helper.py` | Analysis functions (stats, timelines, wordcloud, emoji) |
| `tests/` | Pytest unit tests for the parser |
| `sample_chat.txt` | Dummy chat to try the app |

## 🚀 Run Locally
```bash
git clone https://github.com/Reyaz99578/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 📱 How to export your chat
WhatsApp → open chat → ⋮ menu → More → **Export chat** → **Without media**.
Upload the `.txt` file in the app sidebar.

## 🧪 Run Tests
```bash
pytest
```

## 🔒 Privacy
The uploaded chat is processed in memory only and is never stored.

## 🧠 What I Learned
- Parsing messy real-world text with regex (multi-line messages, 12h/24h formats)
- Debugging library version changes (emoji 2.x, pandas 2.x)
- Handling edge cases: empty results, group notifications, missing stop-words file
- Writing unit tests for data preprocessing

## 👤 Author
**Reyaz Ansari** · [GitHub](https://github.com/Reyaz99578) · [LinkedIn](YOUR_LINKEDIN_URL)
