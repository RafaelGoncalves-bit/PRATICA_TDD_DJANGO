from django.urls import path
from core.views import editar, login, logout, home, listar, criar


urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', home, name='index'),
    path('', home,name='home'),
    path('listar/', listar,name='listar'),
    path('criar/', criar,name='criar'),
    path('editar/<int:id>/', editar,name='editar'),
]