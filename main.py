import smtplib

import requests
import requests_cache

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# 🔑 Replace with your own Alpha Vantage API key
# Get a free one here: https://www.alphavantage.co/support/#api-key
stocks_api_key = "YOUR_ALPHA_VANTAGE_API_KEY"

# 🔑 Replace with your own NewsAPI key
# Get a free one here: https://newsapi.org/register
news_api_key = "YOUR_NEWS_API_KEY"

# ✉️ Replace with your own Gmail address
MY_EMAIL = "your_email@gmail.com"

# 🔑 Replace with your own Gmail App Password (NOT your normal password)
# Generate one here: https://myaccount.google.com/apppasswords
MY_PASSWORD = "YOUR_GMAIL_APP_PASSWORD"

# ✉️ Replace with the email address you want to receive alerts on
TO_EMAIL = "recipient_email@gmail.com"

stocks_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stocks_api_key,
}

## STEP 1: Get yesterday's and the day-before-yesterday's closing stock price
# Cache responses for 1 hour so we don't burn through the free API request limit
session = requests_cache.CachedSession('stock_cache', expire_after=3600)
response = session.get(STOCK_ENDPOINT, params=stocks_params)
response.raise_for_status()
data = response.json()

time_series = data["Time Series (Daily)"]
dates = list(time_series.keys())
yesterday = dates[0]
day_before_yesterday = dates[1]

# Get yesterday's closing price
yesterday_closing = [float(value["4. close"]) for (date, value) in time_series.items() if date == yesterday][0]

# Get the day before yesterday's closing price
day_before_yesterday_closing = [float(value["4. close"]) for (date, value) in time_series.items() if date == day_before_yesterday][0]

# Find the positive (absolute) difference between the two prices
absolute_difference = abs(yesterday_closing - day_before_yesterday_closing)

# Work out the percentage difference between the two closing prices
percentage_difference = (absolute_difference / day_before_yesterday_closing) * 100

# Pick an emoji to show whether the price went up or down
up_down = "🔺" if yesterday_closing > day_before_yesterday_closing else "🔻"

news_params = {
    "q": COMPANY_NAME,
    "from": yesterday,
    "sortBy": "popularity",
    "apiKey": news_api_key,
}

# Only fetch news and send emails if the price moved by more than 5%
if percentage_difference > 5:

    ## STEP 2: Get the top 3 news articles about the company
    response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    response.raise_for_status()
    articles = response.json()["articles"]

    # Slice the list to keep only the first 3 articles
    three_articles = articles[:3]

    # Build one formatted message per article (title + description)
    # The "Subject:" line at the top is required for Gmail's SMTP server
    # to recognize it as the email subject
    formatted_articles = [
        f"Subject: {STOCK_NAME} Alert!\n\n"
        f"{STOCK_NAME}: {up_down}{percentage_difference:.1f}%\n"
        f"Headline: {article['title']}\n"
        f"Brief: {article['description']}"
        for article in three_articles
    ]

    ## STEP 3: Send each article as a separate email
    # Note: SMTP (port 587) + starttls() is used here, not SMTP_SSL,
    # since starttls() is what upgrades this connection to a secure one
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)

        for message_body in formatted_articles:
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=TO_EMAIL,
                # encode() is needed because the message contains emoji
                msg=message_body.encode("utf-8"),
            )

    print(f"Sent {len(formatted_articles)} email(s) to {TO_EMAIL}.")
else:
    print(f"{STOCK_NAME} moved {percentage_difference:.2f}%, below the 5% alert threshold. No email sent.")
