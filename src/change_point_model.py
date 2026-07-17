import pymc as pm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import arviz as az

# ==========================================
# 1. DATA PREPARATION
# ==========================================
# IMPORTANT: Check your data folder and update this filename if needed!
# Common names: 'brent_oil_prices.csv', 'BrentOilPrices.csv', etc.
df = pd.read_csv('data/raw/BrentOilPrices.csv') 

# Convert Date to datetime and sort chronologically
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

# Extract the price data and create a numerical time index (0, 1, 2, ..., N)
price_data = df['Price'].values
time_index = np.arange(len(price_data))

print(f"Loaded {len(price_data)} days of data.")
print(f"Price range: ${price_data.min():.2f} to ${price_data.max():.2f}")

# ==========================================
# 2. BUILD THE BAYESIAN CHANGE POINT MODEL
# ==========================================
print("Building model...")
with pm.Model() as change_point_model:
    # A. Define the switch point (tau) as a discrete uniform prior
    tau = pm.DiscreteUniform('tau', lower=0, upper=len(time_index)-1)
    
    # B. Define "Before" and "After" mean prices
    overall_mean = np.mean(price_data)
    overall_std = np.std(price_data)
    
    mu_before = pm.Normal('mu_before', mu=overall_mean, sigma=overall_std * 2)
    mu_after = pm.Normal('mu_after', mu=overall_mean, sigma=overall_std * 2)
    
    # C. Define the standard deviation (sigma)
    sigma = pm.HalfNormal('sigma', sigma=overall_std)
    
    # D. Use pm.math.switch to select the correct mean
    mu = pm.math.switch(tau >= time_index, mu_before, mu_after)
    
    # E. Define the Likelihood
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=price_data)

# ==========================================
# 3. RUN THE SAMPLER (MCMC)
# ==========================================
print("Sampling (this may take 1-2 minutes)...")
with change_point_model:
    trace = pm.sample(2000, tune=1000, return_inferencedata=True, random_seed=42)

# ==========================================
# 4. INTERPRET THE MODEL OUTPUT
# ==========================================
print("\n--- Model Summary ---")
print(pm.summary(trace, var_names=['tau', 'mu_before', 'mu_after', 'sigma']))

# Note: Since we are running this from the terminal, we will save the plots 
# to files instead of trying to display them in a headless terminal.
az.plot_trace(trace, var_names=['tau', 'mu_before', 'mu_after', 'sigma'])
plt.savefig('trace_plot.png')
print("Saved trace_plot.png")

az.plot_posterior(trace, var_names=['tau'])
plt.savefig('posterior_tau.png')
print("Saved posterior_tau.png")
