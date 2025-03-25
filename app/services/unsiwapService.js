const { ethers } = require("ethers");
const provider = require("./utils/web3Provider");

// Uniswap V3 Pool ABI (Minimal required methods)
const POOL_ABI = [
    "function liquidity() view returns (uint128)",
    "function slot0() view returns (uint160, int24, uint16, uint16, uint16, uint8, bool)",
    "function fee() view returns (uint24)"
];

/**
 * Fetch Uniswap V3 Pool Data
 * @param {string} poolAddress - Uniswap V3 Pool contract address
 * @returns {Promise<Object>}
 */
async function getUniswapPoolData(poolAddress) {
    try {
        const poolContract = new ethers.Contract(poolAddress, POOL_ABI, provider);

        const liquidity = await poolContract.liquidity();
        const slot0 = await poolContract.slot0();
        const feeTier = await poolContract.fee();

        return {
            liquidity: liquidity.toString(),
            sqrtPriceX96: slot0[0].toString(),
            tick: slot0[1],
            feeTier: feeTier / 10000 + "%" // Convert fee to percentage
        };
    } catch (error) {
        console.error("Error fetching Uniswap pool data:", error);
        throw new Error("Failed to retrieve Uniswap pool data.");
    }
}

module.exports = { getUniswapPoolData };
