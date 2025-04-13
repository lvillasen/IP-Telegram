import requests
import socket
import re
import netifaces

# 🔹 CONFIGURACIÓN
BOT_TOKEN = "XXXX431784:AAE_kX2ovPmx7P6mP_eTCPuQS0marxbdWbk"  # Reemplázalo con tu token
CHAT_ID = "XXXX83105"  # Reemplázalo con tu ID de Telegram

# 🔹 Función para obtener la IP local de una interfaz (eth0, wlan0, etc.)
def get_ip(interface):
    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    except:
        return "No disponible"

# 🔹 Función para obtener la IP pública
def get_public_ip():
    try:
        return requests.get("https://api64.ipify.org?format=text", timeout=5).text
    except:
        return "No se pudo obtener la IP pública"

# 🔹 Escapar caracteres reservados en MarkdownV2
def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

# 🔹 Obtener IPs y escapar caracteres
ip_eth0 = escape_markdown(get_ip("eth0"))
ip_wlan0 = escape_markdown(get_ip("wlan0"))
ip_publica = escape_markdown(get_public_ip())

mensaje = (
    f"📡 *IP de la Raspberry Pi5*\n\n"
    f"🌍 *Pública:* {ip_publica}\n"
    f"🔌 *eth0:* {ip_eth0}\n"
    f"📶 *wlan0:* {ip_wlan0}"
)

# 🔹 Enviar mensaje por Telegram
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
params = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "MarkdownV2"}

try:
    response = requests.get(URL, params=params, timeout=5)
    if response.status_code == 200:
        print("✅ Mensaje enviado con éxito.")
    else:
        print("❌ Error al enviar el mensaje:", response.text)
except Exception as e:
    print("❌ Error:", e)
