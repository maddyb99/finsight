from flask import Flask, render_template, request, jsonify
from utils.data import load_csv
app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.post("/analyze")
def analyze():
    try:
        f = request.files.get("file")
        csv_df = load_csv(f if f and f.filename else None)
        print(csv_df)
        return jsonify(data=csv_df.to_dict(orient="records"))
    except Exception as exc:  # noqa: BLE001
        return jsonify(error=str(exc)), 400

if __name__ == '__main__':
    app.run(debug=True)