# certificados/forms.py

from django import forms
from .models import Empresa

class CertificadoForm(forms.Form):
    # Campo para o nome do representante
    nome_representante = forms.CharField(
        label='Nome do Representante', 
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome completo'})
    )
    
    # Campo para o documento
    documento = forms.CharField(
        label='Documento (RG ou CPF)', 
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o RG ou CPF'})
    )
    
    # Campo para selecionar uma empresa que já existe
    empresa_existente = forms.ModelChoiceField(
        label='Selecione a Empresa (se já cadastrada)',
        queryset=Empresa.objects.all().order_by('nome'),
        required=False,
        empty_label="--- Nenhuma ---",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    # Campo para digitar o nome de uma nova empresa
    nova_empresa = forms.CharField(
        label='Ou Cadastre uma Nova Empresa',
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Contratada XYZ Ltda'})
    )

    # Função de validação para garantir que o usuário escolheu ou digitou uma empresa
    def clean(self):
        cleaned_data = super().clean()
        empresa_existente = cleaned_data.get("empresa_existente")
        nova_empresa = cleaned_data.get("nova_empresa")

        if not empresa_existente and not nova_empresa:
            raise forms.ValidationError(
                "Você deve selecionar uma empresa existente ou cadastrar uma nova."
            )
        
        if empresa_existente and nova_empresa:
            raise forms.ValidationError(
                "Por favor, selecione uma empresa existente OU cadastre uma nova, não ambos."
            )
        
        return cleaned_data
