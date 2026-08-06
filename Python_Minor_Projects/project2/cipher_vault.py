import time
import base64
import os

def show_banner():
    print("=" * 60)
    print(" 🛡️  C I P H E R   V A U L T   P R O  :  CYBER TOOLKIT  🛡️ ")
    print("=" * 60)

def cyber_loading(action_name):
    """Clean visual loading animation for IDLE."""
    print(f"\n[⚡] {action_name} IN PROGRESS...")
    stages = ["10%", "30%", "60%", "90%", "100%"]
    for stage in stages:
        print(f"--> Processing: {stage}")
        time.sleep(0.1)
    print("✅ OPERATION COMPLETE!\n")

def check_password_strength(password):
    """Evaluates password strength."""
    score = 0
    if len(password) >= 8: score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(not c.isalnum() for c in password): score += 1
    
    if score <= 2: return "🔴 WEAK"
    elif score <= 4: return "🟡 MEDIUM"
    else: return "🟢 STRONG (SECURE)"

def key_based_cipher(text, key, decrypt=False):
    """Custom XOR-based cipher using a secret password key."""
    output = []
    key_length = len(key)
    for i, char in enumerate(text):
        key_char = key[i % key_length]
        output.append(chr(ord(char) ^ ord(key_char)))
            
    combined = "".join(output)
    if not decrypt:
        return base64.b64encode(combined.encode('utf-8')).decode('utf-8')
    else:
        return combined

def run_cipher_vault():
    while True:
        show_banner()
        print("\nSelect Mode:")
        print("1. 🔒 Encrypt Secret Message (With Custom Password)")
        print("2. 🔓 Decrypt Secret Message (Requires Password)")
        print("3. 🔑 Check Password Strength")
        print("4. ❌ Exit Vault")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == '1':
            msg = input("\nEnter original secret message: ").strip()
            if not msg:
                print("⚠️ Message cannot be empty!")
                continue
                
            pwd = input("Enter a secret key/password for locking: ").strip()
            if not pwd:
                print("⚠️ Password required for encryption!")
                continue
                
            cyber_loading("ENCRYPTING DATA")
            
            try:
                # Add a verification tag at the start of text
                tagged_msg = "VAULT_OK:" + msg
                cipher_text = key_based_cipher(tagged_msg, pwd, decrypt=False)
                
                print("=" * 45)
                print("          ENCRYPTED VAULT RESULT          ")
                print("=" * 45)
                print(f"Original Text : {msg}")
                print(f"Cipher Code   : {cipher_text}")
                print(f"Secret Key    : {'*' * len(pwd)}")
                print("=" * 45)
                
                save = input("\nSave encrypted code to file? (y/n): ").lower()
                if save == 'y':
                    with open("secret_vault.txt", "w") as f:
                        f.write(cipher_text)
                    print("📁 Saved to 'secret_vault.txt' successfully!")
                    
            except Exception as e:
                print(f"❌ Encryption Error: {e}")

        elif choice == '2':
            print("\nOptions for decryption:")
            print("a) Paste Cipher Code manually")
            print("b) Read from 'secret_vault.txt' file")
            sub_choice = input("Select (a/b): ").strip().lower()
            
            cipher_input = ""
            if sub_choice == 'b':
                if os.path.exists("secret_vault.txt"):
                    with open("secret_vault.txt", "r") as f:
                        cipher_input = f.read().strip()
                    print(f"Loaded Cipher Code: {cipher_input}")
                else:
                    print("❌ 'secret_vault.txt' file not found!")
                    continue
            else:
                cipher_input = input("\nPaste cipher code: ").strip()

            if not cipher_input:
                print("⚠️ Cipher code required!")
                continue

            pwd = input("Enter secret key/password to unlock: ").strip()
            
            cyber_loading("DECRYPTING DATA")
            
            try:
                decoded_raw = base64.b64decode(cipher_input.encode('utf-8')).decode('utf-8')
                decrypted_msg = key_based_cipher(decoded_raw, pwd, decrypt=True)
                
                # Check verification tag
                if decrypted_msg.startswith("VAULT_OK:"):
                    final_msg = decrypted_msg.replace("VAULT_OK:", "", 1)
                    print("=" * 45)
                    print("          DECRYPTED VAULT RESULT          ")
                    print("=" * 45)
                    print(f"Decrypted Message : {final_msg}")
                    print("=" * 45)
                else:
                    print("=" * 45)
                    print("❌ DECRYPTION FAILED! Incorrect password or corrupted cipher code.")
                    print("=" * 45)
            except Exception:
                print("\n❌ DECRYPTION FAILED! Invalid cipher code format.")

        elif choice == '3':
            pwd = input("\nEnter a password to test: ").strip()
            if pwd:
                strength = check_password_strength(pwd)
                print(f"\nPassword Strength Analysis: {strength}")
            else:
                print("⚠️ Please enter a password.")

        elif choice == '4':
            print("\nShutting down Cipher Vault Pro... System Secured! 👋")
            break
        else:
            print("❌ Invalid Choice! Please select 1-4.")
            
        print("\n" + "-" * 45)
        again = input("Do you want to perform another action? (y/n): ").strip().lower()
        print("-" * 45 + "\n")
        
        if again != 'y':
            print("Vault Locked. Good Luck! 👋")
            break

if __name__ == "__main__":
    run_cipher_vault()
