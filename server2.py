from flask import Flask, request, jsonify
from flask_cors import CORS

import mysql.connector

app = Flask(__name__)
CORS(app)

# Connect to MySQL
db = mysql.connector.connect(
host="sql8.freesqldatabase.com",
        user="sql8777806",
        password="469dV5fzXa",
        port= 3306,
        database="sql8777806",
        autocommit=True
)

# =========================================
# Admin Login Route
# =========================================
@app.route('/admin_login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password required'}), 400

    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM admins WHERE username = %s', (username,))
    admin = cursor.fetchone()
    cursor.close()

    if not admin:
        return jsonify({'status': 'error', 'message': 'Admin not found'}), 404

    # JUST COMPARE THE PASSWORDS DIRECTLY
    if password == admin['password']:
        return jsonify({
            'status': 'success',
            'message': 'Admin login successful',
            'admin': {
                'username': admin['username'],
                'role': admin['role']
            }
        })
    else:
        return jsonify({'status': 'error', 'message': 'Incorrect password'}), 401


# =========================================
# Example Protected Route
# =========================================

# =========================================
# Run the Server
# =========================================

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.1', port=port)
