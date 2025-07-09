"""Flask server for emotion detection web application."""

from flask import Flask, request, render_template, jsonify
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/emotionDetector', methods=['GET'])
def emotion_detector_route():
    """
    Handle GET requests for emotion detection.
    Returns a JSON response containing emotion analysis results,
    or an error message for invalid input.
    """
    text_to_analyze = request.args.get('textToAnalyze', '')
    if not text_to_analyze:
        return jsonify({'result': "Invalid text! Please try again!"})
    result = emotion_detector(text_to_analyze)
    if result.get('dominant_emotion') is None:
        output_message = "Invalid text! Please try again!"
    else:
        output_message = (
            f"For the given statement, the system response is 'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, 'fear': {result['fear']}, "
            f"'joy': {result['joy']} and 'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )
    return jsonify({'result': output_message})

@app.errorhandler(404)
def api_not_found(_error):
    """Return a JSON 404 error for invalid endpoints."""
    return jsonify({"message": "API not found"}), 404

@app.errorhandler(Exception)
def handle_exception(error):
    """Return a JSON 500 error for unhandled exceptions."""
    return jsonify({"message": str(error)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    