from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_file', methods=['POST'])
def process_file():
    file = request.files['file']
    # Process the file
    return "File processed successfully."

if __name__ == '__main__':
    app.run(debug=True)