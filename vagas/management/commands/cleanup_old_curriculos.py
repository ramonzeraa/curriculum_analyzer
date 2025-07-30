from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from vagas.models import Curriculo

class Command(BaseCommand):
    help = 'Remove currículos antigos baseado em critérios configuráveis'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=90,
            help='Remove currículos mais antigos que X dias (padrão: 90)',
        )
        parser.add_argument(
            '--status',
            choices=['aprovado', 'reprovado', 'analise_manual'],
            help='Remove apenas currículos com status específico',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostra quais currículos seriam removidos sem realmente removê-los',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Força a remoção sem confirmação',
        )

    def handle(self, *args, **options):
        days = options['days']
        status = options['status']
        dry_run = options['dry_run']
        force = options['force']
        
        # Calcula a data limite
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Constrói a query
        queryset = Curriculo.objects.filter(data_envio__lt=cutoff_date)
        
        if status:
            if status == 'aprovado':
                queryset = queryset.filter(aprovado=True)
            elif status == 'reprovado':
                queryset = queryset.filter(aprovado=False)
            elif status == 'analise_manual':
                # Para análise manual, precisamos verificar o campo analise_ia
                queryset = queryset.filter(analise_ia__classificacao='analise manual')
        
        # Conta os currículos que seriam removidos
        count = queryset.count()
        
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS(f"🎉 Nenhum currículo encontrado para remoção!")
            )
            self.stdout.write(f"   Critérios: {days} dias, status: {status or 'todos'}")
            return
        
        # Mostra estatísticas
        self.stdout.write(f"📊 Estatísticas de limpeza:")
        self.stdout.write(f"   Data limite: {cutoff_date.strftime('%d/%m/%Y %H:%M')}")
        self.stdout.write(f"   Critérios: {days} dias, status: {status or 'todos'}")
        self.stdout.write(f"   Currículos encontrados: {count}")
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f"\n🔍 MODO DRY-RUN - Nenhum currículo será removido")
            )
            self.stdout.write("Currículos que seriam removidos:")
            
            for curriculo in queryset[:10]:  # Mostra apenas os primeiros 10
                self.stdout.write(f"   - {curriculo.nome} ({curriculo.email}) - {curriculo.data_envio.strftime('%d/%m/%Y')}")
            
            if count > 10:
                self.stdout.write(f"   ... e mais {count - 10} currículos")
            return
        
        # Confirmação para remoção
        if not force:
            self.stdout.write(f"\n⚠️  ATENÇÃO: Esta operação irá remover {count} currículos permanentemente!")
            self.stdout.write("Isso inclui:")
            self.stdout.write("   - Registro no banco de dados")
            self.stdout.write("   - Arquivo físico do currículo")
            self.stdout.write("   - Análise da IA")
            
            confirm = input(f"\nDeseja continuar? (y/N): ")
            if confirm.lower() != 'y':
                self.stdout.write("❌ Operação cancelada pelo usuário")
                return
        
        # Remove os currículos
        removed_count = 0
        
        for curriculo in queryset:
            try:
                nome = curriculo.nome
                email = curriculo.email
                data_envio = curriculo.data_envio
                
                curriculo.delete()  # Isso irá disparar os signals automaticamente
                removed_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Removido: {nome} ({email}) - {data_envio.strftime('%d/%m/%Y')}")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Erro ao remover currículo {curriculo.id}: {e}")
                )
        
        # Resumo final
        self.stdout.write(f"\n🎯 Resumo da operação:")
        self.stdout.write(f"   Currículos removidos: {removed_count}/{count}")
        
        if removed_count == count:
            self.stdout.write(
                self.style.SUCCESS("🎉 Limpeza concluída com sucesso!")
            )
        else:
            self.stdout.write(
                self.style.WARNING("⚠️  Alguns currículos não puderam ser removidos")
            ) 