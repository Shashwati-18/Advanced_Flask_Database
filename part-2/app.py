from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

DATABASE = 'students.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
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

def is_valid_email(email):
    """Basic email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# =============================================================================
# CREATE - Add new student with validation
# =============================================================================
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        course = request.form['course'].strip()
        
        # Validation
        if not name or len(name) < 2:
            flash('Name must be at least 2 characters long.', 'danger')
            return render_template('add.html')
        
        if not is_valid_email(email):
            flash('Please enter a valid email address.', 'danger')
            return render_template('add.html')
        
        if not course or len(course) < 2:
            flash('Course must be at least 2 characters long.', 'danger')
            return render_template('add.html')
        
        # Check if email already exists
        conn = get_db_connection()
        existing = conn.execute('SELECT id FROM students WHERE email = ?', (email,)).fetchone()
        if existing:
            flash('Email already exists! Please use a different email.', 'danger')
            conn.close()
            return render_template('add.html')
        
        # Insert new student
        conn.execute('INSERT INTO students (name, email, course) VALUES (?, ?, ?)', (name, email, course))
        conn.commit()
        conn.close()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add.html')

# =============================================================================
# READ - Display all students with search
# =============================================================================
@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    
    students = []
    search_query = ''
    
    if request.method == 'POST':
        search_query = request.form.get('search', '').strip()
        if search_query:
            students = conn.execute(
                'SELECT * FROM students WHERE name LIKE ? ORDER BY id DESC',
                (f'%{search_query}%',)
            ).fetchall()
            flash(f'Showing results for "{search_query}"', 'info')
        else:
            flash('Please enter a search term.', 'warning')
    else:
        students = conn.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
    
    conn.close()
    return render_template('index.html', students=students, search_query=search_query)

# =============================================================================
# UPDATE - Edit existing student
# =============================================================================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db_connection()
    
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        course = request.form['course'].strip()
        
        # Validation (same as add)
        if not name or len(name) < 2:
            flash('Name must be at least 2 characters long.', 'danger')
        elif not is_valid_email(email):
            flash('Please enter a valid email address.', 'danger')
        elif not course or len(course) < 2:
            flash('Course must be at least 2 characters long.', 'danger')
        else:
            # Check if email already exists for another student
            existing = conn.execute(
                'SELECT id FROM students WHERE email = ? AND id != ?', 
                (email, id)
            ).fetchone()
            
            if existing:
                flash('Email already exists for another student!', 'danger')
            else:
                conn.execute('UPDATE students SET name = ?, email = ?, course = ? WHERE id = ?', 
                           (name, email, course, id))
                conn.commit()
                flash('Student updated successfully!', 'success')
                conn.close()
                return redirect(url_for('index'))
        
        conn.close()
        student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
        return render_template('edit.html', student=student)
    
    # GET request
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    if not student:
        flash('Student not found!', 'danger')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('edit.html', student=student)

# =============================================================================
# DELETE - Remove student
# =============================================================================
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT name FROM students WHERE id = ?', (id,)).fetchone()
    
    if student:
        conn.execute('DELETE FROM students WHERE id = ?', (id,))
        conn.commit()
        flash(f'Student "{student["name"]}" deleted!', 'danger')
    else:
        flash('Student not found!', 'danger')
    
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
