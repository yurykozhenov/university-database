import random

from peewee import (Model, SqliteDatabase, CharField, IntegerField,
                    SmallIntegerField, ForeignKeyField, Check,
                    OperationalError)

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
            "Автоматизації, електротехнічних та комп'ютерно-інтегрованих технологій",
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
    def create_random_subject(cls):
        """Fill database with random subject"""

        fake = Factory.create('uk_UA')

        Subject.create(
            name=fake.word().capitalize(),
            teacher=random.randint(1, 10)
        )


class Mark(BaseModel):
    """Mark model"""
    subject = ForeignKeyField(Subject, related_name='marks')
    student = ForeignKeyField(Student, related_name='marks')
    mark = IntegerField()

    @classmethod
    def create_random_mark(cls):
        """Fill database with random mark"""

        Mark.create(
            subject=random.randint(1, 10),
            student=random.randint(1, 10),
            mark=random.randint(1, 5)
        )


def initialize():
    """Connect to database

    Create tables based on models

    Fill created tables with some test data
    """
    try:
        DATABASE.connect()
        DATABASE.create_tables([Student, Teacher, Subject, Mark])

        fill_db(10)

        DATABASE.close()
    except OperationalError:
        print("Database already created")


def fill_db(n):
    """Fill database with dummy data

    n -> number of rows created in each table

    """

    for _ in range(n):
        Student.create_random_student()
        Teacher.create_random_teacher()
        Subject.create_random_subject()
        Mark.create_random_mark()
