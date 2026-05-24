import os 
import sys
import requests
from dotenv import load_dotenv
from time import sleep
from utils.resend_email import send_email
from utils.emails_templates import get_template
from datetime import datetime

load_dotenv()

today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
only_date = datetime.now().strftime("%d/%m/%Y")

URL = os.getenv('URL') or sys.exit("URL no está configurado en las variables de entorno.")
URL_JOBS = os.getenv('URL_JOBS') or sys.exit("URL no está configurado en las variables de entorno.")
N_ACCOUNT = os.getenv('N_ACCOUNT') or sys.exit("N_ACCOUNT no está configurado en las variables de entorno.")
MAILS_TO = os.getenv('MAILS_TO') or sys.exit("MAILS_TO no está configurado en las variables de entorno.")

def get_job():
    headers = {
        "utility-id": "24"
    }
    for i in range(1, 6):  # Intentar hasta 5 veces
        try:
            print(f"{today_date} - Intento {i}: Obteniendo job ID para la cuenta {N_ACCOUNT}...")
            print(f"{today_date} - URL de solicitud: {URL}?client_number={N_ACCOUNT}&gateway=bco_macro")
            response = requests.get(f"{URL}/?client_number={N_ACCOUNT}&gateway=bco_macro", headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["job_id"] is not None:
                print(f"{today_date} - Job ID obtenido: {data['job_id']}")
                return data["job_id"]
            elif data["message"] == "No outstanding debt":
                return 0,
            else:
                return None,
        except Exception:
            sleep(2) #Esperar 2 segundos antes de reintentar

def get_debt():
    job_id = get_job()
    if job_id is None:
        return None
    elif job_id == 0:
        return 0,
    
    for i in range(1, 6):  # Intentar hasta 5 veces
        try:
            print(f"{today_date} - Intento {i}: Verificando deuda para el job ID {job_id}...")
            print(f"{today_date} - URL de solicitud: {URL_JOBS}?id={job_id}")
            response = requests.get(f"{URL_JOBS}?id={job_id}", timeout=10)
            response.raise_for_status()
            data = response.json()
            if data["debts"] is not None and len(data["debts"]) > 0:
                print(f"{today_date} - Deuda encontrada: {data['debts'][0]['amount']}")
                debt = data["debts"][0]["amount"]
                return debt,
            else:
                print(f"{today_date} - No se encontró deuda para el job ID {job_id}.")
                return 0,
        except Exception:
            print(f"{today_date} - Error al verificar deuda para el job ID {job_id}. Reintentando...")
            sleep(2) #Esperar 2 segundos antes de reintentar
    return None
    


if __name__ == "__main__":
    print(f"{today_date} - Iniciando proceso de verificación de deuda...")
    data = get_debt()
    if data is None:
        print(f"{today_date} - No se pudo obtener la información de deuda.")
        sys.exit(1)
    if data[0] == 0 or data[0] is None:
        print(f"{today_date} - No hay deuda pendiente.")
    elif data[0] > 0:
        print(f"{today_date} - Cliente presenta deuda de ${data[0]}")
        for emails in MAILS_TO.split(","):
            html_content = get_template(
                type_account="Gas",
                user_name="Marco Peña",
                account_number=N_ACCOUNT,
                due_date=only_date,
                amount=str(data[0]),
                payment_link="https://sucursalvirtual.metrogas.cl/pagos"
            )
            subject = "⚡ Boleta de Gas Disponible"
            response = send_email(
                to=emails.strip(),
                subject=subject,
                html=html_content
            )
            print(f"{today_date} - Correo enviado a {emails.strip()}: {response['id']}")
    print(f"{today_date} - Proceso de verificación de deuda finalizado.")
