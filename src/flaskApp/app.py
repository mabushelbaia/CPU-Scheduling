from flask import Flask, render_template
import time

app = Flask(__name__)

@app.route("/")
def index():
    # Fetch data from the CPU
    data = get_cpu_data()
    return render_template("index.html", data=data)

def get_cpu_data():
    # Simulating a CPU that generates data over time
    data = {'time': time.time(), 'processes': [{'name': 'Process 1', 'state': 'Running'}, {'name': 'Process 2', 'state': 'Waiting'}]}
    return data

if __name__ == "__main__":
    app.run(debug=True)
