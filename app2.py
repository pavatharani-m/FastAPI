from flask import Flask, render_template_string, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Sentiment Analysis Tool
from transformers import pipeline
sentiment_analyzer = pipeline('sentiment-analysis')

# HTML Templates for different projects
HOME_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home - Projects</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #4B0082;
        }
        a {
            display: block;
            margin: 15px 0;
            text-align: center;
            text-decoration: none;
            padding: 15px;
            background-color: #9370DB; /* Lavender */
            color: white;
            border-radius: 8px;
            transition: background-color 0.3s ease;
            font-size: 18px;
            font-weight: bold;
        }
        a:hover {
            background-color: #6a5acd; /* Dark Slate Blue */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My Projects</h1>
        <a href="/sentiment-analysis">Sentiment Analysis Tool</a>
        <a href="/image-upload">Image Upload and Filter Application</a>
        <a href="/emotion-recognition">Emotion Recognition Studio</a>
    </div>
</body>
</html>
'''

SENTIMENT_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sentiment Analysis Tool</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #4B0082;
        }
        textarea {
            width: 100%;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 16px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
        button {
            width: 100%;
            padding: 15px;
            background-color: #9370DB; /* Lavender */
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #6a5acd; /* Dark Slate Blue */
        }
        #result {
            padding: 15px;
            background-color: #f0f8ff;
            border: 1px solid #ccc;
            margin-top: 10px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sentiment Analysis Tool</h1>
        <form id="sentiment-form">
            <textarea id="input-text" rows="10" placeholder="Enter text here..."></textarea>
            <button type="submit">Analyze Sentiment</button>
        </form>
        <h2>Result</h2>
        <div id="result"></div>
    </div>
    <script>
        document.getElementById('sentiment-form').addEventListener('submit', async function(event) {
            event.preventDefault();
            const inputText = document.getElementById('input-text').value;
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: new URLSearchParams({ text: inputText })
            });
            const data = await response.json();
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `<strong>Sentiment:</strong> ${data.sentiment} <br> <strong>Confidence:</strong> ${data.confidence}%`;
        });
    </script>
</body>
</html>
'''

IMAGE_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Upload and Filter Application</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            text-align: center;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            max-width: 700px;
            width: 100%;
            margin: 0 auto;
        }
        h1 {
            margin-bottom: 20px;
            color: #4B0082;
        }
        input[type="file"] {
            display: none;
        }
        label {
            display: inline-block;
            padding: 12px 30px;
            background-color: #9370DB; /* Lavender */
            color: white;
            border-radius: 8px;
            cursor: pointer;
            margin-bottom: 20px;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        label:hover {
            background-color: #6a5acd; /* Dark Slate Blue */
        }
        canvas {
            margin-top: 20px;
            max-width: 100%;
            border-radius: 8px;
            border: 2px solid #ddd;
        }
        button {
            padding: 12px 20px;
            margin: 10px;
            border: none;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            color: white;
            background-color: #9370DB; /* Lavender */
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #6a5acd; /* Dark Slate Blue */
        }
        button:disabled {
            background-color: #ccc;
            cursor: not-allowed;
        }
        .filter-buttons {
            margin-top: 20px;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }
        .filter-buttons button {
            background-color: #9370DB; /* Lavender */
        }
        .filter-buttons button:hover {
            background-color: #6a5acd; /* Dark Slate Blue */
        }
        .reset-button {
            background-color: #ffc107;
        }
        .reset-button:hover {
            background-color: #e0a800;
        }
        .download-button {
            background-color: #17a2b8;
        }
        .download-button:hover {
            background-color: #138496;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Image Upload and Filter Application</h1>

        <label for="upload">Choose an Image</label>
        <input type="file" id="upload" accept="image/*" />

        <canvas id="canvas"></canvas>

        <div class="filter-buttons">
            <button onclick="applyFilter('grayscale')" disabled id="grayscaleBtn">Grayscale</button>
            <button onclick="applyFilter('sepia')" disabled id="sepiaBtn">Sepia</button>
            <button onclick="applyFilter('brightness')" disabled id="brightnessBtn">Brightness</button>
        </div>

        <div class="filter-buttons">
            <button onclick="resetImage()" disabled id="resetBtn" class="reset-button">Reset</button>
            <button onclick="downloadImage()" disabled id="downloadBtn" class="download-button">Download</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let originalImageData;

        document.getElementById('upload').addEventListener('change', (event) => {
            const file = event.target.files[0];
            if (file) {
                const img = new Image();
                img.onload = () => {
                    canvas.width = img.width;
                    canvas.height = img.height;
                    ctx.drawImage(img, 0, 0, img.width, img.height);
                    originalImageData = ctx.getImageData(0, 0, img.width, img.height);
                    enableButtons(true);
                };
                img.src = URL.createObjectURL(file);
            }
        });

        function resetImage() {
            ctx.putImageData(originalImageData, 0, 0);
        }

        function downloadImage() {
            const link = document.createElement('a');
            link.download = 'filtered_image.png';
            link.href = canvas.toDataURL();
            link.click();
        }

        function enableButtons(enable) {
            document.getElementById('resetBtn').disabled = !enable;
            document.getElementById('downloadBtn').disabled = !enable;
            document.getElementById('grayscaleBtn').disabled = !enable;
            document.getElementById('sepiaBtn').disabled = !enable;
            document.getElementById('brightnessBtn').disabled = !enable;
        }

        function applyFilter(type) {
            const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imgData.data;

            for (let i = 0; i < data.length; i += 4) {
                if (type === 'grayscale') {
                    const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
                    data[i] = avg;     // Red
                    data[i + 1] = avg; // Green
                    data[i + 2] = avg; // Blue
                } else if (type === 'sepia') {
                    const tr = 0.393 * data[i] + 0.769 * data[i + 1] + 0.189 * data[i + 2];
                    const tg = 0.349 * data[i] + 0.686 * data[i + 1] + 0.168 * data[i + 2];
                    const tb = 0.272 * data[i] + 0.534 * data[i + 1] + 0.131 * data[i + 2];
                    data[i] = Math.min(255, tr);     // Red
                    data[i + 1] = Math.min(255, tg); // Green
                    data[i + 2] = Math.min(255, tb); // Blue
                } else if (type === 'brightness') {
                    const brightnessFactor = 1.2; // Increase brightness by 20%
                    data[i] = Math.min(255, data[i] * brightnessFactor);     // Red
                    data[i + 1] = Math.min(255, data[i + 1] * brightnessFactor); // Green
                    data[i + 2] = Math.min(255, data[i + 2] * brightnessFactor); // Blue
                }
            }

            ctx.putImageData(imgData, 0, 0);
        }
    </script>

</body>
</html>
'''

EMOTION_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Recognition Studio</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #4B0082;
        }
        button {
            width: 100%;
            padding: 15px;
            background-color: #9370DB; /* Lavender */
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s ease;
            margin-bottom: 10px;
        }
        button:hover {
            background-color: #6a5acd; /* Dark Slate Blue */
        }
        .emotion {
            font-size: 24px;
            text-align: center;
            margin-top: 20px;
            font-weight: bold;
            color: #333;
        }
    </style>
</head>
<body>

    <div class="container">
        <h1>Emotion Recognition Studio</h1>
        <button id="startRecording">🎤 Start Recording</button>
        <button id="stopRecording" disabled>🛑 Stop Recording</button>
        <div class="emotion" id="emotionDisplay">
            <span id="emotion">Neutral</span>
        </div>
    </div>

    <script>
        let mediaRecorder;
        let audioChunks = [];
        const emotionElement = document.getElementById("emotion");
        
        async function predictEmotion(audioBlob) {
            // Simulate emotion prediction
            const emotion = ["happy", "sad", "angry", "neutral"][Math.floor(Math.random() * 4)];
            displayEmotion(emotion);
        }

        function displayEmotion(emotion) {
            emotionElement.textContent = emotion.charAt(0).toUpperCase() + emotion.slice(1);
        }

        document.getElementById("startRecording").onclick = async () => {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                await predictEmotion(audioBlob);
            };
            mediaRecorder.start();
            document.getElementById("startRecording").disabled = true;
            document.getElementById("stopRecording").disabled = false;
        };

        document.getElementById("stopRecording").onclick = () => {
            mediaRecorder.stop();
            document.getElementById("startRecording").disabled = false;
            document.getElementById("stopRecording").disabled = true;
        };
    </script>

</body>
</html>
'''

# Home route
@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

# Sentiment Analysis route
@app.route('/sentiment-analysis')
def sentiment_analysis():
    return render_template_string(SENTIMENT_TEMPLATE)

# Image Upload route
@app.route('/image-upload')
def image_upload():
    return render_template_string(IMAGE_TEMPLATE)

# Emotion Recognition route
@app.route('/emotion-recognition')
def emotion_recognition():
    return render_template_string(EMOTION_TEMPLATE)

# Route for sentiment analysis
@app.route('/analyze', methods=['POST'])
def analyze_sentiment():
    text = request.form.get('text')
    if not text or len(text.strip()) == 0:
        return jsonify({"error": "Please provide some text to analyze."})

    # Perform sentiment analysis using Hugging Face's pre-trained model
    result = sentiment_analyzer(text)[0]
    sentiment = result['label']
    confidence = round(result['score'] * 100, 2)

    return jsonify({"sentiment": sentiment, "confidence": confidence})

if __name__ == '__main__':
    app.run(debug=True)
