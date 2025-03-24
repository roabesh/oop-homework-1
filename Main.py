class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_courses(self, course_name):
        self.finished_courses.append(course_name)

    def rate_lecturer(self, lecturer, course, grade):
        if not (1 <= grade <= 10):
            return 'Ошибка: оценка должна быть от 1 до 10'
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка: можно оценивать только лекторов'
        if course not in self.courses_in_progress:
            return 'Ошибка: студент не изучает этот курс'
        if course not in lecturer.courses_attached:
            return 'Ошибка: лектор не ведет этот курс'

        if course in lecturer.grades:
            lecturer.grades[course] += [grade]
        else:
            lecturer.grades[course] = [grade]
        return 'Оценка добавлена'

    def calculate_avg_grade(self):
        """Вычисление средней оценки студента по всем курсам."""
        if not self.grades:
            return 0.0
        all_grades = [grade for course_grades in self.grades.values() for grade in course_grades]
        return round(sum(all_grades) / len(all_grades), 1)

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\nЗавершенные курсы: {', '.join(self.finished_courses)}\nКурсы в процессе: {', '.join(self.courses_in_progress)}"

    def __lt__(self, other):
        """Сравнение студентов по средней оценке."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.calculate_avg_grade() < other.calculate_avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.calculate_avg_grade() == other.calculate_avg_grade()

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def calculate_avg_grade(self):
        if not self.grades:
            return 0.0
        all_grades = [grade for course_grades in self.grades.values() for grade in course_grades]
        return round(sum(all_grades) / len(all_grades), 1)

    def __str__(self):
        avg_grade = self.calculate_avg_grade()
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade}"

    def __lt__(self, other):
        """Сравнение лекторов по средней оценке."""
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.calculate_avg_grade() < other.calculate_avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.calculate_avg_grade() == other.calculate_avg_grade()

class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"

# Функции для подсчета средней оценки по курсу
def average_student_grade(course, students):
    """Средняя оценка студентов за домашние задания по конкретному курсу."""
    grades = [student.grades[course] for student in students if course in student.grades]
    all_grades = [grade for sublist in grades for grade in sublist]
    return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0


def average_lecturer_grade(course, lecturers):
    """Средняя оценка лекторов за лекции по конкретному курсу."""
    grades = [lecturer.grades[course] for lecturer in lecturers if course in lecturer.grades]
    all_grades = [grade for sublist in grades for grade in sublist]
    return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0.0

# тестирование
# Тестирование
student1 = Student('Петя', 'Иванов', 'муж')
student1.finished_courses += ['Git']
student1.courses_in_progress += ['Python']
student1.grades['Git'] = [10, 8, 9, 10, 10]
student1.grades['Python'] = [10, 9]

student2 = Student('Аня', 'Смирнова', 'жен')
student2.finished_courses += ['SQL']
student2.courses_in_progress += ['Python']
student2.grades['Python'] = [7, 8, 9]

reviewer1 = Reviewer('Якоб', 'Ингебритцен')
reviewer1.courses_attached += ['Python']
reviewer1.rate_hw(student1, 'Python', 9)
reviewer1.rate_hw(student2, 'Python', 10)

lecturer1 = Lecturer('Сергей', 'Макаренко')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('Мария', 'Попова')
lecturer2.courses_attached += ['Python']

student1.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer1, 'Python', 10)
student2.rate_lecturer(lecturer2, 'Python', 8)
student2.rate_lecturer(lecturer2, 'Python', 7)

# Вывод результатов
print(student1)
print(student2)
print(lecturer1)
print(lecturer2)
print(reviewer1)

# Проверка сравнения
print(student1 > student2)
print(lecturer1 < lecturer2)

# Средняя оценка за курс
print(average_student_grade('Python', [student1, student2]))
print(average_lecturer_grade('Python', [lecturer1, lecturer2]))
