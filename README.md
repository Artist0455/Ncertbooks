# NCERT Books Download Bot


This bot lets Telegram users select a class and book, then downloads the PDF from a known catalog of links.


## Quick start (local)
1. Create a Telegram Bot with @BotFather and copy the token.
2. Clone this repo (or copy these files).
3. Create and activate a Python 3.10+ venv.
4. `pip install -r requirements.txt`
5. Export your token: `export BOT_TOKEN=123456:ABC...`
6. `python main.py`


## Deploy on Render
1. Push this project to a public GitHub repo.
2. On Render → **New +** → **Blueprint** → pick your repo (or **Web Service** → **Worker** and paste `render.yaml`).
3. Add environment variable **BOT_TOKEN** with your BotFather token.
4. Deploy.


## Add or edit books
Edit `data/catalog.json`. Use this structure:


```json
{
"Class 10": {
"Mathematics (English) 2024-25": "https://example.com/path/to/Maths_Class10_Eng_2024-25.pdf",
"Science (Hindi) 2024-25": "https://example.com/path/to/Science_Class10_Hin_2024-25.pdf"
},
"Class 12": {
"Physics Part 1 (English) 2024-25": "https://example.com/path/to/Physics_Part1_Class12_Eng.pdf",
"Physics Part 2 (English) 2024-25": "https://example.com/path/to/Physics_Part2_Class12_Eng.pdf"
}
}
