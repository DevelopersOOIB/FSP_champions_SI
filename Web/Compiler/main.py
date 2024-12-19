import io
import subprocess
from contextlib import redirect_stdout
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        user_code = request.form.get('code', '')
        try:
            f = io.StringIO()
            with redirect_stdout(f):
                exec_globals = {"__builtins__": __builtins__, "subprocess": subprocess}
                exec(user_code, exec_globals)
            output = f.getvalue().strip()
            if not output:
                output = exec_globals.get('result', 'Код выполнен успешно, но результат не возвращён.')
        except Exception as e:
            output = f"Ошибка: {e}"

    return render_template("index.html", output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
