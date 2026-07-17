import pymc as pm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import arviz as az

# ==========================================
# 1. DATA PREPARATION
# ==========================================
df = pd.read_csv('data/raw/BrentOilPrices.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

price_data = df['Price'].values
time_index = np.arange(len(price_data))

print(f"Loaded {len(price_data)} days of data.")
print(f"Price range: ${price_data.min():.2f} to ${price_data.max():.2f}")

# ==========================================
# 2. BUILD THE TWO-CHANGE-POINT MODEL
# ==========================================
print("Building two-change-point model...")
with pm.Model() as two_cp_model:
    # A. Define TWO switch points
    # Create two independent change points
    taus_raw = pm.DiscreteUniform("taus_raw", lower=0, upper=len(time_index)-1, shape=2)
    # Use minimum and maximum to guarantee tau1 < tau2
    tau1 = pm.Deterministic('tau1', pm.math.minimum(taus_raw[0], taus_raw[1]))
    tau2 = pm.Deterministic('tau2', pm.math.maximum(taus_raw[0], taus_raw[1]))
    
    # B. Define THREE mean prices (one for each regime)
    overall_mean = np.mean(price_data)
    overall_std = np.std(price_data)
    
    mu1 = pm.Normal('mu1', mu=overall_mean, sigma=overall_std * 2)
    mu2 = pm.Normal('mu2', mu=overall_mean, sigma=overall_std * 2)
    mu3 = pm.Normal('mu3', mu=overall_mean, sigma=overall_std * 2)
    
    # C. Define the standard deviation
    sigma = pm.HalfNormal('sigma', sigma=overall_std)
    
    # D. Use nested pm.math.switch to select the correct mean
    mu = pm.math.switch(
        time_index <= tau1,
        mu1,
        pm.math.switch(time_index <= tau2, mu2, mu3)
    )
    
    # E. Define the Likelihood
    y = pm.Normal('y', mu=mu, sigma=sigma, observed=price_data)

# ==========================================
# 3. RUN THE SAMPLER (MCMC)
# ==========================================
print("Sampling (this may take 2-3 minutes)...")
with two_cp_model:
    trace = pm.sample(2000, tune=1000, return_inferencedata=True, random_seed=42)

# ==========================================
# 4. INTERPRET THE MODEL OUTPUT
# ==========================================
print("\n--- Two-Change-Point Model Summary ---")
print(pm.summary(trace, var_names=['tau1', 'tau2', 'mu1', 'mu2', 'mu3', 'sigma']))

# Plot the trace
az.plot_trace(trace, var_names=['tau1', 'tau2', 'mu1', 'mu2', 'mu3', 'sigma'])
plt.tight_layout()
plt.savefig('two_cp_trace_plot.png')
print("Saved two_cp_trace_plot.png")

# Plot posterior distributions for the two change points
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
az.plot_posterior(trace, var_names=['tau1', 'tau2'], ax=axes)
plt.tight_layout()
plt.savefig('two_cp_posterior_taus.png')
print("Saved two_cp_posterior_taus.png")

# ==========================================
# 5. FIND THE EXACT DATES
# ==========================================
print("\n--- Change Point Dates ---")
tau1_mean = int(trace.posterior['tau1'].mean().values)
tau2_mean = int(trace.posterior['tau2'].mean().values)

print(f"First Change Point (tau1): Day {tau1_mean} -> {df.iloc[tau1_mean]['Date']}")
print(f"Second Change Point (tau2): Day {tau2_mean} -> {df.iloc[tau2_mean]['Date']}")

print(f"\nRegime 1 (before {df.iloc[tau1_mean]['Date'].strftime('%Y-%m-%d')}): Mean = ${trace.posterior['mu1'].mean().values:.2f}")
print(f"Regime 2 (between {df.iloc[tau1_mean]['Date'].strftime('%Y-%m-%d')} and {df.iloc[tau2_mean]['Date'].strftime('%Y-%m-%d')}): Mean = ${trace.posterior['mu2'].mean().values:.2f}")
print(f"Regime 3 (after {df.iloc[tau2_mean]['Date'].strftime('%Y-%m-%d')}): Mean = ${trace.posterior['mu3'].mean().values:.2f}")
