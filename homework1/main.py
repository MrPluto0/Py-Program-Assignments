'''
Descripttion: 
Author: Gypsophlia
Date: 2021-10-20 17:16:56
LastEditTime: 2021-10-20 17:18:36
'''
from users.user import User
from users.student import Student
from users.teacher import Teacher
import random


def fn():
    User.printUsersClassInfo()

    students = []
    teachers = []
    print("不断输入内容，ID为空时结束输入")

    while 1:
        id = input("输入学生ID：")
        if id == "":
            break
        token = input("输入学生Token：")
        students.append(Student(token, id))

    while 1:
        id = input("输入老师ID：")
        if id == "":
            break
        subject = input("输入老师教学科：")
        teachers.append(Teacher(id, subject))
    scount = Student.getStudentCount()
    tcount = Teacher.getTeacherCount()
    print(f"学生总数为{scount}")
    print(f"学生列表如下")
    Student.showStudentsList()
    print(f"老师总数为{tcount}")
    print(f"老师列表如下")
    Teacher.showTeachersList()

    print("将以上学生均加入各老师班级")
    for student in students:
        for teacher in teachers:
            teacher.addStudent(student)

    print("随机选取老师，随机提问：")
    sindex = random.randint(0, scount - 1)
    tindex = random.randint(0, tcount - 1)
    print(f"老师{teachers[tindex].getUserId()}向学生{students[sindex].getUserId()}提问：")

    question = {}
    question["content"] = input("输入题目内容：")
    question["answer"] = input("输入题目答案：")
    question["score"] = input("输入题目分值：")

    teachers[tindex].askStudentQues(students[sindex], question)


if __name__ == '__main__':
    fn()
