
from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


app_name = 'calorie_tracker'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/',views.login,name="login"),
    path('signup_view/',views.signup_view, name="signup_view"),
    path('logout/',views.logout_view,name="logout"),
    path('home1/' , views.home1 , name = 'home1'),
    path('ThanksView/',views.ThanksView.as_view() , name='ThanksView'),
    path('contact/' , views.contact , name='contact'), 
    path('password-reset/', PasswordResetView.as_view(template_name='registration/password_reset.html'),name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
    path('bmi/', views.calculator, name='bmi'),
    path('result/', views.result, name='result'),
    path('search/', views.FoodSearchView.as_view(), name='food_search'),
    path("FoodDetail/",views.FoodDetailView.as_view(),name="FoodDetail"),
    path("FoodConsumed/",views.FoodConsumedView.as_view(),name="FoodConsumed"),
    path("delete/<int:id>/", views.FoodDeleteView.as_view(),name="delete"),
    path('recipe_list', views.recipe_list, name='recipe_list'),
    path('<int:category_id>/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),

    path("FoodListView/",views.FoodListView.as_view(),name="FoodListView"),
    path('weekly_report/', views.weekly_report_view, name='weekly_report'),
    path('recipe_search/', views.recipe_search, name='search'),








    




]




    

    




