from flask import render_template
import requests

def verificar_bin(bin_number):
    is_dono = True  # Aqui você pode definir a lógica para verificar se o usuário é o dono
    is_vip = False  # Aqui você pode definir a lógica para verificar se o usuário é VIP

    pode_usar = is_dono or is_vip

    if not pode_usar:
        return render_template('bin.html', message="🔐 Apenas pessoas autorizadas podem usar!")

    try:
        headers = {
            "X-RapidAPI-Key": "99bb57d209mshb6ca809dc147a3ep1a51e7jsnf829ae92aef6",
            "X-RapidAPI-Host": "bin-ip-checker.p.rapidapi.com",
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"https://bin-ip-checker.p.rapidapi.com/?bin={bin_number}",
            headers=headers,
            json={"bin": bin_number}
        )

        if response.status_code != 200:
            return render_template('bin.html', message="Erro na API: " + str(response.status_code))

        data = response.json()

        # Debug: Imprima a resposta da API
        print("Resposta da API:", data)

        if 'BIN' in data:
            result = (
                f"<div>📍 <strong>BIN Identificada:</strong> {data['BIN']['number']}</div>"
                f"<div>💳 <strong>Tipo:</strong> {data['BIN']['type']}</div>"
                f"<div>📶 <strong>Level:</strong> {data['BIN']['level']}</div>"
                f"<div>🏳️ <strong>Bandeira:</strong> {data['BIN']['scheme']}</div>"
                f"<div>🏦 <strong>Banco:</strong> {data['BIN']['issuer']['name']}</div>"
                f"<div>🌎 <strong>País:</strong> {data['BIN']['country']['name']}</div>"
                f"<div>💰 <strong>Moeda:</strong> {data['BIN']['country']['currency']}</div>"
                f"<div>🏠 <strong>Capital:</strong> {data['BIN']['country']['capital']}</div>"
            )
            return render_template('bin.html', message=result)  # Retorna para a página com a mensagem
        else:
            return render_template('bin.html', message="BIN não encontrada!")

    except Exception as e:
        print(f"Erro ao processar a solicitação: {e}")
        return render_template('bin.html', message="Erro ao buscar BIN!")
