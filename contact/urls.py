from . import views
from django.urls import path
app_name='contact'
urlpatterns=[
    path('',views.home,name='home'),
    path('message/',views.logout_message,name='logout_message'),
    path('sent/',views.validation,name='validation')
]