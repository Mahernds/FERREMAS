from django.urls import path
from django.urls import include, path

from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('login', views.login, name='login'),
    path('trabajos', views.nuestros_trabajos, name='trabajos'),
    path('trabajos/<str:pk>', views.ver_trabajo, name='ver-trabajo'),
    path('productos', views.productos, name='productos'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('auth_error', views.auth_error, name='auth_error'),


    path('admin_taller', views.admin_taller, name='admin-taller'),
    path('admin_taller/nueva-cuenta', views.admin_taller_crearcuenta, name='admin-taller-crearcuenta'),
    path('admin_taller/actualizar-cuenta/<str:pk>', views.admin_taller_actualizarcuenta, name='admin-taller-actualizarcuenta'),
    path('admin_taller/borrar-cuenta/<str:pk>', views.admin_taller_borrarcuenta, name='admin-taller-borrarcuenta'),
    #path('admin_taller/trabajos-pendientes', views.admin_taller_vertrabajos, name='admin-taller-vertrabajos'),
    path('admin_taller/revision/<str:pk>', views.admin_taller_revisartrabajo, name='admin-taller-revisartrabajo'),
    path('admin_taller/trabajos', views.admin_taller_trabajos, name='admin-taller-trabajos'),


    path('admin_mecanico', views.admin_mecanico, name='admin-mecanico'),
    path('admin_mecanico/trabajos', views.admin_mecanico_trabajos, name='admin-mecanico-trabajos'),
    path('admin_mecanico/nuevo-trabajo', views.admin_mecanico_nuevotrabajo, name='admin-mecanico-nuevotrabajo'),
    path('admin_mecanico/trabajo/<str:pk>', views.admin_mecanico_vertrabajo, name='admin-mecanico-vertrabajo'),
    path('admin_mecanico/modificar/<str:pk>', views.admin_mecanico_modtrabajo, name='admin-mecanico-modtrabajo'),
    path('admin_mecanico/revision/<str:pk>', views.admin_mecanico_arreglartrabajo, name='admin-mecanico-arreglartrabajo'),
    path('admin_mecanico/eliminar/<str:pk>', views.admin_mecanico_eliminartrabajo, name='admin-mecanico-eliminartrabajo'),
]