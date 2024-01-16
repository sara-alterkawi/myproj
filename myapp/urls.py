from django.urls import path
from .views import Signup, Login, Logout, HomePage, AboutPage, OrderPage, RasPi


urlpatterns = [
    path('signup/', Signup, name='signup'),
    path('login/', Login, name='login'),
    path('logout', Logout, name='logout'),
    path('', HomePage, name='home'),
    path('about/', AboutPage, name='about'),
    path('order/', OrderPage, name='order'),
    path('raspi/', RasPi, name="raspi" )
]