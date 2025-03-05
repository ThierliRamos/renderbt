from flask import Flask, request, render_template
import requests
import time

app = Flask(__name__)

def buscar_informacoes_ip(ip_address, is_dono, is_vip):
    try:
        # Verifica se o usuário pode usar o comando
        pode_usar = is_dono or is_vip
        if not pode_usar:
            return "🔐 Apenas pessoas autorizadas podem usar!"
        
        time.sleep(1)  # Espera 1 segundo

        url = f"https://ip-geo-location.p.rapidapi.com/ip/check?format=json&language=pt&filter={ip_address}"
        headers = {
            "x-rapidapi-key": "99bb57d209mshb6ca809dc147a3ep1a51e7jsnf829ae92aef6",
            "x-rapidapi-host": "ip-geo-location.p.rapidapi.com",
        }

        print(f"Consultando: {url}")

        response = requests.get(url, headers=headers)

        # Verifica se a resposta da API foi bem-sucedida
        if response.status_code != 200:
            print(f"Erro na API: {response.status_code} - {response.text}")
            return f"Erro na API: {response.status_code} - {response.text}"

        data = response.json()
        print(f"Dados recebidos: {data}")  # Log para verificar o que foi recebido

        if data:
            # Monta a resposta a ser retornada
            resultado = (f"<div><strong>IP Identificado:</strong> {data['ip']}</div>"
                         f"<div><strong>Organização:</strong> {data['asn']['organisation']}</div>"
                         f"<div><strong>País:</strong> {data['country']['name']}</div>"
                         f"<div><strong>Região:</strong> {data['area']['name']}</div>"  # Alterado para 'area'
                         f"<div><strong>Cidade:</strong> {data['city']['name']}</div>"
                         f"<div><strong>População:</strong> {data['city']['population']}</div>"  # Alterado para 'city'
                         f"<div><strong>Latitude:</strong> {data['location']['latitude']}</div>"
                         f"<div><strong>Longitude:</strong> {data['location']['longitude']}</div>"
                         f"<div><strong>Fuso Horário:</strong> {data['time']['timezone']}</div>")
            return resultado
        else:
            print("Nenhum dado encontrado para este IP.")
            return "Nenhum dado encontrado para este IP."
    except requests.exceptions.RequestException as req_error:
        print(f"Erro de requisição: {req_error}")
        return "Erro ao buscar informações! Verifique a conexão com a API."
    except Exception as error:
        print(f"Erro inesperado: {error}")
        return "Erro ao buscar informações!"

@app.route('/check_ip', methods=['POST'])
def check_ip():
    ip_address = request.form.get('ip')
    print(f"IP recebido: {ip_address}")  # Log para verificar o IP recebido
    resultado = buscar_informacoes_ip(ip_address, is_dono=False, is_vip=True)
    
    # Verifica se o resultado é uma string e imprime no console
    print(f"Resultado da consulta: {resultado}")  # Log para verificar o resultado
    return render_template('ip.html', message=resultado)

@app.route('/')
def ip():
    return render_template('ip.html', message=None)

if __name__ == '__main__':
    app.run(debug=True)
