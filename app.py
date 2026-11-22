
from flask import Flask, render_template_string, request, jsonify
import math

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>BMI Calculator | Premium</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont,
                         "SF Pro Display", "Helvetica Neue", sans-serif;

            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 30px 18px;
            color: #1d1d1f;

            background:
                radial-gradient(circle at 10% 15%, #dbeafe 0%, transparent 35%),
                radial-gradient(circle at 90% 85%, #e9d5ff 0%, transparent 35%),
                linear-gradient(135deg, #f5f7ff, #e9edfa, #f5f0ff);
        }

        .container {
            width: 100%;
            max-width: 460px;
            padding: 38px;

            background: rgba(255, 255, 255, 0.48);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);

            border: 1px solid rgba(255, 255, 255, 0.8);
            border-radius: 30px;

            box-shadow:
                0 25px 70px rgba(31, 38, 135, 0.12),
                inset 0 1px 1px rgba(255,255,255,0.8);
        }

        .header {
            text-align: center;
            margin-bottom: 32px;
        }

        .header .icon {
            width: 75px;
            height: 75px;
            margin: 0 auto 18px;

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 36px;
            background: rgba(255,255,255,0.7);
            border: 1px solid white;
            border-radius: 23px;

            box-shadow: 0 10px 25px rgba(80,90,150,0.1);
        }

        .header h1 {
            font-size: 32px;
            font-weight: 750;
            letter-spacing: -1.3px;
            color: #171923;
            margin-bottom: 9px;
        }

        .header p {
            font-size: 14px;
            color: #777d91;
        }

        label {
            display: block;
            margin: 19px 0 9px;
            font-size: 13px;
            font-weight: 650;
            color: #42475a;
        }

        input, select {
            width: 100%;
            padding: 15px 16px;

            border: 1px solid rgba(255,255,255,0.9);
            border-radius: 14px;

            background: rgba(255,255,255,0.55);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);

            color: #202332;
            font-size: 15px;
            font-family: inherit;

            outline: none;
            transition: all 0.25s ease;

            box-shadow: inset 0 1px 3px rgba(0,0,0,0.025);
        }

        input::placeholder {
            color: #a0a5b4;
        }

        input:focus, select:focus {
            border-color: #8b91ff;
            background: rgba(255,255,255,0.85);
            box-shadow: 0 0 0 4px rgba(99,102,241,0.11);
        }

        select {
            cursor: pointer;
        }

        select option {
            background: white;
            color: #202332;
        }

        .height-fields {
            display: flex;
            gap: 12px;
        }

        .height-fields div {
            flex: 1;
        }

        button {
            width: 100%;
            padding: 16px;
            margin-top: 27px;

            border: none;
            border-radius: 15px;

            background: linear-gradient(135deg, #6767ee, #8c69ed);
            color: white;

            font-family: inherit;
            font-size: 16px;
            font-weight: 650;
            letter-spacing: -0.2px;

            cursor: pointer;
            box-shadow: 0 9px 22px rgba(104,101,235,0.25);

            transition: all 0.25s ease;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 13px 28px rgba(104,101,235,0.32);
        }

        button:active {
            transform: scale(0.98);
        }

        button:disabled {
            opacity: 0.6;
            cursor: wait;
        }

        #result {
            display: none;
            margin-top: 25px;
            padding: 25px 20px;

            text-align: center;

            background: rgba(255,255,255,0.65);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);

            border: 1px solid rgba(255,255,255,0.9);
            border-radius: 22px;

            box-shadow: 0 12px 30px rgba(31,38,135,0.07);
            animation: appear 0.4s ease;
        }

        #result h2 {
            font-size: 17px;
            font-weight: 650;
            color: #50556a;
        }

        .bmi-number {
            font-size: 58px;
            font-weight: 750;
            letter-spacing: -2px;
            margin: 13px 0;
            color: #6767ee;
        }

        .category {
            font-size: 17px;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .note {
            font-size: 13px;
            line-height: 1.7;
            color: #777d91;
            margin-top: 12px;
        }

        #error {
            display: none;
            margin-top: 15px;
            padding: 12px;
            color: #c24141;
            background: rgba(255,230,230,0.7);
            border-radius: 12px;
            font-size: 13px;
            text-align: center;
        }

        .footer {
            text-align: center;
            color: #999daf;
            font-size: 12px;
            margin-top: 25px;
        }

        @keyframes appear {
            from {
                opacity: 0;
                transform: translateY(10px);
            }

            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @media(max-width: 480px) {
            .container {
                padding: 25px 21px;
                border-radius: 25px;
            }

            .header h1 {
                font-size: 28px;
            }

            .bmi-number {
                font-size: 50px;
            }
        }

        @media(prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
</head>

<body>

<div class="container">

    <div class="header">
        <div class="icon">⚖️</div>
        <h1>BMI Calculator</h1>
        <p>Calculate your Body Mass Index</p>
    </div>

    <form id="bmiForm">

        <label for="age">Age (years)</label>
        <input
            type="number"
            id="age"
            min="2"
            max="120"
            step="1"
            placeholder="Enter your age"
            required
        >

        <label for="unit">Measurement Unit</label>

        <select id="unit" onchange="changeUnit()">
            <option value="metric">Metric (kg / cm)</option>
            <option value="imperial">Imperial (lb / ft / in)</option>
        </select>

        <label for="weight">
            Weight (<span id="weightUnit">kg</span>)
        </label>

        <input
            type="number"
            id="weight"
            min="0.1"
            step="any"
            placeholder="Enter your weight"
            required
        >

        <div id="metricHeight">

            <label for="heightCm">Height (cm)</label>

            <input
                type="number"
                id="heightCm"
                min="1"
                max="300"
                step="any"
                placeholder="Enter your height"
                required
            >

        </div>

        <div id="imperialHeight" style="display:none;">

            <label>Height</label>

            <div class="height-fields">

                <div>
                    <input
                        type="number"
                        id="heightFt"
                        min="0"
                        max="8"
                        step="1"
                        placeholder="Feet"
                    >
                </div>

                <div>
                    <input
                        type="number"
                        id="heightIn"
                        min="0"
                        max="11.99"
                        step="any"
                        placeholder="Inches"
                    >
                </div>

            </div>

        </div>

        <button type="submit" id="calculateBtn">
            Calculate BMI
        </button>

    </form>

    <div id="error" role="alert"></div>

    <div id="result" aria-live="polite">

        <h2>Your BMI Result</h2>

        <div class="bmi-number" id="bmiValue"></div>

        <div class="category" id="category"></div>

        <p class="note" id="ageContext"></p>

        <p class="note" id="advice"></p>

    </div>

    <div class="footer">
        BMI Calculator | Python Flask Project
    </div>

</div>

<script>

function changeUnit() {

    const unit = document.getElementById("unit").value;

    document.getElementById("weightUnit").textContent =
        unit === "metric" ? "kg" : "lb";

    document.getElementById("metricHeight").style.display =
        unit === "metric" ? "block" : "none";

    document.getElementById("imperialHeight").style.display =
        unit === "imperial" ? "block" : "none";

    document.getElementById("heightCm").required =
        unit === "metric";

    document.getElementById("heightFt").required =
        unit === "imperial";

    document.getElementById("heightIn").required = false;

    document.getElementById("result").style.display = "none";
    document.getElementById("error").style.display = "none";
}


document.getElementById("bmiForm").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const button = document.getElementById("calculateBtn");
        const error = document.getElementById("error");
        const result = document.getElementById("result");

        error.style.display = "none";
        result.style.display = "none";

        button.disabled = true;
        button.textContent = "Calculating...";

        const unit = document.getElementById("unit").value;

        const data = {
            age: document.getElementById("age").value,
            weight: document.getElementById("weight").value,
            unit: unit
        };

        if (unit === "metric") {

            data.height_cm =
                document.getElementById("heightCm").value;

        } else {

            data.height_ft =
                document.getElementById("heightFt").value || 0;

            data.height_in =
                document.getElementById("heightIn").value || 0;
        }

        try {

            const response = await fetch("/calculate", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)

            });

            const output = await response.json();

            if (!response.ok) {
                throw new Error(
                    output.error || "Calculation failed."
                );
            }

            document.getElementById("bmiValue").textContent =
                output.bmi;

            document.getElementById("category").textContent =
                output.category;

            document.getElementById("category").style.color =
                output.color;

            document.getElementById("ageContext").textContent =
                output.age_context;

            document.getElementById("advice").textContent =
                output.advice;

            result.style.display = "block";

        } catch (err) {

            error.textContent = err.message;
            error.style.display = "block";

        } finally {

            button.disabled = false;
            button.textContent = "Calculate BMI";

        }

    }
);

