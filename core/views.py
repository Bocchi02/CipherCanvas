import os
from django.shortcuts import render
from django.conf import settings
from .forms import EncodeForm
from .services.hashing import generate_sha256, verify_integrity
from .services.steganography import decode_image, encode_image, extract_message_and_hash

# Create your views here.
def home(request):
    return render(request, 'index.html')

def encode(request):
    context = {}

    if request.method == "POST":
        uploaded_image = request.FILES.get("image")
        secret_message = request.POST.get("message")

        if not uploaded_image or not secret_message:
            context["error"] = "Please upload an image and enter a secret message."
            return render(request, "encode.html", context)

        if len(secret_message) > 1000:
            context["error"] = "Secret message must not exceed 1000 characters."
            return render(request, "encode.html", context)

        message_hash = generate_sha256(secret_message)
        combined_data = f"{secret_message}|||HASH|||{message_hash}"

        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
        output_dir = os.path.join(settings.MEDIA_ROOT, "encoded")
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        original_path = os.path.join(upload_dir, uploaded_image.name)
        output_filename = f"encoded_{uploaded_image.name}"
        output_path = os.path.join(output_dir, output_filename)

        with open(original_path, "wb+") as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        try:
            encode_image(original_path, combined_data, output_path)

            context["success"] = "Message encoded successfully."
            context["hash_value"] = message_hash
            context["encoded_image_url"] = f"{settings.MEDIA_URL}encoded/{output_filename}"

        except ValueError as e:
            context["error"] = str(e)

    return render(request, "encode.html", context)

def decode(request):
    # if request.method == 'POST':
    #     text = request.POST.get('text')
    #     shift = int(request.POST.get('shift', 0))
    #     decoded_text = caesar_decipher(text, shift)
    #     return render(request, 'index.html', {'decoded_text': decoded_text})
    return render(request, 'decode.html')

def verify(request):
    context = {}

    if request.method == "POST":
        uploaded_image = request.FILES.get("image")

        if not uploaded_image:
            context["error"] = "Please upload an encoded image."
            return render(request, "verify.html", context)

        temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
        os.makedirs(temp_dir, exist_ok=True)

        image_path = os.path.join(temp_dir, uploaded_image.name)

        with open(image_path, "wb+") as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)

        # Step 1: Extract hidden data
        extracted_data = decode_image(image_path)

        if not extracted_data:
            context["error"] = "No hidden data found in the image."
            return render(request, "verify.html", context)

        # Step 2: Split message + hash
        message, stored_hash = extract_message_and_hash(extracted_data)

        if not message or not stored_hash:
            context["error"] = "Invalid or corrupted hidden data."
            return render(request, "verify.html", context)

        # Step 3: Verify integrity
        result = verify_integrity(message, stored_hash)

        context = {
            "message": message,
            "stored_hash": result["stored_hash"],
            "generated_hash": result["generated_hash"],
            "is_match": result["is_match"]
        }

    return render(request, "verify.html", context)

def about(request):
    return render(request, 'about.html')