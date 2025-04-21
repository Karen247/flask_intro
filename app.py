from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    
db = SQLAlchemy(app)

# row of data
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(100), nullable = False)
    complete = db.Column(db.Integer, default = 0)
    created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task: {self.id}"
    
with app.app_context():
    db.create_all()

# Home page
@app.route("/", methods=["POST","GET"])
def index():
    # Add a Task
    if request.method == "POST":
        current_task = request.form['content']
        new_task = Task(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    
    # See all current Tasks
    else:
        tasks = Task.query.order_by(Task.created).all()
        return render_template("index.html", tasks=tasks)

# Delete a Task
@app.route("/delete/<int:id>")
def delete(id: int):
    delete_task = Task.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"ERROR: {e}"

# Update a Task
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id: int):
    update_task = Task.query.get_or_404(id)
    if request.method == "POST":
        update_task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"ERROR: {e}"
    else:
        return render_template('update.html', task = update_task)



if __name__=="__main__":
    app.run(debug=True)