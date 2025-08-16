import numpy as np
from sklearn.linear_model import LogisticRegression

def predict_rug(liq_history, holder_pcts):
    """Simple rug risk prediction using volatility and concentration."""
    features = np.array([np.std(liq_history), max(holder_pcts)]).reshape(1, -1)  # Reshape for model
    model = LogisticRegression()  # Placeholder; in real use, train on data
    # Mock prediction (since no training data here)
    risk_prob = 1 if features[0, 0] > 0.1 or features[0, 1] > 50 else 0
    return "High rug risk" if risk_prob else "Safe"
