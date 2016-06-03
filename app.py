from flask import (Flask, render_template, redirect, flash, request)
from peewee import CharField

import models
import forms


app = Flask(__name__)
# Secret key for CSRF protection to work
app.secret_key = 'sfdp[ogdsohg53jt0438jk0=alsojdohgfdgpwpdfjhvc8oxhvsfj]'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/students")
@app.route("/students/<int:student_id>")
def students_list(student_id=None):
    if student_id:
        students = models.Student.select().where(
            models.Student.id == student_id
        )
    else:
        students = models.Student.select()

        for key in request.args:
            if isinstance(getattr(models.Student, key), CharField):
                students = students.where(
                    getattr(models.Student, key) % request.args.get(key)
                )
            else:
                students = students.where(
                    getattr(models.Student, key) % request.args.get(key)
                )

    return render_template('table.html',
                           title="Студенти",
                           active_page="students",
                           fields=models.Student.fields,
                           records=students)


@app.route('/students/find', methods=('GET', 'POST'))
def find_students():
    if request.form:
        query_list = []

        for key in request.form:
            if request.form[key] and key != 'csrf_token':
                query_list.append("{}={}".format(key, request.form[key]))

        query = "&&".join(query_list)

        return redirect('/students?{}'.format(query))

    form = forms.StudentForm()
    return render_template('students_find.html', form=form)


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


@app.route("/students/delete/<student_id>", methods=('GET', 'DELETE'))
def delete_student(student_id):
    student = models.Student.get(models.Student.id == student_id)

    student.delete_instance()

    flash("Запис {} успішно видаленний!".format(
        student.id), "success")

    return redirect('/students')


@app.route("/teachers")
@app.route("/teachers/<int:teacher_id>")
def teacher_list(teacher_id=None):
    if teacher_id:
        teachers = models.Teacher.select().where(
            models.Teacher.id == teacher_id
        )
    else:
        teachers = models.Teacher.select()

        for key in request.args:
            if isinstance(getattr(models.Teacher, key), CharField):
                teachers = teachers.where(
                    getattr(models.Teacher, key) % request.args.get(key)
                )
            else:
                teachers = teachers.where(
                    getattr(models.Teacher, key) % request.args.get(key)
                )

    return render_template('table.html',
                           title="Викладачі",
                           active_page="teachers",
                           fields=models.Teacher.fields,
                           records=teachers)


@app.route("/subjects")
@app.route("/subjects/<int:subject_id>")
def subjects_list(subject_id=None):
    if subject_id:
        subjects = models.Subject.select().where(
            models.Subject.id == subject_id
        )
    else:
        subjects = models.Subject.select()

        for key in request.args:
            if isinstance(getattr(models.Subject, key), CharField):
                subjects = subjects.where(
                    getattr(models.Subject, key) % request.args.get(key)
                )
            else:
                subjects = subjects.where(
                    getattr(models.Subject, key) % request.args.get(key)
                )

        return render_template('table.html',
                               title="Предмети",
                               active_page="subjects",
                               fields=models.Subject.fields,
                               records=subjects)


@app.route("/marks")
@app.route("/marks/<mark_id>")
def marks_list(mark_id=None):
    if mark_id:
        marks = models.Mark.select().where(
            models.Mark.id == mark_id
        )
    else:
        marks = models.Mark.select()

        for key in request.args:
            if isinstance(getattr(models.Mark, key), CharField):
                marks = marks.where(
                    getattr(models.Mark, key) % request.args.get(key)
                )
            else:
                marks = marks.where(
                    getattr(models.Mark, key) % request.args.get(key)
                )

        return render_template('table.html',
                               title="Оцінки",
                               active_page="marks",
                               fields=models.Mark.fields,
                               records=marks)


@app.route('/students/avg_marks')
def students_average_marks():
    students = models.Student.get_with_average_mark()

    return render_template('students_with_avg_marks.html', students=students)


@app.route('/good_students')
def good_students():
    students = models.Student.get_good_students()

    return render_template('students_with_avg_marks.html', students=students)


@app.route('/excellent_students')
def excellent_students():
    students = models.Student.get_excellent_students()

    return render_template('students_with_avg_marks.html', students=students)


if __name__ == "__main__":
    models.initialize()

    app.run(debug=True)  # debug=True, host=8000, port='0.0.0.0'
