# CryptoBuddy — Your First AI-Powered Financial Sidekick

## Overview
CryptoBuddy is a beginner-friendly, rule-based chatbot that gives simple investment advice using a small predefined crypto dataset. It ranks coins by profitability (price trend & market cap) and sustainability (energy use & sustainability score).

## Features
- Rule-based decision logic (no external APIs required)
- Interactive chat loop
- Demo mode for quick testing
- Clear risk disclaimer for ethical guidance

## How to run
1. `python cryptobuddy.py` — interactive mode
2. `python cryptobuddy.py demo` — sample outputs

## Files submited
- `cryptobuddy.py`
- `README.md` 
- `screenshots/` folder with conversation screenshots
- Short screen recording (30s) of an interaction on the PLP LMS community.

## Extensions 
- Added NLTK to parse more natural queries
- Replace hard rules with a weighted ML model (after collecting historical data)

## Sample conversations while running the application 
You: Which crypto should I buy for long-term growth?
CryptoBuddy: For potential long-term growth, my top pick is Cardano (ADA). Why: price trend = rising, market cap = medium. Note: This is rule-based — score 6.50. Disclaimer: This bot uses simple rules; crypto is risky—DYOR.

You: What’s the most sustainable coin?
CryptoBuddy: The most sustainable coin in my list is Algorand (ALGO). 🌱 Sustainability score (rule-based) = 11.00. Disclaimer: educational only.

## Disclaimer
This bot is educational. Not financial advice. Crypto investments are risky. Always do your own research (DYOR).
