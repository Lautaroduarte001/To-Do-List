from flask import Blueprint, render_template, request, redirect
import pymysql

main = Blueprint('main', __name__)

# Conexion a MySQL
def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="7778742049",
        database="to_do_db"
    )
    
    return connection

@main.route('/')

def index():
    #Obtener tareas de la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id, name, status FROM tasks")
    tasks = cursor.fetchall()
    cursor.fetchall()
    connection.close()
    return render_template('tasks.html', tasks=tasks)

@main.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task')
    if task_name:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO tasks (name, status) VALUES (%s, 'incomplete')", (task_name,))
        connection.commit()
        connection.close()
    return redirect('/')

@main.route('/delete_task', methods=['POST'])
def delete_task():
    task_id = request.form.get('delete_task')
    if task_id:
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM tasks WHERE id = %s', (task_id,))
            connection.commit()
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error deleting task: {e}")
        finally:
            connection.close()
    return redirect('/')
    
@main.route('/update_status', methods=['POST'])
def update_status():
    # Obtenemos los datos del formulario
    task_id = request.form.get('task_id')
    task_status = 'complete' if request.form.get('task_status') else 'incomplete'

    # Actualizamos el status de la tarea en la base de datos
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET status = %s WHERE id = %s", (task_status, task_id))
    connection.commit()
    connection.close()

    return redirect('/')