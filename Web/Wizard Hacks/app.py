from flask import Flask, request, render_template, redirect, url_for, render_template_string
import os

app = Flask(__name__)

CREDENTIALS = {'admin': 'dakota'}

def filter_input(user_input):
    blacklist = ['eval', 'exec', 'getattr', 'setattr', 'delattr']
    for char in blacklist:
        user_input = user_input.replace(char, '')
    return user_input

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username in CREDENTIALS and CREDENTIALS[username] == password:
        return redirect(url_for('organization_page'))
    return render_template('login.html', error="Invalid credentials")

@app.route('/organization')
def organization_page():
    return render_template('organization.html')

@app.route('/generate', methods=['POST'])
def generate():
    query = request.form.get('query')
    safe_query = filter_input(query)
    try:
        rendered_result = render_template_string(safe_query)
        flag = os.environ.get('FLAG', 'default_flag')
        if rendered_result.strip() == flag:
            response_header = "Congratulations!"
            response_body = flag
        else:
            response_header = query
            response_body = rendered_result
    except Exception as e:
        response_header = query
        response_body = str(e)

    return render_template('result.html', response_header=response_header, response_body=response_body)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
