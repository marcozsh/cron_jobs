import requests
from dotenv import load_dotenv
import os
import sys
from datetime import datetime
from utils.emails_templates import get_down_alert_template
from utils.resend_email import send_email


load_dotenv()
URL_CHECK = os.getenv('URL_CHECK') or sys.exit("URL_CHECK no está configurado en las variables de entorno.")
today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    urls = URL_CHECK.split(',')
    for url in urls:
        url = url.strip()
        print(f"{today_date} - Verificando {url}...")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'}
            response = requests.get(f"https://{url}", timeout=10, headers=headers, allow_redirects=True)
            if response.status_code == 200:
                print(f"{today_date} - {url} está disponible.")
            else:
                response_google_api = requests.get(f"https://dns.google/resolve?name={url}", timeout=10)
                data = response_google_api.json()
                status = data.get('Status')
                if status == 0:
                    print(f"{today_date} - {url} tiene resolución DNS correcta pero respondió con código {response.status_code}.")
                else:
                    html_content = get_down_alert_template(url, today_date, "DNS resolution failed", str(response.status_code), 0)
                    send_email('marc.penar@outlook.cl', f"Alerta: {url} no responde", html_content)
                    print(f"{today_date} - {url} no tiene resolución DNS (Status: {status}) y respondió con código {response.status_code}.")
        except requests.exceptions.ConnectionError as e:
            html_content = get_down_alert_template(url, today_date, "Connection failed", "N/A", 0)
            send_email('marc.penar@outlook.cl', f"Alerta: {url} no responde", html_content)
            print(f"{today_date} - {url} no se pudo conectar: {e}")
        except requests.RequestException as e:
            html_content = get_down_alert_template(url, today_date, str(type(e).__name__), "N/A", 0)
            send_email('marc.penar@outlook.cl', f"Alerta: {url} no responde", html_content)
            print(f"{today_date} - {url} error: {e}")

if __name__ == '__main__':
    main()
