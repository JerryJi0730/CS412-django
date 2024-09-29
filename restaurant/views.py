import time
from django.shortcuts import render, redirect, HttpResponse
import random

# Create your views here.
def main(request):
    '''Show the HTML form to the client.'''
    # use this template to produce the response
    template_name = 'restaurant/main.html'
    return render(request, template_name)

def order(request):
    special= ["apple", "pineapple","watermelon" ]
    instruction=["may be too sweet", "may be too salty","may be having a lot of seeds"]
    template_name = 'restaurant/order.html'
    index = random.randint(0, len(special) - 1)
    daily_special = special[index]
    special_instruction = instruction[index]
    context = {
        'daily_special': daily_special,
        'special_instruction': special_instruction
    }

    return render(request, template_name, context)

def confirmation(request):
    template_name = 'restaurant/confirmation.html'
    if request.method == 'POST':
        items = request.POST.getlist('items')
        customer_name = request.POST['name']
        customer_phone = request.POST['phone']
        customer_email = request.POST['email']
        
        total_price =0
        for item in items:
            if item=="Burger":
                total_price+=8
            elif item=="Salad":
                total_price+=7
            elif item=="Pizza":
                total_price+=10
            elif item=="Spaghetti Bolognese":
                total_price+=2

        # Generate random ready time between 30 and 60 minutes
        randometime= random.randint(30, 60)
        current_time = time.time()
        ready_time = current_time + (randometime * 60)
        ready_time_formatted = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ready_time))
        context = {
            'items': items,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'total_price': total_price,
            'ready_time': ready_time_formatted,
        }

        return render(request, template_name, context)
    return redirect("main")