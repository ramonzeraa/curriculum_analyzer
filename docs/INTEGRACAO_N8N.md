# 🔗 Integração com N8N - Sistema de Emails Automáticos

## 📋 **Visão Geral**

Este documento descreve como configurar o N8N para automatizar o envio de emails para candidatos que enviaram currículos através do sistema.

## 🚀 **APIs Disponíveis**

### 1. **Buscar Currículos Recentes**
```
GET /api/curriculos-recentes/
```

**Descrição**: Retorna currículos dos últimos 7 dias que ainda não receberam email de confirmação.

**Resposta de Sucesso**:
```json
{
  "status": "success",
  "curriculos": [
    {
      "id": 1,
      "nome": "João Silva",
      "email": "joao@email.com",
      "vaga_titulo": "Desenvolvedor Python",
      "data_envio": "2024-01-15T10:30:00Z",
      "classificacao_ia": "aprovado",
      "compatibilidade": 85,
      "justificativa": "Perfil muito adequado para a vaga..."
    }
  ],
  "total": 1
}
```

### 2. **Marcar Email como Enviado**
```
POST /api/marcar-email-enviado/
```

**Body**:
```json
{
  "curriculo_id": 1
}
```

**Resposta de Sucesso**:
```json
{
  "status": "success",
  "message": "Email marcado como enviado para currículo 1"
}
```

## 🔧 **Configuração no N8N**

### **Passo 1: Criar Workflow**

1. Abra o N8N
2. Clique em "New Workflow"
3. Nome: "Sistema de Emails - Currículos"

### **Passo 2: Configurar Trigger (Cron)**

1. Adicione um nó **Cron**
2. Configure para executar a cada 1 hora:
   ```
   Cron Expression: 0 * * * *
   ```

### **Passo 3: Buscar Currículos (HTTP Request)**

1. Adicione um nó **HTTP Request**
2. Configure:
   - **Method**: GET
   - **URL**: `http://localhost:8000/api/curriculos-recentes/`
   - **Response Format**: JSON

### **Passo 4: Iterar sobre Currículos (Split In Batches)**

1. Adicione um nó **Split In Batches**
2. Configure:
   - **Batch Size**: 1
   - **Options**: 
     - **Input Field**: `{{ $json.curriculos }}`

### **Passo 5: Preparar Email (Set)**

1. Adicione um nó **Set**
2. Configure as variáveis:
   ```javascript
   {
     "nome_candidato": "{{ $json.nome }}",
     "email_candidato": "{{ $json.email }}",
     "vaga_titulo": "{{ $json.vaga_titulo }}",
     "classificacao": "{{ $json.classificacao_ia }}",
     "compatibilidade": "{{ $json.compatibilidade }}",
     "justificativa": "{{ $json.justificativa }}",
     "curriculo_id": "{{ $json.id }}"
   }
   ```

### **Passo 6: Enviar Email (Gmail/SMTP)**

1. Adicione um nó **Gmail** ou **SMTP**
2. Configure:
   - **To**: `{{ $json.email_candidato }}`
   - **Subject**: `Recebemos seu currículo - {{ $json.vaga_titulo }}`
   - **Message**:
   ```
   Olá {{ $json.nome_candidato }},

   Recebemos seu currículo para a vaga de {{ $json.vaga_titulo }}.

   Nossa análise inicial indica:
   - Classificação: {{ $json.classificacao }}
   - Compatibilidade: {{ $json.compatibilidade }}%

   {{ $json.justificativa }}

   Em breve entraremos em contato com mais detalhes.

   Atenciosamente,
   Equipe de Recursos Humanos
   ```

### **Passo 7: Marcar como Enviado (HTTP Request)**

1. Adicione outro nó **HTTP Request**
2. Configure:
   - **Method**: POST
   - **URL**: `http://localhost:8000/api/marcar-email-enviado/`
   - **Body**: 
   ```json
   {
     "curriculo_id": "{{ $json.curriculo_id }}"
   }
   ```

### **Passo 8: Tratamento de Erros (Error Trigger)**

1. Adicione um nó **Error Trigger**
2. Configure para capturar erros e enviar notificação

## 📧 **Templates de Email Sugeridos**

### **Email para Candidatos Aprovados**
```
Assunto: Parabéns! Seu perfil foi aprovado - {{ vaga_titulo }}

Olá {{ nome }},

Excelente notícia! Analisamos seu currículo para a vaga de {{ vaga_titulo }} e ficamos muito impressionados com seu perfil.

Nossa análise mostra uma compatibilidade de {{ compatibilidade }}% com a vaga.

{{ justificativa }}

Nos próximos dias entraremos em contato para agendar uma entrevista.

Parabéns e boa sorte!

Equipe de Recursos Humanos
```

### **Email para Candidatos em Análise**
```
Assunto: Seu currículo está em análise - {{ vaga_titulo }}

Olá {{ nome }},

Recebemos seu currículo para a vaga de {{ vaga_titulo }} e ele está sendo analisado por nossa equipe.

Devido ao alto volume de candidaturas, nossa análise pode levar alguns dias.

Aguardamos seu currículo com interesse e entraremos em contato em breve.

Obrigado pela paciência!

Equipe de Recursos Humanos
```

### **Email para Candidatos Reprovados**
```
Assunto: Obrigado pelo interesse - {{ vaga_titulo }}

Olá {{ nome }},

Agradecemos seu interesse na vaga de {{ vaga_titulo }} e o tempo dedicado para enviar seu currículo.

Após análise cuidadosa, infelizmente não conseguimos avançar com sua candidatura neste momento.

{{ justificativa }}

Mantenha-se conectado conosco! Novas oportunidades podem surgir que sejam mais adequadas ao seu perfil.

Desejamos sucesso em sua busca profissional!

Equipe de Recursos Humanos
```

## 🔄 **Fluxo Completo do Workflow**

```
[Cron Trigger] → [HTTP Request - Buscar Currículos] → [Split In Batches] → [Set - Preparar Dados] → [Gmail - Enviar Email] → [HTTP Request - Marcar Enviado] → [Error Handler]
```

## ⚙️ **Configurações Adicionais**

### **Variáveis de Ambiente no N8N**
```bash
DJANGO_API_URL=http://localhost:8000
EMAIL_FROM=recursos.humanos@empresa.com
EMAIL_SIGNATURE=Equipe de Recursos Humanos
```

### **Filtros Avançados**
- Enviar emails apenas para currículos com classificação "aprovado"
- Enviar emails em horários comerciais
- Limitar número de emails por hora

### **Monitoramento**
- Log de emails enviados
- Relatórios de entrega
- Alertas para falhas

## 🚨 **Considerações de Segurança**

1. **Autenticação**: Considere adicionar autenticação nas APIs
2. **Rate Limiting**: Implemente limitação de requisições
3. **Logs**: Mantenha logs de todas as operações
4. **Backup**: Faça backup regular dos dados

## 📞 **Suporte**

Para dúvidas sobre a integração:
- Verifique os logs do Django
- Teste as APIs individualmente
- Consulte a documentação do N8N 