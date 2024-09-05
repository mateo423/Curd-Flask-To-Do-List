from flask import Blueprint, request, render_template, redirect, url_for
from src.db.pymysql import Basedata

tasks = Blueprint("tasks", __name__, template_folder="templates")
db = Basedata(host="localhost", user="root", password="", db="to-do-list")

default_tasks = [
    {
        "id_task": 1,
        "title": "Comprar alimentos",
        "description": "Comprar leche, huevos, pan, etc",
    },
    {
        "id_task": 2,
        "title": "Comprar ropa",
        "description": "Comprar ropa para la fiesta",
    },
    {
        "id_task": 3,
        "title": "Comprar bebidas",
        "description": "Comprar bebidas para la fiesta",
    },
]


# Read all tasks
@tasks.route("/")
def get_tasks():
    all_tasks = db.get_all_tasks()
    print(f"all_tasks: {all_tasks}")
    if not all_tasks:
        print("Inserting default tasks")
        for task in default_tasks:
            db.add_task(task["title"], task["description"])
        all_tasks = db.get_all_tasks()
        print(f"all_tasks after inserting default tasks: {all_tasks}")
    return render_template("index.html", tasks=all_tasks)


# Create a new task
@tasks.route("/add_tasks", methods=["GET", "POST"])
def add_tasks():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        db.add_task(title, description)
        return redirect(url_for("tasks.get_tasks"))
    return render_template("add_task.html")


# Update a task
@tasks.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        db.update_task(task_id, title, description)
        return redirect(url_for("tasks.get_tasks"))
    task = db.get_task_by_id(task_id)
    if task:
        task = {
            "id_task": task["id_task"],
            "title": task["title"],
            "description": task["description"],
        }
    return render_template("edit_task.html", task=task)


# Delete a task
@tasks.route("/delete/<int:task_id>", methods=["GET", "POST"])
def delete_task(task_id):
    db.delete_task(task_id)
    return redirect(url_for("tasks.get_tasks"))
