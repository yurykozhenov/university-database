from flask_wtf import Form
from wtforms import (StringField, IntegerField)
from wtforms.validators import (DataRequired, NumberRange, Regexp)


class StudentForm(Form):
    last_name = StringField("Прізвище", validators=[DataRequired()])

    first_name = StringField("Ім'я", validators=[DataRequired()])

    patronymic = StringField("По батькові",
                             validators=[DataRequired()])

    group = StringField("Група", validators=[
        DataRequired(),
        Regexp(
            r'^[А-Яа-яЄІЇҐєіїґ]{2,}-[0-9]{2}$',
            message=("Назва групи має бути у форматі "
                     "[букви]-[курс][номер_групи]")
        )
    ])

    grade = IntegerField("Курс", validators=[
        DataRequired(),
        NumberRange(min=1, max=5,
                    message=("Курс має бути від 1 до 5"))
    ])


class TeacherForm(Form):
    last_name = StringField("Прізвище", validators=[DataRequired()])

    first_name = StringField("Ім'я", validators=[DataRequired()])

    patronymic = StringField("По батькові",
                             validators=[DataRequired()])

    department = StringField("Кафедра")

    position = StringField("Посада")


class SubjectForm(Form):
    name = StringField("Назва предмета",
                       validators=[DataRequired()])

    teacher = IntegerField("Викладач")


class MarkForm(Form):
    subject = IntegerField("Предмет")

    student = IntegerField("Студент")

    mark = IntegerField("Оцінка", validators=[
        DataRequired(),
        NumberRange(min=1, max=5,
                    message=("Оцінка має бути від 1 до 5"))
    ])
