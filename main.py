from flask import Flask, jsonify, Response
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Sistemas disponibles y sus códigos
SYSTEMS = {
    "navigation": "NAV-01",
    "communications": "COM-02",
    "life_support": "LIFE-03",
    "engines": "ENG-04",
    "deflector_shield": "SHLD-05"
}

current_damaged_system = 'navigation'

# Template HTML básico
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Repair</title>
</head>
<body>
    <div class="anchor-point">{code}</div>
</body>
</html>
"""

@app.route("/status", methods=['GET'])
def get_status():
    global current_damaged_system
    if current_damaged_system is None:
        current_damaged_system = random.choice(list(SYSTEMS.keys()))
    return jsonify({"damaged_system": current_damaged_system})

@app.route("/repair-bay", methods=['GET'])
def repair_bay():
    global current_damaged_system
    if current_damaged_system is None:
        current_damaged_system = random.choice(list(SYSTEMS.keys()))
    repair_code = SYSTEMS[current_damaged_system]
    return HTML_TEMPLATE.format(code=repair_code)

@app.route("/teapot", methods=['POST'])
def teapot():
    return Response(status=418)

if __name__ == '__main__':
    app.run(debug=True)