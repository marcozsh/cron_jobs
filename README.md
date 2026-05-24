# Envio Gastos - Notificacion Automatica de Boletas
Sistema automatizado que consulta deudas de servicios basicos (**Agua**, **Gas**, **Luz**) y envia notificaciones por email cuando hay boletas pendientes.
## Estructura del Proyecto
envio_gastos/
├── agua/           # Scraper de Aguas Andinas (bypass Imperva)
│   ├── main.py
│   └── requirements.txt
├── gas/            # Consulta de Metrogas
│   └── main.py
├── luz/            # Consulta de CGE Luz
│   └── main.py
├── utils/          # Utilidades compartidas
│   ├── emails_templates.py   # Templates HTML para emails
│   └── resend_email.py       # Envio de emails via Resend API
├── requirements.txt
└── .env            # Variables de entorno
## Servicios
| Servicio | Metodo | Descripcion |
|----------|--------|-------------|
| **Agua** | Playwright + curl_cffi | Scraper con bypass de Imperva Incapsula |
| **Gas** | API REST (NO OFICIAL) | Consulta via Metrogas API |
| **Luz** | API REST (NO OFICIAL) | Consulta via CGE API |
## Instalacion
### Dependencias del sistema (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y python3-venv python3-pip
sudo apt install -y libgbm1 libnss3 libatk1.0-0 libatk-bridge2.0-0 \
  libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
  libxrandr2 libpango-1.0-0 libcairo2 libasound2 libxshmfence1
Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Playwright (solo para modulo Agua)
playwright install chromium
playwright install-deps chromium
Configuracion
Crear un archivo .env en la raiz con las siguientes variables:
# Resend API (envio de emails)
RESEND_API_KEY=re_xxxxxxxxxxxxx
FROM_EMAIL=notificaciones@tudominio.com
# Destinatarios (separados por coma)
MAILS_TO=email1@gmail.com,email2@gmail.com
# === AGUA ===
N_ACCOUNT=2854021
# === GAS ===
URL=https://api-metrogas.example.com
URL_JOBS=https://api-metrogas.example.com/jobs
# === LUZ ===
URL=https://api-cge.example.com/consulta
Uso
Ejecutar un modulo individual
# Agua
python agua/main.py
# Gas
python gas/main.py
# Luz
python luz/main.py
Ejecutar con cron
# Abrir editor de cron
crontab -e
# Consultar deuda todos los dias a las 9:00 AM
0 11 * * * cd /home/ubuntu/desktop/cron_jobs && /home/ubuntu/desktop/.venv/bin/python -m luz.main >> /home/ubuntu/desktop/cron_jobs/logs/luz_$(date +\%Y-\%m-\%d).log 2>&1
0 11 * * * cd /home/ubuntu/desktop/cron_jobs && /home/ubuntu/desktop/.venv/bin/python -m gas.main >> /home/ubuntu/desktop/cron_jobs/logs/gas_$(date +\%Y-\%m-\%d).log 2>&1
0 11 * * * cd /home/ubuntu/desktop/cron_jobs && /home/ubuntu/desktop/.venv/bin/python -m agua.main >> /home/ubuntu/desktop/cron_jobs/logs/agua_$(date +\%Y-\%m-\%d).log 2>&1
Bypass de Imperva (Modulo Agua)
El modulo de Agua utiliza un enfoque hibrido para bypass de Imperva Incapsula:
1. Playwright carga la pagina y resuelve los JS challenges de Imperva, obteniendo cookies validas (visid_incap, incap_ses)
2. curl_cffi realiza el POST con TLS fingerprint de Chrome 131 (evita deteccion por JA3 fingerprint)
Tecnicas aplicadas:
- TLS fingerprint matching (impersonate="chrome131")
- Cookies de sesion obtenidas via navegador real
- Headers completos de navegador (Sec-CH-UA, Sec-Fetch-*)
- User-Agent de Chrome 143
- Delays y comportamiento humano simulado
Dependencias
resend
python-dotenv
playwright
curl_cffi
beautifulsoup4
requests
