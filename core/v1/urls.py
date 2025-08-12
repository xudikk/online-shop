from django.urls import path

from .sql_api import CategorySQLView
from .views import CategoryViews, ProductView, NewApi
from . import auth


urlpatterns = [
    path("ctg/", CategoryViews.as_view()),
    path("ctg/<int:id>/", CategoryViews.as_view()),

    path("product/", ProductView.as_view()),
    path("product/<int:pk>/", ProductView.as_view()),

    path("new/", NewApi.as_view()),

    # auth
    path("regis/", auth.RegisterView.as_view()),
    path("logout/", auth.LogoutView.as_view()),
    path("login/", auth.LoginView.as_view()),
    path("step/one/", auth.StepOne.as_view()),
    path("step/two/", auth.StepTwo.as_view()),

    # SQL API
    path('sql/ctg/', CategorySQLView.as_view()),
    path('sql/ctg/<int:pk>/', CategorySQLView.as_view())


]





