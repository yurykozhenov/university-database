from flask import (Flask, render_template, redirect, flash)

import models
import forms


app = Flask(__name__)
# Secret key for CSRF protection to work
app.secret_key = 'sfdp[ogdsohg53jt0438jk0=alsojdohgfdgpwpdfjhvc8oxhvsfj]'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/students")
@app.route("/students/<student_id>")
def students_list(student_id=None):
    if student_id:
        students = models.Student.select().where(
            models.Student.id == student_id
        )
    else:
        students = models.Student.select()

    return render_template('students.html', students=students)


@app.route("/students/new", methods=('GET', 'POST'))
def new_student():
    form = forms.StudentForm()

    if form.validate_on_submit():
        models.Student.create(
            last_name=form.last_name.data.strip().capitalize(),
            first_name=form.first_name.data.strip().capitalize(),
            patronymic=form.patronymic.data.strip().capitalize(),
            group=form.group.data.strip().upper(),
            grade=form.grade.data
        )

        flash("Запис успішно створенний!", "success")
        return redirect('/students')

    return render_template('students_new.html', form=form)


@app.route("/students/edit/<student_id>", methods=('GET', 'POST'))
def edit_student(student_id):
    form = forms.StudentForm()

    student = models.Student.get(models.Student.id == student_id)

    if form.validate_on_submit():
        student.last_name = form.last_name.data.strip()
        student.first_name = form.first_name.data.strip()
        student.patronymic = form.patronymic.data.strip()
        student.group = form.group.data.strip().upper()
        student.grade = form.grade.data

        student.save()

        flash("Запис {} успішно змінений!".format(
            student.id), "success")
        return redirect('/students')

    return render_template('students_edit.html', form=form, student=student)


@app.route("/teachers")
@app.route("/teachers/<teacher_id>")
def teachers_list(teacher_id=None):
    if teacher_id:
        teachers = models.Teacher.select().where(
            models.Teacher.id == teacher_id
        )
    else:
        teachers = models.Teacher.select()

    return render_template('teachers.html', teachers=teachers)


@app.route("/subjects")
@app.route("/subjects/<subject_id>")
def subjects_list(subject_id=None):
    if subject_id:
        subjects = models.Subject.select().where(
            models.Subject.id == subject_id
        )
    else:
        subjects = models.Subject.select()

    return render_template('subjects.html', subjects=subjects)


@app.route("/marks")
@app.route("/marks/<mark_id>")
def marks_list(mark_id=None):
    if mark_id:
        marks = models.Mark.select().where(
            models.Mark.id == mark_id
        )
    else:
        marks = models.Mark.select()

    return render_template('marks.html', marks=marks)


if __name__ == "__main__":
    models.initialize()

    app.run(debug=True)  # debug=True, host=8000, port='0.0.0.0'
