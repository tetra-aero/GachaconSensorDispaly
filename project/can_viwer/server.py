from bottle import Bottle,route,template,static_file,request,HTTPResponse
import json

app = Bottle()
app.config['autojson'] = True


@app.route("/")
def index():
    return template('index')

@app.route('/static/<filename>')
def static(filename):
    return static_file(filename, root='./static')

@app.route('/js/<filename>')
def static(filename):
    return static_file(filename, root='./js')

@app.route('/json')
def static():
    with open('/mnt/ramdisk/output.json', 'r') as f:
        jdata = json.load(f)
        #print(jdata)
        #response.content_type = 'application/json'
    return  json.dumps(jdata) 

@app.route('/jsonv1')
def static():
    with open('/mnt/ramdisk/outputv1.json', 'r') as f:
        jdatav1 = json.load(f)
        #print(jdata)
        #response.content_type = 'application/json'
    return  json.dumps(jdatav1) 

@app.route('/css/<filename>')
def static(filename):
    return static_file(filename, root='./css')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80", debug=True)

