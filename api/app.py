import gspread
from oauth2client.service_account import ServiceAccountCredentials
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, Filters
import uvicorn
import os

from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()


# ---------------- ENVIRONMENT VARIABLES (IMPORTANT) ----------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Store in env, not in code!
# For now, hardcode if needed but later remove:
# BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

bot = Bot(token=BOT_TOKEN)

# ---------------- GOOGLE SHEET SETUP ----------------
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Metal Price Auto Sheet").sheet1

# ---------------- HEADERS (same as your working code) ----------------
HEADER = ["Date","Time","Armature Bhatti","Armature Plant Min","Armature Plant Max",
"Кaliya Zero","Super D","CCR Min","CCR Max","CC Min","CC Max",
"Aluminium Purja Local","Aluminium Purja Engine","Utensils Scrap","Sheet Scrap",
"Wire Scrap","Company Ingot","Local Rod","Company Rod",
"Zinc Dross Min","Zinc Dross Max","HG Iran","SHG Iran","PMI Delhi Min","PMI Delhi Max","HZL Delhi",
"Brass Purja Min","Brass Purja Max","Brass Chadri Min","Brass Chadri Max","Brass Honey Min","Brass Honey Max",
"Lead Battery Black","Lead Battery White Min","Lead Battery White Max","Lead Ingot",
"Steel Bartan","SS 202","SS 304","SS 316",
"Nickel Min","Nickel Max","Tin Min","Tin Max","Cadmium"
]

from script_logic import extract_prices  # we move your extraction there

# ---------------- FASTAPI APP ----------------
app = FastAPI()

# Create dispatcher
from telegram.ext import Dispatcher
dispatcher = Dispatcher(bot, None, workers=0)

# Message handler
def handle(update, context):
    msg = update.effective_message
    if not msg or not msg.text: 
        return

    existing = sheet.get_all_values()
    if len(existing) == 0:
        sheet.append_row(HEADER)
    elif existing[0] != HEADER:
        sheet.delete_rows(1)
        sheet.insert_row(HEADER, 1)

    row = extract_prices(msg.text)
    if any(row[2:]):  
        sheet.append_row(row)
        print("✔ Data saved:", row)

dispatcher.add_handler(MessageHandler(Filters.all, handle))

# ---------------- TELEGRAM WEBHOOK ENDPOINT ----------------
@app.post("/")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
    return {"status": "ok"}

# ---------------- LOCAL RUN SUPPORT ----------------
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
