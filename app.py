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

        return render_template('connect.html',
                               business_name=BUSINESS_NAME,
                               link_login_only=session['link_login_only'],
                               linkorig=REDIRECT_URL,
                               uname=session['mac'],
                               passw=session['mac'],
                               error=session['error'])

    print("Did I get here ++++++++++++++")
    username = request.args.get('username', '')
    redirect_url = url_for('redirect_to_status')
    return redirect(redirect_url)



@app.route('/redirect_to_status', methods=['GET'])
def redirect_to_status():
    # Replace with your MikroTik Hotspot IP or domain
    hotspot_ip = "192.168.88.1"
    status_url = f"http://{hotspot_ip}/status"
    return redirect(status_url)

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
