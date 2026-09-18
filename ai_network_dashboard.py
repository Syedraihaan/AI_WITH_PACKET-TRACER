import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

# ============================================================
# LOAD NETWORK DATA
# ============================================================

data = pd.read_csv("network_data.csv")

features = [
    "packets_input",
    "bytes_input",
    "packets_output",
    "bytes_output",
    "input_errors",
    "output_errors",
    "drops"
]

X = data[features]


# ============================================================
# AI ANOMALY DETECTION
# ============================================================

ai_model = IsolationForest(
    contamination=0.25,
    random_state=42
)

data["ml_prediction"] = ai_model.fit_predict(X)


# ============================================================
# NETWORK ANOMALY RULES
# ============================================================
# These thresholds are for our simulated student dataset.
#
# High packet volume, errors or drops indicate unusual traffic.

data["rule_anomaly"] = (
    (data["packets_input"] >= 400) |
    (data["input_errors"] >= 8) |
    (data["output_errors"] >= 5) |
    (data["drops"] >= 3)
)


# ============================================================
# COMBINE ML + NETWORK RULES
# ============================================================

data["Status"] = "NORMAL"

data.loc[
    (data["ml_prediction"] == -1) |
    (data["rule_anomaly"]),
    "Status"
] = "ANOMALY"


# ============================================================
# FIND REASON FOR ANOMALY
# ============================================================

def find_reason(row):

    reasons = []

    if row["packets_input"] >= 400:
        reasons.append("High packet volume")

    if row["input_errors"] >= 8:
        reasons.append("High input errors")

    if row["output_errors"] >= 5:
        reasons.append("Output errors")

    if row["drops"] >= 3:
        reasons.append("Packet drops")

    if row["ml_prediction"] == -1:
        reasons.append("ML detected unusual pattern")

    if len(reasons) == 0:
        return "Normal traffic"

    return ", ".join(reasons)


data["Reason"] = data.apply(find_reason, axis=1)


# ============================================================
# DISPLAY AI NETWORK ANALYTICS
# ============================================================

print()
print("=" * 70)
print("                  AI NETWORK ANALYTICS")
print("=" * 70)


# ============================================================
# ANOMALY DETECTION RESULTS
# ============================================================

print()
print("ANOMALY DETECTION")
print("-" * 70)

print(
    data[
        [
            "sample",
            "packets_input",
            "input_errors",
            "output_errors",
            "drops",
            "Status",
            "Reason"
        ]
    ].to_string(index=False)
)


# ============================================================
# ANOMALY SUMMARY
# ============================================================

normal_count = (data["Status"] == "NORMAL").sum()
anomaly_count = (data["Status"] == "ANOMALY").sum()

print()
print("-" * 70)
print("ANOMALY SUMMARY")
print("-" * 70)

print(f"Normal samples  : {normal_count}")
print(f"Anomaly samples : {anomaly_count}")


# ============================================================
# PREDICTIVE ANALYTICS
# ============================================================

prediction_model = LinearRegression()

prediction_model.fit(
    data[["sample"]],
    data["packets_input"]
)

future_samples = pd.DataFrame({
    "sample": [31, 32, 33, 34, 35]
})

predictions = prediction_model.predict(
    future_samples
)


# ============================================================
# TRAFFIC PREDICTION
# ============================================================

print()
print("=" * 70)
print("                  TRAFFIC PREDICTION")
print("=" * 70)

for sample, prediction in zip(
    future_samples["sample"],
    predictions
):

    print(
        f"Sample {sample} -> "
        f"Predicted packets: {prediction:.0f}"
    )


# ============================================================
# AI ANALYSIS
# ============================================================

latest_prediction = predictions[-1]

print()
print("=" * 70)
print("                     AI ANALYSIS")
print("=" * 70)

print(
    f"Predicted traffic at sample 35: "
    f"{latest_prediction:.0f} packets"
)

if anomaly_count > 0:

    print(
        "AI Alert: Anomalous network activity detected!"
    )

if latest_prediction > 500:

    print(
        "AI Warning: Future traffic may become high."
    )

else:

    print(
        "AI Status: Predicted traffic is within normal range."
    )


# ============================================================
# SAVE RESULTS
# ============================================================

data.to_csv(
    "ai_network_results.csv",
    index=False
)

print()
print("=" * 70)
print("Analysis completed successfully.")
print("=" * 70)

print()
print(
    "Results saved to: ai_network_results.csv"
)