from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load data at startup
print("Loading data...")
df_prices = pd.read_csv('../data/raw/BrentOilPrices.csv')
df_prices['Date'] = pd.to_datetime(df_prices['Date'])
df_prices = df_prices.sort_values('Date').reset_index(drop=True)

df_events = pd.read_csv('../data/events.csv')
df_events['Date'] = pd.to_datetime(df_events['Date'])

# Change point results (from our models)
change_points = {
    'single_cp': {
        'date': '2005-02-23',
        'day_index': 4520,
        'mu_before': 21.42,
        'mu_after': 75.61,
        'description': 'Mid-2000s commodity supercycle onset'
    },
    'two_cp': {
        'cp1': {
            'date': '2004-02-24',
            'day_index': 4260,
            'mu_before': 20.28,
            'mu_after': 44.10,
            'description': 'Post-Iraq War demand shock'
        },
        'cp2': {
            'date': '2005-07-29',
            'day_index': 4631,
            'mu_before': 44.10,
            'mu_after': 76.19,
            'description': 'Spare capacity exhaustion'
        }
    }
}

print("Data loaded successfully!")

@app.route('/')
def index():
    return jsonify({'message': 'Brent Oil Price Analysis API', 'status': 'running'})

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Get historical price data"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    filtered_df = df_prices.copy()
    
    if start_date:
        filtered_df = filtered_df[filtered_df['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        filtered_df = filtered_df[filtered_df['Date'] <= pd.to_datetime(end_date)]
    
    result = {
        'dates': filtered_df['Date'].dt.strftime('%Y-%m-%d').tolist(),
        'prices': filtered_df['Price'].tolist()
    }
    return jsonify(result)

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all historical events"""
    result = []
    for _, row in df_events.iterrows():
        result.append({
            'date': row['Date'].strftime('%Y-%m-%d'),
            'event': row['Event'],
            'category': row['Category'],
            'description': row['Description'],
            'expected_direction': row['Expected_Direction']
        })
    return jsonify(result)

@app.route('/api/change-points', methods=['GET'])
def get_change_points():
    """Get detected change points from Bayesian models"""
    return jsonify(change_points)

@app.route('/api/change-points/single', methods=['GET'])
def get_single_cp():
    """Get single change point model results"""
    return jsonify(change_points['single_cp'])

@app.route('/api/change-points/two', methods=['GET'])
def get_two_cp():
    """Get two change point model results"""
    return jsonify(change_points['two_cp'])

if __name__ == '__main__':
    from flask import request
    app.run(debug=True, port=5000)
