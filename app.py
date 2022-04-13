from urllib.robotparser import RequestRate
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from matplotlib.pyplot import title
import mysql.connector

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


database = mysql.connector.connect(
    host="localhost",
    user="root",
    password='Lahari@2001'
)
cursor = database.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS Todo')
cursor.execute('USE Todo')
lists = "CREATE TABLE IF NOT EXISTS lists (id int primary key auto_increment, title varchar(100), items varchar(400));"
cursor.execute(lists)

@app.route("/")
def index():
    return render_template(["home.html","style.css"])

@app.route("/list")
def list():
    cursor.execute(f"SELECT * FROM lists")
    data = cursor.fetchall()
    return render_template("list.html", todo_list=data)

@app.route("/addList", methods=["POST"])
def addList():
    title = request.form.get("title")
    items = request.form.get("items")
    cursor.execute(f"INSERT INTO lists(title, items) VALUES ('{title}', '{items}');")
    database.commit()
    print(f'List {title} created/updated Successfully!')
    return redirect(url_for("list"))


@app.route("/deleteList/<int:todo_id>")
def deleteList(todo_id):
    cursor.execute(f'SELECT * FROM lists WHERE id = {todo_id};')
    data = cursor.fetchall()
    if not data:
        print('No such list found!')
    else:
        cursor.execute(f"DELETE FROM lists WHERE id ={todo_id};")
        print('List Deleted')
        database.commit()
    return redirect(url_for("list"))

@app.route("/searchList", methods = ["POST"])
def searchList():
    title = request.form.get("title")
    cursor.execute(f"SELECT * FROM lists WHERE title = '{title}';")
    data = cursor.fetchall()
    return render_template("list.html", todo_list=data)

@app.route("/updateList/<int:todo_id>", methods = ["POST"])
def updateList(todo_id):
    var = request.form.get("list")
    sql = "UPDATE lists SET title = %s WHERE id = %s"
    val = (var, todo_id)
    cursor.execute(sql, val)
    database.commit()
    return redirect(url_for("list"))


@app.route("/authenticate",methods=["POST"])
def authenticate():
    return render_template("temp.html")

@app.route("/task")
def task():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')



@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("task"))




@app.route("/search", methods = ["POST"])
def search():
    name = request.form.get("name")
    variable = Todo.query.filter(Todo.title.contains(name))
    return render_template("base.html", todo_list=variable)


@app.route("/search_by_hash", methods = ["POST"])
def search_by_hash():
    name = request.form.get("name")
    hash = Todo.query.filter(Todo.title.contains(name))
    return render_template("base.html", todo_list=hash)



@app.route("/mac/<int:todo_id>")
def mac(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("task"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("task"))

#@@app.route("/updateTask/<int:todo_id>", methods = ["POST"])
@app.route("/updateTask/<int:todo_id>", methods=["POST"])
def updateTask(todo_id):
    delete(todo_id)
    title = request.form.get("task")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("task"))
    # var = request.form.get("task")
    # sql = "UPDATE task SET title = %s WHERE id = %s"
    # val = (var,todo_id)
    # cursor.execute(sql, val)
    # db.session.commit()
    # return redirect(url_for("task"))




if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
