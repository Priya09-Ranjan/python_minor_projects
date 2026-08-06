import time
import pyttsx3

def show_banner():
    print("=" * 55)
    print(" 🗣️    S M A R T    V O I C E    R E A D E R    ( T T S )   🗣️ ")
    print("=" * 55)

def get_engine(rate=160, volume=1.0, voice_index=0):
    """Initializes and returns a fresh speech engine instance."""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    
    voices = engine.getProperty('voices')
    if voice_index < len(voices):
        engine.setProperty('voice', voices[voice_index].id)
    return engine

def speak_text(text, rate, volume, voice_index):
    """Converts text into speech output using a fresh engine session."""
    print(f"\n🔊 Speaking: '{text}'")
    try:
        # Re-initialize engine each time to prevent loop deadlock/silence
        engine = get_engine(rate, volume, voice_index)
        engine.say(text)
        engine.runAndWait()
        engine.stop()  # Properly release the sound hardware
    except Exception as e:
        print(f"❌ Speech Error: {e}")

def run_voice_reader():
    current_rate = 160
    current_volume = 1.0
    current_voice_idx = 0
    
    while True:
        show_banner()
        print("\nSelect an Option:")
        print("1. 💬 Type Text & Read Aloud")
        print("2. 📁 Read Text from a .txt File")
        print("3. ⚙️ Change Voice Settings (Speed / Voice Type)")
        print("4. ❌ Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            user_text = input("\nEnter text to speak: ").strip()
            if user_text:
                speak_text(user_text, current_rate, current_volume, current_voice_idx)
            else:
                print("⚠️ Input cannot be empty!")

        elif choice == '2':
            file_path = input("\nEnter filename (e.g., sample.txt): ").strip()
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if content:
                    print(f"\n📄 Reading file content ({len(content)} characters)...")
                    speak_text(content, current_rate, current_volume, current_voice_idx)
                else:
                    print("⚠️ File is empty!")
            except FileNotFoundError:
                print(f"❌ Error: File '{file_path}' not found!")

        elif choice == '3':
            print("\n--- Voice Settings ---")
            print("1. Male Voice")
            print("2. Female Voice")
            v_choice = input("Select voice (1/2): ").strip()
            
            current_voice_idx = 1 if v_choice == '2' else 0
            
            try:
                speed_in = input("Enter speaking speed (Recommended: 150-200, Default 160): ").strip()
                if speed_in:
                    current_rate = int(speed_in)
                
                print("✅ Settings Updated Successfully!")
                speak_text("Voice settings updated successfully!", current_rate, current_volume, current_voice_idx)
            except ValueError:
                print("⚠️ Invalid speed number! Keeping previous settings.")

        elif choice == '4':
            speak_text("Thank you for using Smart Voice Reader. Goodbye!", current_rate, current_volume, current_voice_idx)
            print("\nExiting Voice Reader... 👋")
            break
        else:
            print("❌ Invalid choice! Select 1-4.")

        # Loop Continuation Control
        print("\n" + "-" * 40)
        again = input("Do you want to perform another task? (y/n): ").strip().lower()
        print("-" * 40 + "\n")
        
        if again != 'y':
            speak_text("Goodbye!", current_rate, current_volume, current_voice_idx)
            print("Shutting down... 👋")
            break

if __name__ == "__main__":
    run_voice_reader()
