from flask import Flask, request, session, redirect, url_for, render_template
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)

load_dotenv()

BASE_API_URL = os.getenv('BASE_API_URL')
PARTNER_ID = os.getenv('PARTNER_ID')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['mac'] = request.form['mac']
        session['ip'] = request.form['ip']
        session['link_login'] = request.form['link-login']
        session['link_login_only'] = request.form['link-login-only']
        session['error'] = request.form['error']

        if session['error']:
            return render_template('connect.html',
                                   business_name=os.getenv('BUSINESS_NAME'),
                                   link_login_only=session['link_login_only'],
                                   linkorig=session['link_login'],
                                   uname=session['mac'],
                                   passw=session['mac'],
                                   error=session['error'])

        api_url = f"{BASE_API_URL}/api/user/profile/{request.form['mac']}"
        response = requests.get(api_url)
        if response.status_code == 200:
            print("Did I get here ---------------------------- ")
            print("Error: ", response.json())
            print("session['error']: ", session['error'])

            return render_template('connect.html',
                                   business_name=os.getenv('BUSINESS_NAME'),
                                   link_login_only=session['link_login_only'],
                                   linkorig=session['link_login'],
                                   uname=session['mac'],
                                   passw=session['mac'],
                                   error=session['error'])

        api_url = f"{BASE_API_URL}/api/user/packages/{PARTNER_ID}"
        response = requests.get(api_url)
        packages = response.json()

        print("Did I get here  **************************")
        return render_template('index-list.html',
                               business_name=os.getenv('BUSINESS_NAME'),
                               packages=packages["data"],
                               session=session)
    print("Did I get here ++++++++++++++")
    return render_template('index.html', business_name=os.getenv('BUSINESS_NAME'))


@app.route('/subscribe', methods=['POST'])
def subscribe():
    phone = request.form['phone']
    package_id = request.form['package_id']
    mac_address = session.get('mac')
    linkorig = session.get('link_login')
    link_login_only = session.get('link_login_only')

    api_url = f"{BASE_API_URL}/api/user/signup"
    data = {
        'phone_number': phone,
        'package_id': package_id,
        'mac_address': mac_address,
        'partner_id': PARTNER_ID,
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        return render_template('connect.html',
                               business_name=os.getenv('BUSINESS_NAME'),
                               link_login_only=link_login_only,
                               linkorig=linkorig,
                               uname=mac_address,
                               passw="")
    else:
        return redirect(url_for('failure'))


if __name__ == '__main__':
    app.run(debug=True)
