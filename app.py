from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
   id = db.Column(db.Integer , primary_key = True)
   text = db.Column(db.String(100) , nullable = False)
   date = db.Column(db.DateTime , default = datetime.utcnow)

   def __repr__(self):
      return '<Task %r>' % self.id


@app.route('/',methods = ['GET','POST'])
def index():
   if request.method == 'POST':
      task_content = request.form['task']
      task = Todo(text = task_content)

      try:
         db.session.add(task)
         db.session.commit()
         return redirect('/')

      except:
         return 'there was an issue adding your task'

   else:
      tasks = Todo.query.order_by(Todo.date).all()
      return render_template('index.html',tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
   todo_tobe_deleted = Todo.query.get_or_404(id)

   try:
      db.session.delete(todo_tobe_deleted)
      db.session.commit()
      return redirect('/')

   except:
      return'soemthing went wrong'


@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
   task = Todo.query.get_or_404(id)
   if request.method == 'GET':
      try:
         return render_template('update.html',task=task)
      except:
         return 'Soemthing didn\'t work well'
   else:
      try:
         task.text = request.form['updatedtask']
         db.session.commit()
         return redirect('/')
      except:
         return 'there is some problem updating'
      

   

if __name__ == "__main__":
    app.run(debug = True)