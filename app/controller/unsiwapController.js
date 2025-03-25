const { getUniswapPoolData } = require("./services/uniswapService");

/**
 * Controller to handle pool data request
 */
const fetchPoolData = async (req, res) => {
    try {
        const { poolAddress } = req.params;
        if (!poolAddress) {
            return res.status(400).json({ error: "Missing poolAddress parameter." });
        }

        const data = await getUniswapPoolData(poolAddress);
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};

module.exports = { fetchPoolData };
