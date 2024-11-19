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
        session['mac'] = request.form['mac']
        session['ip'] = request.form['ip']
        session['link_login'] = request.form['link-login']
        session['link_login_only'] = request.form['link-login-only']

        api_url = f"{BASE_API_URL}/api/user/{session['mac']}"
        response = requests.get(api_url)
        if response.status_code != 200:
            api_url = f"{BASE_API_URL}/api/user/packages/{PARTNER_ID}"
            response = requests.get(api_url)
            packages = response.json()
            print("Did I get here  **************************")
            return render_template('index-list.html',
                                   business_name=BUSINESS_NAME,
                                   packages=packages["data"],
                                   session=session)

        session['error'] = request.form['error']

        if session['error']:
            api_url = f"{BASE_API_URL}/api/user/profile/clear"
            data = {
                'mac': session['mac']
            }
            headers = {'Content-Type': 'application/json'}
            response = requests.post(api_url, json=data, headers=headers)
            if response.status_code == 200:
                print("+++++++++++++ Profile Cleared Successful +++++++++++++++++")

            api_url = f"{BASE_API_URL}/api/user/packages/{PARTNER_ID}"
            response = requests.get(api_url)
            packages = response.json()
            print("Did I get here  **************************")
            return render_template('index-list.html',
                                   business_name=BUSINESS_NAME,
                                   packages=packages["data"],
                                   session=session)

        print(f" **************************************************************")
        print(f'BUSINESS_NAME: {BUSINESS_NAME}')
        print(f'Link Login Only: {session["link_login_only"]}')
        print(f'linkorig: {REDIRECT_URL}')
        print(f'IP: {session["ip"]}')
        print(f'MAC: {session["mac"]}')
        print(f'Link Login: {session["link_login"]}')
        print(f" **************************************************************")

        return render_template('connect.html',
                               business_name=BUSINESS_NAME,
                               link_login_only=session['link_login_only'],
                               linkorig=REDIRECT_URL,
                               uname=session['mac'],
                               passw=session['mac'],
                               error=session['error'])

    print("Did I get here ++++++++++++++")
    return render_template('marketting.html')


@app.route('/subscribe', methods=['POST'])
def subscribe():
    phone = request.form['phone']
    package_id = request.form['package_id']
    mac_address = session.get('mac')
    linkorig = session.get('link_login')
    link_login_only = session.get('link_login_only')

    api_url = f"{BASE_API_URL}/api/user/subscribe"
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
