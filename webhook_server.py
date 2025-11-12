import os
import hmac

from flask import Flask, request, jsonify
import logging
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# armazenamento simples em memória para evitar duplicados
received_ids = set()

import os
import hmac
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Pega o segredo do ambiente
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", None)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Pega o segredo configurado no Render
    WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", None)
    
    # Pega o token do header da requisição
    received_token = request.headers.get("X-Webhook-Token", "")
    
    # Validação segura do token
    if not WEBHOOK_SECRET or not hmac.compare_digest(received_token, WEBHOOK_SECRET):
        return jsonify({"ok": False, "error": "invalid token"}), 401

    # Continua o fluxo normal se o token for válido
    data = request.json
    received_id = data.get("id", "unknown")
    print(f"ok receivedId {received_id}")
    return jsonify({"ok": True, "receivedId": received_id})
if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0", debug=True)
