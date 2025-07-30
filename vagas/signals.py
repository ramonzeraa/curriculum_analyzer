from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver
from django.conf import settings
import os
from .models import Curriculo

@receiver(pre_delete, sender=Curriculo)
def delete_curriculo_file(sender, instance, **kwargs):
    """
    Remove o arquivo físico do currículo antes de deletar o registro do banco
    """
    if instance.arquivo:
        # Obtém o caminho completo do arquivo
        file_path = instance.arquivo.path
        
        # Verifica se o arquivo existe
        if os.path.exists(file_path):
            try:
                # Remove o arquivo físico
                os.remove(file_path)
                print(f"✅ Arquivo removido: {file_path}")
            except OSError as e:
                print(f"❌ Erro ao remover arquivo {file_path}: {e}")
        else:
            print(f"⚠️  Arquivo não encontrado: {file_path}")

@receiver(post_delete, sender=Curriculo)
def cleanup_empty_directories(sender, instance, **kwargs):
    """
    Remove diretórios vazios após deletar currículos
    """
    if instance.arquivo:
        # Obtém o diretório do arquivo
        file_dir = os.path.dirname(instance.arquivo.path)
        
        try:
            # Verifica se o diretório está vazio
            if os.path.exists(file_dir) and not os.listdir(file_dir):
                # Remove o diretório vazio
                os.rmdir(file_dir)
                print(f"🗂️  Diretório vazio removido: {file_dir}")
        except OSError as e:
            print(f"⚠️  Erro ao remover diretório {file_dir}: {e}")

@receiver(pre_delete, sender=Curriculo)
def log_curriculo_deletion(sender, instance, **kwargs):
    """
    Log da exclusão do currículo para auditoria
    """
    print(f"🗑️  Excluindo currículo: {instance.nome} (ID: {instance.id})")
    print(f"   📧 Email: {instance.email}")
    print(f"   💼 Vaga: {instance.vaga.titulo if instance.vaga else 'N/A'}")
    print(f"   📁 Arquivo: {instance.arquivo.name if instance.arquivo else 'N/A'}") 