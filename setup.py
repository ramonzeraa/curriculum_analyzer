#!/usr/bin/env python3
"""
Script de configuração inicial do Sistema de Análise de Currículos
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao {description.lower()}: {e}")
        print(f"Saída de erro: {e.stderr}")
        return False

def create_env_file():
    """Cria o arquivo .env com configurações básicas"""
    env_file = Path('.env')
    if env_file.exists():
        print("⚠️  Arquivo .env já existe. Pulando criação...")
        return True
    
    print("\n📝 Criando arquivo .env...")
    
    # Gerar chave secreta do Django
    try:
        from django.core.management.utils import get_random_secret_key
        secret_key = get_random_secret_key()
    except ImportError:
        import secrets
        secret_key = secrets.token_urlsafe(50)
    
    env_content = f"""# Configurações do Django
SECRET_KEY={secret_key}
DEBUG=True

# API Google Gemini
GEMINI_API_KEY=sua_chave_da_api_gemini_aqui

# Configurações de Banco de Dados (opcional)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Configurações de Email (opcional)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=seu_email@gmail.com
# EMAIL_HOST_PASSWORD=sua_senha_de_app
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Arquivo .env criado com sucesso!")
        print("⚠️  IMPORTANTE: Configure sua chave da API Gemini no arquivo .env")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar arquivo .env: {e}")
        return False

def main():
    """Função principal do script de setup"""
    print("🚀 Configuração inicial do Sistema de Análise de Currículos")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not Path('manage.py').exists():
        print("❌ Erro: Execute este script no diretório raiz do projeto (onde está o manage.py)")
        sys.exit(1)
    
    # Verificar se o ambiente virtual está ativo
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Aviso: Ambiente virtual não detectado.")
        print("   Recomendamos usar um ambiente virtual para este projeto.")
        response = input("   Continuar mesmo assim? (s/N): ")
        if response.lower() != 's':
            print("❌ Setup cancelado.")
            sys.exit(1)
    
    # Instalar dependências
    if not run_command("pip install -r requirements.txt", "Instalando dependências"):
        print("❌ Falha na instalação das dependências. Verifique se o requirements.txt existe.")
        sys.exit(1)
    
    # Criar arquivo .env
    if not create_env_file():
        print("❌ Falha na criação do arquivo .env.")
        sys.exit(1)
    
    # Executar migrações
    if not run_command("python manage.py migrate", "Executando migrações do banco de dados"):
        print("❌ Falha nas migrações. Verifique as configurações do banco de dados.")
        sys.exit(1)
    
    # Criar superusuário
    print("\n👤 Criação do superusuário")
    print("   Este usuário será usado para acessar o painel administrativo.")
    response = input("   Criar superusuário agora? (S/n): ")
    if response.lower() != 'n':
        run_command("python manage.py createsuperuser", "Criando superusuário")
    
    print("\n" + "=" * 60)
    print("🎉 Configuração concluída com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Configure sua chave da API Gemini no arquivo .env")
    print("2. Execute: python manage.py runserver")
    print("3. Acesse: http://localhost:8000")
    print("4. Para administração: http://localhost:8000/admin/")
    print("\n📚 Documentação completa: README.md")
    print("=" * 60)

if __name__ == "__main__":
    main() 