from predict_match import predict_match

def get_top_bets(live_data):

    bets = []

    for m in live_data[:15]:  # 🔥 MAX 15 MATCHS

        try:
            pred = predict_match(
                m["home"],
                m["away"],
                2.0,
                3.2,
                3.5,
                ...
            )

            if odds is None:
                continue

            pred = predict_match(
                m["home"],
                m["away"],
                odds["home"],
                odds["draw"],
                odds["away"],
                {"attack":1.2,"defense":1.2},
                {"attack":1.2,"defense":1.2},
                {"attack":1.2,"defense":1.2},
                {"attack":1.2,"defense":1.2},
                5,5,50,50,1.2,1.2
            )

            if pred and pred["prediction"] != "NO BET" and pred["confidence"] > 0.15:

                bets.append({
                    "match": f"{m['home']} vs {m['away']}",
                    "bet": pred["prediction"],
                    "confidence": pred["confidence"],
                    "value": pred["best_value"]
                })

        except Exception as e:
            print("TOP BET ERROR:", e)
            continue

    bets = sorted(bets, key=lambda x: x["value"], reverse=True)

    return bets[:5]