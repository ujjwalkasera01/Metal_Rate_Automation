# import re


# def extract_prices(text):
#     def find(pattern):
#         m = re.search(pattern, text)
#         return m.group(1) if m else ""

#     def find_pair(pattern):
#         m = re.search(pattern, text)
#         return (m.group(1), m.group(2)) if m else ("","")

#     # Brass
#     purja = find_pair(r"Purja\s*:\s*(\d+)\+?/?(\d+)?")
#     chadri = find_pair(r"Chadri\s*:\s*(\d+)\+?/?(\d+)?")
#     honey = find_pair(r"Honey\s*:\s*(\d+)\+?/?(\d+)?")

#     # Copper
#     arm_bhatti = find(r"Armature\s*\(Bhatti\)\s*:\s*(\d+)")
#     arm_plant = find_pair(r"Armature\s*\(Plant\)\s*:\s*(\d+)\+?/?(\d+)?")
#     kaliya = find(r"Kaliya\s*\(Zero\)\s*Rod\s*:\s*(\d+)")
#     super_d = find(r"Super D Rod\s*:\s*(\d+)")
#     ccr = find_pair(r"CCR Rod\s*:\s*(\d+)\+?/?(\d+)?")
#     cc = find_pair(r"CC Rod\s*:\s*(\d+)\+?/?(\d+)?")

#     # Aluminium
#     purja_local = find(r"Purja\s*\(Local\)\s*:\s*(\d+)")
#     purja_engine = find(r"Purja\s*\(Engine, Imported\)\s*:\s*(\d+)")
#     utensil = find(r"Utensils Scrap\s*:\s*(\d+)")
#     sheet_scrap = find(r"Sheet Scrap\s*:\s*(\d+)")
#     wire = find(r"Wire Scrap\s*:\s*(\d+)")
#     ingot = find(r"Company Ingot\s*:\s*(\d+)")
#     local_rod = find_pair(r"Local Rod\s*:\s*(\d+)\+?/?(\d+)?")
#     comp_rod = find(r"Company Rod\s*:\s*(\d+)")

#     # Zinc
#     dross = find_pair(r"Dross\s*:\s*(\d+)\+?/?(\d+)?")
#     hg = find(r"HG\s*\(Iran\)\s*:\s*(\d+)")
#     shg = find(r"SHG\s*\(Iran\)\s*:\s*(\d+)")
#     pmi = find_pair(r"PMI\s*\(Delhi\)\s*:\s*(\d+)\+?/?(\d+)?")
#     hzl = find(r"HZL\s*\(Delhi\)\s*:\s*(\d+)")

#     # Lead
#     lead_black = find(r"Battery Scrap\s*\(Black\)\s*:\s*(\d+)")
#     lead_white = find_pair(r"Battery Scrap\s*\(White\)\s*:\s*(\d+)\+?/?(\d+)?")
#     lead_ingot = find(r"Ingot\s*:\s*(\d+)")

#     # Steel & Other Metals
#     steel_bartan = find(r"BARTAN\s*:\s*(\d+)")
#     ss202 = find(r"SS 202\s*:\s*(\d+)")
#     ss304 = find(r"SS 304\s*:\s*(\d+)")
#     ss316 = find(r"SS 316\s*:\s*(\d+)")
#     nickel = find_pair(r"NICKEL\s*:\s*(\d+)\+?/?(\d+)?")
#     tin = find_pair(r"TIN\s*:\s*(\d+)\+?/?(\d+)?")
#     cadmium = find(r"CADMIUM\s*:\s*(\d+)")

#     # Date & Time
#     date = find(r"DATE\s*:\s*(.*)")
#     time = find(r"TIME\s*:\s*(.*)")

#     return [
#         date, time,
#         arm_bhatti, arm_plant[0], arm_plant[1],
#         kaliya, super_d, ccr[0], ccr[1], cc[0], cc[1],
#         purja_local, purja_engine, utensil, sheet_scrap,
#         wire, ingot, local_rod[0], local_rod[1], comp_rod,
#         dross[0], dross[1], hg, shg, pmi[0], pmi[1], hzl,
#         purja[0], purja[1], chadri[0], chadri[1], honey[0], honey[1],
#         lead_black, lead_white[0], lead_white[1], lead_ingot,
#         steel_bartan, ss202, ss304, ss316,
#         nickel[0], nickel[1], tin[0], tin[1], cadmium
#     ]

import re

def clean(v):
    if not v: return ""
    return re.sub(r"[^\d]", "", v)  # remove + / mm text etc.


