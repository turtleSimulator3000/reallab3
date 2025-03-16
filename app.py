from flask import Flask, render_template, request, send_file, redirect, jsonify, Response
import uuid
app = Flask(__name__)
from static.games.minesweeper.minesweeper import MineSweeper
import redis
R = redis.StrictRedis()
try: R.ping()
except:
    print('ERROR: No server')
    R = None
users = {
    'help': 'me'
}
runningGames = dict()

@app.route("/login", methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        mode = request.form.get("mode")
        print('mode')
        if mode == 'login':
            if username in users and users[username] == password:
                return 'Welcome ' + username
            else: 
                return 'Incorrect credentials'
        elif mode == 'register':
            users.update({username: password})
            return 'Welcome new ' + username

    else:
        return send_file('static/login.html')

@app.route("/games/minesweeper", methods = ['GET', 'POST'])
def mine():
    
    return send_file('static/games/minesweeper/intro.html')

@app.route("/games/minesweeper/game", methods = ['GET', 'POST'])
def mineGame():
    
    return send_file('static/games/minesweeper/minesweeper.html')
@app.errorhandler(404)
def notFound(error):
    return send_file('static/404.html'),404

@app.route('/<game>/game', methods = ['GET','PUT','POST'])
def indexGame(game):
    if request.method == 'GET' and 'id' not in request.args: return send_file(f'static/games/{game}/intro.html')
    if request.method == 'POST': 
            if 'rows' not in request.form or 'cols' not in request.form or 'name' not in request.form: return "ERROR: missing arguments"
            rows = int(request.form.get('rows'))
            cols = int(request.form.get('cols'))
            name = request.form.get('name')
            Minegame = MineSweeper(rows,cols)
            id = uuid.uuid1()
            runningGames[str(id)] = Minegame
            send_file(f'static/games/{game}/{game}.html')
            #R.publish(id,"id made")
            return redirect(f'/{game}/game?id={id}&rows={rows}&cols={cols}&name={name}')
            return send_file(f'static/games/{game}/{game}.html')
    if 'id' not in request.args:
        return "Error: No game id"
    ID = request.args.get('id')
    if ID in runningGames.keys() :
        if request.method == 'GET': return send_file(f'static/games/{game}/{game}.html')
        
        else:
            currentGame = runningGames[ID]
            jsonData = request.get_json()
            if jsonData.get("action") == 'board':
                boar = {

                }
                for i in range(currentGame.rows):
                    for j in range(currentGame.cols):
                        boar[(i,j)] = currentGame.getSpace(i,j)
                return jsonify({"board": boar,"gameOver": currentGame.gameOver, "score": currentGame.score})
            elif jsonData.get("action") == 'pick':
                row = int(jsonData.get("row"))
                col = int(jsonData.get("col"))
                flag = jsonData.get("flag")
                over = currentGame.gameOver
                #id =request.args("id")
                
                #print(currentGame.pickSpace(row,col,flag))
                print("OVER: " + str(over))
                return jsonify({"space": currentGame.pickSpace(row,col,flag), 'gameOver': over})
            elif jsonData.get("action") == 'space':
                row = int(jsonData.get("row"))
                col = int(jsonData.get("col"))
                over = currentGame.gameOver
                return jsonify({'space': currentGame.getSpace(row,col),'gameOver': over})
            elif jsonData.get("action") == 'name':
                return jsonify({'name': currentGame.name})
            elif jsonData.get("action") == 'score':
                return jsonify({'score': currentGame.score})
            elif jsonData.get("action") == 'time':
                #print(currentGame.time)
                return jsonify({'time': currentGame.time})
                   

    else:
        print(runningGames.keys())
        return "Error: invalid game id"
"""
@app.route("/stream")
def stream():
    def emitter():
        pubsub = R.pubsub()
        pubsub.subscribe(request.args('id'))
        for message in pubsub.listen():
            message = message['data']
            yield message
    return Response(emitter(),mimetype='text/event-stream')
"""

"""
@app.route('/<game>/game', methods = ['POST'])
def indexGame(game):
    rows = request.args.get('rows')
    cols = request.args.get('cols')
    name = request.args.get('name')
    game = MineSweeper(rows,cols)
    id = uuid.uuid()
    runningGames[id] = game
    redirect(f'/{game}/game?id = {id}')

    
    return send_file('static/games/' + game + "/game")
"""  




app.run(port=8080)