from django.contrib import admin
from django.urls import include, path
from EntrepriseApp.views import register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('expedition/', include('ExpeditionApp.urls')),
    path('entreprise/', include('EntrepriseApp.urls')),
    path('vehicule/', include('VehiculeApp.urls')),
    path('offre/', include('OffreApp.urls')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
]
