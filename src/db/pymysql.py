import pymysql

class Basedata:
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db
            )
            print("Conexion a la base de datos exitosa.")

        except pymysql.MySQLError as e:
            print(f"Error al conectar a la base de datos : {e}")
            self.connection = None

    def cursor(self):
        if self.connection:
            return self.connection.cursor()
        else:
            raise ConnectionError("No se puede crear un cursor . la conexion ala base de datos fallo")

    def get_all_tasks(self):
        with self.cursor() as cursor:
            cursor.execute("SELECT * FROM task")
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_task_by_id(self, id_task):
        with self.cursor() as cursor:
            cursor.execute("SELECT * FROM task WHERE id_task =%s", (id_task,))
            result = cursor.fetchone()
            if result:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, result))
            return None

    def add_task(self, title, description):
        with self.cursor() as cursor:
            cursor.execute("INSERT INTO task (title, description) VALUES (%s, %s)", (title, description))
            self.connection.commit()

    def update_task(self, id_task, title, description):
        with self.cursor() as cursor:
            cursor.execute("UPDATE task SET title = %s, description = %s WHERE id_task = %s", (title, description, id_task))
        self.connection.commit()

    def delete_task(self, id_task):
        with self.cursor() as cursor:
            cursor.execute("DELETE FROM task WHERE id_task = %s", (id_task,))
        self.connection.commit()

    def __del__(self):
        if self.connection:
            self.connection.close()

