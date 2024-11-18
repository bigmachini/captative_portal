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

        session['user_type'] = 'new'

        api_url = f"{BASE_API_URL}/user/packages/{PARTNER_ID}"
        response = requests.get(api_url)
        user_data = response.json()

        if user_data:
            session['user_type'] = 'repeat'

        return redirect(url_for('connect'))

    else:
        api_url = f"{BASE_API_URL}/user/packages/{PARTNER_ID}"
        response = requests.get(api_url)
        packages = response.json()

        return render_template('index-list.html', business_name=os.getenv('BUSINESS_NAME'), packages=packages["data"])


@app.route('/connect', methods=['POST'])
def connect():
    mac = session.get('mac')
    ip = session.get('ip')
    link_login = session.get('link_login')
    link_login_only = session.get('link_login_only')
    linkorig = request.referrer

    uname = request.form['uname']
    passw = request.form['pass']

    if session.get('user_type') == 'new':
        api_url = f"{BASE_API_URL}/user/signup"
        data = {
            'username': uname,
            'mac': mac,
            'ip': ip,
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=data, headers=headers)

    return render_template('connect.html', business_name=os.getenv('BUSINESS_NAME'), link_login_only=link_login_only,
                           linkorig=linkorig, uname=uname, passw=passw)


if __name__ == '__main__':
    app.run(debug=True)
