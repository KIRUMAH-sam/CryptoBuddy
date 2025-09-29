# A simple rule-based cryptocurrency advisor chatbot.
import sys
import textwrap

# Predefined crypto dataset 
crypto_db = {
    "Bitcoin": {
        "symbol": "BTC",
        "price_trend": "rising",
        "market_cap": "high",
        "energy_use": "high",
        "sustainability_score": 3 / 10
    },
    "Ethereum": {
        "symbol": "ETH",
        "price_trend": "stable",
        "market_cap": "high",
        "energy_use": "medium",
        "sustainability_score": 6 / 10
    },
    "Cardano": {
        "symbol": "ADA",
        "price_trend": "rising",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 8 / 10
    },
    "Polkadot": {
        "symbol": "DOT",
        "price_trend": "falling",
        "market_cap": "medium",
        "energy_use": "low",
        "sustainability_score": 7 / 10
    },
    "Algorand": {
        "symbol": "ALGO",
        "price_trend": "stable",
        "market_cap": "low",
        "energy_use": "low",
        "sustainability_score": 9 / 10
    }
}

# Helper scoring / rule functions
def score_profitability(info):
    """Return a simple profitability score (higher = more attractive)."""
    score = 0
    trend = info.get("price_trend", "")
    cap = info.get("market_cap", "")
    if trend == "rising":
        score += 3
    elif trend == "stable":
        score += 1
    elif trend == "falling":
        score -= 2

    if cap == "high":
        score += 2
    elif cap == "medium":
        score += 1
    elif cap == "low":
        score -= 1

    # sustainability slightly affects profitability perception
    score += info.get("sustainability_score", 0) * 1.5
    return score

def score_sustainability(info):
    """Return a sustainability score (higher = greener)."""
    base = info.get("sustainability_score", 0) * 10  # convert to 0-10 scale
    energy = info.get("energy_use", "")
    if energy == "low":
        base += 2
    elif energy == "medium":
        base += 0
    elif energy == "high":
        base -= 2
    return base

# Natural language
def interpret_intent(user_query):
    q = user_query.lower()
    # intent categories: profitability, sustainability, compare, explain, list, help, quit
    if any(w in q for w in ["sustainab", "green", "eco", "energy", "low energy", "environment"]):
        return "sustainability"
    if any(w in q for w in ["trend", "trending", "rising", "buy for long", "long-term", "growth"]):
        return "profitability"
    if any(w in q for w in ["compare", "vs", "which is better", "best of"]):
        return "compare"
    if any(w in q for w in ["list", "show", "available", "what coins"]):
        return "list"
    if any(w in q for w in ["explain", "how", "why"]):
        return "explain"
    if any(w in q for w in ["quit", "exit", "bye"]):
        return "quit"
    # fallback: try to detect coin name
    for coin in crypto_db:
        if coin.lower() in q or crypto_db[coin]['symbol'].lower() in q:
            return ("coin_query", coin)
    return "unknown"

# Response generators 
def recommend_most_profitable():
    scored = {coin: score_profitability(info) for coin, info in crypto_db.items()}
    # sort desc
    best = sorted(scored.items(), key=lambda x: x[1], reverse=True)
    top_name, top_score = best[0]
    return top_name, top_score, best

def recommend_most_sustainable():
    scored = {coin: score_sustainability(info) for coin, info in crypto_db.items()}
    best = sorted(scored.items(), key=lambda x: x[1], reverse=True)
    top_name, top_score = best[0]
    return top_name, top_score, best

def explain_coin(coin_name):
    info = crypto_db.get(coin_name)
    if not info:
        return f"I don't have data for {coin_name}."
    expl = textwrap.dedent(f"""
        {coin_name} ({info.get('symbol','')}):
          - Price trend: {info.get('price_trend')}
          - Market cap: {info.get('market_cap')}
          - Energy use: {info.get('energy_use')}
          - Sustainability score: {info.get('sustainability_score'):.1f}/1.0
        Rule-based conclusion: Profitability score = {score_profitability(info):.2f}, Sustainability = {score_sustainability(info):.2f}
    """)
    return expl.strip()

# Chatbot UI
BOT_NAME = "CryptoBuddy"
BOT_TONE = "friendly-professional"

