from telegram.ext import Updater, MessageHandler, Filters
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

BOT_TOKEN = "8529310569:AAFWbF4z-wwfz56d4i6LkdV5LCu4MhUhFpg"

# Google Sheet Setup
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Metal Price Auto Sheet").sheet1

# Create header row only once
HEADER = ["Date","Time","Armature Bhatti","Armature Plant Min","Armature Plant Max",
          "Kaliya Zero","Super D","CCR Min","CCR Max","CC Min","CC Max",
          "Aluminium Purja Local","Aluminium Purja Engine","Utensils Scrap","Sheet Scrap",
          "Wire Scrap","Company Ingot","Local Rod","Company Rod",
          "Zinc Dross Min","Zinc Dross Max","HG Iran","SHG Iran","PMI Delhi Min","PMI Delhi Max","HZL Delhi",
          "Brass Purja Min","Brass Purja Max","Brass Chadri Min","Brass Chadri Max","Brass Honey Min","Brass Honey Max",
          "Lead Battery Black","Lead Battery White Min","Lead Battery White Max","Lead Ingot",
          "Steel Bartan","SS 202","SS 304","SS 316",
          "Nickel Min","Nickel Max","Tin Min","Tin Max","Cadmium"
]


def extract_prices(text):
    def find(pattern):
        m = re.search(pattern, text)
        return m.group(1) if m else ""

    def find_pair(pattern):
        m = re.search(pattern, text)
        return (m.group(1), m.group(2)) if m else ("","")

    # Brass
    purja = find_pair(r"Purja\s*:\s*(\d+)\+?/?(\d+)?")
    chadri = find_pair(r"Chadri\s*:\s*(\d+)\+?/?(\d+)?")
    honey = find_pair(r"Honey\s*:\s*(\d+)\+?/?(\d+)?")

    # Copper
    arm_bhatti = find(r"Armature\s*\(Bhatti\)\s*:\s*(\d+)")
    arm_plant = find_pair(r"Armature\s*\(Plant\)\s*:\s*(\d+)\+?/?(\d+)?")
    kaliya = find(r"Kaliya\s*\(Zero\)\s*Rod\s*:\s*(\d+)")
    super_d = find(r"Super D Rod\s*:\s*(\d+)")
    ccr = find_pair(r"CCR Rod\s*:\s*(\d+)\+?/?(\d+)?")
    cc = find_pair(r"CC Rod\s*:\s*(\d+)\+?/?(\d+)?")

    # Aluminium
    purja_local = find(r"Purja\s*\(Local\)\s*:\s*(\d+)")
    purja_engine = find(r"Purja\s*\(Engine, Imported\)\s*:\s*(\d+)")
    utensil = find(r"Utensils Scrap\s*:\s*(\d+)")
    sheet_scrap = find(r"Sheet Scrap\s*:\s*(\d+)")
    wire = find(r"Wire Scrap\s*:\s*(\d+)")
    ingot = find(r"Company Ingot\s*:\s*(\d+)")
    local_rod = find_pair(r"Local Rod\s*:\s*(\d+)\+?/?(\d+)?")
    comp_rod = find(r"Company Rod\s*:\s*(\d+)")

    # Zinc
    dross = find_pair(r"Dross\s*:\s*(\d+)\+?/?(\d+)?")
    hg = find(r"HG\s*\(Iran\)\s*:\s*(\d+)")
    shg = find(r"SHG\s*\(Iran\)\s*:\s*(\d+)")
    pmi = find_pair(r"PMI\s*\(Delhi\)\s*:\s*(\d+)\+?/?(\d+)?")
    hzl = find(r"HZL\s*\(Delhi\)\s*:\s*(\d+)")

    # Lead
    lead_black = find(r"Battery Scrap\s*\(Black\)\s*:\s*(\d+)")
    lead_white = find_pair(r"Battery Scrap\s*\(White\)\s*:\s*(\d+)\+?/?(\d+)?")
    lead_ingot = find(r"Ingot\s*:\s*(\d+)")

    # Steel & Other Metals
    steel_bartan = find(r"BARTAN\s*:\s*(\d+)")
    ss202 = find(r"SS 202\s*:\s*(\d+)")
    ss304 = find(r"SS 304\s*:\s*(\d+)")
    ss316 = find(r"SS 316\s*:\s*(\d+)")
    nickel = find_pair(r"NICKEL\s*:\s*(\d+)\+?/?(\d+)?")
    tin = find_pair(r"TIN\s*:\s*(\d+)\+?/?(\d+)?")
    cadmium = find(r"CADMIUM\s*:\s*(\d+)")

    # Date & Time
    date = find(r"DATE\s*:\s*(.*)")
    time = find(r"TIME\s*:\s*(.*)")

    return [
        date, time,
        arm_bhatti, arm_plant[0], arm_plant[1],
        kaliya, super_d, ccr[0], ccr[1], cc[0], cc[1],
        purja_local, purja_engine, utensil, sheet_scrap,
        wire, ingot, local_rod[0], local_rod[1], comp_rod,
        dross[0], dross[1], hg, shg, pmi[0], pmi[1], hzl,
        purja[0], purja[1], chadri[0], chadri[1], honey[0], honey[1],
        lead_black, lead_white[0], lead_white[1], lead_ingot,
        steel_bartan, ss202, ss304, ss316,
        nickel[0], nickel[1], tin[0], tin[1], cadmium
    ]


def on_msg(update, context):
    msg = update.effective_message  
    if not msg or not msg.text:
        print("⚠️ Ignored non-text or preview event")
        return
    
    # HEADER CHECK (safe)
    existing = sheet.get_all_values()

    if len(existing) == 0:
        sheet.append_row(HEADER)
        print("🟥 Header added (sheet was empty)")

    elif existing[0] != HEADER:
        print("⚠️ Wrong header detected. Fixing...")
        sheet.delete_rows(1)              # remove only first row
        sheet.insert_row(HEADER, 1)       # add correct header
        print("🟩 Header fixed (old data kept)")

    text = msg.text
    row = extract_prices(text)

    print("📩 MESSAGE DETECTED")

    # SAVE DATA ONLY IF VALUES WERE FOUND
    if any(row[2:]):  
        sheet.append_row(row)
        print("✔ Appended to Google Sheet:", row)
    else:
        print("⚠️ No valid data found, skipped")


updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.all, on_msg))


print("🤖 Bot running... Waiting for Telegram messages")
updater.start_polling()
updater.idle()
