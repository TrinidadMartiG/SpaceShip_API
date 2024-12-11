from flask import Flask, jsonify, Response, request
import random
from flask_cors import CORS
import math

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

# Critical and reference points
CRITICAL_POINT = {
    'pressure': 10.0,  # MPa
    'specific_volume': 0.0035  # m³/kg
}

REFERENCE_POINT = {
    'pressure': 0.05,  # MPa
    'specific_volume_liquid': 0.00105,  # m³/kg
    'specific_volume_vapor': 30.00  # m³/kg
}

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

@app.route("/phase-change-diagram", methods=['GET'])
def get_phase_change_values():
    try:
        pressure = float(request.args.get('pressure', type=float))
        
        # Validate pressure range
        if pressure < REFERENCE_POINT['pressure'] or pressure > CRITICAL_POINT['pressure']:
            return jsonify({
                "error": f"Pressure must be between {REFERENCE_POINT['pressure']} and {CRITICAL_POINT['pressure']} MPa"
            }), 400

        # At critical point, both volumes are equal
        if math.isclose(pressure, CRITICAL_POINT['pressure']):
            return jsonify({
                "specific_volume_liquid": CRITICAL_POINT['specific_volume'],
                "specific_volume_vapor": CRITICAL_POINT['specific_volume']
            })

        # Calculate interpolation factor (logarithmic)
        log_p = math.log(pressure)
        log_p1 = math.log(REFERENCE_POINT['pressure'])
        log_p2 = math.log(CRITICAL_POINT['pressure'])
        factor = (log_p - log_p1) / (log_p2 - log_p1)

        # Calculate specific volumes using logarithmic interpolation
        log_v_liquid = math.log(REFERENCE_POINT['specific_volume_liquid']) + \
                      factor * (math.log(CRITICAL_POINT['specific_volume']) - math.log(REFERENCE_POINT['specific_volume_liquid']))
        
        log_v_vapor = math.log(REFERENCE_POINT['specific_volume_vapor']) + \
                     factor * (math.log(CRITICAL_POINT['specific_volume']) - math.log(REFERENCE_POINT['specific_volume_vapor']))

        return jsonify({
            "specific_volume_liquid": round(math.exp(log_v_liquid), 4),
            "specific_volume_vapor": round(math.exp(log_v_vapor), 4)
        })

    except (ValueError, TypeError):
        return jsonify({"error": "Invalid pressure value"}), 400

if __name__ == '__main__':
    app.run(debug=True)