WELCOME = f"""
Hey! I'm {BOT_NAME} — your friendly crypto sidekick.  
I can give simple, rule-based suggestions about profitability and sustainability for a small crypto dataset.
Type questions like:
  - "Which crypto is trending up?"
  - "What's the most sustainable coin?"
  - "Explain Cardano"
  - "List coins"
Type 'quit' to exit.
"""

DISCLAIMER = ("Disclaimer: This bot uses simple, hard-coded rules and a tiny sample dataset. "
              "This is educational only — crypto is risky. Always do your own research (DYOR)😉.")

def chat_loop():
    print(WELCOME)
    print("Type a question (or 'help'):")
    while True:
        try:
            user = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            return

        if not user:
            print("CryptoBuddy: Say something — e.g., 'Which is most sustainable?'")
            continue

        intent = interpret_intent(user)

        if intent == "quit":
            print("CryptoBuddy: Bye — trade safely! ")
            break

        if intent == "list":
            names = ", ".join(f"{name} ({info['symbol']})" for name, info in crypto_db.items())
            print(f"CryptoBuddy: Available coins in my tiny dataset: {names}")
            continue

        if intent == "unknown":
            print("CryptoBuddy: I didn't catch that. Try questions about 'sustainability', 'trending', 'compare', or ask 'Explain <coin>'.")
            continue

        if isinstance(intent, tuple) and intent[0] == "coin_query":
            coin = intent[1]
            print("CryptoBuddy:", explain_coin(coin))
            continue

        if intent == "profitability":
            top_name, top_score, ranking = recommend_most_profitable()
            print(f"CryptoBuddy: For potential long-term growth, my top pick is {top_name} ({crypto_db[top_name]['symbol']}).")
            print(f"  Why: price trend = {crypto_db[top_name]['price_trend']}, market cap = {crypto_db[top_name]['market_cap']}.")
            print(f"  Note: This is rule-based — score {top_score:.2f}. {DISCLAIMER}")
            continue

        if intent == "sustainability":
            top_name, top_score, ranking = recommend_most_sustainable()
            print(f"CryptoBuddy: The most sustainable coin in my list is {top_name} ({crypto_db[top_name]['symbol']}).")
            print(f"  Sustainability score (rule-based) = {top_score:.2f}. {DISCLAIMER}")
            continue

        if intent == "compare":
            # naive compare: pick top two by profit and top two by sustainability then show
            p_top, _, p_rank = recommend_most_profitable()
            s_top, _, s_rank = recommend_most_sustainable()
            print(f"CryptoBuddy: Profit-focused pick: {p_top} ({crypto_db[p_top]['symbol']}).")
            print(f"CryptoBuddy: Sustainability-focused pick: {s_top} ({crypto_db[s_top]['symbol']}).")
            print("CryptoBuddy: If you want both, look for coins that appear in both lists or ask for an explain of a specific coin.")
            continue

        if intent == "explain":
            # try extract coin name
            found = None
            for coin in crypto_db:
                if coin.lower() in user.lower():
                    found = coin
                    break
            if found:
                print("CryptoBuddy:", explain_coin(found))
            else:
                print("CryptoBuddy: Ask 'Explain <coin>' or name a coin from the list.")
            continue

        # fallback
        print("CryptoBuddy: I can help with 'sustainability', 'profitability', 'list', 'explain <coin>', or 'compare'.")

# Small automated test (prints sample interactions)
def run_demo():
    print("=== Demo: sample outputs ===\n")
    print("Q: Which crypto is trending up?")
    print("A:", end=" ")
    top_name, top_score, _ = recommend_most_profitable()
    print(f"For growth: {top_name} ({crypto_db[top_name]['symbol']}) — score {top_score:.2f}")
    print()
    print("Q: Most sustainable coin?")
    print("A:", end=" ")
    s_name, s_score, _ = recommend_most_sustainable()
    print(f"{s_name} ({crypto_db[s_name]['symbol']}) — sustainability {s_score:.2f}")
    print()
    print("Q: Explain Cardano")
    print("A:\n", explain_coin("Cardano"))
    print("\n=== End demo ===\n")

# Entry point
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        run_demo()
    else:
        chat_loop()
