from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# armazenamento simples em memória para evitar duplicados
received_ids = set()

@app.route("/webhook", methods=["POST"])
def webhook():
    lead = request.get_json(silent=True)
    now = datetime.now().isoformat()
    app.logger.info(f"[{now}] Recebido raw: {lead}")

    if not lead:
        app.logger.warning("Payload vazio ou inválido JSON")
        return jsonify({"ok": False, "error": "payload inválido"}), 400

    lead_id = lead.get("id")
    nome = lead.get("nome")

    if not lead_id or not nome:
        app.logger.warning("Campos mínimos faltando (id ou nome)")
        return jsonify({"ok": False, "error": "id ou nome faltando"}), 400

    if lead_id in received_ids:
        app.logger.info(f"Lead {lead_id} já recebido — ignorando duplicata")
        return jsonify({"ok": True, "status": "duplicate", "receivedId": lead_id}), 200

    received_ids.add(lead_id)
    app.logger.info(f"Processando lead {lead_id} - {nome}")

    return jsonify({"ok": True, "receivedId": lead_id}), 200

if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0", debug=True)
