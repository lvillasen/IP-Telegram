import socket
import re
import http.client
import urllib.parse
import subprocess

# 🔹 CONFIGURACIÓN
BOT_TOKEN = "XXXXX31784:AAE_kX2ovPmx7P6mP_eTCPuQS0marxbdWbk"
CHAT_ID = "XXXXX3105"

# 🔹 Función para obtener la IP de una interfaz como eth0 o wlan0
def get_ip(interface):
    try:
        output = subprocess.check_output(["ip", "addr", "show", interface]).decode("utf-8")
        for line in output.split("\n"):
            line = line.strip()
            if line.startswith("inet "):
                return line.split()[1].split("/")[0]
        return "No disponible"
    except Exception as e:
        return "Error al obtener IP de {}: {}".format(interface, e)

# 🔹 Función para obtener la IP pública
def get_public_ip():
    conn = None
    try:
        conn = http.client.HTTPSConnection("api64.ipify.org", timeout=5)
        conn.request("GET", "/?format=text")
        response = conn.getresponse()
        if response.status == 200:
            ip_publica = response.read().decode("utf-8")
            return ip_publica
        else:
            return "Error código {}".format(response.status)
    except Exception as e:
        return "Error: {}".format(e)
    finally:
        if conn:
            conn.close()

# 🔹 Escapar caracteres reservados en MarkdownV2
def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(r"([{}])".format(re.escape(escape_chars)), r"\\\1", text)

# 🔹 Obtener IPs
ip_eth0 = escape_markdown(get_ip("eth0"))
ip_wlan0 = escape_markdown(get_ip("wlan0"))
ip_publica = escape_markdown(get_public_ip())

# 🔹 Armar el mensaje
mensaje = "📡 *IP del dispositivo*\n\n🌐 *Pública:* {0}\n🔌 *eth0:* {1}\n📶 *wlan0:* {2}".format(
    ip_publica, ip_eth0, ip_wlan0
)

# 🔹 Enviar mensaje por Telegram
URL = "/bot{0}/sendMessage".format(BOT_TOKEN)
params = urllib.parse.urlencode({
    "chat_id": CHAT_ID,
    "text": mensaje,
    "parse_mode": "MarkdownV2"
})

try:
    conn = http.client.HTTPSConnection("api.telegram.org", timeout=10)
    conn.request("GET", "{0}?{1}".format(URL, params))
    response = conn.getresponse()
    if response.status == 200:
        print("✅ Mensaje enviado con éxito.")
    else:
        print("❌ Error al enviar el mensaje:", response.read().decode())
except Exception as e:
    print("❌ Error:", e)
finally:
    if conn:
        conn.close()
