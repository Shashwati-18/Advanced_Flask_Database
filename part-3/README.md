# Part 3: Flask-SQLAlchemy ORM

## One-Line Summary
Flask-SQLAlchemy ORM integration with models and relationships

## What You'll Learn
- Setting up Flask-SQLAlchemy
- Creating Models (Python classes = database tables)
- ORM queries instead of raw SQL
- One-to-Many relationships between tables

## Prerequisites
- Complete part-1 and part-2
- Install: `pip install flask-sqlalchemy`

## How to Run
```bash
cd part-3
pip install flask-sqlalchemy
python app.py
```
Open: http://localhost:5000

## What is ORM?
**ORM = Object-Relational Mapping**

Instead of writing SQL:
```sql
SELECT * FROM students WHERE id = 1
```

You write Python:
```python
Student.query.get(1)
```

## ORM vs Raw SQL Comparison

| Operation | Raw SQL | SQLAlchemy ORM |
|-----------|---------|----------------|
| Get all | `SELECT * FROM students` | `Student.query.all()` |
| Get by ID | `SELECT * WHERE id = ?` | `Student.query.get(id)` |
| Filter | `SELECT * WHERE name = ?` | `Student.query.filter_by(name='John')` |
| Insert | `INSERT INTO students...` | `db.session.add(student)` |
| Update | `UPDATE students SET...` | `student.name = 'New'; db.session.commit()` |
| Delete | `DELETE FROM students...` | `db.session.delete(student)` |

## Key Files
```
part-3/
├── app.py              <- Models + ORM queries
├── templates/
│   ├── index.html      <- List students
│   ├── add.html        <- Add student form
│   ├── edit.html       <- Edit student form
│   ├── courses.html    <- List courses (relationship demo)
│   └── add_course.html <- Add course form
└── README.md
```

## Understanding Relationships

```python
class Course(db.Model):
    # ...
    students = db.relationship('Student', backref='course')

class Student(db.Model):
    # ...
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
```

This allows:
- `course.students` → Get all students in a course
- `student.course` → Get the course a student belongs to

## Exercise
1. Add a `Teacher` model with a relationship to Course
2. Try different query methods: `filter()`, `order_by()`, `limit()`

## Next Step
→ Go to **part-4** to learn REST API for database operations
