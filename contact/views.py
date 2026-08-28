from django.shortcuts import render

def home(request):
    return render(request,'contact/home.html')

def logout_message(request):
    return render(request,'contact/logout.html')
def validation(request):
    return render(request,'contact/validation.html')