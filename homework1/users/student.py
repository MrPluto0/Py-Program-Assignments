from .user import User
# from .teacher import Teacher
import logging


class Student(User):
    __stuCount = 0
    __students = []

    def __init__(self, token, id=None, subjects={}):
        super().__init__(token, id, 1)
        self._subjects = subjects
        Student.__stuCount += 1
        Student.__students.append({
            "token": token,
            "id": id
        })

    @classmethod
    def getStudentCount(cls):
        return cls.__stuCount

    @classmethod
    def showStudentsList(cls):
        for student in cls.__students:
            print(f"ID:{student['id']} token:{student['token']}")

    def getStudentSubjects(self):
        return self._subjects

    def addStudentSubject(self, subjectName, score=0):
        self._subjects[subjectName] = score

    def setStudentSubject(self, subjectName, score):
        for subject in self._subjects:
            if subject["name"] == subjectName:
                subject["score"] = score
                break

    def getAverageScore(self):
        sumScore = 0
        for subject in self._subjects:
            sumScore += subject["score"]
        return sumScore / len(self._subjects)

    def ansTeacherQues(self, teacher, question: dict):
        ans = input(f"输入问题{question['content']}的答案：")
        if ans == question["answer"]:
            print("Excellent，回答正确")
            self._subjects[teacher.getSubject()] += int(question["score"])
            return True
        else:
            print("Sorry，回答错误")
            return False
