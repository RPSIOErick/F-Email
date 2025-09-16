import pyshark
import os
import json
import re
from datetime import datetime

# Pasta onde os arquivos serão salvos
output_dir = "capturas"
os.makedirs(output_dir, exist_ok=True)

# Arquivo único de log
log_file = os.path.join(output_dir, "emails.txt")

# Lista interfaces
print("🔎 Interfaces disponíveis:")
interfaces = pyshark.LiveCapture().interfaces
for i, iface in enumerate(interfaces):
    print(f"{i}: {iface}")

choice = int(input("Selecione a interface (número): "))
interface_name = interfaces[choice]

print(f"\n✅ Capturando pacotes na interface: {interface_name} (porta 5000)\n")

# Filtra apenas TCP porta 5000
capture = pyshark.LiveCapture(interface=interface_name, bpf_filter="tcp port 5000")

# Função para verificar se o payload é um email válido
def is_valid_email_json(payload):
    return all(x in payload for x in ['"from"', '"to"', '"message"'])

for packet in capture.sniff_continuously():
    try:
        ip_layer = packet.ip
        tcp_layer = packet.tcp

        # Pega o payload TCP se existir
        payload = ""
        if hasattr(packet.tcp, 'payload'):
            payload = bytes.fromhex(packet.tcp.payload.replace(":", "")).decode(errors="ignore")

        # Filtra apenas payloads válidos
        if payload and is_valid_email_json(payload):
            # Extrai JSON do payload
            match = re.search(r'\{.*\}', payload, re.DOTALL)
            email_content = match.group(0) if match else None
            if not email_content:
                continue

            # Converte para dict e formata
            email_dict = json.loads(email_content)
            remetente = email_dict.get("from", "<remetente não informado>")
            destinatario = email_dict.get("to", "<destinatário não informado>")
            mensagem = email_dict.get("message", "<mensagem vazia>")

            # IP e porta de origem/destino
            src_ip = ip_layer.src
            src_port = tcp_layer.srcport
            dst_ip = ip_layer.dst
            dst_port = tcp_layer.dstport

            # Cria texto final
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            output_text = (
                f"📦 EMAIL CAPTURADO [{timestamp}]\n"
                f"Origem: {src_ip}:{src_port}\n"
                f"Destino: {dst_ip}:{dst_port}\n"
                f"De: {remetente}\n"
                f"Para: {destinatario}\n"
                f"Conteúdo:\n{mensagem}\n"
                + "-"*50 + "\n"
            )

            # Salva em arquivo único (append)
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(output_text)

            # Mostra no terminal
            print(output_text)

    except (AttributeError, json.JSONDecodeError):
        continue