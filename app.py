from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create a Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy database instance
db = SQLAlchemy(app)

# Define a Todo model for tasks
class Todo(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    done = db.Column(db.Boolean)

# Define the route for the home page, which displays the to-do list
@app.route('/')
def home():
    # Retrieve all tasks from the database
    todo_list = Todo.query.all()
    # Render the home page template with the to-do list
    return render_template("index.html", todo_list=todo_list)

# Define the route for adding a new task
@app.route('/add', methods=['POST'])
def add():
    # Retrieve the task name from the form submission
    name = request.form.get("name")
    # Create a new task with the given name and set 'done' to False
    new_task = Todo(name=name, done=False)
    # Add the new task to the database
    db.session.add(new_task)
    # Commit the changes to the database
    db.session.commit()
    # Redirect to the home page after adding the task
    return redirect(url_for("home"))

# Define the route for updating the status of a task
@app.route('/update/<int:task_id>')
def update(task_id):
    # Retrieve the task with the specified task_id from the database
    todo = Todo.query.get(task_id)
    # Toggle the 'done' status of the task
    todo.done = not todo.done
    # Commit the changes to the database
    db.session.commit()
    # Redirect to the home page after updating the task
    return redirect(url_for('home'))

# Define the route for deleting a task
@app.route('/delete/<int:task_id>')
def delete(task_id):
    # Retrieve the task with the specified task_id from the database
    todo = Todo.query.get(task_id)
    # Delete the task from the database
    db.session.delete(todo)
    # Commit the changes to the database
    db.session.commit()
    # Redirect to the home page after deleting the task
    return redirect(url_for('home'))

# Run the Flask application if the script is executed
if __name__ == "__main__":
    app.run(debug=True)
