from django.core.management.base import BaseCommand
from vagas.utils import analisar_curriculo_gemini
import json

class Command(BaseCommand):
    help = 'Testa a conectividade e funcionamento da API Gemini'

    def add_arguments(self, parser):
        parser.add_argument(
            '--texto-teste',
            type=str,
            default='João Silva\nDesenvolvedor Python\nExperiência: 2 anos\nHabilidades: Python, Django, SQL\nEmail: joao@email.com',
            help='Texto de teste para enviar para a API',
        )

    def handle(self, *args, **options):
        texto_teste = options['texto_teste']
        
        self.stdout.write("🧪 Testando API Gemini...")
        self.stdout.write("=" * 50)
        
        # Teste 1: Verificar se a chave da API está configurada
        from vagas.utils import GEMINI_API_KEY
        if not GEMINI_API_KEY:
            self.stdout.write(
                self.style.ERROR("❌ Chave da API Gemini não configurada!")
            )
            self.stdout.write("Configure a variável GEMINI_API_KEY no arquivo .env")
            return
        
        self.stdout.write("✅ Chave da API configurada")
        
        # Teste 2: Fazer uma requisição de teste
        self.stdout.write("\n📡 Fazendo requisição de teste...")
        
        try:
            resultado = analisar_curriculo_gemini(texto_teste, "Desenvolvedor Python")
            
            if 'erro' in resultado:
                self.stdout.write(
                    self.style.ERROR(f"❌ Erro na API: {resultado['erro']}")
                )
                
                if 'status_code' in resultado and resultado['status_code'] == 503:
                    self.stdout.write(
                        self.style.WARNING("⚠️  API temporariamente indisponível (503)")
                    )
                    self.stdout.write("💡 Dicas:")
                    self.stdout.write("   - Aguarde alguns minutos e tente novamente")
                    self.stdout.write("   - Verifique se há problemas na API do Google")
                    self.stdout.write("   - Considere usar uma chave de API diferente")
                
                return
            
            # Teste 3: Verificar estrutura da resposta
            self.stdout.write("✅ Requisição bem-sucedida!")
            
            campos_obrigatorios = ['classificacao', 'compatibilidade', 'justificativa', 'melhorias_curriculo']
            campos_faltando = []
            
            for campo in campos_obrigatorios:
                if campo not in resultado:
                    campos_faltando.append(campo)
            
            if campos_faltando:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Campos faltando na resposta: {campos_faltando}")
                )
            else:
                self.stdout.write("✅ Estrutura da resposta válida")
            
            # Mostrar resultado
            self.stdout.write("\n📋 Resultado da análise:")
            self.stdout.write(f"   Classificação: {resultado.get('classificacao', 'N/A')}")
            self.stdout.write(f"   Compatibilidade: {resultado.get('compatibilidade', 'N/A')}")
            self.stdout.write(f"   Justificativa: {resultado.get('justificativa', 'N/A')[:100]}...")
            
            # Teste 4: Verificar se a resposta é JSON válido
            try:
                json.dumps(resultado)
                self.stdout.write("✅ Resposta é JSON válido")
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"❌ Resposta não é JSON válido: {e}")
                )
            
            self.stdout.write("\n🎉 Teste concluído com sucesso!")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro inesperado: {e}")
            )
        
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("💡 Para mais informações, consulte:")
        self.stdout.write("   - https://makersuite.google.com/app/apikey")
        self.stdout.write("   - https://ai.google.dev/docs/errors") 