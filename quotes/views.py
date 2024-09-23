from django.shortcuts import render

# Create your views here.
import random

# Define lists of quotes and images (all from the same famous person)
quotes_list = [
    "Change will not come if we wait for some other person or some other time. We are the ones we've been waiting for. We are the change that we seek.",
    "We cannot continue to rely only on our military in order to achieve the national security objectives that we've set. We've got to have a civilian national security force that's just as powerful, just as strong, just as well-funded.",
    "There is not a liberal America and a conservative America - there is the United States of America. There is not a black America and a white America and latino America and asian America - there's the United States of America."
]

images_list = [
    '../../static/picture1.jpg',
    '../../static/picture2.jpeg',
    '../../static/picture3.jpeg'
]

def quote(request):
    random_quote = random.choice(quotes_list)
    random_image = random.choice(images_list)
    return render(request, 'quote.html', {'quote': random_quote, 'image': random_image})

def show_all(request):
    return render(request, 'showall.html', {'quotes': quotes_list, 'images': images_list})

def about(request):
    return render(request, 'about.html')