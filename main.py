import os

from fastapi import FastAPI, HTTPException

app = FastAPI()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "")

latest_signal = None


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "TradingView webhook service is running"
    }


@app.post("/webhook/tradingview")
def receive_alert(data: dict):
    global latest_signal

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

   latest_signal = {
    "signal_id": str(uuid.uuid4()),
    "symbol": data.get("symbol"),
    "timeframe": data.get("timeframe"),
    "price": data.get("price"),
    "action": data.get("action"),
    "timestamp": data.get("timestamp"),
    "status": "PENDING"
}
    }

    return {
        "success": True,
        "message": "Alert received",
        "signal": latest_signal
    }


@app.get("/api/signals/latest")
def get_latest_signal():
    if latest_signal is None:
        return {
            "success": False,
            "message": "No signal received yet"
        }

    return {
        "success": True,
        "signal": latest_signal
    }
@app.post("/api/signals/confirm")
def confirm_signal(data: dict):
    global latest_signal

    if latest_signal is None:
        raise HTTPException(
            status_code=404,
            detail="No signal available"
        )

    received_signal_id = data.get("signal_id")

    if received_signal_id != latest_signal.get("signal_id"):
        raise HTTPException(
            status_code=400,
            detail="Signal ID does not match"
        )

    latest_signal["status"] = "EXECUTED"
    latest_signal["ticket"] = data.get("ticket")

    return {
        "success": True,
        "message": "Signal confirmed",
        "signal": latest_signal
    }
