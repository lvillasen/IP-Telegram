import requests
import re
import netifaces

BOT_TOKEN = "XXXXXXXX_XXXXXXXXXX_XXXXXXXXXX"
CHAT_ID = "XXXXXXXXXX"

def get_local_ips():
    ips = {}
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                ip = addr.get('addr')
                if ip != "127.0.0.1":
                    ips[iface] = ip
    if not ips:
        return {"No disponible": "No disponible"}
    return ips

def get_public_ip():
    try:
        r = requests.get("https://api.ipify.org?format=text", timeout=5)
        ip = r.text.strip()
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
            return ip
        else:
            return "No se pudo obtener la IP pública"
    except:
        return "No se pudo obtener la IP pública"

def escape_markdown(text):
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)

local_ips = get_local_ips()
ip_publica = escape_markdown(get_public_ip())

mensaje = "📡 *IP de la PC Home*\n\n"
mensaje += f"🌍 *Pública:* {ip_publica}\n"
mensaje += "💻 *Locales:*\n"
for iface, ip in local_ips.items():
    # Cambié el bullet '-' por '•' para evitar conflicto en MarkdownV2
    mensaje += f"  • *{escape_markdown(iface)}:* {escape_markdown(ip)}\n"

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
