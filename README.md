# Sistema de Filtragem de Currículos (MVP)

Este projeto é um MVP de uma plataforma para recebimento, análise e filtragem de currículos, com cadastro de vagas, envio de currículos via formulário web, e administração via painel do Django. O sistema está preparado para evoluir com automação, IA e integrações futuras.

## Funcionalidades
- Cadastro de vagas pelo RH (admin Django)
- Envio de currículos (PDF/DOCX) por formulário web
- Armazenamento dos dados extraídos dos currículos
- Visualização e gestão de vagas/currículos pelo admin
- Estrutura pronta para filtragem automática e notificações por e-mail
- Pronto para exportação de dados para análise (pandas/Power BI)

## Tecnologias Utilizadas
- Python 3.10+
- Django 5.2+
- SQLite (padrão, fácil migração para PostgreSQL)
- pdfplumber (leitura de PDF)
- python-docx (leitura de DOCX)
- pandas (manipulação/exportação de dados)

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd <pasta-do-projeto>
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ajuste as configurações se necessário:**
   - O banco padrão é SQLite, mas pode ser migrado para PostgreSQL facilmente.
   - Configure o envio de e-mails no `settings.py` para notificações automáticas.

5. **Aplique as migrações:**
   ```bash
   python manage.py migrate
   ```

6. **Crie um superusuário para acessar o admin:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

## Uso

- **Administração:**
  - Acesse `/admin` para cadastrar vagas e gerenciar currículos.
- **Envio de Currículo:**
  - Acesse `/enviar-curriculo/` para preencher o formulário e enviar o currículo.

## Estrutura do Projeto

```
├── curriculos/
│   ├── curriculos/           # Configurações do projeto Django
│   ├── vagas/                # App principal (vagas e currículos)
│   │   ├── templates/vagas/  # Templates HTML
│   │   ├── models.py         # Modelos de Vaga e Currículo
│   │   ├── forms.py          # Formulários
│   │   ├── views.py          # Lógica das views
│   ├── manage.py             # Gerenciador Django
├── requirements.txt          # Dependências do projeto
├── README.md                 # Este arquivo
└── venv/                     # Ambiente virtual (não versionar)
```

## Próximos Passos / Futuras Funcionalidades
- Extração automática de dados dos currículos (PDF/DOCX)
- Filtragem automática baseada em critérios configuráveis
- Notificações automáticas por e-mail (OAuth 2.0)
- Exportação de dados para Power BI
- Integração com LinkedIn e outros sistemas de RH
- Dashboard para gestores
- Implementação de IA para análise semântica dos currículos

## Observações
- O projeto segue as boas práticas de privacidade e LGPD.
- Dados de currículos reprovados podem ser excluídos automaticamente após período definido.
- O produto está pronto para evoluir conforme as necessidades do RH.

---

Dúvidas ou sugestões? Abra uma issue ou entre em contato!