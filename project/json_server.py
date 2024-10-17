from bottle import Bottle,route,template,static_file,request,HTTPResponse
import json
import time

with open('config.json', 'r') as f:
    config = json.load(f)

app = Bottle()
app.config['autojson'] = True
jdata = {}
@app.route("/")
def index():
    for test in range(5):
        try:
            with open(config['can_json']['json'], 'r') as f:
                jdata = json.load(f)
            return json.dumps(jdata, indent=4)
        except Exception:
            time.sleep(0.1)
            #return " "#json.dumps(jdata)
@app.route("/get")
def GET():
    for test in range(5):
        try:
            with open(config['can_json']['json'], 'r') as f:
                jdata = json.load(f)
            return json.dumps(jdata, indent=4)
        except Exception:
            time.sleep(0.1)
            #return " "#json.dumps(jdata)
@app.route('/post', method='POST')
def POST():
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="1001", debug=True)