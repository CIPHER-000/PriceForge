from apscheduler.schedulers.background import BackgroundScheduler
from app.liquidity import get_liquidity

scheduler = BackgroundScheduler()

def update_liquidity():
    """Fetch & store liquidity for multiple tokens."""
    tokens = ["0xToken1", "0xToken2"]  # Add more tokens
    for token in tokens:
        get_liquidity(token)  # This will auto-save to MongoDB

scheduler.add_job(update_liquidity, "interval", minutes=5)
scheduler.start()
