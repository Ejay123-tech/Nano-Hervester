import streamlit as st
import pandas as pd
import serial
import time
from datetime import datetime
import random  # For simulation fallback

st.set_page_config(page_title="Arduino Voltage Monitor", layout="wide")
st.title("🔋 Real-Time Arduino Voltage Monitor")

# User-editable settings
PORT = "COM4"
BAUD_RATE = 9600

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Time", "Voltage"])
if "running" not in st.session_state:
    st.session_state.running = False

# Sidebar controls
refresh_rate = st.sidebar.slider("Update interval (s)", 0.5, 5.0, 1.0)
start = st.sidebar.button("▶️ Start Reading")
stop = st.sidebar.button("⏹ Stop Reading")

status_placeholder = st.sidebar.empty()
chart_placeholder = st.empty()
table_placeholder = st.empty()
info_placeholder = st.empty()

def read_voltage_from_serial(ser):
    try:
        line = ser.readline().decode(errors="ignore").strip()
        return float(line) if line else None
    except:
        return None

# Simulation fallback (if no Arduino)
def simulate_voltage():
    return round(random.uniform(2.5, 5.0), 2)

# Handle start/stop logic
if start:
    st.session_state.running = True
if stop:
    st.session_state.running = False

if st.session_state.running:
    try:
        # Try connecting to Arduino
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
        status_placeholder.success(f"✅ Connected to {PORT}")
        voltage_source = lambda: read_voltage_from_serial(ser)
    except serial.SerialException:
        status_placeholder.warning(f"⚠️ Could not open {PORT}. Using simulated data instead.")
        voltage_source = simulate_voltage
else:
    voltage_source = None
    status_placeholder.info("Click ▶️ Start Reading to begin.")

# Continuous reading
if st.session_state.running:
    placeholder = st.empty()
    while st.session_state.running:
        voltage = voltage_source()
        if voltage is not None:
            timestamp = datetime.now().strftime("%H:%M:%S")
            new_row = pd.DataFrame({"Time": [timestamp], "Voltage": [voltage]})
            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
            st.session_state.data = st.session_state.data.iloc[-50:]  # Keep last 50 points

            # Update dashboard
            chart_placeholder.line_chart(st.session_state.data.set_index("Time"))
            table_placeholder.dataframe(st.session_state.data.tail(10))
            info_placeholder.success(f"📈 Latest voltage: {voltage} V")
        else:
            info_placeholder.warning("No data received...")

        time.sleep(refresh_rate)
        st.rerun()

else:
    # Display stored data when not running
    if not st.session_state.data.empty:
        chart_placeholder.line_chart(st.session_state.data.set_index("Time"))
        table_placeholder.dataframe(st.session_state.data.tail(10))
    else:
        st.info("No data recorded yet.")
