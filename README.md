# 📜 Certificate Generator — Certificados de Integração em PDF

## 📋 Sobre o Projeto

O **Certificate Generator** emite automaticamente certificados de conclusão do **treinamento de integração de segurança** para representantes de empresas terceirizadas. Foi criado para a **Norte Tech – Serviços em Energia**, em Manaus, substituindo a edição manual de certificados um a um.

O fluxo é simples: o responsável preenche nome, documento e empresa do representante, e o sistema registra o cadastro e gera na hora um **PDF em A4 paisagem**, com moldura, logo, marca d'água, nome em destaque e data por extenso em português.

## 🚀 Tecnologias Utilizadas

- **Framework:** Django 5.2 (views e templates server-side)
- **Geração de PDF:** [fpdf2](https://py-pdf.github.io/fpdf2/), com layout desenhado em código
- **Fontes:** DejaVu Sans embutida (suporte completo a acentuação)
- **Interface:** templates Django + Bootstrap
- **Database:** SQLite

---

## ✨ Funcionalidades

- 📝 **Cadastro do representante:** nome completo, RG ou CPF e empresa.
- 🏢 **Empresas reaproveitáveis:** escolha uma empresa já cadastrada ou cadastre uma nova no mesmo formulário, com validação para não aceitar as duas opções juntas.
- ⚡ **Emissão imediata:** ao salvar, o certificado é criado e o usuário vai direto para a visualização.
- 🖨️ **PDF pronto para imprimir:** A4 paisagem, moldura dupla, logo, imagem de fundo e tipografia com acentos.
- 📅 **Data por extenso:** "Manaus, 20 de Novembro de 2026", com os meses traduzidos.
- 🛠️ **Painel administrativo:** empresas, pessoas e certificados gerenciáveis pelo Django Admin.

---

## 🔧 Como Rodar o Projeto

### Pré-requisitos
- Python 3.12+

### Passo a passo
```bash
git clone https://github.com/LuizPitohui/certificate-generator.git
cd certificate-generator

python -m venv .venv
# Windows: .venv\Scripts\activate | Linux/macOS: source .venv/bin/activate

pip install "Django==5.2.6" "fpdf2==2.7.7"
python manage.py migrate
python manage.py createsuperuser   # opcional, para o /admin
python manage.py runserver
```

Acesse `http://localhost:8000` para cadastrar e emitir certificados.

### Rotas
| Rota | Descrição |
|------|-----------|
| `/` | Formulário de cadastro |
| `/certificado/<id>/` | Visualização do certificado emitido |
| `/certificado/<id>/pdf/` | Download / abertura do PDF |
| `/admin/` | Painel administrativo |

---

## 🎨 Personalização

- **Logo e marca d'água:** o PDF usa `static/images/logo.png` e `static/images/background.png`. Se os arquivos não existirem, o certificado é gerado sem eles.
- **Texto do certificado:** edite a função `gerar_certificado_pdf` em `certificados/views.py` (título, texto, cores e posições).
- **Fontes:** substitua os arquivos em `fonts/` e ajuste as chamadas `add_font`.

---

## 📂 Estrutura do Projeto

```
certificate-generator/
├── integracao_app/          # settings e urls do projeto
├── certificados/
│   ├── models.py            # Empresa, Pessoa, Certificado
│   ├── forms.py             # Formulário com validação de empresa
│   ├── views.py             # Cadastro, visualização e geração do PDF (fpdf2)
│   └── templates/certificados/
├── fonts/                   # DejaVu Sans (regular e bold)
├── static/images/           # Logo e imagem de fundo
└── manage.py
```
