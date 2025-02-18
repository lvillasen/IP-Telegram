import requests
import socket
import re

# 🔹 CONFIGURACIÓN
BOT_TOKEN = "XXXXXXX:AAE_kX2ovPmx7P6mP_eTCPuQS0marxbdWbk"  # Reemplázalo con tu token
CHAT_ID = "540XXXXX"  # Reemplázalo con tu ID de Telegram

# 🔹 Función para obtener la IP local de la Raspberry Pi
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except:
        return "No se pudo obtener la IP local"

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
ip_local = escape_markdown(get_local_ip())
ip_publica = escape_markdown(get_public_ip())

mensaje = f"📡 *IP de la Raspberry Pi*\n\n🌍 *Pública:* {ip_publica}\n🏠 *Local:* {ip_local}"

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
