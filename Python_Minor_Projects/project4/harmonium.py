import winsound
import time

def show_banner():
    print("=" * 60)
    print(" 🎹   P Y T H O N   V I R T U A L   H A R M O N I U M   🎹 ")
    print("=" * 60)

# Exact Harmonium Scale Frequencies (Middle Octave / Madhya Saptak in Hz)
HARMONIUM_KEYS = {
    '1': ('Sa', 261),       # C4
    '2': ('re (Komal)', 277),# C#4
    '3': ('Re', 294),       # D4
    '4': ('ga (Komal)', 311),# D#4
    '5': ('Ga', 329),       # E4
    '6': ('Ma', 349),       # F4
    '7': ('Ma (Teevra)', 370),# F#4
    '8': ('Pa', 392),       # G4
    '9': ('dha (Komal)', 415),# G#4
    '0': ('Dha', 440),      # A4
    '-': ('ni (Komal)', 466),# A#4
    '=': ('Ni', 493),       # B4
    '+': ('Sa (Taar)', 523)  # C5
}

# Shortcut Swar Mapping for quick typing
SWAR_MAP = {
    'sa': 261, 're_k': 277, 're': 294, 'ga_k': 311, 'ga': 329,
    'ma': 349, 'ma_t': 370, 'pa': 392, 'dha_k': 415, 'dha': 440,
    'ni_k': 466, 'ni': 493, 'sa2': 523
}

def play_tone(freq, duration=400):
    """Plays harmonium frequency note."""
    winsound.Beep(freq, duration)

def manual_harmonium():
    """Allows playing keys interactively."""
    print("\n--- 🎹 Harmonium Keymap ---")
    for key, (swar, freq) in HARMONIUM_KEYS.items():
        print(f"Key [{key}] -> {swar:<12} ({freq} Hz)")
    print("----------------------------")
    print("Press 'q' to stop playing.\n")

    while True:
        key = input("Press Key to Play Swar: ").strip()
        if key.lower() == 'q':
            break
        elif key in HARMONIUM_KEYS:
            swar, freq = HARMONIUM_KEYS[key]
            print(f"🎵 Playing: {swar}")
            play_tone(freq, duration=500)
        else:
            print("⚠️ Invalid Key! Look at the keymap above.")

def play_composition(notes_str):
    """Plays a sequence of swars passed as string."""
    notes = notes_str.lower().split()
    print("\n🎶 Playing Composition on Harmonium...")
    for note in notes:
        if note in SWAR_MAP:
            print(f"▶️ Swar: {note.upper()}")
            play_tone(SWAR_MAP[note], duration=400)
        else:
            print(f"⚠️ Unknown Swar '{note}', skipping...")
        time.sleep(0.05)
    print("✨ Playback Complete!\n")

def run_harmonium():
    while True:
        show_banner()
        print("\nSelect Mode:")
        print("1. 🎹 Play Harmonium Keys Manually")
        print("2. 🎼 Play Full Sargam (Sa Re Ga Ma Pa Dha Ni Sa)")
        print("3. 📜 Play Sample Tune (Bhajan / Melody Sequence)")
        print("4. ❌ Exit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == '1':
            manual_harmonium()

        elif choice == '2':
            sargam = "sa re ga ma pa dha ni sa2"
            play_composition(sargam)

        elif choice == '3':
            # Demo melody using swars
            sample_tune = "sa re ga ma pa pa pa pa ma ga ma pa pa dha pa ma ga re ga ma re sa"
            print(f"\nPlaying Sample Tune: {sample_tune}")
            play_composition(sample_tune)

        elif choice == '4':
            print("\nHarmonium Closed. Happy Learning! 👋")
            break
        else:
            print("❌ Invalid Choice! Select 1-4.")

        print("\n" + "-" * 40)
        again = input("Do you want to continue playing? (y/n): ").strip().lower()
        print("-" * 40 + "\n")

        if again != 'y':
            print("Harmonium Closed! Bye Bye 👋")
            break

if __name__ == "__main__":
    run_harmonium()
