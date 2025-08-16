from flask import Flask, jsonify
from dotenv import load_dotenv

from scanner import fast_memecoin_scan

load_dotenv()

app = Flask(__name__)

@app.route('/fast_scan/<token>')
def fast_scan(token):
    result = fast_memecoin_scan(token)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
