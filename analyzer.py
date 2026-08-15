def score_network(ping_ms, jitter_ms, download_mbps, upload_mbps):

    # Normalize each metric to a 0-100 sub-score
    download_score = min(download_mbps / 50 * 100, 100)       # 50 Mbps -> 100
    upload_score = min(upload_mbps / 20 * 100, 100)           # 20 Mbps -> 100
    ping_score = max(0, 100 - ping_ms)                        # 0 ms -> 100, 100ms+ -> 0
    jitter_score = max(0, 100 - jitter_ms * 4)                # 0 ms -> 100, 25ms+ -> 0

    total = (
        download_score * 0.40
        + upload_score * 0.20
        + ping_score * 0.25
        + jitter_score * 0.15
    )
    return round(total, 1)


def classify(score):
    """Map a numeric score to a quality band."""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 35:
        return "Fair"
    else:
        return "Poor"


def analyze(ping_ms, jitter_ms, download_mbps, upload_mbps):
    """
    Master function: runs scoring + classification + recommendations
    and returns one consolidated result dictionary.
    """

    if ping_ms is None or download_mbps is None:
        return {
            "score": 0,
            "quality": "Unknown",
            "tips": ["Could not measure the network. Check your internet connection."],
        }

    score = score_network(ping_ms, jitter_ms, download_mbps, upload_mbps)
    quality = classify(score)
    tips = recommend(quality, ping_ms, download_mbps)

    return {"score": score, "quality": quality, "tips": tips}


def recommend(quality, ping_ms, download_mbps):
    """Return a list of practical, use-case based suggestions."""
    tips = []

    if quality == "Excellent":
        tips.append("Great connection — suitable for 4K streaming, gaming, and large uploads.")
    elif quality == "Good":
        tips.append("Solid connection — good for HD video calls and browsing.")
    elif quality == "Fair":
        tips.append("Usable, but expect buffering on HD video. SD streaming recommended.")
    else:
        tips.append("Weak connection — expect frequent drops and slow loading.")

    if ping_ms is not None and ping_ms > 100:
        tips.append("High latency detected — avoid real-time gaming or video calls right now.")

    if download_mbps < 5:
        tips.append("Low download speed — move closer to the router or switch to Wi-Fi/5G.")

    if download_mbps < 2:
        tips.append("Consider restarting your router/modem or checking for network congestion.")

    return tips
