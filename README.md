# 📊 Solana Memecoin Helper

A comprehensive Python-based tool for analyzing and monitoring Solana memecoins to detect potential rug pulls and whale activity.

## ✨ Features

### 🔍 **Holder Analysis**
- Scan top token holders via BirdEye API
- Identify "whale wallets" with configurable SOL thresholds (default: 100 SOL)
- Display ownership percentages and wallet balances
- Rich wallet detection for dump risk assessment

### 💧 **Liquidity Monitoring**
- Real-time liquidity tracking via BirdEye API
- Alert when liquidity drops by configurable percentage (default: 10%)
- Continuous polling with customizable intervals
- Peak liquidity tracking

### 📦 **Bundle Tracking**
- Monitor Jito MEV bundles
- Check transaction bundle status via Jito Block Engine
- MEV activity analysis

### 🤖 **Telegram Integration**
- Automated bot responding to commands
- Real-time alerts and notifications
- Command: `scan [token_address]` for quick analysis

## 🏗️ Architecture

```
├── backend/
│   ├── app.py              # Flask API server + Telegram bot
│   ├── holder_scanner.py   # Token holder analysis
│   ├── liquidity_alert.py  # Liquidity monitoring
│   ├── bundle_checker.py   # Jito bundle tracking
│   └── notify.py          # Telegram notifications
├── frontend/
│   └── dashboard.html     # Web dashboard interface
└── .env                   # Configuration (not included)
```

## 🚀 Setup

### Prerequisites
- Python 3.7+
- API Keys for:
  - BirdEye API
  - Helius API
  - Telegram Bot Token

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/solana-memecoin-helper.git
   cd solana-memecoin-helper
   ```

2. **Install dependencies**
   ```bash
   pip install flask flask-cors python-dotenv requests
   ```

3. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   HELIUS_API_KEY=your_helius_api_key
   BIRDEYE_API_KEY=your_birdeye_api_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   JITO_BLOCK_ENGINE_URL=https://mainnet.block-engine.jito.wtf
   ```

4. **Run the application**
   ```bash
   cd backend
   python app.py
   ```

5. **Access the dashboard**
   Open `frontend/dashboard.html` in your browser

## 📖 API Usage

### Scan Token Holders
```bash
POST http://localhost:5000/scan
Content-Type: application/json

{
  "token": "token_address_here",
  "limit": 10,
  "sol_threshold": 100
}
```

### Check Bundle Status
```bash
GET http://localhost:5000/bundle/{bundle_id}
```

### Start Liquidity Monitor
```bash
POST http://localhost:5000/monitor
Content-Type: application/json

{
  "token": "token_address_here",
  "threshold_pct": 10.0
}
```

## 🤖 Telegram Commands

- `scan [token_address]` - Analyze token holders
- Bot automatically sends alerts for liquidity drops

## ⚠️ Use Cases

### Memecoin Risk Assessment
- **Whale Detection**: Identify large holders who could dump
- **Rug Pull Alerts**: Monitor for sudden liquidity removal
- **Distribution Analysis**: Check token concentration

### Trading Signals
- Real-time liquidity monitoring for exit signals
- Holder analysis for entry timing
- MEV activity tracking

## 🔧 Configuration

### Environment Variables
- `HELIUS_API_KEY`: For wallet balance checks
- `BIRDEYE_API_KEY`: For token data and holder information
- `TELEGRAM_BOT_TOKEN`: For bot notifications
- `JITO_BLOCK_ENGINE_URL`: For bundle tracking

### Customizable Parameters
- SOL threshold for "rich wallet" detection
- Liquidity drop alert percentage
- Monitoring intervals
- Number of top holders to analyze

## 🛡️ Security Notes

- Keep your `.env` file secure and never commit it
- Use read-only API keys where possible
- Monitor your API usage and rate limits

## 📊 APIs Used

- **BirdEye API**: Token data, holders, liquidity information
- **Helius API**: Solana wallet balances and transaction data
- **Jito Block Engine**: MEV bundle status and information
- **Telegram Bot API**: Real-time notifications and commands

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## ⚖️ Disclaimer

This tool is for educational and research purposes. Always do your own research before making any trading decisions. Cryptocurrency trading involves significant risk.

## 📄 License

MIT License - see LICENSE file for details

---

**Built for the Solana memecoin community** 🚀
