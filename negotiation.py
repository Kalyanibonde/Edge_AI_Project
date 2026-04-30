def calculate_scores(anomaly):
    scores = {}

    # If anomaly → fault detection high priority
    scores["Fault Detection"] = 0.95 if anomaly else 0.3

    # Vision runs when system is safe
    scores["Vision"] = 0.8 if not anomaly else 0.4

    # Navigation always needed
    scores["Navigation"] = 0.6

    return scores


def select_module(scores):
    return max(scores, key=scores.get)