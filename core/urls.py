from django.urls import path
from core.views import login, logout, home, listar


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('', home,name='home'),
    path('listar/', listar,name='listar')
]