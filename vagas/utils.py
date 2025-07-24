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

Sua tarefa é analisar de forma completa o seguinte currículo, considerando todos os aspectos relevantes para a vaga informada: hard skills, soft skills, experiências profissionais, formação acadêmica, idiomas, tempo de experiência e aderência à descrição da vaga, incluindo requisitos e responsabilidades.

Vaga: "{vaga if vaga else 'N/A'}".

Baseado nesta análise, classifique o candidato em uma das categorias:

- "aprovado": candidato atende bem aos requisitos e pode avançar para a próxima fase;
- "reprovado": candidato não atende aos critérios mínimos da vaga;
- "analise manual": currículo necessita de avaliação humana por falta de informações claras ou dúvidas na interpretação.

Retorne sua resposta **exclusivamente em JSON**, com a seguinte estrutura:
{{"classificacao": "aprovado|reprovado|analise manual", "justificativa": "..."}}

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