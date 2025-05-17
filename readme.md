
# 📈 Fundamentor

This project attempt to analyse the long term future trend of a stock based on 3 data points. It integrates:

- **Shareholder Data** (gathered by scraping the BSE India website)
- **Financial Trends** (via Yahoo Finance)
- **Recent News Articles** (via SerpAPI and newspaper3k)

The data from these sources is then analyzed using OpenAI’s GPT-4o Mini model, providing predictions with clear reasoning.

---


## 🛠️ Technologies Used

- **Python 3.11**
- **Asyncio** for concurrent data gathering
- **OpenAI GPT-4o Mini** for market analysis and predictions
- **yfinance** for financial trend extraction
- **SerpAPI** and **newspaper3k** for news aggregation
- **BeautifulSoup/Selenium** (for scraping shareholder data from the BSE website)

---

## 🗃️ Project Structure

```

.
├── config
│   └── common_configs.py
├── requirements.txt
├── README.md
└── src
    ├── main.py
    ├── ShareholderAnalyser.py
    ├── FinancialAnalyser.py
    ├── NewsAnalyser.py
    ├── data
    │   └── top_investors.csv
    ├── prompt
    │   └── system_prompt.txt
    └── utils
        └── datetime_utils.py


````

---

## 📖 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/hopeless-programmer/fundamentor.git
cd fundamentor
````

### 2. Create and Activate a Virtual Environment (Recommended)

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
.\env\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. API Keys Configuration

You don’t need a separate config file. Just **edit `main.py`** directly at the bottom:

```python
if __name__ == "__main__":
    asyncio.run(main(
        serp_api_key="YOUR_SERP_API_KEY",
        openai_api_key="YOUR_OPENAI_API_KEY"
    ))
```

Replace the placeholder strings with your actual keys.

* Get your **SerpAPI key** from [serpapi.com](https://serpapi.com/)
* Get your **OpenAI API key** from [platform.openai.com](https://platform.openai.com/)

---

## 🏃 Running the Prediction

```bash
python src/main.py
```

You’ll be prompted:

```
Enter stock symbol (e.g. TATAMOTORS): TITAN
```

The result is a structured JSON, like:

```json
{
  "prediction": "UP",
  "confidence": 80,
  "key_factors": [
    "Major investors hold significant allocations in TITAN, indicating strong confidence in the stock",
    "Total Revenue and Net Income have shown consistent growth over the last four years",
    "Recent news highlights strategic acquisitions that may enhance future growth prospects"
  ],
  "caveats": "Quarterly Gross Profit has shown a decline, which may impact short-term performance"
}
```

---

## 🎯 How the Prediction Works

### **1. Shareholder Analysis**

The program analyzes holdings of key investors scraped directly from BSE India. Significant portfolio changes indicate investor confidence or lack thereof.

### **2. Financial Trend Analysis**

Using Yahoo Finance, it analyzes key metrics like revenue growth, gross profit margins, net income, and EPS trends, providing structured trends.

### **3. News Sentiment Analysis**

The recent company news is retrieved via SerpAPI and summarized, capturing events that impact short-term investor sentiment.

### **4. GPT-4o Mini Integration**

The GPT-4o Mini model synthesizes these inputs to deliver an informed, quantitative prediction.

---

## ⚠️ Disclaimer

This project is for educational purposes and experimentation only. **Do not** use the predictions from this tool as financial advice. Always perform your own due diligence.

---

## 🤝 Contributing

Pull requests and improvements are welcome! Please open an issue to discuss your ideas before submitting.

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

