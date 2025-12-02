import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

if 'data' not in st.session_state:
    st.session_state.data = None

st.markdown('<h2 style="text-align:left;">Probability Distribution Fitting Tool</h3>', unsafe_allow_html=True)
st.markdown("A single-file app to fit histograms with scipy.stats distributions. Paste data or upload CSV")

st.sidebar.header("Data Input")
input_method = st.sidebar.radio("Choose data input method:", ["Manual Entry", "Upload CSV"])

if input_method == "Manual Entry":
    manual_data = st.sidebar.text_area("Enter comma-separated values:")
    load_data = st.sidebar.button("Load Data")
    
    if load_data:
        if manual_data.strip() == "":  # empty box
            st.session_state.data = None
            st.toast("Data cleared.")
        else:
            try:
                st.session_state.data = np.array([float(x.strip()) for x in manual_data.split(',')])
                st.toast("Data loaded successfully!")
            except ValueError:
                st.sidebar.error("Please enter valid numbers separated")

            
else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        column = st.sidebar.selectbox("Select data column", df.columns)
        st.session_state.data = df[column].dropna().values
        if not st.session_state.get("toast_shown", False):
            st.toast(f"Loaded '{column}' from CSV!")
            st.session_state.toast_shown = True
        
Distributions = {
    "Normal": stats.norm,
    "Uniform": stats.uniform,
    "Exponential": stats.expon,
    "Gamma": stats.gamma,
    "Beta": stats.beta,
    "Chi-Squared": stats.chi2,
    "T": stats.t,
    "F": stats.f,
    "Log-normal": stats.lognorm,
    "Weibull": stats.weibull_min
}

data = st.session_state.data

autoFit, manualFit = st.tabs(["Automatic Fit", "Manual Fit"])

with autoFit:
    
    if data is None:
        st.info("⚠️ No data loaded yet. Please enter data or upload a CSV.")
    elif len(data) < 2 or len(np.unique(data)) < 2:
        st.warning("⚠️ Not enough data to generate a distribution plot. Please add more data.")
    else:
        st.header("Automatic Distribution Fitting")
        selected_dist = st.selectbox("Select distribution to fit:", list(Distributions.keys()))
        
        dist_obj = Distributions[selected_dist]
        
        params = dist_obj.fit(data)
        fitted_dist = dist_obj(*params)
        x = np.linspace(data.min(), data.max(), 100)
        fit = fitted_dist.pdf(x)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(data, bins=30, density=True, alpha=0.7, label='Data')
        ax.plot(x, fit, 'r-', lw=2, label=f'Fitted {selected_dist}')
        ax.set_xlabel('Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
        
        hist, bin_edges = np.histogram(data, bins=30, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        predicted_pdf = fitted_dist.pdf(bin_centers)
        
        mse = np.mean((hist - predicted_pdf) ** 2)
        max_error = np.max(np.abs(hist - predicted_pdf))
        
        float_params = [float(p) for p in params]
        param_names = dist_obj.shapes.split(', ') if dist_obj.shapes else []
        names = param_names + ["loc", "scale"]
        
        parameter_names = names
        parameter_values = float_params
        
        quality_names = ["Mean Squared Error", "Maximum Error"]
        quality_values = [mse, max_error]
        
        parameter_table = pd.DataFrame({
            "Name": parameter_names,
            "Value": [f"{v:.6f}" for v in parameter_values]
        })
        
        quality_table = pd.DataFrame({
            "Name": quality_names,
            "Value": [f"{v:.6f}" for v in quality_values]
        })

        st.subheader("Parameters")
        st.dataframe(parameter_table, hide_index=True)
        st.subheader("Quality of the Fit")
        st.dataframe(quality_table, hide_index=True)

with manualFit:
    
    if data is None:
        st.info("⚠️ No data loaded yet. Please enter data or upload a CSV.")
    elif len(data) < 2 or len(np.unique(data)) < 2:
        st.warning("⚠️ Not enough data to generate a distribution plot. Please add more data.")
    else:
        st.header("Manual Distribution Fitting")
        st.write("Adjust parameters manually and see how the fitted curve changes. Useful for intuition and fine-tuning.")
        
        manual_dist = st.selectbox("Select distribution:", list(Distributions.keys()), key="manual")
        dist_obj = Distributions[manual_dist]
        
        if manual_dist == "Normal":
            loc = st.slider("Mean (μ)", float(data.min()), float(data.max()), float(data.mean()))
            scale = st.slider("Std Dev (σ)", 0.1, float(data.std() * 3), float(data.std()))
            manual_params = [loc, scale]
            
        elif manual_dist == "Uniform":
            loc = st.slider("Lower bound", float(data.min()-1), float(data.max()), float(data.min()))
            scale = st.slider("Upper bound", float(data.min()), float(data.max()+1), float(data.max()))
            manual_params = [loc, scale - loc]
            
        elif manual_dist == "Exponential":
            scale = st.slider("Scale (β)", 0.1, float(data.max()*2), 1.0)
            manual_params = [0, scale]
            
        elif manual_dist == "Gamma":
            a = st.slider("Shape (a)", 0.1, 20.0, 2.0)
            loc = st.slider("Location", float(data.min()), float(data.max()), float(data.min()))
            scale = st.slider("Scale", 0.1, 10.0, 1.0)
            manual_params = [a, loc, scale]
            
        elif manual_dist == "Beta":
            a = st.slider("Shape α", 0.1, 10.0, 2.0)
            b = st.slider("Shape β", 0.1, 10.0, 2.0)
            loc = st.slider("Lower bound", float(data.min()), float(data.max()), float(data.min()))
            scale = st.slider("Upper bound", float(data.min()), float(data.max()), float(data.max()))
            manual_params = [a, b, loc, scale - loc]
            
        elif manual_dist == "Chi-Squared":
            df = st.slider("Degrees of freedom", 1, 50, 2)
            manual_params = [df]

        elif manual_dist == "T":
            df = st.slider("Degrees of freedom", 1, 50, 10)
            manual_params = [df]

        elif manual_dist == "F":
            dfn = st.slider("Numerator df", 1, 50, 5)
            dfd = st.slider("Denominator df", 1, 50, 10)
            manual_params = [dfn, dfd]

        elif manual_dist == "Log-normal":
            sigma = st.slider("Shape (σ)", 0.1, 2.0, 1.0)
            mu = st.slider("Scale (e^μ)", 0.1, float(data.max()), float(np.exp(1)))
            manual_params = [sigma, 0, mu]

        elif manual_dist == "Weibull":
            c = st.slider("Shape (c)", 0.1, 10.0, 1.5)
            scale = st.slider("Scale (λ)", 0.1, float(data.max()*2), float(data.mean()))
            manual_params = [c, 0, scale]
        
        # Plot
        manual_fitted = dist_obj(*manual_params)
        x = np.linspace(data.min(), data.max(), 100)
        manual_pdf = manual_fitted.pdf(x)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(data, bins=30, density=True, alpha=0.7, label='Data')
        ax.plot(x, manual_pdf, 'r-', lw=2, label=f'Manual {manual_dist}')
        ax.set_xlabel('Value')
        ax.set_ylabel('Density')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        st.pyplot(fig)
