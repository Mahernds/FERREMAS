from django.urls import path
from . import views

urlpatterns = [
    # Páginas públicas
    path('', views.index, name='index'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('login/', views.login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('auth_error/', views.auth_error, name='auth_error'),

    path('carrito/', views.carrito, name='carrito'),

    path('productos/', views.productos, name='productos'),
    path('producto/<int:pk>/', views.ver_producto, name='ver_producto'),
    path('trabajos/', views.trabajos, name='trabajos'),

    # Vistas adicionales
    path('landing/', views.landing, name='landing'),
    path('gracias/', views.gracias, name='gracias'),
    path('carrito/', views.carrito, name='carrito'),
    path('session/', views.session, name='session'),

    # Admin Ferretería
    path('admin_ferreteria/', views.admin_ferreteria, name='admin_ferreteria'),
    path('admin_ferreteria/crear_trabajador/', views.admin_ferreteria_crear_trabajador, name='admin_ferreteria_crear_trabajador'),
    path('admin_ferreteria/eliminar_trabajador/<str:pk>/', views.admin_ferreteria_eliminar_trabajador, name='admin_ferreteria_eliminar_trabajador'),

    # Admin Trabajador
    path('admin_trabajador/', views.admin_trabajador, name='admin_trabajador'),
    path('admin_trabajador/nuevo_producto/', views.admin_trabajador_nuevo_producto, name='admin_trabajador_nuevo_producto'),
    path('admin_trabajador/modificar_producto/<int:pk>/', views.admin_trabajador_modificar_producto, name='admin_trabajador_modificar_producto'),
    path('admin_trabajador/eliminar_producto/<int:pk>/', views.admin_trabajador_eliminar_producto, name='admin_trabajador_eliminar_producto'),
]
