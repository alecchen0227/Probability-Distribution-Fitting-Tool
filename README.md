# Probability Distribution Fitting Tool

A Streamlit web app that fits probability distributions to a dataset and shows how well each one matches. Paste in numbers or upload a CSV, pick a distribution, and the app fits it automatically, plots the curve over a histogram of your data, and reports the fitted parameters and fit quality. A manual mode lets you tune each distribution with sliders.

Final project for NE 111 at the University of Waterloo (Fall 2025).

## Features

- **Two ways to load data:** type comma-separated values, or upload a CSV and choose a column
- **10 distributions:** Normal, Uniform, Exponential, Gamma, Beta, Chi-Squared, Student's t, F, Log-normal and Weibull
- **Automatic fit:** estimates parameters with SciPy's `fit()` and plots the fitted PDF over a 30-bin histogram
- **Fit quality:** reports the mean squared error and maximum error between the histogram and the fitted curve
- **Manual fit:** sliders for each distribution's parameters (mean, standard deviation, shape, scale, degrees of freedom) so you can see how each one changes the curve
- **Input checks:** warns when no data is loaded or there are too few distinct values to fit

## How it works

1. The data is stored as a NumPy array in Streamlit's session state, so it stays loaded as you switch tabs.
2. In **Automatic Fit**, the chosen `scipy.stats` distribution's `fit()` method estimates its parameters from the data.
3. The fitted probability density function is evaluated across the data's range and drawn over a normalized histogram with Matplotlib.
4. Fit quality is measured by comparing the histogram's bin heights with the fitted PDF at each bin centre:
   - **Mean squared error:** the average squared difference across all bins
   - **Maximum error:** the largest single difference
5. In **Manual Fit**, the slider values are passed straight to the distribution, and the curve redraws on every change.

## Run it locally

Requires Python 3.9 or newer.

```bash
git clone https://github.com/alecchen0227/Probability-Distribution-Fitting-Tool.git
cd Probability-Distribution-Fitting-Tool
pip install -r requirements.txt
streamlit run Project.py
```

The app opens in your browser at `http://localhost:8501`. If the `streamlit` command isn't found, run `python -m streamlit run Project.py` instead.

### Sample data to try

Paste this into **Manual Entry** in the sidebar, click **Load Data**, then try the Normal distribution:

```
4.8, 5.1, 5.3, 4.9, 5.0, 5.6, 4.7, 5.2, 5.4, 4.6, 5.0, 5.1, 4.9, 5.5, 5.2, 4.8, 5.0, 5.3
```

## Built with

- [Streamlit](https://streamlit.io/) for the interface
- [SciPy](https://scipy.org/) (`scipy.stats`) for distributions and fitting
- [NumPy](https://numpy.org/) and [pandas](https://pandas.pydata.org/) for data handling
- [Matplotlib](https://matplotlib.org/) for plots
