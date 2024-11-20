import uuid

from flask import Flask, request, session, redirect, url_for, render_template
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)

load_dotenv()

BASE_API_URL = os.getenv('BASE_API_URL')
PARTNER_ID = os.getenv('PARTNER_ID')
REDIRECT_URL = os.getenv('REDIRECT_URL')
BUSINESS_NAME = os.getenv('BUSINESS_NAME')


# SESSION_UUID = str(uuid.uuid4())


@app.route('/test')
def test():
    mac = '00:0c:29:8e:6d:6c'
    ip = '192.168.11.20'
    link_login = '192.168.11.11'
    link_login_only = '192.168.3.3'

    # Prepare the data to be sent in the POST request
    data = {
        'mac': mac,
        'ip': ip,
        'link-login': link_login,
        'link-login-only': link_login_only,
        'error': 'error'
    }

    # Make a POST request to the index route
    response = requests.post(url_for('index', _external=True), data=data)

    # Handle the response if needed
    if response.status_code == 200:
        return response.text
    else:
        return "Failed to redirect to index", response.status_code


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        app_data = {
            'mac': request.form['mac'],
            'ip': request.form['ip'],
            'link_login': request.form['link-login'],
            'link_login_only': request.form['link-login-only'],
            'error': request.form['error']
        }

        api_url = f"{BASE_API_URL}/api/user/{app_data['mac']}"
        data = {'mac': app_data['mac']}
        headers = {'Content-Type': 'application/json'}
        response = requests.get(api_url, json=data, headers=headers)
        if response.status_code == 200:
            return render_template('connect.html',
                                   business_name=BUSINESS_NAME,
                                   link_login_only=app_data['link_login_only'],
                                   linkorig=REDIRECT_URL,
                                   app_data=app_data)

        api_url = f"{BASE_API_URL}/api/user/packages/{PARTNER_ID}"
        response = requests.get(api_url)
        packages = response.json()
        return render_template('index-list.html',
                               business_name=BUSINESS_NAME,
                               packages=packages["data"],
                               app_data=app_data)

    return render_template('marketting.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    phone = request.form['phone']
    package_id = request.form['package_id']

    app_data = {
        'mac': request.form['mac'],
        'ip': request.form['ip'],
        'link_login': request.form['link-login'],
        'link_login_only': request.form['link-login-only'],
        'error': request.form['error']
    }
    print(f"app_data Data in index: {app_data}")

    api_url = f"{BASE_API_URL}/api/user/subscribe"
    data = {
        'phone_number': phone,
        'package_id': package_id,
        'mac_address': app_data['mac'],
        'partner_id': PARTNER_ID,
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        return render_template('connect.html',
                               business_name=BUSINESS_NAME,
                               app_data=app_data)

    else:
        return redirect(url_for('failure'))


if __name__ == '__main__':
    app.run(debug=True, port=9000)
