from django.db import models

# Create your models here.

class Vaga(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    requisitos = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Curriculo(models.Model):
    vaga = models.ForeignKey(Vaga, on_delete=models.CASCADE, related_name='curriculos')
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    arquivo = models.FileField(upload_to='curriculos/')
    dados_extraidos = models.JSONField(null=True, blank=True)
    analise_ia = models.JSONField(null=True, blank=True)  # Resultado da IA Gemini
    aprovado = models.BooleanField(default=False)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.vaga.titulo}"
