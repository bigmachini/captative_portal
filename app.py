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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        app_data = {
            'mac': request.form['mac'],
            'ip': request.form['ip'],
            'link_login': request.form['link-login'],
            'link_login_only': request.form['link-login-only'],
            'error': request.form['error'],
        }

        print(f"index:: request.form['error'] --> {request.form['error']}")
        print(f"index:: app_data --> {app_data}")

        api_url = f"{BASE_API_URL}/api/user/{app_data['mac']}"
        data = {'mac': app_data['mac']}
        headers = {'Content-Type': 'application/json'}
        response = requests.get(api_url, json=data, headers=headers)
        if response.status_code == 200:
            # Make a POST request to the index route
            return render_template('redirect_form.html', app_data=app_data)

        api_url = f"{BASE_API_URL}/api/user/packages/{PARTNER_ID}"
        response = requests.get(api_url)
        packages = response.json()
        return render_template('index-list.html',
                               business_name=BUSINESS_NAME,
                               packages=packages["data"],
                               app_data=app_data)

    return render_template('marketting.html')


@app.route('/connect', methods=['POST'])
def connect():
    app_data = {
        'mac': request.form['mac'],
        'ip': request.form['ip'],
        'link_login': request.form['link_login'],
        'link_login_only': request.form['link_login_only'],
        'error': request.form['error'],
    }
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ app_data:', app_data)
    return render_template('connect.html',
                           business_name=BUSINESS_NAME,
                           linkorig=REDIRECT_URL,
                           app_data = app_data)


@app.route('/subscribe', methods=['POST'])
def subscribe():
    phone = request.form['phone']
    package_id = request.form['package_id']
    app_data = {
        'mac': request.form['mac'],
        'ip': request.form['ip'],
        'link_login': request.form['link_login'],
        'link_login_only': request.form['link_login_only'],
        'error': request.form['error'],
    }
    print(f"subscribe app_data: {app_data}")

    api_url = f"{BASE_API_URL}/api/user/subscribe"
    data = {
        'phone_number': phone,
        'package_id': package_id,
        'mac_address': app_data['mac'],
        'partner_id': PARTNER_ID,
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json=data, headers=headers)
    print(f"subscribe response: {response}")
    if response.status_code == 200:
        # Redirect to the connect route with query parameters
        return render_template('redirect_form.html', app_data=app_data)
    else:
        return redirect(url_for('failure'))


if __name__ == '__main__':
    app.run(debug=True)
