from predict_match import predict_match

def get_top_bets():

    # 🔥 données fake (pas d’API)
    matches = [
        {"home": "Liverpool", "away": "Arsenal", "odds": (2.0, 3.2, 3.5)},
        {"home": "Barcelona", "away": "Real Madrid", "odds": (2.1, 3.3, 3.2)},
    ]

    bets = []

    for m in matches:

        odd_home, odd_draw, odd_away = m["odds"]

        result = predict_match(
            m["home"],
            m["away"],
            odd_home,
            odd_draw,
            odd_away
        )

        if result is None:
            continue

        match = f"{m['home']} vs {m['away']}"

        bets.append({
            "match": match,
            "bet": "TEST",
            "value": result["prob_home"],
            "edge": result["edge_home"],
            "odds": odd_home
        })

    return bets