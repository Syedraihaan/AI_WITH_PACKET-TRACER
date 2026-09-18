import pandas as pd
from sklearn.linear_model import LinearRegression

# Load network data
data = pd.read_csv("network_data.csv")

# Input: sample number
X = data[["sample"]]

# Output: number of packets
y = data["packets_input"]

# Create and train the AI model
model = LinearRegression()
model.fit(X, y)

# Predict the next 5 samples
future_samples = pd.DataFrame({
    "sample": [31, 32, 33, 34, 35]
})

predictions = model.predict(future_samples)

print("\n========== AI PREDICTIVE ANALYTICS ==========\n")

for sample, prediction in zip(
    future_samples["sample"],
    predictions
):
    print(
        f"Sample {sample} → "
        f"Predicted packets: {prediction:.0f}"
    )

print("\n==============================================")
print("Prediction completed successfully!")
print("==============================================")