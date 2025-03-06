import yfinance as yf
import smtplib
import email.message
import time
from datetime import datetime, timedelta

# Função para obter o preço da ação
def obter_preco_acao(ativo):
    dados = yf.Ticker(ativo)
    preco_atual = dados.info.get("regularMarketPrice")

    if preco_atual:
        return preco_atual
    else:
        return None

# Função para enviar o e-mail
def enviar_email(ativo, preco_acao, preco_limite, ultima_verificacao):
    if preco_acao is None:
        print(f"Não foi possível obter o preço da ação {ativo}.")
        return ultima_verificacao

    # Verifica se já passou 5 minutos desde o último envio de e-mail
    if ultima_verificacao and datetime.now() < ultima_verificacao + timedelta(minutes=5):
        print(f"\033[93mO e-mail já foi enviado para {ativo} nos últimos 5 minutos. Aguardando próxima verificação.\033[0m")
        return ultima_verificacao

    if preco_acao <= preco_limite:
        corpo_email = f"""
        <p>O preço atual de {ativo} é <strong>R$ {preco_acao:.2f}<strong></p>
        """
        
        msg = email.message.Message()
        msg['Subject'] = f"Preço Atual da Ação {ativo}"
        msg['From'] = 'lucasthiago553@gmail.com'
        msg['To'] = 'lucasthiago553@gmail.com'
        password = 'isgc vmqg avmd etwj'  # Senha de aplicativo do Gmail
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(msg['From'], password)
            s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            s.quit()
            print(f'\033[92mE-mail enviado com sucesso para {ativo}!\033[0m')

            # Atualiza o horário do último envio de e-mail
            return datetime.now()
        except Exception as e:
            print(f'Erro ao enviar e-mail para {ativo}: {e}')
    else:
        print(f'\033[91mO preço da ação {ativo} é R$ {preco_acao:.2f}. O e-mail não será enviado.\033[0m')
    
    return ultima_verificacao

# Dicionário de ativos com seus respectivos preços limites e tempos de última verificação
ativos_limite = {
    "BBDC4.SA": {"limite": 10.40, "ultima_verificacao": None},
    "PETR4.SA": {"limite": 34.92, "ultima_verificacao": None},
    "MGLU3.SA": {"limite": 6.02, "ultima_verificacao": None}
}

# Loop para verificar os preços periodicamente
while True:
    for ativo, dados in ativos_limite.items():
        preco_acao = obter_preco_acao(ativo)
        # Chama a função para enviar e-mail e atualizar a última verificação
        dados["ultima_verificacao"] = enviar_email(ativo, preco_acao, dados["limite"], dados["ultima_verificacao"])
    print("-"*65)
    time.sleep(10)  # Espera 10 segundos antes da próxima verificação
