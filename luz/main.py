import resend
from dotenv import load_dotenv
import os 
import sys
import json
import requests
from time import sleep
from datetime import datetime

today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
only_date = datetime.now().strftime("%d/%m/%Y")

load_dotenv()

API_KEY=os.getenv('RESEND_API_KEY') or sys.exit("RESEND_API_KEY no está configurado en las variables de entorno.")
resend.api_key = API_KEY
FROM_EMAIL = os.getenv('FROM_EMAIL') or sys.exit("FROM_EMAIL no está configurado en las variables de entorno.")
URL = os.getenv('URL') or sys.exit("URL no está configurado en las variables de entorno.")
N_ACCOUNT = os.getenv('N_ACCOUNT') or sys.exit("N_ACCOUNT no está configurado en las variables de entorno.")
MAILS_TO = os.getenv('MAILS_TO') or sys.exit("MAILS_TO no está configurado en las variables de entorno.")

def send_email(to, subject, html):
    response = resend.Emails.send({
        "from": FROM_EMAIL,
        "to": to,
        "subject": subject,
        "html": html
    })
    return response
    
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

def get_electricity_bill_template(user_name: str, account_number: str, due_date: str, amount: str, payment_link: str = "#") -> str:
    """
    Template HTML para notificación de factura de luz disponible
    
    Args:
        user_name: Nombre del usuario
        account_number: Número de cuenta
        due_date: Fecha de vencimiento
        amount: Monto a pagar
        payment_link: URL para realizar el pago
    """
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Factura de Luz Disponible</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
        <table role="presentation" style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 20px 0; text-align: center; background-color: #f4f4f4;">
                    <table role="presentation" style="width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <!-- Header -->
                        <tr>
                            <td style="padding: 40px 40px 20px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px 8px 0 0;">
                                <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: bold;">⚡ Factura Disponible</h1>
                            </td>
                        </tr>
                        
                        <!-- Saludo -->
                        <tr>
                            <td style="padding: 30px 40px 20px;">
                                <p style="margin: 0; font-size: 16px; color: #333333; line-height: 1.5;">
                                    Hola <strong>{user_name}</strong>,
                                </p>
                                <p style="margin: 15px 0 0; font-size: 16px; color: #333333; line-height: 1.5;">
                                    Tu factura de electricidad ya está disponible para consulta y pago.
                                </p>
                            </td>
                        </tr>
                        
                        <!-- Detalles de la factura -->
                        <tr>
                            <td style="padding: 20px 40px;">
                                <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f8f9fa; border-radius: 6px; padding: 20px;">
                                    <tr>
                                        <td style="padding: 15px;">
                                            <table role="presentation" style="width: 100%; border-collapse: collapse;">
                                                <tr>
                                                    <td style="padding: 8px 0; font-size: 14px; color: #666666;">
                                                        <strong>Número de cuenta:</strong>
                                                    </td>
                                                    <td style="padding: 8px 0; font-size: 14px; color: #333333; text-align: right;">
                                                        {account_number}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 8px 0; font-size: 14px; color: #666666; border-top: 1px solid #e0e0e0;">
                                                        <strong>Monto a pagar:</strong>
                                                    </td>
                                                    <td style="padding: 8px 0; font-size: 20px; color: #667eea; text-align: right; font-weight: bold; border-top: 1px solid #e0e0e0;">
                                                        ${amount}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="padding: 8px 0; font-size: 14px; color: #666666; border-top: 1px solid #e0e0e0;">
                                                        <strong>Fecha de consulta:</strong>
                                                    </td>
                                                    <td style="padding: 8px 0; font-size: 14px; color: #d32f2f; text-align: right; font-weight: bold; border-top: 1px solid #e0e0e0;">
                                                        {due_date}
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        
                        <!-- Botón de acción -->
                        <tr>
                            <td style="padding: 20px 40px 30px; text-align: center;">
                                <a href="{payment_link}" style="display: inline-block; padding: 14px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; border-radius: 6px; font-size: 16px; font-weight: bold; box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);">
                                    Ver Factura y Pagar
                                </a>
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    return html_template

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
                subject="Alerta de deuda pendiente",
                html=get_electricity_bill_template(
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