import json
import re
import yaml
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process_data():
    try:
        raw_data = request.get_json()
        query = raw_data.get("query", "").strip()
        if not query:
            return jsonify({"error": "Input cannot be empty"}), 400
        if re.search(r'\b(exec|eval|subprocess|open)\b', query):
            return jsonify({"error": "Forbidden query detected"}), 400
        if re.search(r'__import__', query):
            return jsonify({"error": "Forbidden query detected"}), 400
        if re.search(r'\b(globals|locals)\b', query):
            return jsonify({"error": "Forbidden query detected"}), 400


        try:
            data_dict = yaml.safe_load(query) 
            if not isinstance(data_dict, dict):
                raise ValueError("Input is not a valid YAML dictionary")
        except yaml.YAMLError as e:
            return jsonify({"error": f"Invalid YAML format: {str(e)}"}), 400

        for key, value in data_dict.items():
            if isinstance(value, str):
                try:
                    data_dict[key] = eval(value)
                except Exception:
                    pass 
        return jsonify({"result": data_dict})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
