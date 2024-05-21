
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import re


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="asistencias"
)


def ver(tabla):
    if tabla == "alumnos":
        columns = ("ID", "Nombre", "Grado")
        Stringyiyi = "SELECT * FROM alumnos"
    elif tabla == "registro":
        columns = ("Registro ID", "Estudiante ID", "Asistente", "Fecha", "Hora")
        Stringyiyi = "SELECT * FROM registro"
    else:
        return

    mycursor = mydb.cursor()
    mycursor.execute(Stringyiyi)
    myresult = mycursor.fetchall()


    results_window = tk.Toplevel()
    results_window.title(f"Datos - {tabla}")


    tree = ttk.Treeview(results_window, columns=columns, show='headings')


    for col in columns:
        tree.heading(col, text=col)


    for row in myresult:
        if tabla == "registro":

            row = list(row)
            asistente = int(row[2])
            row[2] = f"{asistente} ( {'Asistente' if asistente == 1 else 'No asistente'} )"
            tree.insert("", "end", values=row)
        else:
            tree.insert("", "end", values=row)

    tree.pack(expand=True, fill='both')


def open_table_options():
    table_window = tk.Toplevel()
    table_window.title("Oprima boton para ver tabla")

    estudiantes_button = tk.Button(table_window, text="Alumnos", command=lambda: ver("alumnos"))
    estudiantes_button.pack(pady=10)

    registro_button = tk.Button(table_window, text="Registro", command=lambda: ver("registro"))
    registro_button.pack(pady=10)
   

def crear_estudiante(nombre_entry, grado_entry, window, status_label):
    nombre = nombre_entry.get()
    grado = grado_entry.get()
    
    if not nombre or not grado:
        messagebox.showerror("Error", "Ambos campos deben estar llenos.", parent=window)
        return

    if len(nombre) > 100:
        messagebox.showerror("Error", "El texto supera los 100 caracteres, escriba un texto mas corto", parent=window)
        return
    if len(grado) > 100:
        messagebox.showerror("Error", "El grado supera los 100 caracteres, escriba un texto mas corto", parent=window)
        return

    mycursor = mydb.cursor()
    sql = "INSERT INTO alumnos (nombre, grado) VALUES (%s, %s)"
    val = (nombre, grado)
    mycursor.execute(sql, val)
    mydb.commit()

    status_label.config(text="Alumno creado exitosamente")
    window.after(3000, lambda: status_label.config(text=""))
    

    nombre_entry.delete(0, tk.END)
    grado_entry.delete(0, tk.END)


    nombre_entry.focus_set()


