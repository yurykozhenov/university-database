from flask import (Flask, render_template, redirect, flash, request)
from peewee import CharField

import models
import forms


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
                           title='Студенти',
                           active_page='students',
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
    return render_template('search_form.html',
                           title='Пошук студентів',
                           active_page='students',
                           form=form)


@app.route('/students/new', methods=('GET', 'POST'))
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

    return render_template('form.html',
                           title='Новий студент',
                           active_page='students',
                           form=form)


@app.route('/students/edit/<int:student_id>', methods=('GET', 'POST'))
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
            student_id), "success")
        return redirect('/students')

    return render_template('form.html',
                           title='Зміна студента',
                           active_page='students',
                           form=form,
                           record=student)


@app.route('/students/delete/<int:student_id>', methods=('GET', 'DELETE'))
def delete_student(student_id):
    student = models.Student.get(models.Student.id == student_id)

    student.delete_instance()

    flash("Запис {} успішно видаленний!".format(
        student_id), "success")

    return redirect('/students')


# ************************* TEACHER **************************************


@app.route('/teachers')
@app.route('/teachers/<int:teacher_id>')
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
                    getattr(models.Teacher, key) == request.args.get(key)
                )

    return render_template('table.html',
                           title='Викладачі',
                           active_page='teachers',
                           fields=models.Teacher.fields,
                           records=teachers)


@app.route('/teachers/find', methods=('GET', 'POST'))
def find_teachers():
    if request.form:
        query_list = []

        for key in request.form:
            if request.form[key] and key != 'csrf_token':
                query_list.append("{}={}".format(key, request.form[key]))

        query = "&&".join(query_list)

        return redirect('/teachers?{}'.format(query))

    form = forms.TeacherForm()
    return render_template('search_form.html',
                           title='Пошук викладачів',
                           active_page='teachers',
                           form=form)


@app.route('/teachers/new', methods=('GET', 'POST'))
def new_teacher():
    form = forms.TeacherForm()

    if form.validate_on_submit():
        models.Teacher.create(
            last_name=form.last_name.data.strip().capitalize(),
            first_name=form.first_name.data.strip().capitalize(),
            patronymic=form.patronymic.data.strip().capitalize(),
            department=form.department.data.strip(),
            position=form.position.data.strip()
        )

        flash("Запис успішно створенний!", "success")
        return redirect('/teachers')

    return render_template('form.html',
                           title='Новий викладач',
                           active_page='teachers',
                           form=form)


@app.route('/teachers/edit/<int:teacher_id>', methods=('GET', 'POST'))
def edit_teacher(teacher_id):
    form = forms.TeacherForm()

    teacher = models.Teacher.get(models.Teacher.id == teacher_id)

    if form.validate_on_submit():
        models.Teacher.create(
            last_name=form.last_name.data.strip().capitalize(),
            first_name=form.first_name.data.strip().capitalize(),
            patronymic=form.patronymic.data.strip().capitalize(),
            department=form.department.data.strip(),
            position=form.position.data.strip()
        )

        flash("Запис {} успішно змінений!".format(
            teacher_id), "success")
        return redirect('/teachers')

    return render_template('form.html',
                           title='Зміна викладача',
                           active_page='teachers',
                           form=form,
                           record=teacher)


@app.route('/teachers/delete/<int:teacher_id>', methods=('GET', 'DELETE'))
def delete_teacher(teacher_id):
    teacher = models.Teacher.get(models.Teacher.id == teacher_id)

    teacher.delete_instance()

    flash("Запис {} успішно видаленний!".format(
        teacher_id), "success")

    return redirect('/teachers')


# ************************* SUBJECT **************************************


@app.route('/subjects')
@app.route('/subjects/<int:subject_id>')
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
                               title='Предмети',
                               active_page='subjects',
                               fields=models.Subject.fields,
                               records=subjects)


