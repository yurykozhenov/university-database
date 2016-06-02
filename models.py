import random

from peewee import (Model, SqliteDatabase, CharField, IntegerField,
                    SmallIntegerField, ForeignKeyField, Check,
                    OperationalError, fn, JOIN)

from faker import Factory


DATABASE = SqliteDatabase('university.db')


class BaseModel(Model):
    """Base model with some meta information"""
    class Meta:
        database = DATABASE
        order_by = ('-id',)


class Student(BaseModel):
    """Student model"""
    last_name = CharField()
    first_name = CharField()
    patronymic = CharField()
    group = CharField()
    grade = SmallIntegerField(constraints=[Check('grade > 0 AND grade < 6')])

    @classmethod
    def get_with_average_mark(cls):
        return (Student
                .select(Student, fn.Avg(Mark.mark).alias('average_mark'))
                .join(Mark, JOIN.LEFT_OUTER)
                .group_by(Student)
                .order_by(fn.Avg(Mark.mark).desc()))

    @classmethod
    def get_good_students(cls):
        return (Student
                .select(Student, fn.Avg(Mark.mark).alias('average_mark'))
                .join(Mark, JOIN.LEFT_OUTER)
                .group_by(Student)
                .having(fn.Avg(Mark.mark) >= 4)
                .order_by(fn.Avg(Mark.mark).desc()))

    @classmethod
    def get_excellent_students(cls):
        return (Student
                .select(Student, fn.Avg(Mark.mark).alias('average_mark'))
                .join(Mark, JOIN.LEFT_OUTER)
                .group_by(Student)
                .having(fn.Avg(Mark.mark) == 5)
                .order_by(fn.Avg(Mark.mark).desc()))

    @classmethod
    def create_random_student(cls):
        """Fill database with random student"""

        fake = Factory.create('uk_UA')

        groups = ["ІН", "ПМ", "КІ", "КН", "АУТП"]

        random_grade = random.randint(1, 5)

        if random.choice([True, False]):
            Student.create(
                last_name=fake.last_name(),
                first_name=fake.first_name_male(),
                patronymic=fake.first_name_male()+"ович",
                group="{}-{}{}".format(
                    random.choice(groups),
                    random_grade,
                    random.randint(1, 3)
                ),
                grade=random_grade
            )

        else:
            Student.create(
                last_name=fake.last_name(),
                first_name=fake.first_name_female(),
                patronymic=fake.first_name_male()+"івна",
                group="{}-{}{}".format(
                    random.choice(groups),
                    random_grade,
                    random.randint(1, 3)
                ),
                grade=random_grade
            )


class Teacher(BaseModel):
    """Teacher model"""
    last_name = CharField()
    first_name = CharField()
    patronymic = CharField()
    department = CharField(null=True)
    position = CharField(null=True)

    @classmethod
    def create_random_teacher(cls):
        """Fill database with random teacher"""

        fake = Factory.create('uk_UA')

        positions = [
            "Асистент",
            "Старший викладач",
            "Доцент",
            "Професор"
        ]

        departments = [
            "Комп'ютерних наук",
            "Автоматизації, електротехнічних та "
            "комп'ютерно-інтегрованих "
            "технологій",
            "Вищої математики",
            "Обчислювальної техніки",
            "Прикладної математики"
        ]

        if random.choice([True, False]):
            Teacher.create(
                last_name=fake.last_name(),
                first_name=fake.first_name_male(),
                patronymic=fake.first_name_male()+"ович",
                department=random.choice(departments),
                position=random.choice(positions)
            )

        else:
            Teacher.create(
                last_name=fake.last_name(),
                first_name=fake.first_name_female(),
                patronymic=fake.first_name_male()+"івна",
                department=random.choice(departments),
                position=random.choice(positions)
            )


class Subject(BaseModel):
    """Subject model"""
    name = CharField()
    teacher = ForeignKeyField(Teacher, related_name='subjects', null=True)

    @classmethod
    def create_random_subject(cls, n_teachers=10):
        """Fill database with random subject"""

        fake = Factory.create('uk_UA')

        Subject.create(
            name=fake.word().capitalize(),
            teacher=random.randint(1, n_teachers)
        )


class Mark(BaseModel):
    """Mark model"""
    subject = ForeignKeyField(Subject, related_name='marks')
    student = ForeignKeyField(Student, related_name='marks')
    mark = IntegerField()

    @classmethod
    def create_random_mark(cls, n_subjects=10, n_students=10):
        """Fill database with random mark"""

        Mark.create(
            subject=random.randint(1, n_subjects),
            student=random.randint(1, n_students),
            mark=random.randint(2, 5)
        )


def initialize():
    """Connect to database

    Create tables based on models

    Fill created tables with some test data
    """
    DATABASE.connect()

    try:
        print("Initializing database...")
        DATABASE.create_tables([Student, Teacher, Subject, Mark])
        fill_db(40, 20, 30, 200)
        print("Database was successfully initialized!")

    except OperationalError:
        print("Database already initialized!")

    DATABASE.close()


def fill_db(n_students=0, n_teachers=0, n_subjects=0, n_marks=0):
    """Fill database with dummy data

    n_* -> number of rows created in table *

    """

    for _ in range(n_students):
        Student.create_random_student()

    for _ in range(n_teachers):
        Teacher.create_random_teacher()

    for _ in range(n_subjects):
        Subject.create_random_subject(n_teachers)

    for _ in range(n_marks):
        Mark.create_random_mark(n_subjects, n_students)
