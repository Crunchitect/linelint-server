from thin import thin
from get_code import main
from flask import Flask, request
from flask_cors import CORS
from pycloudflared import try_cloudflare

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

url = try_cloudflare(port=5000).tunnel

start = (0, 0)
end = (0, 0)

@app.route("/process")
def hello_world():
    thin()
    main(start, end)
    with open('output.txt', 'r') as f:
        contents = f.read()
    return f'{contents}'


@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save('map.png')
    return "OK!"

@app.route("/config")
def config():
    global start, end
    sx = int(request.args.get('sx'))
    sy = int(request.args.get('sy'))
    ex = int(request.args.get('ex'))
    ey = int(request.args.get('ey'))

    start = (sx, sy)
    end = (ex, ey)
    return "Ok!"
