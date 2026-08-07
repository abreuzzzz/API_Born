import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 🔐 Lê o segredo e salva como credentials.json
gdrive_credentials = os.getenv("GDRIVE_SERVICE_ACCOUNT")
with open("credentials.json", "w") as f:
    json.dump(json.loads(gdrive_credentials), f)

# 📌 Autenticação com Google
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# === IDs das planilhas ===
planilhas_ids = {
        "Financeiro_contas_a_receber_Born": "15ely1E3KHyTtvonlDDLd5RlY_0RCf90WIQpiKOeD98A",
    "Financeiro_contas_a_pagar_Born": "1e-BALMUv6bKHcMzRWC6at46i56APoy1hmGip0FSklws",
    "Financeiro_Completo_Born": "1Sy2A40cmbpObAQeXMTgB6RtquFFS6CypzBrrpQ9TzyA"
}

def limpar_aba_completa(aba, nome_aba):
    """Limpa conteúdo E formatação de uma aba"""
    print(f"  🗑️ Limpando conteúdo de {nome_aba}...")
    aba.clear()
    
    print(f"  🎨 Removendo formatação de {nome_aba}...")
    aba.format('A:ZZ', {
        "numberFormat": {"type": "TEXT"},  # Força formato texto
        "backgroundColor": {"red": 1, "green": 1, "blue": 1},  # Branco
        "textFormat": {
            "bold": False,
            "italic": False,
            "foregroundColor": {"red": 0, "green": 0, "blue": 0}
        }
    })
    print(f"  ✅ {nome_aba} - Conteúdo e formatação removidos")

print("🗑️ Iniciando exclusão COMPLETA de todas as linhas das planilhas...")

# 1. Limpa TUDO de Contas a Receber
print("\n📋 Limpando: Financeiro_contas_a_receber_Born")
planilha_receber = client.open_by_key(planilhas_ids["Financeiro_contas_a_receber_Born"])
aba_receber = planilha_receber.sheet1
limpar_aba_completa(aba_receber, "Contas a Receber")

# 2. Limpa TUDO de Contas a Pagar
print("\n📋 Limpando: Financeiro_contas_a_pagar_Born")
planilha_pagar = client.open_by_key(planilhas_ids["Financeiro_contas_a_pagar_Born"])
aba_pagar = planilha_pagar.sheet1
limpar_aba_completa(aba_pagar, "Contas a Pagar")

# 3. Limpa TUDO de Financeiro Completo - Aba principal (sheet1)
print("\n📋 Limpando: Financeiro_Completo_Born (sheet1)")
planilha_completo = client.open_by_key(planilhas_ids["Financeiro_Completo_Born"])
aba_completo = planilha_completo.sheet1
limpar_aba_completa(aba_completo, "Financeiro Completo - Principal")

# 4. Limpa TUDO de Financeiro Completo - Aba Dados_Pivotados (se existir)
print("\n📋 Limpando: Financeiro_Completo_Born (Dados_Pivotados)")
try:
    aba_pivotada = planilha_completo.worksheet("Dados_Pivotados")
    limpar_aba_completa(aba_pivotada, "Dados Pivotados")
except:
    print("  ⚠️ Aba 'Dados_Pivotados' não encontrada")

print("\n🎉 Limpeza completa concluída com sucesso!")
print("⚠️ ATENÇÃO: Conteúdo e formatação removidos. Células resetadas para formato TEXTO")
