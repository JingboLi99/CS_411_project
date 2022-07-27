from django.urls import path
#include is used when we have a seperate url.py file for each app, then we can include the individual url.py files here using path('',include('tmc_pp.urls'))
from . import views

urlpatterns = [
    path('login/', views.login_view, name = 'login'),
    path('', views.login_view, name = 'login'),
    path('loginauth/', views.login_auth_view, name = 'loginauth'),
    path('categories/', views.categories_view, name = 'cat'),
    path('login/categories/', views.categories_view, name = 'cat'),
    path('profiles/', views.profile_view, name = 'profiles'),
    path('login/profiles/', views.profile_view, name = 'profiles'),
    path('searchresult/', views.search_result_view, name = 'searchresult'),
    path('updateuser/', views.update_del_user_view, name = 'updateuser'),
    path('updateuserauth/', views.update_user_auth_view, name = 'updateuserauth'),
    path('reccomendations/', views.recs_view, name = 'reccomendations'),
    path('choose_category/', views.choose_category_view, name = 'choose_category'),
    path('recipe/', views.recipe_view, name = 'recipe')
]