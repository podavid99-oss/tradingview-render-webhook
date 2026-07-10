from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "online",
        "message": "TradingView webhook service is running"
    }


@app.post("/webhook/tradingview")
def receive_alert(data: dict):
    return {
        "success": True,
        "received": data
    }
