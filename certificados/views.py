# certificados/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from fpdf import FPDF
import io
import os
from django.conf import settings

# Importações atualizadas
from .models import Pessoa, Empresa, Certificado
from .forms import CertificadoForm # Usando o novo formulário

# Função renomeada para 'cadastro' para ser mais genérica
def cadastro(request ):
    if request.method == 'POST':
        form = CertificadoForm(request.POST)
        if form.is_valid():
            # Pega os dados validados do formulário
            nome_rep = form.cleaned_data['nome_representante']
            doc = form.cleaned_data['documento']
            empresa_existente = form.cleaned_data['empresa_existente']
            nova_empresa_nome = form.cleaned_data['nova_empresa']
            
            # Determina qual empresa usar
            if nova_empresa_nome:
                empresa_obj, created = Empresa.objects.get_or_create(nome=nova_empresa_nome)
            else:
                empresa_obj = empresa_existente
            
            # Cria o objeto Pessoa com os novos dados
            pessoa = Pessoa.objects.create(
                nome_representante=nome_rep,
                documento=doc,
                empresa=empresa_obj
            )
            
            # Cria o certificado associado
            certificado = Certificado.objects.create(pessoa=pessoa)
            
            # Mensagem de sucesso atualizada
            messages.success(request, f'Certificado para {pessoa.nome_representante} gerado com sucesso!')
            return redirect('certificados:visualizar_certificado', certificado_id=certificado.id)
    else:
        form = CertificadoForm()
    
    return render(request, 'certificados/cadastro.html', {'form': form})


def visualizar_certificado(request, certificado_id):
    certificado = get_object_or_404(Certificado, id=certificado_id)
    return render(request, 'certificados/certificado.html', {'certificado': certificado})


def gerar_certificado_pdf(request, certificado_id ):
    certificado = get_object_or_404(Certificado, id=certificado_id)

    # --- CLASSE PDF PERSONALIZADA PARA ESTILIZAÇÃO ---
    class PDF(FPDF):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.caminho_logo = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
            self.caminho_fundo = os.path.join(settings.BASE_DIR, 'static', 'images', 'background.png')

        def header(self):
            # 1. IMAGEM DE FUNDO (MARCA D'ÁGUA)
            # Verificamos se o arquivo de fundo existe antes de tentar usá-lo
            if os.path.exists(self.caminho_fundo):
                # Posiciona no centro, com 80% da altura da página
                self.image(self.caminho_fundo, x=60, y=30, w=180, h=150)

            # 2. BORDA ESTILIZADA
            self.set_line_width(1)
            self.set_draw_color(34, 49, 63) # Cor azul escuro
            self.rect(5.0, 5.0, 287.0, 200.0) # Borda externa (Largura A4 paisagem: 297mm, Altura: 210mm)
            self.rect(8.0, 8.0, 281.0, 194.0) # Borda interna para efeito de moldura

        def footer(self):
            # Rodapé pode ser usado para informações adicionais, se necessário
            pass

    # --- GERAÇÃO DO PDF ---
    pdf = PDF(orientation='L', unit='mm', format='A4')

    # Registrar as fontes
    font_path = os.path.join(settings.BASE_DIR, 'fonts')
    pdf.add_font('DejaVu', '', os.path.join(font_path, 'DejaVuSans.ttf'), uni=True)
    pdf.add_font('DejaVu', 'B', os.path.join(font_path, 'DejaVuSans-Bold.ttf'), uni=True)

    pdf.add_page()

    # 3. ADICIONAR O LOGO PRINCIPAL
    # Verificamos se o arquivo de logo existe
    if os.path.exists(pdf.caminho_logo):
        pdf.image(pdf.caminho_logo, x=10, y=12, w=40) # Logo no canto superior esquerdo

    # 4. TÍTULO DO CERTIFICADO
    pdf.set_y(40) # Pula para a posição vertical 40mm
    pdf.set_font('DejaVu', 'B', 32)
    pdf.set_text_color(44, 62, 80) # Cor de texto mais escura
    pdf.cell(0, 10, 'CERTIFICADO', 0, 1, 'C')
    pdf.ln(5)
    pdf.set_font('DejaVu', '', 16)
    pdf.set_text_color(127, 140, 141) # Cor de texto cinza
    pdf.cell(0, 10, 'DE CONCLUSÃO DE INTEGRAÇÃO', 0, 1, 'C')
    pdf.ln(20)

    # 5. CORPO DO TEXTO
    pdf.set_font('DejaVu', '', 14)
    pdf.set_text_color(52, 73, 94) # Cor de texto principal
    texto = (
        f"Certificamos, para os devidos fins, que "
    )
    pdf.set_x(30) # Define margem esquerda
    pdf.multi_cell(237, 8, texto, 0, 'L') # Largura ajustada para margens
    pdf.ln(5)

    # Nome do representante em destaque
    pdf.set_font('DejaVu', 'B', 20)
    pdf.set_text_color(41, 128, 185) # Cor azul para destaque
    pdf.cell(0, 10, certificado.pessoa.nome_representante.upper(), 0, 1, 'C')
    pdf.ln(5)

    # Continuação do texto
    pdf.set_font('DejaVu', '', 14)
    pdf.set_text_color(52, 73, 94)
    texto_continuacao = (
        f"portador(a) do documento {certificado.pessoa.documento}, "
        f"representante da empresa {certificado.pessoa.empresa.nome}, "
        f"concluiu com aproveitamento o treinamento de integração de segurança da empresa "
        f"Norte Tech – Serviços em Energia Ltda."
    )
    pdf.set_x(30)
    pdf.multi_cell(237, 8, texto_continuacao, 0, 'C')
    pdf.ln(15)

    # 6. DATA DE EMISSÃO
    meses = {
        "January": "Janeiro", "February": "Fevereiro", "March": "Março",
        "April": "Abril", "May": "Maio", "June": "Junho",
        "July": "Julho", "August": "Agosto", "September": "Setembro",
        "October": "Outubro", "November": "Novembro", "December": "Dezembro"
    }
    nome_mes_en = certificado.data_emissao.strftime("%B")
    nome_mes_pt = meses.get(nome_mes_en, nome_mes_en)
    data_formatada = certificado.data_emissao.strftime(f"%d de {nome_mes_pt} de %Y")

    pdf.set_font('DejaVu', '', 12)
    pdf.set_text_color(52, 73, 94)
    pdf.cell(0, 10, f"Manaus, {data_formatada}", 0, 1, 'C')

    # --- GERAÇÃO DA RESPOSTA HTTP ---
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="certificado_{certificado.pessoa.nome_representante.replace(" ", "_")}.pdf"'
    
    return response
