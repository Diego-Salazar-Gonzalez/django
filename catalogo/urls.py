from . import views
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import registro,inicio,login,admin, productos_por_categoria,vista_productos
urlpatterns =[
    path('inicio/',inicio, name='inicio'),
    path('login/', login , name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('registro/', registro, name='registro'),
    path('admin/', admin, name ='admin'),
    path('productos/<int:categoria_id>/', productos_por_categoria, name='productos_categoria'),
     path('categoria/', vista_productos, name='categoria'),

]