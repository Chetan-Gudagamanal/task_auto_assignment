
import mysql.connector as sql
import os
def get_connection():
    connection=sql.connect(
        host=os.environ.get("db_host") or 'localhost',
        port=os.environ.get("db_port") or '3306',
        database=os.environ.get("db_name") or 'task_assign_db2',
        user=os.environ.get("db_user") or 'root',
        password=os.environ.get("db_password") or 'password'
    )
    return connection

def update_task_status_complete(task_id):
    try:
        connection=get_connection()
        cursor=connection.cursor(buffered=True)
        update_query=f'update Tasks set TaskStatus=1 where TaskID={task_id}'
        cursor.execute(update_query)
        connection.commit()
        return True
    except sql.DatabaseError as e:
        if connection:
            connection.rollback()
        return False
            
    finally:
        if cursor:
            cursor.close()
            
        if connection:
            connection.close()


def assign_task_to_user(id):
    try:
        connection=get_connection()
        cursor=connection.cursor(buffered=True)
        select_query=f"select TaskId from Tasks where UserId is null"
        cursor.execute(select_query)
        task_id=cursor.fetchone()
        print(task_id)
        
        
        if task_id and len(task_id):
            try:
                task_id=task_id[0]
                print(task_id)
                update_query=f'update Tasks set UserID={id} where TaskID={task_id}'
                cursor.execute(update_query)
                connection.commit()
                return {'task_id':task_id,'status':'success'}
            except sql.DatabaseError as e:
                if connection:
                    connection.rollback()
                return {'status':'failure'} 
        else:
            return {'status':'success'}       
    finally:
        if cursor:
            cursor.close()
            
        if connection:
            connection.close()



def get_all_user_task_data():
    try:
        connection=get_connection()
        cursor=connection.cursor(buffered=True)
        select_task_query="select * from Users left join Tasks on Users.UserId=Tasks.UserID where Tasks.TaskStatus is null or Tasks.TaskStatus=0"
        cursor.execute(select_task_query)
        task_records=cursor.fetchall()
        return task_records
    finally:
        if cursor:
            cursor.close()
            
        if connection:
            connection.close()

def check_user_has_task(id):
    try:
        connection=get_connection()
        cursor=connection.cursor(buffered=True)
        select_query=f"select count(*) from Tasks where UserId={id}"
        cursor.execute(select_query)
        count=cursor.fetchone()
        count=count[0]
        return True if count>0 else False
    finally:
        if cursor:
            cursor.close()
            
        if connection:
            connection.close()

#this functionality just utilized for demo purpose
def reset_all_tasks():
    try:
        connection=get_connection()
        cursor=connection.cursor(buffered=True)
        select_query=f"update Tasks set TaskStatus=0,UserID=null"
        cursor.execute(select_query)
        connection.commit()
        return True
    except:
        return False
    finally:
        if cursor:
            cursor.close()
            
        if connection:
            connection.close()
    
    


