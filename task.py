import streamlit as st
import csv
from datetime import datetime
import os

def task1_page():

 # File setup
 TASK_FILE = 'tasks.csv'

# Ensure CSV file exists and has proper headers
 def initialize_csv():
     if not os.path.exists(TASK_FILE):
         with open(TASK_FILE, mode='w', newline='') as file:
             writer = csv.DictWriter(file, fieldnames=['name', 'due_date', 'description', 'priority'])
             writer.writeheader()

 # Load tasks from CSV
 def load_tasks():
     tasks = []
     with open(TASK_FILE, mode='r', newline='') as file:
         reader = csv.DictReader(file)
         tasks = [row for row in reader]
     return tasks

 # Save a new task to CSV
 def save_task(task):
     with open(TASK_FILE, mode='a', newline='') as file:
         writer = csv.DictWriter(file, fieldnames=['name', 'due_date', 'description', 'priority'])
         writer.writerow(task)

 # Rewrite the entire CSV to update tasks
 def update_tasks(tasks):
     with open(TASK_FILE, mode='w', newline='') as file:
         writer = csv.DictWriter(file, fieldnames=['name', 'due_date', 'description', 'priority'])
         writer.writeheader()
         for task in tasks:
             writer.writerow(task)




 def add_task():
     task = {
         'name': st.session_state.get('Taskname', ''),
         'due_date': st.session_state.get('Due Date', datetime.today()).strftime('%Y-%m-%d'),
         'description': st.session_state.get('Description', ''),
         'priority': st.session_state.get('Priority', '1')
     }
     st.session_state.tasks.append(task)
     save_task(task)
     st.success('Task added successfully!')
     # Clear the inputs after adding the task
     for key in ['Taskname', 'Due Date', 'Description', 'Priority']:
         if key in st.session_state:
             del st.session_state[key]
            
 # Update a task
 def edit_task(idx):
     task = st.session_state.tasks[idx]
     with st.form(f"form_edit_{idx}"):
         new_name = st.text_input("Task Name", value=task['name'])
         new_due_date = st.date_input("Due Date", value=datetime.strptime(task['due_date'], '%Y-%m-%d'))
         new_description = st.text_area("Description", value=task['description'])
         new_priority = st.selectbox("Priority", ["1", "2", "3"], index=int(task['priority']) - 1)

         if st.form_submit_button("Update Task"):
             updated_task = {
                 'name': new_name,
                 'due_date': new_due_date.strftime('%Y-%m-%d'),
                 'description': new_description,
                 'priority': new_priority
             }
             st.session_state.tasks[idx] = updated_task
             update_tasks(st.session_state.tasks)
             st.success('Task updated successfully!')


 def delete_task(idx):
     del st.session_state.tasks[idx]
     update_tasks(st.session_state.tasks)
     st.experimental_rerun()
 initialize_csv()


 if 'logged_in' not in st.session_state:
     st.session_state.logged_in = False
 if 'tasks' not in st.session_state:
     st.session_state.tasks = load_tasks()
 if 'new_task' not in st.session_state:
     st.session_state.new_task = False

 # Define login function
 def login():
     st.title("To-Do APP")
     st.header("Login Page")
     username = st.text_input("Username", key='username')
     password = st.text_input("Password", type="password", key='password')
     if st.button("Login"):
         if username == "vivek" and password == "vivek123":  
             st.session_state.logged_in = True
         else:
             st.error("Invalid username or password")


 def main_app():
     st.header("ToDo")
     if st.button("New Task"):
         st.session_state.new_task = not st.session_state.new_task
 
     with st.sidebar:
         if st.session_state.get('new_task', False):
             st.header("Add a New Task")
             st.text_input("Enter Task", key='Taskname')
             st.date_input("Due Date", key='Due Date', value=datetime.today())
             st.text_area("Description", height=200, key='Description')
             st.selectbox("Choose your Priority", ("1", "2", "3"), key='Priority')
             if st.button("Submit"):
                 add_task()

     if st.session_state.tasks:
         for idx, task in enumerate(st.session_state.tasks):
             st.subheader(f"Task {idx + 1}: {task['name']}")
             st.write(f"Due Date: {task['due_date']}")
             st.write(f"Description: {task['description']}")
             st.write(f"Priority: {task['priority']}")

             col1, col2 = st.columns(2)
             with col1:
                 if st.button("Edit", key=f'Edit_Task_{idx}'):
                     edit_task(idx)
             with col2:
                 if st.button("Delete", key=f'Delete_Task_{idx}'):
                     delete_task(idx)
             st.write("---")

 # Control flow based on login
 if not st.session_state.logged_in:
     login()
 else:
     main_app()