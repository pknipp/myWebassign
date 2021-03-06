from net_assign.models import User, Question, Course, Enrollment, Assignment, Appearance, Deployment
from net_assign import app, db
from dotenv import load_dotenv
from datetime import date, datetime, timedelta
from faker import Faker
from random import randrange, seed, random
from werkzeug.security import generate_password_hash, check_password_hash
import json

seed(1)
fake = Faker()
load_dotenv()

users = [
    ("demoInstructor@aol.com", True),
    ("demoStudent@aol.com", False),
    ]

# number of non-demo users (including demo users)
n_instructors = 8
n_students = 40

with app.app_context():
    db.drop_all()
    db.create_all()
    for i in range(n_instructors + n_students):
        created_at = fake.date_time_between(start_date=datetime(2000, 1, 15))
        db.session.add(User(
            email= users[i][0] if (i < 2) else fake.simple_profile()["mail"],
            is_instructor= i == 0 or (i > 1 and i < n_instructors + 1),
            password="password",
            created_at=created_at,
            updated_at=fake.date_time_between(start_date=created_at)
        ))
    db.session.commit()

questions = [
    (1, True, "{a} plus {b} equals ... ", "a + b", [['a', 2, 3, 10], ['b', 5, 7, 20]]),
    (1, True, "What is the capitol of {state}?", "capital", [[['state','Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming'],['capital','Montgomery','Juneau','Phoenix','Little Rock','Sacramento','Denver','Hartford','Dover','Tallahassee','Atlanta','Honolulu','Boise','Springfield','Indianapolis','Des Moines','Topeka','Frankfort','Baton Rouge','Augusta','Annapolis','Boston','Lansing','St. Paul','Jackson','Jefferson City','Helena','Lincoln','Carson City','Concord','Trenton','Santa Fe','Albany','Raleigh','Bismarck','Columbus','Oklahoma City','Salem','Harrisburg','Providence','Columbia','Pierre','Nashville','Austin','Salt Lake City','Montpelier','Richmond','Olympia','Charleston','Madison','Cheyenne']]]),
    (1, True, "T or F: {animal} have four legs?", "TorF", [[["animal","fish", "birds", "lizards", "snakes", "dogs", "humans", "ants"], ["TorF", "F", "F", "T", "F", "T", "F", "F"]]]),
    (1, True, "{a} times {b} equals ... ","a * b", [['a', -3, -1, 20], ['b', 2, 3, 10]]),
    # (1, True, "{a} divided by {b} equals ... ","a/b", [['a', 2, 4, 20], ['b', 1, 3, 20]]),
    (1, True, "{a} raised to the power of {b} equals ... ", "a^b", [['a', 2, 6, 4], ['b', 2, 5, 3]]),
    (1, False, "The square root of {a} equals ... ", "sqrt(a)", [['a', 2, 99, 97]]),
    (1, True, "{a} times {b} plus {c} equals ... ", "a * b + c", [['a', 2,7,5], ['b', 2,9,7], ['c', 2,15,13]]),
    # (1, True, "The natural logarithm of {a} equals ... ", "log(a)", [['a', 2, 99, 97]]),
    (3, True, "The common logarithm of {a} equals ... ", "log(a)/log(10)", [['a', 2, 99, 97]]),
    # (1, True, "The cosine of {a} rads equals ... ", "cos(a)", [['a', -3, 3, 60]]),
    (3, False, "The arctangent of {a} equals (when expressed in radians) ...", "atan(a)", [['a', -4, 4, 80]]),
    (1, True, "If a girl runs at {a} m/s for {b} hours, how many km does she travel?", "a * b * 3.6", [["a", 4, 7, 30], ['b', 2, 3, 10]]),
    (1, True, "What is the {a}th prime number?", "b", [[['a', 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
                                                          ['b', 7,11,13,17,19,23, 29, 31, 37, 41]]]),
    (1, True, "What is the {power}th power of the {ordinal}th prime number?", "prime^power", [['power', 4, 5, 1], [['ordinal', 4, 5, 6], ['prime', 7, 11, 13]]]),
    ]

with app.app_context():
    for question in questions:
        created_at = fake.date_time_between(start_date=datetime(2000, 1, 15))
        db.session.add(Question(
            instructor_id=question[0],
            is_public=question[1],
            question_code=question[2],
            answer_code=question[3],
            inputs=json.dumps(question[4]),
            created_at=created_at,
            updated_at=fake.date_time_between(start_date=created_at)
        ))
    db.session.commit()

courses = [
"DemoClass",
"Aeronautics",
"Algebra",
"Archaeology",
"Art",
"Astrology",
"Astronomy",
"Biology",
"Botany",
"Chemistry",
"Dance",
"Earth Science",
"Egyptology",
"Engineering",
"French",
"Geography",
"Geology",
"Geometry",
"German",
"Heiroglyphics",
"History",
"Italian",
"Karate",
"Latin",
"Music",
"Physics",
"Portuguese",
"Russian",
"Spanish",
]

with app.app_context():

    for i in range(len(courses)):
        created_at = fake.date_time_between(start_date=datetime(2000, 1, 15))
        instructor_id = 1 if (i == 0 or random() < 1 / n_instructors) else randrange(3, 2 + n_instructors)
        courses[i] = [instructor_id, courses[i]]
        db.session.add(Course(
            instructor_id=instructor_id,
            name=courses[i][1],
            is_public=True,
            created_at=created_at,
            updated_at=created_at,
        ))
    db.session.commit()

# average number of enrollments per student
enrollments_per_student = 4

with app.app_context():
    for i in range(len(courses)):
        course_id = i + 1
        instructor_id = courses[i][0]
        for j in range(n_instructors + n_students):
            student_id = j + 1
            if (student_id == 2 and course_id == 1) or (student_id == instructor_id) or (random() < enrollments_per_student/len(courses) and (student_id == 2 or not student_id <= n_instructors + 1)):
                db.session.add(Enrollment(
                    course_id=course_id,
                    student_id=student_id,
                    created_at=fake.date_time_between(start_date=datetime(2000, 1, 15))
                ))
    db.session.commit()

# average number of assignments per instructor
assignments_per_instructor = 10

with app.app_context():
    for i in range(n_instructors * assignments_per_instructor):
        instructor_id = 1 if (i == 0 or random() < 1/n_instructors) else randrange(3, 1 + n_instructors)
        name = "DemoAssignment" if (i == 0) else fake.text(max_nb_chars=20)[0:-1]
        created_at=fake.date_time_between(start_date=datetime(2000, 1, 15))
        db.session.add(Assignment(
            instructor_id=instructor_id,
            is_public=True,
            name=name,
            created_at=created_at,
            updated_at=fake.date_time_between(start_date=created_at)
        ))
    db.session.commit()

# average number of questions per assignment
questions_per_assignment = 6

with app.app_context():
    for i in range(n_instructors * assignments_per_instructor):
        assignment_id = i + 1
        for j in range(len(questions)):
            question_id = j + 1
            if (assignment_id == 1) or random() < questions_per_assignment/len(questions):
                db.session.add(Appearance(
                    assignment_id=assignment_id,
                    question_id=question_id,
                    created_at=fake.date_time_between(start_date=datetime(2000, 1, 15))
                ))
    db.session.commit()

# average number of questions per assignment
deployments_per_assignment = 2
n_assignments = assignments_per_instructor * n_instructors
n_deployments = n_assignments * deployments_per_assignment

with app.app_context():
    for i in range(len(courses)):
        course_id = i + 1
        for j in range(n_instructors * assignments_per_instructor):
            assignment_id = j + 1
            if (assignment_id == 1 and course_id == 1) or random() < deployments_per_assignment/len(courses):
                created_at=fake.date_time_between(start_date=datetime(2000, 1, 15))
                db.session.add(Deployment(
                    assignment_id=assignment_id,
                    course_id=course_id,
                    created_at=created_at,
                    updated_at=fake.date_time_between(start_date=created_at),
                    deadline=created_at
                ))
    db.session.commit()
