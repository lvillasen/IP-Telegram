import socket
import re
import http.client
import urllib.parse

# 🔹 CONFIGURACIÓN
BOT_TOKEN = "XXXXXXXXX84:AAE_kX2ovPmx7P6mP_eTCPuQS0marxbdWbk"  # Reemplázalo con tu token
CHAT_ID = "XXXXXXXX"  # Reemplázalo con tu ID de Telegram

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
        conn = http.client.HTTPSConnection("api64.ipify.org")
        conn.request("GET", "/?format=text")
        response = conn.getresponse()
        if response.status == 200:
            ip_publica = response.read().decode("utf-8")
            conn.close()
            return ip_publica
        else:
            conn.close()
            return "No se pudo obtener la IP pública"
    except:
        return "No se pudo obtener la IP pública"

# 🔹 Escapar caracteres reservados en MarkdownV2
def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r"([{}])".format(re.escape(escape_chars)), r"\\\1", text)

# 🔹 Obtener IPs y escapar caracteres
ip_local = escape_markdown(get_local_ip())
ip_publica = escape_markdown(get_public_ip())

mensaje = "📡 *IP de la Raspberry Pi*\n\n🌍 *Pública:* {0}\n🏠 *Local:* {1}".format(ip_publica, ip_local)

# 🔹 Enviar mensaje por Telegram
URL = "/bot{0}/sendMessage".format(BOT_TOKEN)
params = urllib.parse.urlencode({
    "chat_id": CHAT_ID,
    "text": mensaje,
    "parse_mode": "MarkdownV2"
})

# Conexión HTTPS con Telegram API
try:
    conn = http.client.HTTPSConnection("api.telegram.org")
    conn.request("GET", "{0}?{1}".format(URL, params))
    response = conn.getresponse()
    if response.status == 200:
        print("✅ Mensaje enviado con éxito.")
    else:
        print("❌ Error al enviar el mensaje:", response.read().decode())
    conn.close()
except Exception as e:
    print("❌ Error:", e)
