from web3 import Web3
from flask import jsonify
from datetime import datetime
from app.config import liquidity_collection  # MongoDB connection
from app.config import UNISWAP_FACTORY_ABI

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/4feef31d856a4f6c84f1927bff40879d"))

# Uniswap V3 Factory Contract
UNISWAP_FACTORY = "0x1F98431c8aD98523631AE4a59f267346ea31F984"
factory_contract = w3.eth.contract(address=UNISWAP_FACTORY, abi=UNISWAP_FACTORY_ABI)

# Uniswap V3 Pool ABI
UNISWAP_POOL_ABI = [
    {
        "name": "slot0",
        "outputs": [
            {"type": "uint160", "name": "sqrtPriceX96"},
            {"type": "int24", "name": "tick"},
            {"type": "uint16", "name": "observationIndex"},
            {"type": "uint16", "name": "observationCardinality"},
            {"type": "uint16", "name": "observationCardinalityNext"},
            {"type": "uint8", "name": "feeProtocol"},
            {"type": "bool", "name": "unlocked"}
        ],
        "inputs": [],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "name": "liquidity",
        "outputs": [{"type": "uint128", "name": "liquidity"}],
        "inputs": [],
        "stateMutability": "view",
        "type": "function"
    }
]

def get_liquidity(pool_address):
    """Fetch real-time liquidity from Uniswap V3 pool."""
    pool_contract = w3.eth.contract(address=pool_address, abi=UNISWAP_POOL_ABI)

    try:
        liquidity = pool_contract.functions.liquidity().call()
        slot0 = pool_contract.functions.slot0().call()  # Fetch price and tick

        data = {
            "pool_address": pool_address,
            "liquidity": str(liquidity),  # Convert to string to avoid BigInt issues
            "sqrtPriceX96": str(slot0[0]),  # First value from slot0 (price)
            "tick": slot0[1],  # Second value (tick)
            "timestamp": datetime.utcnow()
        }

        # Save to MongoDB
        liquidity_collection.insert_one(data)

        return data

    except Exception as e:
        return {"error": str(e)}


def get_uniswap_v3_pool(tokenA, tokenB, fee=3000):
    """Fetch the Uniswap V3 pool address for a given token pair and fee tier."""
    try:
        pool_address = factory_contract.functions.getPool(
            Web3.to_checksum_address(tokenA),
            Web3.to_checksum_address(tokenB),
            fee
        ).call()
        
        if pool_address == "0x0000000000000000000000000000000000000000":
            return {"error": "Pool not found for the given token pair"}

        return pool_address

    except Exception as e:
        return {"error": str(e)}

