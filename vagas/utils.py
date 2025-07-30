import pdfplumber
import docx
import re
import os
import requests
from dotenv import load_dotenv

# Lista ampliada de palavras-chave para habilidades
PALAVRAS_CHAVE_HABILIDADES = [
    'python', 'excel', 'power bi', 'scrum', 'sql', 'java', 'c#', 'javascript', 'liderança', 'comunicação',
    'node.js', 'nodejs', 'vue.js', 'vuejs', 'html', 'css', 'postgresql', 'mysql', 'django', 'react', 'typescript',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'linux', 'git', 'rest', 'api', 'agile', 'devops', 'cloud',
    'spring', 'php', 'c++', 'go', 'ruby', 'scala', 'swift', 'objective-c', 'r', 'matlab', 'powerpoint', 'access',
    'tableau', 'sap', 'oracle', 'firebase', 'mongodb', 'redis', 'elasticsearch', 'bigquery', 'spark', 'hadoop',
    'machine learning', 'data science', 'etl', 'ci/cd', 'jira', 'confluence', 'erp', 'crm', 'blockchain', 'iot',
    'microservices', 'testes', 'selenium', 'cypress', 'qa', 'ux', 'ui', 'figma', 'adobe', 'photoshop', 'illustrator'
]

IDIOMAS_LISTA = [
    'inglês', 'ingles', 'espanhol', 'francês', 'frances', 'alemão', 'aleman', 'português', 'portugues', 'italiano'
]

HABILIDADES_CATEGORIZADAS = {
    'database': ['oracle', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'bigquery', 'sap', 'firebase', 'hadoop'],
    'cloud': ['aws', 'azure', 'gcp', 'cloud'],
    'linguagens': ['python', 'java', 'c#', 'javascript', 'typescript', 'php', 'c++', 'go', 'ruby', 'scala', 'swift', 'objective-c', 'r', 'matlab'],
    'devops': ['docker', 'kubernetes', 'linux', 'git', 'ci/cd', 'devops', 'agile', 'microservices'],
    'ferramentas': ['jira', 'confluence', 'power bi', 'excel', 'tableau', 'erp', 'crm', 'rest', 'api', 'etl', 'spring'],
    'design': ['ux', 'ui', 'figma', 'adobe', 'photoshop', 'illustrator'],
    'testes': ['selenium', 'cypress', 'qa', 'testes'],
    'outros': ['blockchain', 'iot', 'machine learning', 'data science']
}

# Carregar variáveis do .env
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Função para análise/classificação via Gemini

def analisar_curriculo_gemini(texto, vaga=None):
    if not GEMINI_API_KEY:
        return {'erro': 'Chave da API Gemini não configurada.'}
    prompt = f"""
Você é um especialista em recrutamento e seleção, com experiência em análise técnica e de RH, similar ao trabalho realizado em plataformas como Gupy, Kenoby e Recrutei.

Sua tarefa é analisar o currículo abaixo com base **na vaga informada**. Considere os seguintes pontos para uma análise completa:
- Habilidades técnicas (hard skills)
- Competências interpessoais (soft skills)
- Experiências profissionais
- Formação acadêmica
- Idiomas
- Tempo de experiência
- Aderência total aos **requisitos** e **descrição** da vaga

Vaga: "{vaga if vaga else 'N/A'}".

**Instruções obrigatórias:**
1. Classifique o candidato com base na aderência à vaga como:
   - `"aprovado"`: atende bem aos requisitos
   - `"reprovado"`: não atende aos critérios mínimos
   - `"analise manual"`: ausência de informações ou ambiguidade que exige avaliação humana

2. Calcule o **nível de compatibilidade** entre o currículo e a vaga, em porcentagem (%).

3. Forneça **justificativa profissional** clara e direta para a classificação, sem tom empático.

4. Apresente **feedbacks detalhados sobre como melhorar o currículo** especificamente para esta vaga, organizados por tópicos:
   - Experiência Profissional
   - Habilidades Técnicas
   - Formação Acadêmica
   - Idiomas
   - Estrutura e Escrita

5. A resposta **deve ser exclusivamente em português**, mesmo que o currículo esteja em outro idioma.

Retorne o resultado **exclusivamente no formato JSON**, exatamente nesta estrutura:

```json
{{
  "classificacao": "aprovado | reprovado | analise manual",
  "compatibilidade": "80%",
  "justificativa": "Texto objetivo explicando os pontos fortes, deficiências e decisões tomadas com base na vaga.",
  "melhorias_curriculo": {{
    "experiencia_profissional": "Sugestões claras e objetivas...",
    "habilidades_tecnicas": "Sugestões...",
    "formacao_academica": "Sugestões...",
    "idiomas": "Sugestões...",
    "estrutura_e_escrita": "Sugestões sobre como organizar melhor o texto, torná-lo mais atrativo e adequado ao perfil buscado."
  }}
}}

Currículo:
{texto}
"""
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + GEMINI_API_KEY
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=20)
        response.raise_for_status()
        resposta = response.json()
        texto_ia = resposta['candidates'][0]['content']['parts'][0]['text']
        # Remover blocos markdown e tentar converter para dict
        import json, re
        texto_ia = re.sub(r'```json|```', '', texto_ia, flags=re.IGNORECASE).strip()
        try:
            return json.loads(texto_ia)
        except Exception:
            return {"resposta_ia": texto_ia}
    except Exception as e:
        return {"erro": str(e)}

# Extrai texto de PDF
def extrair_texto_pdf(caminho_arquivo):
    texto = ''
    with pdfplumber.open(caminho_arquivo) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() or ''
    return texto

# Extrai texto de DOCX
def extrair_texto_docx(caminho_arquivo):
    doc = docx.Document(caminho_arquivo)
    texto = '\n'.join([p.text for p in doc.paragraphs])
    return texto

# Extrai informações-chave do texto do currículo
def extrair_info_curriculo(texto):
    info = {}
    # Nome (primeira linha com mais de 2 palavras, removendo prefixos)
    linhas = texto.split('\n')
    for linha in linhas:
        if len(linha.split()) >= 2:
            nome = linha.strip()
            nome = re.sub(r'^(Contato:|Nome:|Candidate:|Candidato:)', '', nome, flags=re.IGNORECASE).strip()
            info['nome_extraido'] = nome
            break
    # E-mail
    email = re.search(r'[\w\.-]+@[\w\.-]+', texto)
    if email:
        info['email_extraido'] = email.group(0)
    # Habilidades por categoria
    habilidades_categorias = {}
    texto_lower = texto.lower()
    for categoria, palavras in HABILIDADES_CATEGORIZADAS.items():
        encontradas = [p for p in palavras if p in texto_lower]
        if encontradas:
            habilidades_categorias[categoria] = encontradas
    if habilidades_categorias:
        info['habilidades'] = habilidades_categorias
    # Idiomas e níveis
    idiomas = []
    for idioma in IDIOMAS_LISTA:
        padrao = rf'{idioma}(?:\s*-*\s*(básico|intermediário|avançado|fluente))?'
        resultado = re.findall(padrao, texto, re.IGNORECASE)
        if resultado:
            for nivel in resultado:
                if nivel:
                    idiomas.append(f"{idioma.title()} - {nivel.title()}")
                else:
                    idiomas.append(idioma.title())
    if idiomas:
        info['idiomas'] = idiomas
    return info 