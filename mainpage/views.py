from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import FireFightingVehicle, MunicipalityVehicle, AmbulanceVehicle, Pump
from .forms import UserRegisterForm, UserLogInForm, LogoutForm, ContactUsForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages


def index(request):
    fire_vehicles = FireFightingVehicle.objects.all()
    all_municipality = MunicipalityVehicle.objects.all()
    return render(request, 'mainpage/index.html', {'fire_vehicles': fire_vehicles,
                                                   'all_municipality': all_municipality})


def fire_details(request, slug):
    firevehicle = get_object_or_404(FireFightingVehicle, slug=slug)
    return render(request, 'mainpage/fire_datails.html', context={'firevehicle': firevehicle})


def municipality_details(request, slug):
    municipality = get_object_or_404(MunicipalityVehicle, slug=slug)
    return render(request, 'mainpage/municipality_detils.html', {'municipality': municipality})


def team(request):
    fire_vehicles = FireFightingVehicle.objects.all()
    all_municipality = MunicipalityVehicle.objects.all()
    all_ambulance = AmbulanceVehicle.objects.all()
    all_pump = Pump.objects.all()
    return render(request, 'mainpage/team.html', {'fire_vehicles': fire_vehicles,
                                                  'all_municipality': all_municipality,
                                                  'all_ambulance': all_ambulance,
                                                  'all_pump': all_pump})


def single1(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact:home')
    else:
        form = ContactUsForm()
    return render(request, 'mainpage/single.html', {'form': form})


def about(request, slug=None):
    return render(request, 'mainpage/about.html')



def contactmine(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                cd = form.cleaned_data
                name = cd['name']
                email = cd['email']
                title = cd['title']
                message = cd['message']
                msg = "نام فرستنده:{0}\n ایمیل:\n{1}\n عنوان پیام:{2}\n پیام:\n{3}".format(name, email, title, message)

                # ارسال ایمیل
                send_mail(
                    title,
                    msg,
                    'yeganetanhaei@gmail.com',
                    ['yeganetanhaei@gmail.com'],
                    fail_silently=False
                )

                messages.success(request,
                                 ' پیام شما با موفقیت ارسال شد. کارشناسان ما به زودی با شما تماس خواهند گرفت.')
                return redirect('index')

            except Exception as e:
                messages.error(request, f' خطا در ارسال پیام: {str(e)}')
                return redirect('index')
        else:
            messages.error(request, ' لطفاً تمام فیلدها را به درستی پر کنید.')
            return render(request, 'mainpage/contact.html', {'form': form})
    else:
        form = ContactUsForm()

    return render(request, 'mainpage/contact.html', {'form': form})
def service(request, slug=None):
    return render(request, 'mainpage/service.html')


def contactus(request):
    if request.method == 'POST':
        form_register = UserRegisterForm(request.POST)
        if form_register.is_valid():
            data = form_register.cleaned_data
            User.objects.create_user(username=data['user_name'],
                                     email=data['email'],
                                     first_name=data['first_name'],
                                     last_name=data['last_name'],
                                     password=data['password2'])
            messages.success(request, ("اطلاعات شما با موفقیت ثبت شد."))
            return redirect('index')
    else:
        form_register = UserRegisterForm()
    return render(request, 'mainpage/contactus/register.html', {'form_register': form_register})


def login_form(request):
    if request.method == 'POST':
        form_login = UserLogInForm(request.POST)
        if form_login.is_valid():
            data = form_login.cleaned_data
            try:
                user = authenticate(request, username=User.objects.get(email=data['user']), password=data['password'])
            except:
                user = authenticate(request, username=data['user'], password=data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, ("خوش آمدید."))
                return redirect('index')
    else:
        form_login = UserLogInForm()
    return render(request, 'mainpage/contactus/login.html', {'form_login': form_login})


def admin_page(request):
    return redirect('http://127.0.0.1:8000/admin/login/?next=/admin/')


def more_info_fire(request):
    fire_vehicles = FireFightingVehicle.objects.all()
    return render(request, 'mainpage/moreinformation/moreinfofire.html', {'fire_vehicles': fire_vehicles})


def municipality_information(request):
    all_municipality = MunicipalityVehicle.objects.all()
    return render(request, 'mainpage/moreinformation/moreinfomunici.html', {'all_municipality': all_municipality})


def ambulance_information(request):
    ambulance_vehicles = AmbulanceVehicle.objects.all()
    return render(request, 'mainpage/moreinformation/moreinfoambulance.html',
                  {'ambulance_vehicles': ambulance_vehicles})


def pump_information(request):
    pump_info = Pump.objects.all()
    return render(request, 'mainpage/moreinformation/moreinformationpump.html', {'pump_info': pump_info})


def logout_view(request):
    if request.method == 'POST':
        form = LogoutForm(request.POST)
        if form.is_valid():
            logout(request)
            messages.success(request, ("شما از حساب کاربری خود حارج شده اید!"))

            return redirect('index')
    else:
        form = LogoutForm()
    return render(request, 'mainpage/contactus/logout.html', {'form': form})


def ambulance(request, slug):
    ambulance_details = get_object_or_404(AmbulanceVehicle, slug=slug)
    return render(request, 'mainpage/ambulance_details.html', {'ambulance_details': ambulance_details})


def pump(request, slug):
    pump_details = get_object_or_404(Pump, slug=slug)
    return render(request, 'mainpage/pump_details.html', {'pump_details': pump_details})
