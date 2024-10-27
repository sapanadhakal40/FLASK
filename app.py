from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a database model
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) :
        return f"Task {self.id}"
    
with app.app_context():
        db.create_all()
  
  #home page  
@app.route('/', methods=['POST', 'GET'])
def index():
    #add task
    if request.method == 'POST':
        current_task = request.form['content']
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Error: {e}")
            return (f"Error: {e}")
    
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template('index.html', tasks=tasks)
    
    
    #delete task
@app.route('/delete/<int:id>')
def delete_task(id: int):
       delete_task = MyTask.query.get_or_404(id)
       try:
           db.session.delete(delete_task)
           db.session.commit()
           return redirect('/')
       except Exception as e:
          
           return (f"Error: {e}")
       
   

    #update task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id: int):
    task = MyTask.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return (f"Error: {e}")
    else:
        return render_template('update.html', task=task)
    
    #complete task

if __name__ == '__main__':
   
    app.run(debug=True)
