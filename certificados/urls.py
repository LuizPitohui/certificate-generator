# certificados/urls.py

from django.urls import path
from . import views

app_name = 'certificados'

urlpatterns = [
    # A URL raiz do app agora aponta para a view 'cadastro'
    path('', views.cadastro, name='cadastro_pessoa'), 
    path('certificado/<int:certificado_id>/', views.visualizar_certificado, name='visualizar_certificado'),
    path('certificado/<int:certificado_id>/pdf/', views.gerar_certificado_pdf, name='gerar_certificado_pdf'), # Renomeei o name para ser mais claro
]