def extract_prices(text):
    # Remove only NEW LINE noise, keep 1.6MM
    text = text.replace("+", "").replace("-", "")

    def find(pattern):
        m = re.search(pattern, text)
        return clean(m.group(1)) if m else ""

    def find_pair(pattern):
        m = re.search(pattern, text)
        if not m: return ("","")
        return (clean(m.group(1)), clean(m.group(2)) if len(m.groups())>1 and m.group(2) else "")

    # ---------- Copper (with 1.6MM extraction) ----------
    arm_bhatti = find(r"Armature\s*\(Bhatti\)\s*:\s*(\d+)")
    arm_plant = find_pair(r"Armature\s*\(Plant\)\s*:\s*([\d\/]+)\s*([\d\/]+)?")

    kaliya = find(r"Kaliya\s*\(Zero\)\s*Rod\s*:\s*(\d+)")
    kaliya_mm = find(r"Kaliya\s*\(Zero\)\s*Rod\s*:\s*\d+\s*\(1\.6MM\s*:\s*(\d+)")
    
    super_d = find(r"Super D Rod\s*:\s*(\d+)")
    super_d_mm = find(r"Super D Rod\s*:\s*\d+\s*\(1\.6MM\s*:\s*(\d+)")

    ccr = find_pair(r"CCR Rod\s*:\s*([\d\/]+)\s*([\d\/]+)?")
    ccr_mm = find_pair(r"CCR Rod.*1\.6MM\s*:\s*([\d\/]+)\s*([\d\/]+)?")

    cc = find_pair(r"CC Rod\s*:\s*([\d\/]+)\s*([\d\/]+)?")
    cc_mm = find_pair(r"CC Rod.*1\.6MM\s*:\s*([\d\/]+)\s*([\d\/]+)?")

    # ---------- Aluminium ----------
    purja_local = find(r"Purja\s*\(Local\)\s*:\s*(\d+)")
    purja_engine = find(r"Purja\s*\(Engine, Imported\)\s*:\s*(\d+)")
    utensil = find(r"Utensils Scrap\s*:\s*(\d+)")
    sheet_scrap = find(r"Sheet Scrap\s*:\s*(\d+)")
    wire = find(r"Wire Scrap\s*:\s*(\d+)")
    ingot = find(r"Company Ingot\s*:\s*(\d+)")
    local_rod = find_pair(r"Local Rod\s*:\s*([\d\/]+)\s*([\d\/]+)?")
    comp_rod = find(r"Company Rod\s*:\s*(\d+)")

    # ---------- Zinc ----------
    dross = find_pair(r"Dross\s*:\s*([\d\/]+)\s*([\d\/]+)?")
    hg = find(r"HG\s*\(Iran\)\s*:\s*(\d+)")
    shg = find(r"SHG\s*\(Iran\)\s*:\s*(\d+)")
    pmi = find_pair(r"PMI\s*\(Delhi\)\s*:\s*([\d\/]+)\s*([\d\/]+)?")
    hzl = find(r"HZL\s*\(Delhi\)\s*:\s*(\d+)")

    # ---------- Brass ----------
    purja = find_pair(r"Purja\s*:\s*([\d\/]+)\s*([\d\/]+)?")
    chadri = find_pair(r"Chadri\s*:\s*([\d\/]+)\s*([\d\/]+)?")
    honey = find_pair(r"Honey\s*:\s*([\d\/]+)\s*([\d\/]+)?")

    # ---------- Lead ----------
    lead_black = find(r"Battery Scrap\s*\(Black\)\s*:\s*(\d+)")
    lead_white = find_pair(r"Battery Scrap\s*\(White\)\s*:\s*([\d\/]+)\s*([\d\/]+)?")
    lead_ingot = find(r"Ingot\s*:\s*(\d+)")

    # ---------- Steel & Others ----------
    steel_bartan = find(r"BARTAN\s*:\s*(\d+)")
    ss202 = find(r"SS 202\s*:\s*(\d+)")
    ss304 = find(r"SS 304\s*:\s*(\d+)")
    ss316 = find(r"SS 316\s*:\s*(\d+)")
    nickel = find_pair(r"NICKEL\s*:\s*([\d\/]+)\s*([\d\/]+)?")
    tin = find_pair(r"TIN\s*:\s*([\d\/]+)\s*([\d\/]+)?")
    cadmium = find(r"CADMIUM\s*:\s*(\d+)")

    # ---------- Date & Time ----------
    date = find(r"DATE\s*:\s*(.*)")
    time = find(r"TIME\s*:\s*(.*)")

    return [
        date, time,
        arm_bhatti, arm_plant[0], arm_plant[1],
        kaliya, kaliya_mm,
        super_d, super_d_mm,
        ccr[0], ccr[1], ccr_mm[0], ccr_mm[1],
        cc[0], cc[1], cc_mm[0], cc_mm[1],
        purja_local, purja_engine, utensil, sheet_scrap,
        wire, ingot, local_rod[0], local_rod[1], comp_rod,
        dross[0], dross[1], hg, shg, pmi[0], pmi[1], hzl,
        purja[0], purja[1], chadri[0], chadri[1], honey[0], honey[1],
        lead_black, lead_white[0], lead_white[1], lead_ingot,
        steel_bartan, ss202, ss304, ss316,
        nickel[0], nickel[1], tin[0], tin[1], cadmium
    ]
