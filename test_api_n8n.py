#!/usr/bin/env python3
"""
Script para testar as APIs de integração com N8N
"""

import requests
import json

# Configurações
BASE_URL = "http://localhost:8000"
API_CURRICULOS = f"{BASE_URL}/api/curriculos-recentes/"
API_MARCAR_EMAIL = f"{BASE_URL}/api/marcar-email-enviado/"

def test_buscar_curriculos():
    """Testa a API de buscar currículos recentes"""
    print("🔍 Testando API de buscar currículos recentes...")
    
    try:
        response = requests.get(API_CURRICULOS)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso! Status: {data['status']}")
            print(f"📊 Total de currículos: {data['total']}")
            
            if data['curriculos']:
                print("\n📋 Currículos encontrados:")
                for curriculo in data['curriculos']:
                    print(f"  - {curriculo['nome']} ({curriculo['email']})")
                    print(f"    Vaga: {curriculo['vaga_titulo']}")
                    print(f"    Classificação: {curriculo['classificacao_ia']}")
                    print(f"    Compatibilidade: {curriculo['compatibilidade']}%")
                    print()
            else:
                print("ℹ️  Nenhum currículo recente encontrado")
        else:
            print(f"❌ Erro! Status Code: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão! Certifique-se de que o servidor Django está rodando.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def test_marcar_email_enviado(curriculo_id=1):
    """Testa a API de marcar email como enviado"""
    print(f"\n📧 Testando API de marcar email como enviado (ID: {curriculo_id})...")
    
    try:
        data = {"curriculo_id": curriculo_id}
        response = requests.post(API_MARCAR_EMAIL, json=data)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Sucesso! {data['message']}")
        else:
            print(f"❌ Erro! Status Code: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão! Certifique-se de que o servidor Django está rodando.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def mostrar_info_apis():
    """Mostra informações sobre as APIs disponíveis"""
    print("🔗 APIs disponíveis para integração com N8N:")
    print()
    print("1. GET /api/curriculos-recentes/")
    print("   - Retorna currículos dos últimos 7 dias sem email enviado")
    print("   - Resposta: JSON com lista de currículos")
    print()
    print("2. POST /api/marcar-email-enviado/")
    print("   - Marca currículo como tendo recebido email")
    print("   - Body: {'curriculo_id': 123}")
    print("   - Resposta: JSON com confirmação")
    print()
    print("📖 Consulte o arquivo INTEGRACAO_N8N.md para instruções completas")

def main():
    """Função principal"""
    print("🚀 Teste das APIs para Integração com N8N")
    print("=" * 50)
    
    mostrar_info_apis()
    print("=" * 50)
    
    # Testar APIs
    test_buscar_curriculos()
    test_marcar_email_enviado()
    
    print("\n" + "=" * 50)
    print("✅ Teste concluído!")
    print("\n💡 Próximos passos:")
    print("1. Abra o N8N")
    print("2. Crie um novo workflow")
    print("3. Siga as instruções no arquivo INTEGRACAO_N8N.md")
    print("4. Configure o trigger Cron para executar periodicamente")

if __name__ == "__main__":
    main() 