from flask import Flask,redirect,url_for
from src.db.pymysql import Basedata
from src.routes.tasks import tasks

app = Flask(__name__)


# Database
db = Basedata(
    host="localhost",
    user="root",
    password="",
    db="to-do-list"
)

# Blueprints
app.register_blueprint(tasks, url_prefix='/tasks')

@app.route('/')
def index():
    return redirect(url_for('tasks.get_tasks'))
