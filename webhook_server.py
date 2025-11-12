# ======== WEBHOOK SERVER COMPLETO ========
import os
import hmac
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Variável de ambiente do token (pode vir do Render)
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "ionara_2025_supersegredo_9f4X")

@app.route("/")
def home():
    return jsonify({"status": "online", "time": datetime.now().isoformat()})

@app.route("/webhook", methods=["POST"])
def webhook():
    # Captura o token que veio no header
    received_token = request.headers.get("X-Webhook-Token", "")

    # Validação segura com hmac
    if not hmac.compare_digest(received_token, WEBHOOK_SECRET):
        print("❌ Token inválido recebido:", received_token)
        return jsonify({"ok": False, "error": "invalid token"}), 401

    # Se o token for válido, processa os dados
    try:
        data = request.get_json(force=True)
        received_id = data.get("id", "unknown")
        print(f"✅ Token válido — recebido ID: {received_id}")
        return jsonify({"ok": True, "receivedId": received_id}), 200
    except Exception as e:
        print("⚠️ Erro ao processar o corpo:", e)
        return jsonify({"ok": False, "error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
# ========================================
