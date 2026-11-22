from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True) or {}
    unit = data.get("unit", "metric")

    try:
        age = int(data.get("age", 0))
        if age < 2 or age > 120:
            return jsonify({"error": "Please enter a valid age between 2 and 120 years."}), 400

        weight = float(data.get("weight", 0))
        if weight <= 0:
            return jsonify({"error": "Weight must be greater than zero."}), 400

        if unit == "metric":
            height_cm = float(data.get("height_cm", 0))
            if height_cm <= 0:
                return jsonify({"error": "Height must be greater than zero."}), 400
            bmi = weight / ((height_cm / 100.0) ** 2)
        else:
            height_ft = float(data.get("height_ft", 0))
            height_in = float(data.get("height_in", 0))
            total_inches = (height_ft * 12.0) + height_in
            if total_inches <= 0:
                return jsonify({"error": "Height must be greater than zero."}), 400
            bmi = (weight / (total_inches ** 2)) * 703.0

        bmi_rounded = round(bmi, 1)

        if bmi_rounded < 18.5:
            category, color = "Underweight", "#38bdf8"
            advice = "Your BMI falls below the standard range. Consider nutrient-dense meals and strength training."
        elif bmi_rounded < 25.0:
            category, color = "Normal Weight", "#30d158"
            advice = "Your BMI is within the healthy range. Maintain balanced nutrition and regular physical activity."
        elif bmi_rounded < 30.0:
            category, color = "Overweight", "#ffd60a"
            advice = "Your BMI is slightly above the standard range. Regular cardio and mindful portioning can help."
        else:
            category, color = "Obese", "#ff453a"
            advice = "Your BMI indicates obesity. Consulting a healthcare specialist can help build a tailored wellness plan."

        if age < 20:
            age_context = f"Youth Percentile Note (Age {age})"
            advice = f"For children and teens (age {age}), BMI is interpreted using age- and sex-specific CDC/WHO growth percentiles rather than adult cutoffs."
        else:
            age_context = f"Adult WHO Standard (Age {age})"

        return jsonify({
            "bmi": bmi_rounded,
            "age": age,
            "age_context": age_context,
            "category": category,
            "color": color,
            "advice": advice
        })
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid numeric input provided."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)