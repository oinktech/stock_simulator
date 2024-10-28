from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

# Initialize API key and base URL for stock data
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
FINNHUB_API_URL = 'https://finnhub.io/api/v1'
FINNHUB_SECRET = os.getenv('FINNHUB_SECRET')

# Store user data
user_data = {
    'initial_funds': 100000,  # default initial funds
    'current_funds': 100000,
    'portfolio': {}
}

@app.route('/')
def index():
    return render_template('index.html', user_data=user_data)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        stock_code = request.form.get('stock_code')
        headers = {
                'X-Finnhub-Secret': FINNHUB_SECRET  # 添加此头部
            }
        if stock_code:
            response = requests.get(f'{FINNHUB_API_URL}/quote?symbol={stock_code}.TW&token={FINNHUB_API_KEY}', headers=headers)
            stock_data = response.json()
            if 'c' in stock_data:
                return render_template('search.html', stock_data=stock_data, stock_code=stock_code, user_data=user_data)
            else:
                error = "無法獲取股票數據，請檢查代碼是否正確。"
                return render_template('search.html', stock_data=None, error=error, user_data=user_data)
    return render_template('search.html', stock_data=None, user_data=user_data)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        initial_funds = request.form.get('initial_funds')
        if initial_funds:
            user_data['initial_funds'] = float(initial_funds)
            user_data['current_funds'] = float(initial_funds)  # Reset current funds
            user_data['portfolio'].clear()  # Clear portfolio
            return redirect(url_for('index'))
    return render_template('settings.html', user_data=user_data)

@app.route('/portfolio')
def portfolio():
    portfolio_data = user_data['portfolio']
    return render_template('portfolio.html', portfolio_data=portfolio_data, user_data=user_data)

@app.route('/api/save_initial_funds', methods=['POST'])
def save_initial_funds():
    return jsonify({'success': True})

@app.route('/api/save_stock', methods=['POST'])
def save_stock():
    data = request.get_json()
    stock_code = data.get('stockCode')
    price = data.get('price')
    action = data.get('action')

    if action == 'buy':
        if stock_code in user_data['portfolio']:
            user_data['portfolio'][stock_code]['quantity'] += 1
        else:
            user_data['portfolio'][stock_code] = {
                'price': price,
                'quantity': 1,
                'change': 0  # Placeholder for daily change
            }
        user_data['current_funds'] -= price

    elif action == 'sell':
        if stock_code in user_data['portfolio']:
            user_data['portfolio'][stock_code]['quantity'] -= 1
            if user_data['portfolio'][stock_code]['quantity'] == 0:
                del user_data['portfolio'][stock_code]

    return jsonify({'success': True})

@app.route('/api/get_portfolio', methods=['GET'])
def get_portfolio():
    return jsonify({'portfolio': user_data['portfolio']})

@app.route('/api/get_funds', methods=['GET'])
def get_funds():
    return jsonify({'initial_funds': user_data['initial_funds'], 'current_funds': user_data['current_funds']})

if __name__ == '__main__':
    app.run(debug=True,port=10000, host='0.0.0.0')
