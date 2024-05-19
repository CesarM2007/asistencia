import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="asistencia"
)

mycursor = mydb.cursor()
  
def leer():
    
  table = str(input("Ingrese el nombre de la tabla que quiere ver: "))
  varstr = f"SELECT * FROM {table}"
  
  mycursor = mydb.cursor()

  mycursor.execute(varstr)

  myresult = mycursor.fetchall()


  for x in myresult:
    print(x)

def crear():

  table = input("Ingrese el nombre de la tabla a la que quiere agregar datos: ")
  
  if table == "alumnos":
    
    mycursor = mydb.cursor()

    nombre = input("Ingrese nombre del alumno: ")
    grado = input("Ingrese grado del esudiante: ")
    sql = f"INSERT INTO alumnos (nombre, grado) VALUES (%s, %s)"
    val = (nombre,grado)
    mycursor.execute(sql,val)
    mydb.commit()


  elif table == "registro":
    mycursor = mydb.cursor()

    nombre = input("Ingrese ID del alumno: ")
    asistente = input("Ingrese si el estiduante asistio -1- o no -0-: ")
    fecha = input("Ingrese la fecha del registro: ")
    hora = input("Ingrese la hora del registro: ")
    sql = f"INSERT INTO registro (estudiante_id, asistente, fecha, hora) VALUES (%s, %s, %s, %s)"
    val = (nombre, asistente, fecha, hora)
    mycursor.execute(sql,val)
    mydb.commit()

  else:
    print("Ingrese opcion valida")
  
def actualizar():
  table = input("Ingrese el nombre de la tabla a la que quiere agregar datos: ")
  
  mycursor = mydb.cursor()

  
  if table == "alumnos":

    estudiante_id=input("Ingrese el id del estudiante del que quiere actualizar el dato: ")
    campo = input("Que campo quiere actualizar: ")
    actualizado = input("Ingrese informacion a la que quiere cambiar: ")

    sql = f"UPDATE alumnos SET {campo} = '{actualizado}' WHERE estudiante_id = '{estudiante_id}'"
    
    mycursor.execute(sql)
    mydb.commit()
  
  
  elif table == "registro":

    estudiante_id=input("Ingrese el id del estudiante del que quiere actualizar el dato: ")
    campo = input("Que campo quiere actualizar: ")
    actualizado = input("Ingrese informacion a la que quiere cambiar: ")

    sql = f"UPDATE registro SET {campo} = '{actualizado}' WHERE estudiante_id = '{estudiante_id}'"
    mycursor.execute(sql)
    mydb.commit()

  else:
    print("Esa tabla o ese dato no existe")
    