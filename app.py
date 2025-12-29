from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Initialize database
def init_db():
    conn = sqlite3.connect('students.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            course TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    try:
        conn = sqlite3.connect('students.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        students = cursor.execute('SELECT * FROM students').fetchall()
        conn.close()
        return render_template('indx.html', students=students)
    except Exception as e:
        return f"Error: {e}"

@app.route('/add', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        course = request.form['course'].strip()
        conn = sqlite3.connect('students.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name,email,course) VALUES (?,?,?)", (name,email,course))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_student(id):
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        course = request.form['course'].strip()
        cursor.execute("UPDATE students SET name=?, email=?, course=? WHERE id=?", (name,email,course,id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
