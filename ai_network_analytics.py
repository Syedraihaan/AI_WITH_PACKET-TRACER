import pandas as pd
from sklearn.ensemble import IsolationForest

# Load the network dataset
data = pd.read_csv("network_data.csv")

# Features used by the AI model
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

# AI Model (Isolation Forest)
model = IsolationForest(
    contamination=0.25,   # About 25% of data may be anomalies
    random_state=42
)

# Train and predict
data["prediction"] = model.fit_predict(X)

# Convert prediction to readable labels
data["Status"] = data["prediction"].map({
    1: "🟢 NORMAL",
    -1: "🔴 ANOMALY"
})

# Show results
print("\n========== AI NETWORK ANALYTICS ==========\n")
print(data[["sample", "packets_input", "input_errors", "drops", "Status"]])

# Count anomalies
normal = (data["Status"] == "🟢 NORMAL").sum()
anomaly = (data["Status"] == "🔴 ANOMALY").sum()

print("\n=========================================")
print(f"Normal Traffic Samples : {normal}")
print(f"Anomaly Traffic Samples: {anomaly}")
print("=========================================")

# Save results to a CSV
data.to_csv("ai_results.csv", index=False)

print("\nResults saved as ai_results.csv")