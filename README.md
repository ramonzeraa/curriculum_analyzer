# 📄 Sistema de Análise de Currículos com IA

Um sistema completo de recrutamento e seleção que utiliza inteligência artificial (Google Gemini) para analisar e classificar currículos automaticamente.

## 🚀 Funcionalidades

### Para Candidatos
- **Envio de Currículos**: Upload de arquivos PDF e DOCX
- **Visualização de Vagas**: Lista de oportunidades disponíveis
- **Feedback Automático**: Sugestões de melhoria baseadas na IA

### Para Recrutadores
- **Dashboard Inteligente**: Visão geral de todas as candidaturas
- **Análise Automática**: Classificação automática com IA Gemini
- **Filtros Avançados**: Busca por habilidades, idiomas e classificação
- **Detalhes Completos**: Análise detalhada de cada currículo
- **Sugestões de Melhoria**: Feedback estruturado para candidatos

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.1
- **IA**: Google Gemini API
- **Processamento de Documentos**: pdfplumber, python-docx
- **Interface**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento)

## 📋 Pré-requisitos

- Python 3.8+
- pip
- Chave da API Google Gemini

## 🔧 Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd curriculos
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
GEMINI_API_KEY=sua_chave_da_api_gemini_aqui
SECRET_KEY=sua_chave_secreta_django
DEBUG=True
```

5. **Execute as migrações**
```bash
python manage.py migrate
```

6. **Crie um superusuário**
```bash
python manage.py createsuperuser
```

7. **Execute o servidor**
```bash
python manage.py runserver
```

## 🎯 Como Usar

### 1. Configurar Vagas
- Acesse `/admin/`
- Crie vagas com título, descrição e requisitos
- Ative as vagas que devem aparecer publicamente

### 2. Candidatos Enviam Currículos
- Acesse `/vagas/` para ver oportunidades
- Clique em "Candidatar-se" na vaga desejada
- Preencha o formulário e envie o currículo

### 3. Análise Automática
- O sistema extrai texto do currículo
- Identifica habilidades e idiomas
- A IA Gemini analisa e classifica o candidato
- Gera sugestões de melhoria

### 4. Dashboard de Resultados
- Acesse `/dashboard/` para ver todas as candidaturas
- Filtre por classificação, habilidades ou idiomas
- Visualize detalhes completos de cada análise

## 📊 Funcionalidades da IA

### Classificação Automática
- **Aprovado**: Atende bem aos requisitos da vaga
- **Reprovado**: Não atende aos critérios mínimos
- **Análise Manual**: Requer avaliação humana

### Análise Detalhada
- **Compatibilidade**: Percentual de adequação à vaga
- **Justificativa**: Explicação objetiva da classificação
- **Sugestões**: Feedback estruturado por categoria

### Extração de Dados
- **Habilidades Técnicas**: Categorizadas automaticamente
- **Idiomas**: Identificação de idiomas e níveis
- **Informações Pessoais**: Nome e e-mail extraídos

## 🎨 Interface

### Design Responsivo
- Interface moderna e intuitiva
- Compatível com dispositivos móveis
- Navegação fluida entre páginas

### Dashboard Interativo
- Estatísticas em tempo real
- Cards visuais para cada currículo
- Filtros e busca avançada

### Análise Detalhada
- Visualização completa dos dados extraídos
- Sugestões de melhoria organizadas
- Barra de compatibilidade visual

## 🔍 Filtros Disponíveis

### No Admin Django
- **Classificação IA**: Aprovado, Reprovado, Análise Manual
- **Categoria de Habilidade**: Database, Cloud, Linguagens, etc.
- **Habilidade Específica**: Python, Java, AWS, etc.
- **Idioma**: Inglês, Espanhol, Francês, etc.

### No Dashboard
- **Vagas Mais Populares**: Ranking por número de candidaturas
- **Estatísticas Gerais**: Totais e percentuais
- **Currículos Recentes**: Ordenados por data de envio

## 📁 Estrutura do Projeto

```
curriculos/
├── curriculos/          # Configurações do projeto
├── vagas/              # Aplicação principal
│   ├── models.py       # Modelos de dados
│   ├── views.py        # Lógica de negócio
│   ├── forms.py        # Formulários
│   ├── admin.py        # Interface administrativa
│   ├── utils.py        # Funções de IA e extração
│   └── templates/      # Templates HTML
├── media/              # Arquivos enviados
├── requirements.txt    # Dependências
└── README.md          # Documentação
```

## 🔧 Configuração da API Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma nova chave de API
3. Adicione a chave ao arquivo `.env`
4. Reinicie o servidor

## 🚀 Deploy

### Para Produção
1. Configure `DEBUG=False` no `.env`
2. Use um banco de dados PostgreSQL
3. Configure um servidor web (nginx + gunicorn)
4. Configure o armazenamento de mídia

### Variáveis de Ambiente
```env
DEBUG=False
SECRET_KEY=sua_chave_secreta_producao
GEMINI_API_KEY=sua_chave_gemini
DATABASE_URL=postgresql://user:pass@host:port/db
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação do Django
- Verifique a documentação da API Gemini

## 🔮 Próximas Funcionalidades

- [ ] Integração com LinkedIn
- [ ] Análise de compatibilidade cultural
- [ ] Sistema de notificações
- [ ] Relatórios avançados
- [ ] API REST para integração
- [ ] Chatbot para candidatos