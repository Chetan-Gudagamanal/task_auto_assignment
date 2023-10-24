from flask import Flask
import mysql.connector as sql
from utils.common import assign_task_to_user, check_user_has_task, get_all_user_task_data, reset_all_tasks, update_task_status_complete
import os
from flask_cors import CORS, cross_origin

app= Flask(__name__)
CORS(app)

@app.route("/")
def get_data():
    all_data=get_all_user_task_data()
    return {
        'all_data':all_data, 
        'status':200
    }

@app.route("/login/<int:id>")
def login_user(id):
    # login logic...
    user_has_task=check_user_has_task(id)
    if user_has_task==False:
        res=assign_task_to_user(id)
        if res['status'] and res['status']=='success':
            if 'task_id' in res:
                return {
                    'data':{'task_id':res['task_id']}, 'login':True, 'status':200
                }
    return {
        'data':[], 'message':"Login Successful", 'status':200
    }

@app.route("/task_finish/<int:task_id>/<int:user_id>")
def task_finish_assign_new(task_id,user_id):
    update_task_status=update_task_status_complete(task_id)
    if update_task_status==True:
        res=assign_task_to_user(user_id)
        if res['status'] and res['status']=='success':
            if 'task_id' in res:
                return {
                    'data':{'task_id':res['task_id']}, 'login':True, 'status':200
                }
            else:
                return{
                    'data':{}
                }
    else:
        return{
                'data':{},'status':500
            }

@app.route("/reset_db")
def reset_db_data():
    res=reset_all_tasks()
    if res:
        return {
            'status':200
        }
    else:
        return {
            'status':200
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)