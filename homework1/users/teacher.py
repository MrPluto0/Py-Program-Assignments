from .user import User
# from .student import Student
import logging


class Teacher(User):
    __teaCount = 0
    __teachers = []

    def __init__(self, id, subject, token=None):
        self._subject = subject
        super().__init__(token, id, 1)
        Teacher.__teaCount += 1
        self._students = []
        self.__teachers.append({
            "id": id,
            "subject": subject,
        })

    @classmethod
    def getTeacherCount(cls):
        return cls.__teaCount

    @classmethod
    def showTeachersList(cls):
        for teacher in cls.__teachers:
            print(f"ID:{teacher['id']} Subject:{teacher['subject']}")

    def askStudentQues(self, student, question: dict):
        for s in self._students:
            if s["student"].getUserId() == student.getUserId():
                if student.ansTeacherQues(self, question):
                    s["score"] += int(question["score"])
                    print(f"学生{student.getUserId()}回答正确，老师给其加分{question['score']}")
                else:
                    print(f"学生{student.getUserId()}回答错误")

    def getSubject(self):
        return self._subject

    def getStudents(self):
        return self._students

    def addStudent(self, student):
        for s in self._students:
            if s["student"].getUserId() == student.getUserId():
                logging.warning("该学生已存在")
                return False
        self._students.append({
            "student": student,
            "score": 0
        })
        student.addStudentSubject(self._subject, 0)
