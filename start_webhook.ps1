# start_webhook.ps1
# Abre 3 janelas: Flask (servidor), Ngrok (túnel) e uma janela Teste pronta.
# Ajuste caminhos se necessário.

 = "C:\Users\Aspire 5\webhook-poc"
 = "python"
 = Join-Path  ".\venv\Scripts\Activate.ps1"

# 1) Abre janela Flask
Start-Process -FilePath "powershell" -ArgumentList "-NoExit","-Command","cd ''; if (Test-Path '') { & '' };  webhook_server.py" -WindowStyle Normal

# 2) Dá um pequeno pause pra garantir que o Flask suba primeiro (opcional)
Start-Sleep -Seconds 1

# 3) Abre janela Ngrok (assume ngrok no PATH). Se ngrok não estiver no PATH, coloque o caminho completo para ngrok.exe
Start-Process -FilePath "powershell" -ArgumentList "-NoExit","-Command","cd ''; ngrok http 3000" -WindowStyle Normal

# 4) Abre janela Teste pronta (só posiciona na pasta)
Start-Process -FilePath "powershell" -ArgumentList "-NoExit","-Command","cd ''" -WindowStyle Normal

Write-Output "Start script lançado. Verifique as janelas 'Flask - webhook-poc', 'Ngrok - webhook-poc' e 'Teste - webhook-poc'."
