from flask import Flask, render_template, request, jsonify
from graph import run_pipeline
from utils.data import load_csv, to_frames
app = Flask(__name__)

@app.get('/')
def index():
    return render_template('index.html')

@app.post("/analyze")
def analyze():
    try:
        f = request.files.get("file")
        csv_df = load_csv(f if f and f.filename else None)
        long_df, wide_df, cats = to_frames(csv_df)
        result = run_pipeline(long_df, wide_df, cats)
        print(result)
        return jsonify(result)
    except Exception as exc:  # noqa: BLE001
        return jsonify(error=str(exc)), 400

if __name__ == '__main__':
    app.run(debug=True)