from flask import Flask, request, render_template, flash
import os
import zipfile
from lxml import etree
import database

app = Flask(__name__)
app.secret_key = "supersecretkey"

UPLOAD_FOLDER = "uploads"
FLAG_FILE = "/etc/flag.txt"


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        for param in ['name', 'family', 'father', 'team', 'type']:
            if param not in request.form:
                error = "Заполните все поля!"
                return render_template("index.html", error=error)
            
        database.fake_sql_inj(request.form['type'])


        if "file" not in request.files:
            error = "Заполните все поля!"
            return render_template("index.html", error=error)
        file = request.files["file"]
        if file.filename == "":
            error = "Заполните все поля!"
            return render_template("index.html", error=error)


        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        try:
            with zipfile.ZipFile(file_path, 'r') as docx:
                xml_content = docx.read("word/document.xml")
            os.remove(file_path)
        except Exception as e:
            os.remove(file_path)
            error = "Ваше заявление не соответствует требованиям нормативных актов!"
            return render_template("index.html", error=error)


        try:
            parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
            root = etree.fromstring(xml_content, parser)
            parsed_content = etree.tostring(root, pretty_print=True).decode()
            if 'flag{w0w_y0u_spl01t_xx3_1n_d0cx}' not in parsed_content:
                error = "Мы не можем обработать ваше заявление потому что у нас обед"
                return render_template("index.html", error=error)
            return render_template("index.html", success=parsed_content)
        except Exception as e:
            error = "Вы неверно заполнили заявление! Идите в МФЦ и смотрите правильный образец!"
            return render_template("index.html", error=error)

    return render_template("index.html")

if __name__ == "__main__":
    database.init_db()
    app.run(debug=False, host='0.0.0.0')
    
