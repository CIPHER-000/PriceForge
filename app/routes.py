from flask import Blueprint, jsonify, request
from app.liquidity import get_liquidity, get_uniswap_v3_pool  # Import the correct function
from app.config import liquidity_collection

routes = Blueprint("routes", __name__)

@routes.route("/get_pool/<tokenA>/<tokenB>", methods=["GET"])
def get_pool(tokenA, tokenB):
    """Retrieve Uniswap V3 pool address for a token pair."""
    pool_address = get_uniswap_v3_pool(tokenA, tokenB)  # Correct function call
    return jsonify({"pool_address": pool_address})

@routes.route("/liquidity/<pool_address>", methods=["GET"])
def liquidity(pool_address):
    """Fetch real-time liquidity from Uniswap V3."""
    data = get_liquidity(pool_address)  # Now using pool_address, not tokenA/tokenB
    return jsonify(data)

@routes.route("/historical_liquidity", methods=["GET"])
def get_historical_liquidity():
    """Fetch historical liquidity data from MongoDB."""
    pool_address = request.args.get("pool")
    if not pool_address:
        return jsonify({"error": "Pool address is required"}), 400

    data = list(liquidity_collection.find(
        {"pool_address": pool_address},
        {"_id": 0}  # Exclude MongoDB ID
    ).sort("timestamp", -1))

    return jsonify(data)
