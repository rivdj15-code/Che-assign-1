import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import calculate_concentration, generate_unknown

st.set_page_config(page_title="Zinc Virtual Lab", layout="centered")

st.title("🔬 Zinc Detection in Water - Virtual Lab")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Theory",
    "Calibration",
    "Test Sample",
    "Manual Input",
    "Results"
])

# ---------------- THEORY ----------------
if page == "Theory":
    st.header("📘 Theory")
    st.latex("A = \\varepsilon c l")

    st.write("""
    This virtual lab simulates zinc detection using a colorimetric method.

    Zinc reacts with Zincon reagent to form a colored complex.
    The intensity is measured using a spectrophotometer.
    """)

# ---------------- CALIBRATION ----------------
elif page == "Calibration":
    st.header("📊 Calibration Curve")

    df = pd.read_csv("data/standards.csv")

    st.write("Standard Data:")
    st.dataframe(df)

    fig, ax = plt.subplots()
    ax.plot(df["Concentration"], df["Absorbance"], marker='o')
    ax.set_xlabel("Concentration (ppm)")
    ax.set_ylabel("Absorbance")
    ax.set_title("Calibration Curve")

    st.pyplot(fig)

# ---------------- TEST SAMPLE ----------------
elif page == "Test Sample":
    st.header("🧪 Unknown Sample")

    if st.button("Generate Sample"):
        true_conc, absorbance = generate_unknown()

        st.session_state["absorbance"] = absorbance
        st.session_state["true_conc"] = true_conc

        st.success(f"Measured Absorbance: {absorbance:.2f}")

# ---------------- MANUAL INPUT ----------------
elif page == "Manual Input":
    st.header("✍️ Enter Absorbance Manually")

    A = st.number_input("Enter Absorbance", min_value=0.0, step=0.1)

    if st.button("Calculate"):
        conc = calculate_concentration(A)
        st.session_state["manual_conc"] = conc

        st.success(f"Zinc Concentration: {conc:.2f} ppm")

# ---------------- RESULTS ----------------
elif page == "Results":
    st.header("📋 Results")

    if "absorbance" in st.session_state:
        A = st.session_state["absorbance"]
        conc = calculate_concentration(A)

        st.write(f"Calculated Concentration: {conc:.2f} ppm")

        if conc < 3:
            st.success("✅ Safe water (WHO limit < 3 ppm)")
        else:
            st.error("⚠️ Unsafe water")

    elif "manual_conc" in st.session_state:
        conc = st.session_state["manual_conc"]

        if conc < 3:
            st.success("✅ Safe water")
        else:
            st.error("⚠️ Unsafe water")

    else:
        st.warning("No data available. Run experiment first.")
