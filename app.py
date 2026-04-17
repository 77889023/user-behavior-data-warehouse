from flask import Flask, render_template, jsonify
import pymysql

app = Flask(__name__)

# 数据库配置（根据你的实际用户名、密码、数据库名修改）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'itcast',   # 你的数据库名是 itcast
    'charset': 'utf8mb4'
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

@app.route('/api/dau')
def api_dau():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT behavior_date, dau FROM ads_daily_active_users ORDER BY behavior_date")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    dates = [row[0].strftime('%Y-%m-%d') for row in rows]
    dau_values = [row[1] for row in rows]
    return jsonify({'dates': dates, 'dau': dau_values})   # 注意这里是 'dau'

@app.route('/api/funnel')
def api_funnel():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT step, user_count FROM ads_funnel ORDER BY FIELD(step, 'pv', 'fav', 'cart', 'buy')")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    steps = [row[0] for row in rows]
    counts = [row[1] for row in rows]
    return jsonify({'steps': steps, 'counts': counts})

@app.route('/api/hot_products')
def api_hot_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT product_id, click_count FROM ads_hot_products ORDER BY click_count DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    products = [f"商品{row[0]}" for row in rows]
    clicks = [row[1] for row in rows]
    return jsonify({'products': products, 'clicks': clicks})

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)