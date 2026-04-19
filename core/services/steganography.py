from PIL import Image

DELIMITER = "|||END|||"

def text_to_binary(text: str) -> str:
    return ''.join(format(ord(char), '08b') for char in text)

def encode_image(image_path: str, secret_data: str, output_path: str) -> None:
    image = Image.open(image_path)
    image = image.convert("RGB")
    pixels = list(image.getdata())

    binary_data = text_to_binary(secret_data + DELIMITER)
    data_index = 0
    new_pixels = []

    for pixel in pixels:
        r, g, b = pixel

        if data_index < len(binary_data):
            r = (r & ~1) | int(binary_data[data_index])
            data_index += 1

        if data_index < len(binary_data):
            g = (g & ~1) | int(binary_data[data_index])
            data_index += 1

        if data_index < len(binary_data):
            b = (b & ~1) | int(binary_data[data_index])
            data_index += 1

        new_pixels.append((r, g, b))

    if data_index < len(binary_data):
        raise ValueError("The image is too small to hold the secret message.")

    image.putdata(new_pixels)
    image.save(output_path, "PNG")

def binary_to_text(binary_data: str) -> str:
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    text = ''.join(chr(int(char, 2)) for char in chars)
    return text

def decode_image(image_path: str) -> str:
    image = Image.open(image_path)
    pixels = list(image.getdata())

    binary_data = ""

    for pixel in pixels:
        for color in pixel[:3]:  # R, G, B
            binary_data += str(color & 1)

    # Convert binary to text
    all_text = binary_to_text(binary_data)

    # Stop at delimiter
    if DELIMITER in all_text:
        return all_text.split(DELIMITER)[0]
    else:
        return ""
    
def extract_message_and_hash(data: str):
    # DEBUG: show raw extracted data

    # Verify the data is valid
    if not data:
        return None, None
    
    if not isinstance(data, str):
        return None, None
    
    if "|||HASH|||" not in data:
        return None, None

    message, stored_hash = data.split("|||HASH|||", 1)

    
    # Clean hash
    stored_hash = stored_hash.strip().replace('\x00', '')

    if "|||END|||" in stored_hash:
        stored_hash = stored_hash.split("|||END|||", 1)[0].strip()

    # Verify both parts are non-empty
    if not message or not stored_hash:
        return None, None
    
    # Verify hash format
    if len(stored_hash) != 64 or not all(c in '0123456789abcdefABCDEF' for c in stored_hash):
        return None, None
    return message, stored_hash.lower()