import os
import sys
import re
import time
import random
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from curl_cffi import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.emails_templates import get_template
from utils.resend_email import send_email

load_dotenv()

today_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
only_date = datetime.now().strftime("%d/%m/%Y")

N_ACCOUNT = os.getenv('N_ACCOUNT') or sys.exit("N_ACCOUNT no está configurado en las variables de entorno.")
MAILS_TO = os.getenv('MAILS_TO') or sys.exit("MAILS_TO no está configurado en las variables de entorno.")




def get_aguas_andinas_info(numero_cuenta: str, headless: bool = True):
    
    session = requests.Session()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            args=['--disable-blink-features=AutomationControlled', '--disable-dev-shm-usage', '--no-sandbox']
        )
        
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            locale='es-ES',
            timezone_id='America/Santiago',
        )
        
        page = context.new_page()
        
        try:
            print(f"{today_date} - Navegando a Aguas Andinas...")
            main_url = 'https://www.aguasandinas.cl/web/aguasandinas/pagar-mi-cuenta'
            
            response = page.goto(main_url, wait_until='networkidle', timeout=45000)
            
            if response.status == 403:
                print(f"{today_date} - Bloqueado 403, reintentando...")
                time.sleep(random.uniform(5, 10))
                response = page.goto(main_url, wait_until='networkidle', timeout=45000)
            
            page_content = page.content()
            if 'Access Denied' in page_content or 'Powered By Incapsula' in page_content:
                print(f"{today_date} - Esperando challenge de JS...")
                time.sleep(random.uniform(10, 20))
                page.reload(wait_until='networkidle', timeout=45000)
                page_content = page.content()
                
                if 'Access Denied' in page_content or 'Powered By Incapsula' in page_content:
                    print(f"{today_date} - Sigue bloqueado.")
                    return None
            
            print(f"{today_date} - Pagina cargada. Status: {response.status}")
            
            cookies = context.cookies()
            
            for c in cookies:
                session.cookies.set(c['name'], c['value'], domain=c.get('domain', '.aguasandinas.cl'), path=c.get('path', '/'))
            
            p_auth_match = re.search(r'p_auth=([a-zA-Z0-9]+)', page_content)
            p_auth = p_auth_match.group(1) if p_auth_match else "33ZMEBla"
            
            browser.close()
            
        except Exception as e:
            print(f"{today_date} - Error en Playwright: {e}")
            browser.close()
            return None
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'es,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://www.aguasandinas.cl',
        'Pragma': 'no-cache',
        'Referer': 'https://www.aguasandinas.cl/web/aguasandinas/pagar-mi-cuenta',
        'Sec-CH-UA': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    }
    
    portlet_id = "cl_aguasandinas_pago_cuenta_pub_PagarCuentaPubPorltetPortlet_INSTANCE_jL3QTDf9o9xo"
    
    print(f"\n=== {today_date} - PASO 1: Buscando cuenta ===")
    
    search_url = (
        f"https://www.aguasandinas.cl/web/aguasandinas/pagar-mi-cuenta"
        f"?p_p_id={portlet_id}"
        f"&p_p_lifecycle=1"
        f"&p_p_state=normal"
        f"&p_p_mode=view"
        f"&_{portlet_id}_javax.portlet.action=%2Fcuenta%2Fbuscar"
        f"&_{portlet_id}_cmd=buscar"
        f"&p_auth={p_auth}"
    )
    
    form_data = {
        f'_{portlet_id}_buscador_cuenta': numero_cuenta,
        f'_{portlet_id}_tipoBuscar': 'cuenta',
        f'_{portlet_id}_agregarCuenta': 'x',
        f'_{portlet_id}_tipoConvenio': 'x',
    }
    
    response = session.post(search_url, headers=headers, data=form_data, timeout=30, impersonate="chrome131")
    #print(f"POST Status: {response.status_code}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    form_agregar = soup.find('form', {'id': 'agregar_cuentas'})
    if not form_agregar:
        print(f"{today_date} - No se encontro formulario 'agregar_cuentas'")
        return None
    
    form_action = form_agregar.get('action', '')
    if form_action.startswith('/'):
        form_action = f"https://www.aguasandinas.cl{form_action}"
    
    radios = form_agregar.find_all('input', {'type': 'radio'})
    if not radios:
        print(f"{today_date} - No se encontraron radio buttons")
        return None
    
    first_radio = radios[0]
    first_radio_name = first_radio.get('name', '')
    first_radio_value = first_radio.get('value', '')
    print(f"{today_date} - Cuenta encontrada: {first_radio_value}")
    
    result = {
        'numero_cuenta': numero_cuenta,
        'cuenta_info': first_radio_value,
    }
    
    print(f"\n=== {today_date} - PASO 2: Seleccionando cuenta ===")
    
    submit_data = {first_radio_name: first_radio_value}
    
    hidden_inputs = form_agregar.find_all('input', {'type': 'hidden'})
    for hidden in hidden_inputs:
        name = hidden.get('name')
        value = hidden.get('value', '')
        if name:
            submit_data[name] = value
    
    time.sleep(random.uniform(2, 4))
    
    response2 = session.post(form_action, headers=headers, data=submit_data, timeout=30, impersonate="chrome131")
    #print(f"Submit Status: {response2.status_code}")
    
    print(f"\n=== {today_date} - PASO 3: Analizando pagina de pago ===")
    
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    
    if 'Realizar el Pago' in soup2.get_text():
        #print("Pagina de pago cargada correctamente")
        result['realizar_pago'] = True
    else:
        result['realizar_pago'] = False
    
    div_total = soup2.find('div', {'id': 'div-total'})
    if div_total:
        saldo_text = div_total.get_text(strip=True)
        print(f"{today_date} - Deuda encontrada: {saldo_text}")
        result['tiene_deuda'] = True
        result['saldo'] = saldo_text.replace("$", "")
        
        monto_match = re.search(r'\$[\d.,]+', saldo_text)
        if monto_match:
            result['monto_deuda'] = monto_match.group()
    else:
        cuenta_dia = soup2.find(class_='palabra-cuenta-dia')
        if cuenta_dia:
            texto = cuenta_dia.get_text(strip=True)
            print(f"{today_date} - Estado: {texto}")
            result['tiene_deuda'] = False
            result['estado'] = texto
        else:
            print(f"{today_date} - No se encontro informacion de deuda")
            result['tiene_deuda'] = None
    
    return result


def scrape_aguas_andinas():
    #numero_cuenta = "2854021"
    #N_ACCOUNT=1704598
    #N_ACCOUNT=2854021
    result = get_aguas_andinas_info(N_ACCOUNT, headless=True)
    
    if result:
        print("\n" + "="*50)
        print(f"{today_date} - DATOS EXTRAIDOS:")
        print("="*50)
        for key, value in result.items(): 
            print(f"{today_date} - {key}: {value}")
        print("="*50 + "\n")
        if result['tiene_deuda']:
            for emails in MAILS_TO.split(","):
                html_content = get_template(
                    type_account="Agua",
                    user_name="Marco Peña",
                    account_number=N_ACCOUNT,
                    due_date=only_date,
                    amount=str(result['saldo']),
                    payment_link="https://www.aguasandinas.cl/web/aguasandinas/pagar-mi-cuenta"
                )
                subject = "⚡ Boleta de Agua Disponible"
                response = send_email(
                    to=emails.strip(),
                    subject=subject,
                    html=html_content
                )
                print(f"{today_date} - Correo enviado a {emails.strip()}: {response['id']}")
    else:
        print(f"{today_date} - No se pudo obtener informacion.")


if __name__ == "__main__":
    scrape_aguas_andinas()
