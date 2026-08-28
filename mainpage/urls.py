from . import views
from django.urls import path
urlpatterns=[
    path('', views.index, name='index'),
    path('products/', views.team, name='team'),
    path('aboutus/', views.single1, name='single1'),
    path('about/', views.about, name='about'),
    path('contact/', views.contactmine, name='contact'),
    path('service/', views.service, name='service'),
    path('fire/<slug:slug>/', views.fire_details, name='single'),
    path('municipality/<slug:slug>/', views.municipality_details, name='municipality_single'),
    path('register/',views.contactus,name='user-register'),
    path('logIn/',views.login_form,name='user-login'),
    path('admin_page/',views.admin_page,name='admin_page'),
    path('informationfire/',views.more_info_fire,name='information_fire'),
    path('mymunicipality/',views.municipality_information,name='own_municipality'),
    path('moreambulance/',views.ambulance_information,name='all_ambulance'),
    path('logout/', views.logout_view, name='logout'),
    path('ambulance/<slug:slug>/', views.ambulance, name='ambulance_single'),
    path('pump/<slug:slug>/', views.pump, name='pump_single'),
    path('pupminformation/',views.pump_information,name='my_pump')
]