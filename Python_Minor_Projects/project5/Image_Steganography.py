import time
import os
from PIL import Image

def show_banner():
    print("=" * 60)
    print(" 🖼️    I M A G E    S T E G A N O G R A P H Y    T O O L    🔐 ")
    print("=" * 60)

def text_to_bin(text):
    """Converts string message into binary format."""
    return ''.join(format(ord(char), '08b') for char in text)

def hide_text_in_image(image_path, secret_text):
    """Encodes secret text inside image pixels using LSB method."""
    image_path = image_path.strip("\"'")
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found!")
        return

    # Clean enclosing quotes from the secret message if present
    if (secret_text.startswith('"') and secret_text.endswith('"')) or \
       (secret_text.startswith("'") and secret_text.endswith("'")):
        secret_text = secret_text[1:-1]

    # Save output image in the exact same folder as the source image
    folder = os.path.dirname(image_path)
    output_path = os.path.join(folder, "secret_image.png") if folder else "secret_image.png"

    # Open image and convert to RGB
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    
    # Add delimiter to mark end of message
    formatted_secret = secret_text + "#####"
    binary_secret = text_to_bin(formatted_secret)
    data_len = len(binary_secret)
    
    width, height = img.size
    max_capacity = width * height * 3
    
    if data_len > max_capacity:
        print("❌ Error: Text too large for this image size!")
        return

    print("\n🔒 Encoding secret message into pixels...")
    data_index = 0

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            if data_index < data_len:
                r = (r & ~1) | int(binary_secret[data_index])
                data_index += 1
            if data_index < data_len:
                g = (g & ~1) | int(binary_secret[data_index])
                data_index += 1
            if data_index < data_len:
                b = (b & ~1) | int(binary_secret[data_index])
                data_index += 1

            pixels[x, y] = (r, g, b)

            if data_index >= data_len:
                break
        if data_index >= data_len:
            break

    # Save output image as PNG
    img.save(output_path, "PNG")
    print(f"✅ Success! Secret image saved as:\n   '{output_path}'")

def extract_text_from_image(image_path):
    """Decodes hidden text from stego image pixels safely."""
    image_path = image_path.strip("\"'")
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found!")
        return

    print("\n🔓 Scanning pixel channels for hidden binary data...")
    img = Image.open(image_path).convert('RGB')
    pixels = img.load()
    
    width, height = img.size
    extracted_bits = []

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            extracted_bits.append(str(r & 1))
            extracted_bits.append(str(g & 1))
            extracted_bits.append(str(b & 1))

    binary_data = "".join(extracted_bits)
    
    decoded_message = ""
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) < 8:
            break
        try:
            char = chr(int(byte, 2))
            decoded_message += char
            if "#####" in decoded_message:
                break
        except ValueError:
            continue

    if "#####" in decoded_message:
        final_text = decoded_message.split("#####")[0]
        print("\n" + "=" * 55)
        print("          ✨ HIDDEN MESSAGE FOUND ✨           ")
        print("=" * 55)
        print(f"Secret Text: {final_text}")
        print("=" * 55)
    else:
        print("❌ No hidden steganographic message found in this image.")

def run_steganography():
    while True:
        show_banner()
        print("\nSelect Mode:")
        print("1. 🔒 Hide Secret Text inside Image (Encode)")
        print("2. 🔓 Extract Hidden Text from Image (Decode)")
        print("3. ❌ Exit")

        choice = input("\nEnter choice (1-3): ").strip()

        if choice == '1':
            img_path = input("\nEnter original image path (e.g., photo.jpg): ").strip()
            secret_msg = input("Enter secret message to hide: ").strip()
            
            if img_path and secret_msg:
                hide_text_in_image(img_path, secret_msg)
            else:
                print("⚠️ Inputs cannot be empty!")

        elif choice == '2':
            stego_path = input("\nEnter encoded image path (e.g., secret_image.png): ").strip()
            if stego_path:
                extract_text_from_image(stego_path)
            else:
                print("⚠️ Path cannot be empty!")

        elif choice == '3':
            print("\nShutting down Steganography Tool... Stay Safe! 👋")
            break
        else:
            print("❌ Invalid Choice! Select 1-3.")

        print("\n" + "-" * 40)
        again = input("Do you want to perform another task? (y/n): ").strip().lower()
        print("-" * 40 + "\n")

        if again != 'y':
            print("Vault Locked! 👋")
            break

if __name__ == "__main__":
    run_steganography()
