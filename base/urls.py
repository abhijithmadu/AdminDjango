from django.urls import path
from .import views

urlpatterns = [
    path('home',views.home,name='home'),
    path('',views.register,name="register"),
    path('login',views.user_login,name="login"),
    path('logout',views.logout,name="logout"),
    path('admin_login',views.admin_login,name="admin_login"),
    path('admin_panel',views.admin_panel,name="admin_panel"),
    path('update_user/<int:id>',views.update_user,name="update_user"),
    path('delete_user/<int:id>',views.delete_user,name="delete_user"),
    path('adduser',views.add_user,name="adduser"),
    path('admin_logout',views.admin_logout,name="admin_logout"),


]