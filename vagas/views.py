from django.shortcuts import render, redirect
from .forms import CurriculoForm
from .models import Vaga
from .utils import extrair_texto_pdf, extrair_texto_docx, extrair_info_curriculo, analisar_curriculo_gemini
import os
import tempfile

# Create your views here.

def enviar_curriculo(request):
    if request.method == 'POST':
        form = CurriculoForm(request.POST, request.FILES)
        if form.is_valid():
            curriculo = form.save(commit=False)
            arquivo = request.FILES['arquivo']
            extensao = os.path.splitext(arquivo.name)[1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as temp_file:
                for chunk in arquivo.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            if extensao == '.pdf':
                texto = extrair_texto_pdf(temp_file_path)
            elif extensao == '.docx':
                texto = extrair_texto_docx(temp_file_path)
            else:
                texto = ''
            info = extrair_info_curriculo(texto)
            curriculo.dados_extraidos = info
            # Chamar IA Gemini para análise/classificação
            vaga_nome = curriculo.vaga.titulo if curriculo.vaga else None
            analise_ia = analisar_curriculo_gemini(texto, vaga_nome)
            curriculo.analise_ia = analise_ia
            curriculo.save()
            os.remove(temp_file_path)
            return render(request, 'vagas/sucesso.html')
    else:
        form = CurriculoForm()
    return render(request, 'vagas/enviar_curriculo.html', {'form': form})
