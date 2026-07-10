import os

from fastapi import FastAPI, HTTPException

app = FastAPI()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "TradingView webhook service is running"
    }


@app.post("/webhook/tradingview")
def receive_alert(data: dict):
        print("TRADINGVIEW ALERT:", data, flush=True)
    received_secret = data.get("secret")

    if not WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500,
            detail="WEBHOOK_SECRET is not configured"
        )

    if received_secret != WEBHOOK_SECRET:
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook secret"
        )

    return {
        "success": True,
        "message": "Alert received",
        "received": data
    }
