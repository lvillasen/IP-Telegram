import requests
import socket
import re
import netifaces

# 🔹 CONFIGURACIÓN
BOT_TOKEN = "XXXXXXXXXX_XXXXXXXXXXX_XXXX"  # Reemplázalo con tu token
CHAT_ID = "XXXXXXXXXX"  # Reemplázalo con tu ID de Telegram

# 🔹 Función para obtener la IP local de la primera interfaz activa
def get_local_ip():
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip = addr.get('addr')
                if ip != "127.0.0.1":
                    return ip
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
ip_local = escape_markdown(get_local_ip())
ip_publica = escape_markdown(get_public_ip())

mensaje = (
    f"📡 *IP de la PC Home*\n\n"
    f"🌍 *Pública:* {ip_publica}\n"
    f"💻 *Local:* {ip_local}"
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
