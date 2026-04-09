from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def encode(request):
    # if request.method == 'POST':
    #     text = request.POST.get('text')
    #     shift = int(request.POST.get('shift', 0))
    #     encoded_text = caesar_cipher(text, shift)
    #     return render(request, 'index.html', {'encoded_text': encoded_text})
    return render(request, 'encode.html')

def decode(request):
    # if request.method == 'POST':
    #     text = request.POST.get('text')
    #     shift = int(request.POST.get('shift', 0))
    #     decoded_text = caesar_decipher(text, shift)
    #     return render(request, 'index.html', {'decoded_text': decoded_text})
    return render(request, 'decode.html')