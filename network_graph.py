import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LinearRegression

# Load data
data = pd.read_csv("network_data.csv")

# ==========================================
# AI ANOMALY DETECTION
# ==========================================

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

model = IsolationForest(
    contamination=0.25,
    random_state=42
)

data["ml_prediction"] = model.fit_predict(X)

# Network behavior rules
data["rule_anomaly"] = (
    (data["packets_input"] >= 400) |
    (data["input_errors"] >= 8) |
    (data["output_errors"] >= 5) |
    (data["drops"] >= 3)
)

# Hybrid result
data["Status"] = "NORMAL"

data.loc[
    (data["ml_prediction"] == -1) |
    (data["rule_anomaly"]),
    "Status"
] = "ANOMALY"


# ==========================================
# PLOT NORMAL VS ANOMALY TRAFFIC
# ==========================================

normal = data[data["Status"] == "NORMAL"]
anomaly = data[data["Status"] == "ANOMALY"]

plt.figure(figsize=(10, 6))

plt.scatter(
    normal["sample"],
    normal["packets_input"],
    label="Normal Traffic"
)

plt.scatter(
    anomaly["sample"],
    anomaly["packets_input"],
    label="Anomaly"
)

plt.xlabel("Network Sample")
plt.ylabel("Packets Input")
plt.title("AI Network Anomaly Detection")
plt.legend()
plt.grid(True)

plt.savefig("anomaly_detection.png", dpi=300)

plt.show()


# ==========================================
# PREDICTIVE ANALYTICS
# ==========================================

prediction_model = LinearRegression()

prediction_model.fit(
    data[["sample"]],
    data["packets_input"]
)

future = pd.DataFrame({
    "sample": [31, 32, 33, 34, 35]
})

predictions = prediction_model.predict(
    future
)


# ==========================================
# TRAFFIC PREDICTION GRAPH
# ==========================================

plt.figure(figsize=(10, 6))

plt.plot(
    data["sample"],
    data["packets_input"],
    marker="o",
    label="Historical Traffic"
)

plt.plot(
    future["sample"],
    predictions,
    marker="o",
    linestyle="--",
    label="AI Prediction"
)

plt.xlabel("Network Sample")
plt.ylabel("Packets Input")
plt.title("AI Network Traffic Prediction")
plt.legend()
plt.grid(True)

plt.savefig("traffic_prediction.png", dpi=300)

plt.show()


print()
print("======================================")
print("       GRAPH GENERATION COMPLETE")
print("======================================")

print()
print("Created files:")
print("1. anomaly_detection.png")
print("2. traffic_prediction.png")

print()
print("AI prediction:")

for sample, prediction in zip(
    future["sample"],
    predictions
):
    print(
        f"Sample {sample} -> "
        f"{prediction:.0f} packets"
    )