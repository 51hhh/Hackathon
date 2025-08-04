from flask import Flask, render_template, send_from_directory
from .device import device_bp
from .calendar import calendar_bp
from .summary import summary_bp
import os

app = Flask(__name__)

# Register blueprints
app.register_blueprint(device_bp, url_prefix='/api')
app.register_blueprint(calendar_bp, url_prefix='/api')
app.register_blueprint(summary_bp, url_prefix='/api')

# Serve mp3 files from the 'mp3' directory
@app.route('/mp3/<path:filename>')
def serve_mp3(filename):
    return send_from_directory('mp3', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calendar')
def calendar_view():
    return render_template('calendar.html')

@app.route('/summary')
def summary_view():
    return render_template('summary.html')

@app.route('/summary/<string:filename>') # Change to string:filename
def summary_detail_view(filename):
    return render_template('summary_detail.html', filename=filename)

if __name__ == '__main__':
    app.run(debug=True)