</script>

</body>
</html>
"""


# Homepage
@app.route("/")
def home():
    return render_template_string(HTML)


# BMI Calculation API
@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.get_json(silent=True) or {}

    try:

        age = int(data.get("age", 0))
        weight = float(data.get("weight", 0))
        unit = data.get("unit", "metric")

        if age < 2 or age > 120:
            return jsonify({
                "error": "Please enter a valid age between 2 and 120."
            }), 400

        if not math.isfinite(weight) or weight <= 0:
            return jsonify({
                "error": "Weight must be greater than zero."
            }), 400

        if unit == "metric":

            height_cm = float(data.get("height_cm", 0))

            if not math.isfinite(height_cm) or not (0 < height_cm <= 300):
                return jsonify({
                    "error": "Please enter a valid height."
                }), 400

            bmi = weight / ((height_cm / 100) ** 2)

        elif unit == "imperial":

            height_ft = float(data.get("height_ft", 0))
            height_in = float(data.get("height_in", 0))

            if (
                not math.isfinite(height_ft)
                or not math.isfinite(height_in)
                or height_ft < 0
                or height_in < 0
                or height_in >= 12
            ):
                return jsonify({
                    "error": "Please enter valid feet and inches."
                }), 400

            total_inches = height_ft * 12 + height_in

            if total_inches <= 0 or total_inches > 118:
                return jsonify({
                    "error": "Please enter a valid height."
                }), 400

            bmi = (weight / (total_inches ** 2)) * 703

        else:

            return jsonify({
                "error": "Invalid measurement unit."
            }), 400

        if not math.isfinite(bmi) or bmi <= 0 or bmi > 100:
            return jsonify({
                "error": "Please check your height and weight values."
            }), 400

        bmi = round(bmi, 1)

        # Age-specific interpretation
        if age < 20:

            category = "Age-specific interpretation needed"
            color = "#6767ee"

            age_context = (
                "For children and teenagers, BMI is interpreted "
                "using age- and sex-specific growth percentiles, "
                "not adult BMI categories."
            )

            advice = (
                "This number alone cannot determine your health. "
                "A qualified healthcare professional can interpret "
                "it using the appropriate growth chart."
            )

        else:

            age_context = "Adult BMI screening result"

            if bmi < 18.5:

                category = "Below standard adult range"
                color = "#38bdf8"

            elif bmi < 25:

                category = "Standard adult range"
                color = "#30d158"

            elif bmi < 30:

                category = "Above standard adult range"
                color = "#d69e00"

            else:

                category = "High adult BMI range"
                color = "#ff453a"

            advice = (
                "BMI is a screening measure, not a diagnosis. "
                "A healthcare professional can interpret it "
                "along with other health information."
            )

        return jsonify({

            "bmi": bmi,
            "age": age,
            "age_context": age_context,
            "category": category,
            "color": color,
            "advice": advice

        })

    except (ValueError, TypeError, OverflowError):

        return jsonify({
            "error": "Please enter valid numeric values."
        }), 400


# Local development
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
