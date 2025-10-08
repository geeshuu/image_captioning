import os
from TTS.api import TTS

# === CONFIGURATION ===
DESCRIPTIONS_FILE = r"/home/geeshu/commentary_generation/services/tts_service/descriptions.txt"
MODEL_NAME = "tts_models/en/vctk/vits"

# Commonly expressive speakers
SPEAKER_OPTIONS = {
    "p226": "Male (clear, balanced)",
    "p231": "Male (expressive)",
    "p243": "Male (energetic, emotional)",
    "p228": "Male (deeper tone)",
    "p301": "Female (expressive, bright)",
    "p345": "Female (natural, emotional)"
}

# === LOAD DESCRIPTIONS ===
if not os.path.exists(DESCRIPTIONS_FILE):
    print(f" File not found: {DESCRIPTIONS_FILE}")
    exit(1)

with open(DESCRIPTIONS_FILE, "r", encoding="utf-8") as f:
    descriptions = [line.strip() for line in f if line.strip()]

if not descriptions:
    print(" No descriptions found in the file.")
    exit(1)

# === SPEAKER SELECTION (SHORT MENU) ===
print("\n🎙️ Choose a speaker:")
for code, label in SPEAKER_OPTIONS.items():
    print(f"{code}: {label}")

speaker_choice = input("\nEnter speaker code (default p226): ").strip()
if speaker_choice not in SPEAKER_OPTIONS:
    speaker_choice = "p226"
    print("👉 Defaulting to p226 (male)")

# === ASK ONLY FOR DESCRIPTION NUMBER ===
try:
    choice = int(input(f"\nEnter the description number (0–{len(descriptions)-1}): "))
    if not (0 <= choice < len(descriptions)):
        raise ValueError
except ValueError:
    print(" Invalid description number.")
    exit(1)

selected_text = descriptions[choice]
output_path = f"caption_{choice}_{speaker_choice}.wav"

# === GENERATE OR LOAD AUDIO ===
if os.path.exists(output_path):
    print(f" Using cached audio: {output_path}")
else:
    print(f"\n💬 Generating TTS for line #{choice} using {speaker_choice}...\n")
    tts = TTS(model_name=MODEL_NAME)
    tts.tts_to_file(text=selected_text, speaker=speaker_choice, file_path=output_path)

# === PLAY AUDIO ===
print("🔊 Playing audio through Windows...")
os.system(f"powershell.exe start {output_path}")

print(f"\n Done! Played: description #{choice} with {speaker_choice}")


