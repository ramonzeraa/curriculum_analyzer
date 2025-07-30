from django.shortcuts import render, redirect
from .forms import CurriculoForm
from .models import Vaga, Curriculo
from .utils import extrair_texto_pdf, extrair_texto_docx, extrair_info_curriculo, analisar_curriculo_gemini
import os
import tempfile
from django.db import models

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
        # Pré-selecionar vaga se especificada na URL
        vaga_id = request.GET.get('vaga')
        if vaga_id:
            try:
                vaga = Vaga.objects.get(id=vaga_id, ativa=True)
                form = CurriculoForm(initial={'vaga': vaga})
            except Vaga.DoesNotExist:
                form = CurriculoForm()
        else:
            form = CurriculoForm()
    return render(request, 'vagas/enviar_curriculo.html', {'form': form})

def dashboard_curriculos(request):
    """Dashboard para visualizar currículos analisados"""
    curriculos = Curriculo.objects.all().order_by('-data_envio')
    
    # Estatísticas
    total_curriculos = curriculos.count()
    aprovados = curriculos.filter(aprovado=True).count()
    reprovados = curriculos.filter(aprovado=False).count()
    
    # Classificações da IA
    classificacoes_ia = {
        'aprovado': 0,
        'reprovado': 0,
        'analise manual': 0
    }
    
    for curriculo in curriculos:
        if curriculo.analise_ia and isinstance(curriculo.analise_ia, dict):
            classificacao = curriculo.analise_ia.get('classificacao', '').lower()
            if classificacao in classificacoes_ia:
                classificacoes_ia[classificacao] += 1
    
    # Vagas mais populares
    vagas_populares = Vaga.objects.annotate(
        num_curriculos=models.Count('curriculos')
    ).order_by('-num_curriculos')[:5]
    
    context = {
        'curriculos': curriculos,
        'total_curriculos': total_curriculos,
        'aprovados': aprovados,
        'reprovados': reprovados,
        'classificacoes_ia': classificacoes_ia,
        'vagas_populares': vagas_populares,
    }
    
    return render(request, 'vagas/dashboard.html', context)

def detalhes_curriculo(request, curriculo_id):
    """Página de detalhes de um currículo específico"""
    try:
        curriculo = Curriculo.objects.get(id=curriculo_id)
    except Curriculo.DoesNotExist:
        return redirect('dashboard_curriculos')
    
    context = {
        'curriculo': curriculo,
    }
    
    return render(request, 'vagas/detalhes_curriculo.html', context)

def listar_vagas(request):
    """Lista todas as vagas disponíveis"""
    vagas = Vaga.objects.filter(ativa=True).order_by('-data_criacao')
    
    context = {
        'vagas': vagas,
    }
    
    return render(request, 'vagas/listar_vagas.html', context)
