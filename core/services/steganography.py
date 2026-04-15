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