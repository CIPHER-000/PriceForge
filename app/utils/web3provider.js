const { ethers } = require("ethers");
const { INFURA_API_KEY } = require("../config/dotenv");

// Initialize provider
const provider = new ethers.JsonRpcProvider(`https://mainnet.infura.io/v3/${INFURA_API_KEY}`);

module.exports = provider;
