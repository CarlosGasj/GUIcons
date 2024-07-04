from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

def execute_gui_function(function_name, *args):
    cmd = ["python3", "GUI.py", function_name] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_interfaces')
def get_interfaces():
    result = execute_gui_function("get_interfaces")
    return render_template('data.html', data=result)

@app.route('/get_restconf_native')
def get_restconf_native():
    result = execute_gui_function("get_restconf_native")
    return render_template('data.html', data=result)

@app.route('/get_banner')
def get_banner():
    result = execute_gui_function("get_banner")
    return render_template('data.html', data=result)

@app.route('/set_banner', methods=['POST'])
def set_banner():
    banner = request.form['banner']
    result = execute_gui_function("put_banner", banner)
    return render_template('data.html', data=result)

@app.route('/configure_ospf', methods=['POST'])
def configure_ospf():
    idproc = request.form['idproc']
    ip = request.form['ip']
    wild = request.form['wild']
    area = request.form['area']
    result = execute_gui_function("configure_ospf", idproc, ip, wild, area)
    return render_template('data.html', data=result)

@app.route('/delete_ospf', methods=['POST'])
def delete_ospf():
    idproc = request.form['idproc']
    result = execute_gui_function("delete_ospf", idproc)
    return render_template('data.html', data=result)

@app.route('/show_ospf')
def show_ospf():
    result = execute_gui_function("show_ospf")
    return render_template('data.html', data=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
