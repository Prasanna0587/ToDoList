from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, name, priority=0, due_date=None, completed=False):
        self.tasks.append({
            'name': name,
            'priority': priority,
            'due_date': due_date,
            'completed': completed
        })

    def remove_task(self, name):
        self.tasks = [task for task in self.tasks if task['name'] != name]

    def mark_as_complete(self, name):
        for task in self.tasks:
            if task['name'] == name:
                task['completed'] = True
                break

    def view_all_tasks(self):
        return self.tasks

    def sort_tasks(self, key):
        if key == 'p':
            self.tasks.sort(key=lambda task: task['priority'])
        elif key == 'dd':
            self.tasks.sort(key=lambda task: task['due_date'])
        else:
            print('Invalid sort key. Try again!')

todo_list = ToDoList()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task_name']
    task_priority = int(request.form['task_priority'])
    task_due_date = request.form['task_due_date']
    if 0 <= task_priority <= 10:
        todo_list.add_task(task_name, task_priority, task_due_date)
        return jsonify({'message': 'Task added successfully'})
    else:
        return jsonify({'message': 'Priority must be between 0 and 10'})

@app.route('/sort_tasks', methods=['POST'])
def sort_tasks():
    sort_key = request.form['key']
    todo_list.sort_tasks(sort_key)
    return jsonify({'message': 'Tasks sorted successfully'})

@app.route('/complete_task', methods=['POST'])
def complete_task():
    task_name = request.form['task_name']
    todo_list.mark_as_complete(task_name)
    return jsonify({'message': 'Task marked as complete'})

@app.route('/view_all_tasks', methods=['GET'])
def view_all_tasks():
    return jsonify({'tasks': todo_list.view_all_tasks()})

if __name__ == '__main__':
    app.run(debug=True)