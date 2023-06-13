from flask import Flask, render_template, url_for, redirect
import random

app = Flask(__name__)

@app.route('/')
def sample_top():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)