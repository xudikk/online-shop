from .auth import sign_out, sign_in, sign_up, step_two
from django.urls import path

urlpatterns = [
    # auth
    path('auth/up/', sign_up, name='regis'),
    path('auth/in/', sign_in, name='login'),
    path('auth/out/', sign_out, name='logout'),
    path('auth/two/', step_two, name='step_two'),





]



