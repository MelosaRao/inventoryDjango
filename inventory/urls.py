from django.contrib import admin
from django.urls import path
from .views import Index, SignUpView, Dashboard,AddItem,DeleteItem, EditItem
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='inventory/login.html') , name='login'),
    path('users/logout/', LogoutView.as_view(template_name='inventory/logout.html'), name='logout'),
    path('additem/', AddItem.as_view(), name='additem'),
    path('edititem/<int:pk>', EditItem.as_view(), name='edit_item'),
    path('deleteitem/<int:pk>', DeleteItem.as_view(), name='delete_item')
]
    #path('logout/', LogoutPage.as_view() , name='logout'),
    #path('logout/', auth_views.LogoutView.as_view(template_name='inventory/logout.html', name='logout'))

