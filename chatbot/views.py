from django.shortcuts import render
import easyocr
from .forms import ImageUploadForm
import os, re
from django.conf import settings
from .models import Medicine
from django.core.paginator import Paginator
# Create your views here.

def search(request):
    medicine_objects = Medicine.objects.all()

    #search code
    medicine_name = request.GET.get('medicine_name')
    if medicine_name!='' and medicine_name is not None:
        medicine_objects = Medicine.objects.filter(name__icontains=medicine_name)
    
    #pagination code
    paginator = Paginator(medicine_objects, 100)
    page = request.GET.get('page')
    medicine_objects = paginator.get_page(page)

    return render(request, 'chatbot/search.html', {'medicine_objects':medicine_objects})

def detail(request, id):
    medicine_object = Medicine.objects.get(id=id)
    return render(request, 'chatbot/detail.html', {'medicine_object':medicine_object})

def index(request):
    return render(request, 'chatbot/index.html')

def chatbot(request):
    return render(request, 'chatbot/chatbot.html')

# def image(request):
#     return render(request, "chatbot/image.html")

def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en'])  # Initialize EasyOCR for English
    results = reader.readtext(image_path)
    
    # Combine all recognized text into a single string
    extracted_text = " ".join([result[1] for result in results])
    return extracted_text.strip()


def filter_words_only(text):
    """Filters out numbers and returns only words from the text."""
    words = text.split()
    words_only = [word for word in words if not word.isdigit()]  # Exclude numeric strings
    return words_only

def image_upload_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            # Extract text from the uploaded image
            extracted_text = extract_text_from_image(image_path)

            # Filter out numbers, keep only words
            extracted_words = filter_words_only(extracted_text)

            # Search for medicines matching any of the filtered words
            matched_medicines = Medicine.objects.filter(
                name__iregex=r'\b(?:' + '|'.join(re.escape(word) for word in extracted_words) + r')\b'
            )

            context = {
                'form': form,
                'extracted_text': extracted_text,
                'medicines': matched_medicines if matched_medicines.exists() else None,
            }
            return render(request, 'chatbot/image.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'chatbot/image.html', {'form': form})

