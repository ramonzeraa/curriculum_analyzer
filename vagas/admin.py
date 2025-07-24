from django.contrib import admin
from .models import Vaga, Curriculo

@admin.register(Vaga)
class VagaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ativa', 'data_criacao')
    search_fields = ('titulo',)
    list_filter = ('ativa',)

class ClassificacaoIAFilter(admin.SimpleListFilter):
    title = 'Classificação IA'
    parameter_name = 'classificacao_ia'

    def lookups(self, request, model_admin):
        return [
            ('aprovado', 'Aprovado'),
            ('reprovado', 'Reprovado'),
            ('analise manual', 'Análise Manual'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(analise_ia__classificacao__iexact=value)
        return queryset

class CategoriaHabilidadeFilter(admin.SimpleListFilter):
    title = 'Categoria de Habilidade'
    parameter_name = 'categoria_habilidade'

    def lookups(self, request, model_admin):
        from .utils import HABILIDADES_CATEGORIZADAS
        return [(cat, cat.title()) for cat in HABILIDADES_CATEGORIZADAS.keys()]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(**{f'dados_extraidos__habilidades__{value}__isnull': False})
        return queryset

class HabilidadePorCategoriaFilter(admin.SimpleListFilter):
    title = 'Habilidade (por categoria)'
    parameter_name = 'habilidade_categoria'

    def lookups(self, request, model_admin):
        from .utils import HABILIDADES_CATEGORIZADAS
        habilidades = set()
        for c in Curriculo.objects.all():
            if c.dados_extraidos and 'habilidades' in c.dados_extraidos:
                habs = c.dados_extraidos['habilidades']
                if isinstance(habs, dict):
                    for cat, lista in habs.items():
                        habilidades.update([f'{cat}:{h}' for h in lista])
                elif isinstance(habs, list):
                    # Caso 'habilidades' venha como lista simples
                    habilidades.update([f'geral:{h}' for h in habs])
        return [(h, h.replace(':', ' - ').title()) for h in sorted(habilidades)]

    def queryset(self, request, queryset):
        value = self.value()
        if value and ':' in value:
            cat, hab = value.split(':', 1)
            return queryset.filter(**{f'dados_extraidos__habilidades__{cat}__icontains': hab})
        return queryset

class IdiomaFilter(admin.SimpleListFilter):
    title = 'Idioma'
    parameter_name = 'idioma'

    def lookups(self, request, model_admin):
        idiomas = set()
        for c in Curriculo.objects.all():
            if c.dados_extraidos and 'idiomas' in c.dados_extraidos:
                idiomas.update([i.lower() for i in c.dados_extraidos['idiomas']])
        return [(i, i.title()) for i in sorted(idiomas)]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            return queryset.filter(dados_extraidos__idiomas__icontains=value)
        return queryset

@admin.register(Curriculo)

class CurriculoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'vaga', 'get_classificacao_ia', 'aprovado', 'data_envio')
    search_fields = ('nome', 'email')
    list_filter = (
        'vaga',
        'aprovado',
        ClassificacaoIAFilter,
        CategoriaHabilidadeFilter,
        HabilidadePorCategoriaFilter,
        IdiomaFilter
        )
    
    readonly_fields = (
        'dados_extraidos',
        'analise_ia',
        'arquivo',
        'data_envio',
        'get_classificacao_ia',
        'get_justificativa_ia'
        )

    fieldsets = (
        (None, {
            'fields': ('nome', 'email', 'vaga', 'arquivo', 'aprovado')
        }),
        ('Dados Extraídos', {
            'fields': ('dados_extraidos',)
        }),
        ('Análise IA', {
            'fields': ('analise_ia',)
        }),
    )

    def get_classificacao_ia(self, obj):
        if obj.analise_ia and isinstance(obj.analise_ia, dict):
            return obj.analise_ia.get('classificacao', '-')
        return '-'
    get_classificacao_ia.short_description = 'Classificação IA'

    def get_justificativa_ia(self, obj):
        if obj.analise_ia and isinstance(obj.analise_ia, dict):
            return obj.analise_ia.get('justificativa', '-')
        return '-'
    get_justificativa_ia.short_description = 'Justificativa IA'