import base64, json, re, pathlib

ROOT = pathlib.Path(r"C:\Users\Leo B\AI_Project\AI_or_IRL")
ASSETS = ROOT / "assets"
INDEX = ROOT / "docs" / "index.html"

MIME = {
    ".webm": "video/webm", ".mp4": "video/mp4",
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".wav": "audio/wav", ".mp3": "audio/mpeg", ".ogg": "audio/ogg",
}

def data_uri(filename):
    p = ASSETS / filename
    mime = MIME[p.suffix.lower()]
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}", mime

def media_q(modality, answer, filename):
    src, mime = data_uri(filename)
    return {"modality": modality, "answer": answer, "mime": mime, "src": src}

def text_q(answer, text):
    return {"modality": "text", "answer": answer, "text": text}

LAGERLOF_TEXT = (
    "Det var en gång en pojke. Han var så där en fjorton år gammal, lång och "
    "ranglig och linhårig. Inte stort dugde han till: han hade mest av allt "
    "lust att sova och äta, och därnäst tyckte han om att ställa till odygd.\n\n"
    "Nu var det en söndagsmorgon, och pojkens föräldrar höllo på att göra sig "
    "i ordning för att gå i kyrkan. Pojken själv satt i skjortärmarna på "
    "bordskanten och tänkte på hur lyckligt det var, att både far och mor "
    "gingo sin väg, så att han skulle få rå sig själv under ett par timmar. "
    "»Nu kan jag då ta ner fars bössa och skjuta av ett skott, utan att någon "
    "behöver lägga sig i det,» sade han för sig själv."
)

MORNING_TEXT = (
    "Morgonrutiner ser olika ut för alla, men de flesta av oss delar samma "
    "mål: att komma igång med dagen utan onödig stress. Att vakna vid samma "
    "tid varje morgon, även på helger, hjälper kroppens inre klocka att hitta "
    "en stabil rytm. Ett glas vatten direkt efter uppvaknandet är ett enkelt "
    "sätt att väcka ämnesomsättningen, och några minuters rörelse, till "
    "exempel en kort promenad eller lite stretching, gör ofta större "
    "skillnad än man tror. Många väljer att undvika mobilen de första "
    "minuterna, för att ge hjärnan tid att vakna i sin egen takt istället "
    "för att direkt fyllas med notiser och nyheter. Till syvende och sist "
    "handlar det inte om att följa en perfekt rutin, utan om att hitta vanor "
    "som faktiskt går att hålla fast vid över tid."
)

CAT_TEXT = (
    "Igår kväll hände något som fick mig att stanna upp mitt i diskandet. "
    "Jag hade precis kommit hem, trött efter en lång dag, och tänkte bara "
    "knö igenom disken så fort som möjligt. Men när jag såg ut genom "
    "fönstret över diskbänken satt grannens katt där, mitt på staketet, och "
    "stirrade rakt in i köket som om den undrade vad jag höll på med. Vi såg "
    "på varandra i typ tio sekunder innan den hoppade ner och försvann. Det "
    "är konstigt vad små stunder som den där kan göra för humöret. Jag stod "
    "kvar med händerna i diskvattnet och log för mig själv, utan någon "
    "direkt anledning. Ibland är det just sådana obetydliga ögonblick som "
    "gör en helt vanlig tisdag lite mindre grå."
)

QUESTIONS = [
    media_q("video", "AI", "q01_sora_bodycam.webm"),
    media_q("image", "REAL", "q02_light_pillars.jpg"),
    media_q("audio", "AI", "q03_tts.wav"),
    text_q("REAL", LAGERLOF_TEXT),
    media_q("image", "AI", "q05_netscape_ai.jpg"),
    media_q("video", "REAL", "q06_pexels_coffee.mp4"),
    text_q("AI", MORNING_TEXT),
    media_q("audio", "REAL", "q08_librivox_onskenatt.mp3"),
    media_q("image", "AI", "q09_ai_portrait.jpg"),
    text_q("AI", CAT_TEXT),
    media_q("audio", "REAL", "q11_commons_jutaholm.ogg"),
    media_q("video", "REAL", "q12_nasa_aurora.webm"),
]

CREDITS = [
    "Fråga 1 (video, AI): \u201cExample of Sora AI-Generated Police Body Camera Footage\u201d, Wikimedia Commons, public domain.",
    "Fråga 2 (bild, IRL): Christoph Geisler, \u201cLight pillars over Laramie Wyoming in winter night\u201d, Wikimedia Commons, CC BY-SA 3.0.",
    "Fråga 3 (ljud, AI): talsyntes med Microsoft Bengt (sv-SE), genererad för detta quiz.",
    "Fråga 4 (text, IRL): Selma Lagerlöf, Nils Holgerssons underbara resa genom Sverige (1906), källa Wikisource, public domain.",
    "Fråga 5 (bild, AI): Joseph Ayerle, \u201cMaria and Steve work on the new logo of the Netscape Internet browser (fictional photo)\u201d, Wikimedia Commons, public domain.",
    "Fråga 6 (video, IRL): \u201cPouring Hot Coffee to Cup\u201d, Pexels-licens.",
    "Fråga 7 (text, AI): skriven av Claude för detta quiz.",
    "Fråga 8 (ljud, IRL): \u201cÖnskenatt\u201d av Karin Boye, uppläst av LibriVox-volontär, public domain.",
    "Fråga 9 (bild, AI): \u201cThis Person Does Not Exist example\u201d (StyleGAN2), Wikimedia Commons, public domain.",
    "Fråga 10 (text, AI): skriven av Claude för detta quiz.",
    "Fråga 11 (ljud, IRL): \u201cJutaholms café\u201d, talad Wikipediaartikel av användaren Tanzania, Wikimedia Commons, CC0.",
    "Fråga 12 (video, IRL): NASA, \u201cAurora Australis over Indian Ocean\u201d (ISS, 2011), Wikimedia Commons, public domain.",
]

def js_string(s):
    return json.dumps(s, ensure_ascii=False)

def js_array_of_strings(items):
    return "[\n  " + ",\n  ".join(js_string(s) for s in items) + "\n]"

def js_questions(qs):
    parts = []
    for q in qs:
        fields = [f'modality: {js_string(q["modality"])}', f'answer: {js_string(q["answer"])}']
        if q["modality"] == "text":
            fields.append(f'text: {js_string(q["text"])}')
        else:
            fields.append(f'mime: {js_string(q["mime"])}')
            fields.append(f'src: {js_string(q["src"])}')
        parts.append("  {\n    " + ",\n    ".join(fields) + "\n  }")
    return "[\n" + ",\n".join(parts) + "\n]"

html = INDEX.read_text(encoding="utf-8")

q_block = f"const QUESTIONS = {js_questions(QUESTIONS)};"
html = re.sub(
    r"/\*QUESTIONS_START\*/.*?/\*QUESTIONS_END\*/",
    lambda m: "/*QUESTIONS_START*/\n" + q_block + "\n/*QUESTIONS_END*/",
    html, flags=re.S,
)

c_block = f"const CREDITS = {js_array_of_strings(CREDITS)};"
html = re.sub(
    r"/\*CREDITS_START\*/.*?/\*CREDITS_END\*/",
    lambda m: "/*CREDITS_START*/\n" + c_block + "\n/*CREDITS_END*/",
    html, flags=re.S,
)

INDEX.write_text(html, encoding="utf-8")
print("index.html size:", INDEX.stat().st_size, "bytes")