@app.route('/subjects/find', methods=('GET', 'POST'))
def find_subjects():
    if request.form:
        query_list = []

        for key in request.form:
            if request.form[key] and key != 'csrf_token':
                query_list.append("{}={}".format(key, request.form[key]))

        query = "&&".join(query_list)

        return redirect('/subjects?{}'.format(query))

    form = forms.SubjectForm()
    return render_template('search_form.html',
                           title='Пошук предметів',
                           active_page='subjects',
                           form=form)


@app.route('/subjects/new', methods=('GET', 'POST'))
def new_subject():
    form = forms.SubjectForm()

    if form.validate_on_submit():
        models.Subject.create(
            name=form.name.data.strip().capitalize(),
            teacher_id=form.teacher.data
        )

        flash("Запис успішно створенний!", "success")
        return redirect('/subjects')

    return render_template('form.html',
                           title='Новий предмет',
                           active_page='subjects',
                           form=form)


@app.route('/subjects/edit/<int:subject_id>', methods=('GET', 'POST'))
def edit_subject(subject_id):
    form = forms.SubjectForm()

    subject = models.Subject.get(models.Subject.id == subject_id)

    if form.validate_on_submit():
        models.Subject.create(
            name=form.name.data.strip().capitalize(),
            teacher_id=form.teacher.data
        )

        flash("Запис {} успішно змінений!".format(
            subject_id), "success")
        return redirect('/subjects')

    return render_template('form.html',
                           title='Зміна предмета',
                           active_page='subjects',
                           form=form,
                           record=subject)


@app.route('/subjects/delete/<int:subject_id>', methods=('GET', 'DELETE'))
def delete_subject(subject_id):
    subject = models.Subject.get(models.Subject.id == subject_id)

    subject.delete_instance()

    flash("Запис {} успішно видаленний!".format(
        subject_id), "success")

    return redirect('/subjects')


# ************************** MARK ****************************************


@app.route('/marks')
@app.route('/marks/<int:mark_id>')
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
                               title='Оцінки',
                               active_page='marks',
                               fields=models.Mark.fields,
                               records=marks)


@app.route('/marks/find', methods=('GET', 'POST'))
def find_marks():
    if request.form:
        query_list = []

        for key in request.form:
            if request.form[key] and key != 'csrf_token':
                query_list.append("{}={}".format(key, request.form[key]))

        query = "&&".join(query_list)

        return redirect('/marks?{}'.format(query))

    form = forms.MarkForm()
    return render_template('search_form.html',
                           title='Пошук оцінок',
                           active_page='marks',
                           form=form)


@app.route('/marks/new', methods=('GET', 'POST'))
def new_mark():
    form = forms.MarkForm()

    if form.validate_on_submit():
        models.Mark.create(
            subject_id=form.subject.data,
            student_id=form.student.data,
            mark=form.mark.data
        )

        flash("Запис успішно створенний!", "success")
        return redirect('/marks')

    return render_template('form.html',
                           title='Нова оцінка',
                           active_page='marks',
                           form=form)


@app.route('/marks/edit/<int:mark_id>', methods=('GET', 'POST'))
def edit_mark(mark_id):
    form = forms.MarkForm()

    mark = models.Mark.get(models.Mark.id == mark_id)

    if form.validate_on_submit():
        models.Mark.create(
            subject_id=form.subject.data,
            student_id=form.student.data,
            mark=form.mark.data
        )

        flash("Запис {} успішно змінений!".format(
            mark_id), "success")
        return redirect('/marks')

    return render_template('form.html',
                           title='Зміна оцінки',
                           active_page='marks',
                           form=form,
                           record=mark)


@app.route('/marks/delete/<int:mark_id>', methods=('GET', 'DELETE'))
def delete_mark(mark_id):
    mark = models.Mark.get(models.Mark.id == mark_id)

    mark.delete_instance()

    flash("Запис {} успішно видаленний!".format(
        mark_id), "success")

    return redirect('/marks')


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
