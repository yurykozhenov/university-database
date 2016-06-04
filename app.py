from flask import (Flask, render_template, redirect, flash, request)

import models
import forms
import functions


app = Flask(__name__)
# Secret key for CSRF protection to work
app.secret_key = 'sfdp[ogdsohg53jt0438jk0=alsojdohgfdgpwpdfjhvc8oxhvsfj]'


@app.route('/', methods=('GET', 'POST'))
def index():
    if request.form:
        models.direct_sql_query(request.form['query'])
        flash("Запит успішно виконаний!", "success")
        return redirect('/')

    return render_template('index.html', title="Головна")


# ************************* STUDENT ************************************


@app.route('/students')
@app.route('/students/<int:student_id>')
def list_students(student_id=None):
    return functions.list_records(model=models.Student,
                                  active_page="students",
                                  title="Студенти",
                                  record_id=student_id)


@app.route('/students/find', methods=('GET', 'POST'))
def find_students():
    return functions.find_records(form_class=forms.StudentForm,
                                  active_page="students",
                                  title="Пошук студентів")


@app.route('/students/new', methods=('GET', 'POST'))
def new_student():
    return functions.new_record(model=models.Student,
                                form_class=forms.StudentForm,
                                active_page="students",
                                title="Новий студент")


@app.route('/students/edit/<int:student_id>', methods=('GET', 'POST'))
def edit_student(student_id):
    return functions.edit_record(model=models.Student,
                                 form_class=forms.StudentForm,
                                 record_id=student_id,
                                 active_page="students",
                                 title="Зміна студента")


@app.route('/students/delete/<int:student_id>', methods=('GET', 'DELETE'))
def delete_student(student_id):
    return functions.delete_record(model=models.Student,
                                   record_id=student_id,
                                   active_page="students")


# ************************* TEACHER **************************************


@app.route('/teachers')
@app.route('/teachers/<int:teacher_id>')
def list_teachers(teacher_id=None):
    return functions.list_records(model=models.Teacher,
                                  active_page="teachers",
                                  title="Викладачі",
                                  record_id=teacher_id)


@app.route('/teachers/find', methods=('GET', 'POST'))
def find_teachers():
    return functions.find_records(form_class=forms.TeacherForm,
                                  active_page="teachers",
                                  title="Пошук викладачів")


@app.route('/teachers/new', methods=('GET', 'POST'))
def new_teacher():
    return functions.new_record(model=models.Teacher,
                                form_class=forms.TeacherForm,
                                active_page="teachers",
                                title="Новий викладач")


@app.route('/teachers/edit/<int:teacher_id>', methods=('GET', 'POST'))
def edit_teacher(teacher_id):
    return functions.edit_record(model=models.Teacher,
                                 form_class=forms.TeacherForm,
                                 record_id=teacher_id,
                                 active_page="teachers",
                                 title="Зміна викладача")


@app.route('/teachers/delete/<int:teacher_id>', methods=('GET', 'DELETE'))
def delete_teacher(teacher_id):
    return functions.delete_record(model=models.Teacher,
                                   record_id=teacher_id,
                                   active_page="teachers")


# ************************* SUBJECT **************************************


@app.route('/subjects')
@app.route('/subjects/<int:subject_id>')
def list_subjects(subject_id=None):
    return functions.list_records(model=models.Subject,
                                  active_page="subjects",
                                  title="Предмети",
                                  record_id=subject_id)


@app.route('/subjects/find', methods=('GET', 'POST'))
def find_subjects():
    return functions.find_records(form_class=forms.SubjectForm,
                                  active_page="subjects",
                                  title="Пошук предметів")


@app.route('/subjects/new', methods=('GET', 'POST'))
def new_subject():
    return functions.new_record(model=models.Subject,
                                form_class=forms.SubjectForm,
                                active_page="subjects",
                                title="Новий предмет")


@app.route('/subjects/edit/<int:subject_id>', methods=('GET', 'POST'))
def edit_subject(subject_id):
    return functions.edit_record(model=models.Subject,
                                 form_class=forms.SubjectForm,
                                 record_id=subject_id,
                                 active_page="subjects",
                                 title="Зміна предмета")


@app.route('/subjects/delete/<int:subject_id>', methods=('GET', 'DELETE'))
def delete_subject(subject_id):
    return functions.delete_record(model=models.Subject,
                                   record_id=subject_id,
                                   active_page="subjects")


# ************************** MARK ****************************************


@app.route('/marks')
@app.route('/marks/<int:mark_id>')
def list_marks(mark_id=None):
    return functions.list_records(model=models.Mark,
                                  active_page="marks",
                                  title="Предмети",
                                  record_id=mark_id)


@app.route('/marks/find', methods=('GET', 'POST'))
def find_marks():
    return functions.find_records(form_class=forms.MarkForm,
                                  active_page="marks",
                                  title="Пошук предметів")


@app.route('/marks/new', methods=('GET', 'POST'))
def new_mark():
    return functions.new_record(model=models.Mark,
                                form_class=forms.MarkForm,
                                active_page="marks",
                                title="Новий предмет")


@app.route('/marks/edit/<int:mark_id>', methods=('GET', 'POST'))
def edit_mark(mark_id):
    return functions.edit_record(model=models.Mark,
                                 form_class=forms.MarkForm,
                                 record_id=mark_id,
                                 active_page="marks",
                                 title="Зміна предмета")


@app.route('/marks/delete/<int:mark_id>', methods=('GET', 'DELETE'))
def delete_mark(mark_id):
    return functions.delete_record(model=models.Mark,
                                   record_id=mark_id,
                                   active_page="marks")


# ************************ REQUESTS ***************************************


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
