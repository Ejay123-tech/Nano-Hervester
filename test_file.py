import streamlit as st
import time
import random
import pandas as pd

# Page setup
st.set_page_config(page_title="Vibration Energy Dashboard", layout="wide")

# Title
st.title("⚡ Real-Time Vibration Energy Dashboard (Voltage vs Time)")

# Placeholder for live chart
placeholder = st.empty()

# Empty dataframe to store time and voltage
data = pd.DataFrame(columns=["Time", "Voltage"])

# Simulate real-time voltage readings
for i in range(200):  # you can increase or decrease
    voltage = round(random.uniform(2.0, 5.0), 2)  # Simulated voltage (V)

    # Append new data row
    new_row = {"Time": time.strftime("%H:%M:%S"), "Voltage": voltage}
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

    # Keep last 30 readings for display
    data = data.tail(30)

    # Update the dashboard
    with placeholder.container():
        # Display current voltage as a KPI
        st.metric("🔌 Current Voltage (V)", f"{voltage} V")

        # Voltage vs Time chart
        st.markdown("### 📈 Voltage Over Time")
        st.line_chart(data.set_index("Time")[["Voltage"]])

    # Pause for 1 second before next update
    time.sleep(1)
