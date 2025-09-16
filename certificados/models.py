# certificados/models.py
from django.db import models
import uuid

class Empresa(models.Model):
    nome = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.nome

class Pessoa(models.Model):
    # O campo 'nome' foi substituído por estes dois:
    nome_representante = models.CharField(max_length=200, verbose_name="Nome do Representante")
    documento = models.CharField(max_length=20, verbose_name="Documento (RG ou CPF)")
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="representantes")

    def __str__(self):
        return self.nome_representante

class Certificado(models.Model):
    pessoa = models.OneToOneField(Pessoa, on_delete=models.CASCADE)
    data_emissao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificado de {self.pessoa.nome_representante} emitido em {self.data_emissao.strftime('%d/%m/%Y')}"
