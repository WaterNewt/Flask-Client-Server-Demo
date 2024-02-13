import bson
import json
import random
from flask import Flask, request

app = Flask(__name__)
db = 'bson'

if db == 'bson':
    WORLD_FILE = 'world.bson'

    def write(obj, file=WORLD_FILE):
        with open(file, 'wb') as f:
            f.write(bson.dumps(obj))
    def read(file=WORLD_FILE):
        with open(file, 'rb') as f:
            return bson.loads(f.read())
elif db == 'json':
    WORLD_FILE = 'world.json'

    def write(obj, file=WORLD_FILE):
        with open(file, 'w') as f:
            json.dump(obj, f)
    def read(file=WORLD_FILE):
        with open(file, 'rb') as f:
            return json.load(f)
    

def rand_color() -> list:return [random.randint(0, 255) for i in range(3)]

@app.route("/getworld")
def getworld():
    return read()
    
@app.route("/setpos", methods=['POST'])
def setpos():
    if 'username' in request.args:
        username = request.args.get('username')
    else: return {"success": False, "status": 400, "message": "Specify username as query param"}, 400
    pos = request.get_json()
    world = read()
    try:
        world['players'][username]['pos'] = pos
    except KeyError:
        return {"success": False, "status": 400, "message": "User does not exist"}, 401
    write(world)
    return {"success": True, "status": 200}, 200

@app.route('/getplayer', methods=['GET'])
def getplayer():
    if 'username' in request.args:
        username = request.args.get('username')
    else: return {"success": False, "status": 400, "message": "Specify username as query param"}, 400
    world = read()
    try:
        return world['players'][username]
    except KeyError:
        return {"success": False, "status": 400, "message": "User does not exist"}, 401
    
@app.route('/log/<log>', methods=['GET'])
def log(log):
    if 'username' in request.args: username = request.args.get('username')
    else: return {"success": False, "status": 400, "message": "Specify username as query param"}, 400
    world = read()
    if log == 'true' and world['players'][username]['logged'][0] == True:
        return {"success": False, "status": 409, "message": "Another session is open in same user."}, 409
    if log == 'true':
        log = True
    elif log == 'false':
        log = False
    else:
        return {"success": False, "status": 400}, 400
    try:
        world['players'][username]['logged'] = [log, request.remote_addr]
    except KeyError as e:
        return {"success": False, "status": 401, "message": "User does not exist"}, 401
    write(world)
    return {"success": True, "status": 200}, 200

@app.route('/newuser', methods=['POST'])
def newuser():
    if not all(['username' in request.get_json(), 'pos' in request.get_json()]):
        return {"success": False, "status": 400, "message": "Missing query params"}, 400
    world = read()
    if request.get_json()['username'] in world['players']:
        return {"success": False, "status": 400, "message": "User already exists"}, 400
    new_user = {"pos": request.get_json()['pos'], "color": rand_color(), "logged": [False, request.remote_addr]}
    world['players'][request.get_json()['username']] = new_user
    write(world)
    return new_user, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)