from database import db_session, init_db
from models import User, KerbJSONEncoder, Transaction
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS, cross_origin

init_db()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/kerbholz": {"origins": "localhost"}})

app.json_encoder = KerbJSONEncoder

@app.route('/')
def hello_world():
    # return render_template("booklist.html")
    return 'Hello, World!'

@app.route('/users/list')
def list_users():
    return jsonify(User.query.all())

@app.route('/users/add', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        try:
            nickname = request.form['nickname']
        except:
            nickname = None
        try:
            email = request.form['email']
        except:
            email = None
        try:
            active = bool(request.form['active'])
        except:
            active = False
        try:
            balance = int(request.form['balance'])
        except:
            balance = 0
        try:
            limit = int(request.form['limit'])
        except:
            limit = 0
    elif request.method == 'GET':
        try:
            nickname = request.args.get('nickname', None)
        except:
            nickname = None
        try:
            email = request.args.get('email', None)
        except:
            email = None
        try:
            active = bool(request.args.get('active', None))
        except:
            active = False
        try:
            balance = int(request.args.get('balance', None))
        except:
            balance = 0
        try:
            limit = int(request.args.get('limit', None))
        except:
            limit = 0
    else:
        nickname = None
        email = None
        active = False
        balance = 0
        limit = 0

    if nickname == None:
        result = 'no nickname'
    elif email == None:
        result = 'no email'
    else:
        u = User(nickname, email, active, balance, limit)
        try:
            db_session.add(u)
            db_session.commit()
            result = 'success ' + str(u)
        except Exception as e:
            result = 'failed: ' + str(e)

    return result

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
