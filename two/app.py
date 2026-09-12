from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

# Mock status for distraction check
is_distracted = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-status')
def check_status():
    global is_distracted
    # Orikkal distraction kandethiyaal (e.g., random trigger for demo)
    # Real-world-il ithu OpenCV / Browser history vechu connect cheyyam.
    is_distracted = random.choice([True, False])
    return jsonify({'distracted': is_distracted})

if __name__ == '__main__':
    app.run(debug=True, port=5000)