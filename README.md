# 📈 TSLA Stock Price & News Email Alert

A Python script that checks TSLA's daily closing price. If the price moves
by more than 5% compared to the previous day, it fetches the top 3 related
news articles and emails each one to you separately.

## ✨ What it does

1. Gets yesterday's and the day-before-yesterday's TSLA closing price from the [Alpha Vantage](https://www.alphavantage.co/) API
2. Works out the percentage change between the two
3. If the change is greater than 5%, fetches the top 3 news articles about Tesla from [NewsAPI](https://newsapi.org/)
4. Sends each article as a separate email via Gmail's SMTP server

## 🛠️ Requirements

- Python 3.8+
- A free [Alpha Vantage API key](https://www.alphavantage.co/support/#api-key)
- A free [NewsAPI key](https://newsapi.org/register)
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) (2-Step Verification must be turned on)

## 🚀 Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies**
   ```bash
   pip install requests requests_cache
   ```

3. **Add your own details**

   Open `main.py` and replace the placeholder values near the top of the file:

   | Placeholder | Replace with |
   |---|---|
   | `YOUR_ALPHA_VANTAGE_API_KEY` | Your Alpha Vantage API key |
   | `YOUR_NEWS_API_KEY` | Your NewsAPI key |
   | `your_email@gmail.com` | The Gmail address that will send the alert |
   | `YOUR_GMAIL_APP_PASSWORD` | A 16-character Gmail App Password (not your normal password) |
   | `recipient_email@gmail.com` | Where the alert emails should be sent |

   > ⚠️ Since your keys and password will be typed directly into the code, **do not push this file to a public repo with your real values still in it.** Fill them in locally after cloning, or keep your repo private.

4. **Run it**
   ```bash
   python main.py
   ```

   If TSLA's price move is under 5%, the script just prints a message and
   exits — no email is sent. That's expected, not a bug.

## 📧 Getting a Gmail App Password

1. Turn on 2-Step Verification on your Google account
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Generate a new app password and paste it into `MY_PASSWORD` in `main.py`

## ⚠️ Notes

- Alpha Vantage's free tier has a daily request limit — the script caches responses for 1 hour to help avoid hitting it.
- NewsAPI's free tier only returns articles from the last month.
- Check your Spam folder if the alert email doesn't show up in your inbox right away.
