from django.urls import path, re_path
from . import views
# user identification
from .views import save_user,profile_user
from .views import show_csv_table

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),



    # ---------------------------------------------------------------------------------------------------
    # user identify
    path('api/save-user/', save_user, name='save_user'),
    #
    path('profile_user/', profile_user, name='profile_user'),
    # read CSV
    path('csv/', show_csv_table, name='csv-table'),

    # re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]