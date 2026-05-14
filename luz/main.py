import resend
from dotenv import load_dotenv
import os 
import sys
import json
import requests
from time import sleep
from datetime import datetime
from utils.resend_email import send_email
from utils.emails_templates import get_template


today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
only_date = datetime.now().strftime("%d/%m/%Y")

load_dotenv()


URL = os.getenv('URL') or sys.exit("URL no está configurado en las variables de entorno.")
N_ACCOUNT = os.getenv('N_ACCOUNT') or sys.exit("N_ACCOUNT no está configurado en las variables de entorno.")
MAILS_TO = os.getenv('MAILS_TO') or sys.exit("MAILS_TO no está configurado en las variables de entorno.")

def get_debt():
    headers= {
        "content-type": "application/json",
    }
    
    body ={
        "I_CANAL": "OVIRTUAL",
        "I_VKONT": N_ACCOUNT,
        "Sociedad": "E200",
        "url": "OFVCGE_P" 
    }
    for i in range(1, 6):  # Intentar hasta 5 veces
        try:
            response = requests.post(URL, headers=headers, data=json.dumps(body), timeout=10)
            response.raise_for_status()
            data = response.json()
            if (data["message"]) == "" or data["message"] is None:
                debt = data["deudaActual"]["BETRW"]
                nrzas = data["deudaActual"]["NRZAS"]
                return debt, nrzas
            elif (data["message"]) != "" and data["message"] == "Cliente no presenta deuda":
                return 0, 0
            else:
                return None, None
        except Exception:
            sleep(2) #Esperar 2 segundos antes de reintentar

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
            print(f"{today_date} - Enviando correo a {emails.strip()}...")
            email_send = (send_email(
                to=emails.strip(),
                subject="⚡ Factura de Luz Disponible",
                html=get_template(
                    type_account="luz",
                    user_name="Marcos Peña",
                    account_number=N_ACCOUNT,
                    due_date=only_date,
                    amount=str(data[0]),
                    payment_link=f"https://payments-gateway.grupocge.cl/payment/santander?nrzas={data[1]}&ctaCto={N_ACCOUNT}&debtValue={int(data[0])}&channel=URL&company=CGE&email={emails.strip()}&calloutURL=https://sucursalvirtual.cge.cl/comprobante-de-pago"
                )))
            if email_send["id"] is not None:
                print(f"{today_date} - Correo enviado correctamente a {emails.strip()}. ID: {email_send['id']}")
            else:
                print(f"{today_date} - Error al enviar correo a {emails.strip()}.")
    print(f"{today_date} - Proceso finalizado.")
