import requests
from bs4 import BeautifulSoup
import re

def get_aguas_andinas_info(numero_cuenta: str):
    """
    Obtiene información de cuenta de Aguas Andinas usando requests con cookies de sesión.
    
    Args:
        numero_cuenta: Número de cuenta a consultar
    
    Returns:
        dict con la información de la cuenta o None si hay error
    """
    
    # Crear sesión para mantener cookies
    session = requests.Session()
    
    # Headers que simulan un navegador real
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'es,en-US;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'origin': 'https://www.aguasandinas.cl',
        'referer': 'https://www.aguasandinas.cl/web/aguasandinas/pagar-mi-cuenta',
    }
    
    session.headers.update(headers)
    
    # Cookies de sesión válida (estas expiran, hay que actualizarlas periódicamente)
    cookies = {
        'COOKIE_SUPPORT': 'true',
        'GUEST_LANGUAGE_ID': 'es_ES',
        'visid_incap_39543': 'KCVFrIyrTv2uYPEiTtm1BLvBX2kAAAAAQUIPAAAAAAAcgnFkdmGYuRojRTA2KADm',
        '_gcl_au': '1.1.786990405.1767883226',
        '_fbp': 'fb.1.1767883227440.43597438118615495',
        '_hjSessionUser_2360424': 'eyJpZCI6IjRhZTUzOTIxLTdiN2MtNTQ4Ny1iYTVhLWZhMDYwZjhhNTg3YiIsImNyZWF0ZWQiOjE3Njc4ODMyMjczNzMsImV4aXN0aW5nIjp0cnVlfQ==',
        'JSESSIONID': 'u26514dZw7K7LsMhoAvCo-gL-W4fVKx0E4JD28eu.nodo2',
        'U0z1e0Z0i1': '!pHLD0eUwIYcg2zenAOtUEGzwIRm4A5RPrMFTVeJSpnCoabPzujGojkWJbKKyEQbhJI11eTLK5reDC2i0W9pL+d1T+FnBukGgsNgFo02Sp9o=',
        'nlbi_39543': 'nJIqS5sllVJ+oJ1MXig80gAAAAAvVVAgj5EFx/drFeO9rW+X',
        'incap_ses_1842_39543': 'kJWuWdNbeFp1PA0H3BmQGY9ubmkAAAAAgF8tvdr9azVEeC1T4+EV9A==',
        '_gid': 'GA1.2.364709725.1768844953',
        '_clck': 'bgb12^2^g2u^0^2199',
        '_hjSession_2360424': 'eyJpZCI6IjRjNzBmNDc5LWQ4MDMtNGE1NS1hYWU2LWQzNjU3OTY3YzIzMCIsImMiOjE3Njg4NDQ5NTMwMzYsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=',
        '_ga': 'GA1.2.1626821661.1767883227',
        '_gat_UA-32844294-11': '1',
        'LFR_SESSION_STATE_54701': '1768845678127',
        '_clsk': '1ec21ka^1768845678808^6^1^v.clarity.ms/collect',
        'nlbi_39543_2147483392': 'fdVOUQTvKR8WoIq/Xig80gAAAACqBovgkRpIA8xcVvLRAxGW',
        'reese84': '3:p6UACN2zwo5HNIXV/bINLg==:FogjJkk9J2PxSvcLf5KuX3kXqKJ5wyglLs+08ZeAYZ/Q2epElJf3f9Nbjccdq+mwnK9tRRLTNfkmjU+xhq3COh+J8DzQw5Iw3pcbBtDseJEtw/rd54MKDGAuQZuxo1t2zSy/UxBEOOtTJ/VxxkgKiHSnOVtNv6fniNG2axOcboWCgihMOkDq/rja5+f74leJWzQFO8a9Eb2jg0qWhMRjIHaXpwtqYptrvnu/oDGBbG8PQlAIxdZ6tOlh1eAnZB3CdWmYVvup0YMyKjq1Gy5cmKWVzflm0zU1BRjmigo+iyV0PKVD+swPaQtSGNbObRXfkbzxjxqcf4gL6cQrd736K0DD0ADSxhB47eflRGrOCaMOlWBS4qo9Lz1TaJ6OmP7Xth4rZDoCfpc4aiBW3ieEG2CsFa1WaSa1f6FfXNKa7YS7idXD2NDrZ0TgTcGlTw4U0PLGd2fzPvLUUZS6KjYegvzNBM2ZQHpJxLR6fZ1rAUk=:HrciI9nMK7ZMytpdZks8EIBwQihNIobEuNiWH6ACCHo=',
        '_ga_PLWSNHH20D': 'GS2.1.s1768844945$o8$g1$t1768845696$j39$l0$h0',
    }
    
    session.cookies.update(cookies)
    
    # Primero hacemos GET a la página para obtener el p_auth token
    print("Obteniendo página principal...")
    main_url = 'https://www.aguasandinas.cl/web/aguasandinas/pagar-mi-cuenta'
    
    try:
        response = session.get(main_url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al obtener página principal: {e}")
        return None
    
    # Verificar si estamos bloqueados
    if "Access Denied" in response.text or "Error 15" in response.text:
        print("ERROR: Acceso bloqueado. Las cookies han expirado.")
        print("Necesitas obtener nuevas cookies desde el navegador.")
        return None
    
    # Buscar el p_auth token en la página
    p_auth_match = re.search(r'p_auth=([a-zA-Z0-9]+)', response.text)
    if p_auth_match:
        p_auth = p_auth_match.group(1)
        print(f"Token p_auth encontrado: {p_auth}")
    else:
        print("No se encontró el token p_auth, usando valor por defecto...")
        p_auth = "33ZMEBla"
    
    # URL para buscar cuenta
    portlet_id = "cl_aguasandinas_pago_cuenta_pub_PagarCuentaPubPorltetPortlet_INSTANCE_jL3QTDf9o9xo"
    search_url = f"https://www.aguasandinas.cl/web/aguasandinas/pagar-mi-cuenta?p_p_id={portlet_id}&p_p_lifecycle=1&p_p_state=normal&p_p_mode=view&_{portlet_id}_javax.portlet.action=%2Fcuenta%2Fbuscar&_{portlet_id}_cmd=buscar&p_auth={p_auth}"
    
    # Datos del formulario para buscar por número de cuenta
    form_data = {
        f'_{portlet_id}_buscador_cuenta': numero_cuenta,
        f'_{portlet_id}_tipoBuscar': 'cuenta',
        f'_{portlet_id}_agregarCuenta': 'x',
        f'_{portlet_id}_tipoConvenio': 'x',
    }
    
    print(f"Buscando cuenta: {numero_cuenta}...")
    
    try:
        response = session.post(search_url, data=form_data, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error en la búsqueda: {e}")
        return None
    
    # Verificar si estamos bloqueados
    if "Access Denied" in response.text or "Error 15" in response.text:
        print("ERROR: Acceso bloqueado durante la búsqueda.")
        return None
    
    # Parsear la respuesta HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Buscar información de la cuenta en la respuesta
    result = {
        'numero_cuenta': numero_cuenta,
        'html_response': response.text,
    }
    
    # Intentar extraer datos específicos
    # Buscar tabla de resultados o divs con información
    
    # Buscar el radio button que contiene la info de la cuenta
    radio_inputs = soup.find_all('input', {'type': 'radio'})
    for radio in radio_inputs:
        value = radio.get('value', '')
        if numero_cuenta in value:
            result['cuenta_info'] = value
            print(f"Información encontrada: {value}")
            break
    
    # Buscar montos o deudas
    monto_elements = soup.find_all(text=re.compile(r'\$[\d.,]+'))
    if monto_elements:
        result['montos'] = [m.strip() for m in monto_elements]
        print(f"Montos encontrados: {result['montos']}")
    
    # Buscar tablas con información
    tables = soup.find_all('table')
    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        if rows:
            result[f'tabla_{i}'] = []
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if cells:
                    result[f'tabla_{i}'].append([cell.get_text(strip=True) for cell in cells])
    
    print("\n" + "="*50)
    print("RESPUESTA OBTENIDA")
    print("="*50)
    
    # Mostrar un preview del HTML (primeros 3000 caracteres)
    print("\nPreview del HTML:")
    print(response.text[:3000])
    
    return result


def scrape_aguas_andinas():
    """Función principal para obtener datos de Aguas Andinas"""
    numero_cuenta = "1704598"
    
    result = get_aguas_andinas_info(numero_cuenta)
    
    if result:
        print("\n" + "="*50)
        print("DATOS EXTRAÍDOS:")
        print("="*50)
        for key, value in result.items():
            if key != 'html_response':
                print(f"{key}: {value}")
    else:
        print("No se pudo obtener información de la cuenta.")


if __name__ == "__main__":
    scrape_aguas_andinas()