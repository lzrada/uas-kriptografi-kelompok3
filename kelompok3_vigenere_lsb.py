# =====================================================
# VIGENERE CIPHER + STEGANOGRAFI LSB RGB
# KELOMPOK 3 - UAS KRIPTOGRAFI
# =====================================================

from PIL import Image

# =======================
# KONFIGURASI
# =======================
KEY = "MOCHI"
DELIMITER = "1111111111111110"

# =======================
# VIGENERE CIPHER
# =======================

def vigenere_encrypt(plaintext):
    plaintext = plaintext.upper()
    ciphertext = ""
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            p = ord(char) - 65
            k = ord(KEY[key_index % len(KEY)]) - 65
            c = (p + k) % 26
            ciphertext += chr(c + 65)
            key_index += 1
        else:
            ciphertext += char

    return ciphertext


def vigenere_decrypt(ciphertext):
    plaintext = ""
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            c = ord(char) - 65
            k = ord(KEY[key_index % len(KEY)]) - 65
            p = (c - k) % 26
            plaintext += chr(p + 65)
            key_index += 1
        else:
            plaintext += char

    return plaintext

# =======================
# KONVERSI TEKS KE BINER
# =======================

def text_to_binary(text):
    binary = ""
    for char in text:
        binary += format(ord(char), '08b')
    return binary + DELIMITER

# =======================
# EMBEDDING LSB
# =======================

def embed_lsb(image_path, output_path, secret_text):
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()

    binary_data = text_to_binary(secret_text)
    index = 0

    for y in range(img.height):
        for x in range(img.width):
            if index >= len(binary_data):
                img.save(output_path)
                return

            r, g, b = pixels[x, y]

            r = (r & ~1) | int(binary_data[index])
            index += 1

            if index < len(binary_data):
                g = (g & ~1) | int(binary_data[index])
                index += 1

            if index < len(binary_data):
                b = (b & ~1) | int(binary_data[index])
                index += 1

            pixels[x, y] = (r, g, b)

    img.save(output_path)

# =======================
# EKSTRAKSI LSB
# =======================

def extract_lsb(image_path):
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()

    bits = ""
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            bits += str(r & 1)
            bits += str(g & 1)
            bits += str(b & 1)

            if DELIMITER in bits:
                # cut off at delimiter
                end_index = bits.find(DELIMITER)
                bits = bits[:end_index]

                # convert bits to text
                chars = []
                for i in range(0, len(bits), 8):
                    byte = bits[i:i+8]
                    if len(byte) < 8:
                        break
                    chars.append(chr(int(byte, 2)))

                return ''.join(chars)

    return ''

# =======================
# MENU
# =======================

def menu():
    print("\n======================================")
    print(" PROGRAM KRIPTOGRAFI & STEGANOGRAFI ")
    print("======================================")
    print("1. Enkripsi + Embedding Pesan")
    print("2. Ekstraksi + Dekripsi Pesan")
    print("3. Keluar")

# =======================
# MAIN PROGRAM
# =======================

while True:
    menu()
    pilihan = input("Pilih menu (1/2/3): ")

    # =======================
    # MENU 1
    # =======================
    if pilihan == "1":
        print("\n--- ENKRIPSI + EMBEDDING ---")
        plaintext = input("Masukkan plaintext: ")

        ciphertext = vigenere_encrypt(plaintext)
        print("Ciphertext:", ciphertext)

        embed_lsb("cover.bmp", "stego.bmp", ciphertext)
        print("Pesan berhasil disisipkan ke stego.bmp")
        print("CATAT ciphertext di atas untuk proses dekripsi!")

    elif pilihan == "2":
        print("\n--- DEKRIPSI DARI STEGO IMAGE ---")
        image_path = input("Masukkan path stego image (enter untuk 'stego.bmp'): ")
        if not image_path:
            image_path = "stego.bmp"

        ciphertext_extracted = extract_lsb(image_path)
        if not ciphertext_extracted:
            print("Tidak ada pesan yang ditemukan di gambar atau delimiter tidak ada.")
        else:
            print("Ciphertext hasil ekstraksi:", ciphertext_extracted)
            plaintext = vigenere_decrypt(ciphertext_extracted)
            print("Plaintext asli:", plaintext)

    elif pilihan == "3":
        print("Program selesai.")
        break

    else:
        print("Pilihan tidak valid!")
