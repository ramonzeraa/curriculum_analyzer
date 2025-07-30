from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import models
import os
from vagas.models import Curriculo

class Command(BaseCommand):
    help = 'Remove arquivos órfãos de currículos que não existem mais no banco de dados'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra quais arquivos seriam removidos sem realmente removê-los',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a remoção sem confirmação',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']
        
        # Diretório onde os currículos são armazenados
        media_root = settings.MEDIA_ROOT
        curriculos_dir = os.path.join(media_root, 'curriculos')
        
        if not os.path.exists(curriculos_dir):
            self.stdout.write(
                self.style.WARNING(f'Diretório de currículos não encontrado: {curriculos_dir}')
            )
            return
        
        # Busca todos os arquivos no diretório de currículos
        orphan_files = []
        total_files = 0
        
        for root, dirs, files in os.walk(curriculos_dir):
            for file in files:
                total_files += 1
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, media_root)
                
                # Verifica se o arquivo existe no banco de dados
                try:
                    curriculo = Curriculo.objects.get(arquivo=relative_path)
                    self.stdout.write(f"✅ Arquivo válido: {relative_path}")
                except Curriculo.DoesNotExist:
                    orphan_files.append(file_path)
                    self.stdout.write(
                        self.style.WARNING(f"❌ Arquivo órfão encontrado: {relative_path}")
                    )
        
        if not orphan_files:
            self.stdout.write(
                self.style.SUCCESS(f"🎉 Nenhum arquivo órfão encontrado! Total de arquivos: {total_files}")
            )
            return
        
        # Mostra estatísticas
        self.stdout.write(f"\n📊 Estatísticas:")
        self.stdout.write(f"   Total de arquivos: {total_files}")
        self.stdout.write(f"   Arquivos órfãos: {len(orphan_files)}")
        self.stdout.write(f"   Arquivos válidos: {total_files - len(orphan_files)}")
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f"\n🔍 MODO DRY-RUN - Nenhum arquivo será removido")
            )
            self.stdout.write("Arquivos que seriam removidos:")
            for file_path in orphan_files:
                file_size = os.path.getsize(file_path)
                self.stdout.write(f"   {file_path} ({file_size} bytes)")
            return
        
        # Confirmação para remoção
        if not force:
            confirm = input(f"\n⚠️  Deseja remover {len(orphan_files)} arquivos órfãos? (y/N): ")
            if confirm.lower() != 'y':
                self.stdout.write("❌ Operação cancelada pelo usuário")
                return
        
        # Remove os arquivos órfãos
        removed_count = 0
        total_size_freed = 0
        
        for file_path in orphan_files:
            try:
                file_size = os.path.getsize(file_path)
                os.remove(file_path)
                removed_count += 1
                total_size_freed += file_size
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Removido: {file_path} ({file_size} bytes)")
                )
            except OSError as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Erro ao remover {file_path}: {e}")
                )
        
        # Remove diretórios vazios
        empty_dirs_removed = 0
        for root, dirs, files in os.walk(curriculos_dir, topdown=False):
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                try:
                    if not os.listdir(dir_path):  # Se o diretório está vazio
                        os.rmdir(dir_path)
                        empty_dirs_removed += 1
                        self.stdout.write(
                            self.style.SUCCESS(f"🗂️  Diretório vazio removido: {dir_path}")
                        )
                except OSError as e:
                    self.stdout.write(
                        self.style.WARNING(f"⚠️  Erro ao remover diretório {dir_path}: {e}")
                    )
        
        # Resumo final
        self.stdout.write(f"\n🎯 Resumo da operação:")
        self.stdout.write(f"   Arquivos removidos: {removed_count}/{len(orphan_files)}")
        self.stdout.write(f"   Espaço liberado: {total_size_freed} bytes ({total_size_freed/1024/1024:.2f} MB)")
        self.stdout.write(f"   Diretórios vazios removidos: {empty_dirs_removed}")
        
        if removed_count == len(orphan_files):
            self.stdout.write(
                self.style.SUCCESS("🎉 Limpeza concluída com sucesso!")
            )
        else:
            self.stdout.write(
                self.style.WARNING("⚠️  Alguns arquivos não puderam ser removidos")
            ) 