def validar_estudiante_id(estudiante_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT estudiante_id FROM estudiantes WHERE estudiante_id = %s", (estudiante_id,))
    result = mycursor.fetchone()
    return result is not None

def validar_registro_id(registro_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT registro_id FROM registro WHERE estudiante_id = %s", (registro_id,))
    result = mycursor.fetchone()
    return result is not None


def crear_registro(estudiante_id_entry, asistente_var, fecha_entry, hora_entry, window, status_label):
    estudiante_id = estudiante_id_entry.get()
    asistente = asistente_var.get()
    fecha = fecha_entry.get()
    hora = hora_entry.get()

    if not estudiante_id or not asistente or not fecha or not hora:
        messagebox.showerror("Error", "Rellene todos los campos solicitados", parent=window)
        return

    if not validar_estudiante_id(estudiante_id):
        messagebox.showerror("Error", "El ID del estudiante no es válido", parent=window)
        return

    if asistente not in ("Asistente", "No asistente"):
        messagebox.showerror("Error", "Seleccione una opción válida para Asistente", parent=window)
        return

    if not re.match(r"\d{4}-\d{2}-\d{2}", fecha):
        messagebox.showerror("Error", "Ingrese una fecha en formato YYYY-MM-DD", parent=window)
        return

    if not re.match(r"\d{2}:\d{2}:\d{2}", hora):
        messagebox.showerror("Error", "Ingrese una hora en formato HH:MM:SS", parent=window)
        return

    asistente_val = 1 if asistente == "Asistente" else 0


    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM registro WHERE estudiante_id = %s AND fecha = %s", (estudiante_id, fecha))
    existing_record = mycursor.fetchone()
    if existing_record:
        messagebox.showerror("Error", "Ya existe un registro para este estudiante en la fecha dada", parent=window)
        return


    sql = "INSERT INTO registro (estudiante_id, asistente, fecha, hora) VALUES (%s, %s, %s, %s)"
    val = (estudiante_id, asistente_val, fecha, hora)
    mycursor.execute(sql, val)
    mydb.commit()

    status_label.config(text="Registro creado")
    window.after(3000, lambda: status_label.config(text=""))


    estudiante_id_entry.delete(0, tk.END)
    fecha_entry.delete(0, tk.END)
    hora_entry.delete(0, tk.END)


    asistente_var.set(None)


    estudiante_id_entry.focus_set()


def open_create_student():
    create_window = tk.Toplevel()
    create_window.title("Crear ALumno")

    tk.Label(create_window, text="Ingrese el nombre del estudiante:").pack(pady=5)
    nombre_entry = tk.Entry(create_window)
    nombre_entry.pack(pady=5)

    tk.Label(create_window, text="Ingrese el grado del estudiante:").pack(pady=5)
    grado_entry = tk.Entry(create_window)
    grado_entry.pack(pady=5)

    status_label = tk.Label(create_window, text="")
    status_label.pack(pady=5)

    create_button = tk.Button(create_window, text="Crear", 
                              command=lambda: crear_estudiante(nombre_entry, grado_entry, create_window, status_label))
    create_button.pack(pady=20)


    nombre_entry.focus_set()


def open_create_record():
    create_window = tk.Toplevel()
    create_window.title("Crear Registro")

    def update_hour_entry():

        if asistente_var.get() == "No asistente":
            hora_entry.delete(0, tk.END)
            hora_entry.insert(0, "00:00:00")
            hora_entry.config(state='disabled')  
            
        else:
            hora_entry.config(state='normal')  
            hora_entry.delete(0, tk.END)
            
    tk.Label(create_window, text="Ingrese ID del estudiante:").pack(pady=5)
    estudiante_id_entry = tk.Entry(create_window)
    estudiante_id_entry.pack(pady=5)

    tk.Label(create_window, text="Seleccione si el estudiante asistió:").pack(pady=5)
    asistente_var = tk.StringVar(value=None)
    tk.Radiobutton(create_window, text="Asistente", variable=asistente_var, value="Asistente", command=update_hour_entry).pack(pady=5)
    tk.Radiobutton(create_window, text="No asistente", variable=asistente_var, value="No asistente", command=update_hour_entry).pack(pady=5)

    tk.Label(create_window, text="Ingrese la fecha (YYYY-MM-DD):").pack(pady=5)
    fecha_entry = tk.Entry(create_window)
    fecha_entry.pack(pady=5)

    tk.Label(create_window, text="Ingrese la hora (HH:MM:SS):").pack(pady=5)
    hora_entry = tk.Entry(create_window)
    hora_entry.pack(pady=5)


    update_hour_entry()

    status_label = tk.Label(create_window, text="")
    status_label.pack(pady=5)

    create_button = tk.Button(create_window, text="Crear", 
                              command=lambda: crear_registro(estudiante_id_entry, asistente_var, fecha_entry, hora_entry, create_window, status_label))
    create_button.pack(pady=20)


    estudiante_id_entry.focus_set()


    asistente_var.set(None)


def open_create_options():
    create_options_window = tk.Toplevel()
    create_options_window.title("Seleccionar tabla para crear")

    estudiantes_button = tk.Button(create_options_window, text="Estudiantes", command=open_create_student)
    estudiantes_button.pack(pady=10)

    registro_button = tk.Button(create_options_window, text="Registro", command=open_create_record)
    registro_button.pack(pady=10)

def actualizar_estudiante(estudiante_id_entry, selected_field_entry, new_data_entry, window, status_label):
    id_estudiante = estudiante_id_entry.get()
    campo = selected_field_entry.get()
    nuevo_dato = new_data_entry.get()

    if not id_estudiante or not campo or not nuevo_dato:
        messagebox.showerror("Error", "Complete todos los campos", parent=window)
        return
        
    if not validar_estudiante_id(id_estudiante):
        messagebox.showerror("Error", "El ID del estudiante no es válido", parent=window)
        return
    
    if campo not in ("Nombre", "Grado"):
        messagebox.showerror("Error", "Seleccione una opción válida para Campo", parent=window)
        return


    mycursor = mydb.cursor()
    sql = f"UPDATE alumnos SET {campo} = '{nuevo_dato}' WHERE estudiante_id = {id_estudiante}"
    mycursor.execute(sql)
    mydb.commit()

    status_label.config(text="Estudiante actualizado")
    window.after(3000, lambda: status_label.config(text=""))
        

    estudiante_id_entry.delete(0, tk.END)
    new_data_entry.delete(0, tk.END)


    selected_field_entry.set(None)


    estudiante_id_entry.focus_set()


def open_update_student():
    update_student_window = tk.Toplevel()
    update_student_window.title("Actualizar Estudiante")

    textazo="Nuevo dato para"

    tk.Label(update_student_window, text="Ingrese el ID del estudiante a actualizar:").pack(pady=5)
    estudiante_id_entry = tk.Entry(update_student_window)
    estudiante_id_entry.pack(pady=5)

    tk.Label(update_student_window, text="Seleccione el campo a actualizar:").pack(pady=5)
    selected_field = tk.StringVar()
    tk.Radiobutton(update_student_window, text="Nombre", variable=selected_field, value="Nombre").pack(pady=5)
    tk.Radiobutton(update_student_window, text="Grado", variable=selected_field, value="Grado").pack(pady=5)


    def update_label_text():
        field_value = selected_field.get()
        if field_value == "Nombre":
            label_text.set("Nuevo dato para NOMBRE")
        elif field_value == "Grado":
            label_text.set("Nuevo dato para GRADO")
        else:
            label_text.set("Nuevo dato para")


    label_text = tk.StringVar()
    label_text.set("Nuevo dato para")
    label = tk.Label(update_student_window, textvariable=label_text, anchor="w")
    label.pack(pady=5)


    selected_field.trace("w", lambda *args: update_label_text())

    new_data_entry = tk.Entry(update_student_window)
    new_data_entry.pack(pady=5)

    status_label = tk.Label(update_student_window, text="")
    status_label.pack(pady=5)

    create_button = tk.Button(update_student_window, text="Actualizar", 
                              command=lambda: actualizar_estudiante(estudiante_id_entry, selected_field, new_data_entry, update_student_window, status_label))
    create_button.pack(pady=20)

    #
    estudiante_id_entry.focus_set()

    #
    selected_field.set(None)


def actualizar_registro(registro_id_entry, selected_field_entry, new_data_entry, window, status_label):
    registro_id = registro_id_entry.get()
    campo = selected_field_entry.get()
    nuevo_dato = new_data_entry.get()

    if not registro_id or not campo or not nuevo_dato:
        messagebox.showerror("Error", "Complete todos los campos requeridos", parent=window)
        return

    if campo not in ("Estudiante ID", "Asistente", "Fecha", "Hora"):
        messagebox.showerror("Error", "Seleccione una opción válida para Campo", parent=window)
        return

    if not validar_registro_id(registro_id):
        messagebox.showerror("Error", "El ID del registro no es válido", parent=window)
        return


    if campo == "Estudiante ID" and not validar_estudiante_id(nuevo_dato):
        messagebox.showerror("Error", "El ID del estudiante no es válido", parent=window)
        return

    if campo == "Asistente" and nuevo_dato not in ("1", "0"):
        messagebox.showerror("Error", "Seleccione una opción válida para Asistente", parent=window)
        return

    if campo == "Fecha" and not re.match(r"\d{4}-\d{2}-\d{2}", nuevo_dato):
        messagebox.showerror("Error", "Ingrese una fecha válida en formato YYYY-MM-DD", parent=window)
        return

    if campo == "Hora" and not re.match(r"\d{2}:\d{2}:\d{2}", nuevo_dato):
        messagebox.showerror("Error", "Ingrese una hora válida en formato HH:MM:SS", parent=window)
        return


    mycursor = mydb.cursor()
    sql = f"UPDATE registro SET {campo} = '{nuevo_dato}' WHERE registro_id = {registro_id}"
    mycursor.execute(sql)
    mydb.commit()

    status_label.config(text="Registro actualizado exitosamente")
    window.after(3000, lambda: status_label.config(text=""))


    registro_id_entry.delete(0, tk.END)
    new_data_entry.delete(0, tk.END)

    selected_field_entry.set(None)
    registro_id_entry.focus_set()


def open_update_record():
    update_record_window = tk.Toplevel()
    update_record_window.title("Actualizar Registro")

    textazo="Nuevo dato para"

    tk.Label(update_record_window, text="Ingrese el ID del registro a actualizar:").pack(pady=5)
    registro_id_entry = tk.Entry(update_record_window)
    registro_id_entry.pack(pady=5)

    tk.Label(update_record_window, text="Seleccione el campo que quiere actualizar:").pack(pady=5)
    selected_field = tk.StringVar()
    tk.Radiobutton(update_record_window, text="Estudiante ID", variable=selected_field, value="Estudiante ID").pack(pady=5)
    tk.Radiobutton(update_record_window, text="Asistente", variable=selected_field, value="Asistente").pack(pady=5)
    tk.Radiobutton(update_record_window, text="Fecha", variable=selected_field, value="Fecha").pack(pady=5)
    tk.Radiobutton(update_record_window, text="Hora", variable=selected_field, value="Hora").pack(pady=5)


    def update_label_text():
        field_value = selected_field.get()
        if field_value == "Estudiante ID":
            label_text.set("Nuevo dato para ESTUDIANTE ID")
        elif field_value == "Asistente":
            label_text.set("Nuevo dato para ASISTENTE (1 para Asistente, 0 para No Asistente)")
        elif field_value == "Fecha":
            label_text.set("Nuevo dato para FECHA (YYYY-MM-DD)")
        elif field_value == "Hora":
            label_text.set("Nuevo dato para HORA (HH:MM:SS)")
        else:
            label_text.set("Nuevo dato para")


    label_text = tk.StringVar()
    label_text.set("Nuevo dato para")
    label = tk.Label(update_record_window, textvariable=label_text, anchor="w")
    label.pack(pady=5)


    selected_field.trace("w", lambda *args: update_label_text())

    new_data_entry = tk.Entry(update_record_window)
    new_data_entry.pack(pady=5)

    status_label = tk.Label(update_record_window, text="")
    status_label.pack(pady=5)

    update_button = tk.Button(update_record_window, text="Actualizar", 
                              command=lambda: actualizar_registro(registro_id_entry, selected_field, new_data_entry, update_record_window, status_label))
    update_button.pack(pady=20)

    registro_id_entry.focus_set()
    selected_field.set(None)


def open_update_options():
    update_options_window = tk.Toplevel()
    update_options_window.title("Seleccionar Tabla para Actualizar")

    estudiantes_button = tk.Button(update_options_window, text="Alumnos", command=open_update_student)
    estudiantes_button.pack(pady=10)

    registro_button = tk.Button(update_options_window, text="Registro", command=open_update_record)
    registro_button.pack(pady=10)


root = tk.Tk()
root.title("Base de Datos Asistencias")

ver_button = tk.Button(root, text="Ver", command=open_table_options)
ver_button.pack(pady=20)

crear_button = tk.Button(root, text="Crear", command=open_create_options)
crear_button.pack(pady=20)

actualizar_button = tk.Button(root, text="Actualizar", command=open_update_options)
actualizar_button.pack(pady=20)

root.mainloop()