from .auth import sign_out, sign_in, sign_up, step_two
from django.urls import path
from . import views, products

urlpatterns = [
    # auth
    path('auth/up/', sign_up, name='regis'),
    path('auth/in/', sign_in, name='login'),
    path('auth/out/', sign_out, name='logout'),
    path('auth/two/', step_two, name='step_two'),

    # dashboard
    path('', views.index, name='dashboard-home'),

    # product crud
    path("prod/", products.list, name='prod-list'),
    path("prod/detail/<int:pk>/", products.info, name='prod-info'),
    path("prod/form/add/", products.form, name='prod-add'),
    path("prod/form/edit/<int:pk>/", products.form, name='prod-edit'),



]



