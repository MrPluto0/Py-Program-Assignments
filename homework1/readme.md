# Python程序设计#1作业

## 作业题目

### 内容
独立设计并实现一个小型python程序（功能不限），代码需要涉及：class类、对象实例化、继承（分别定义父类和子类）、对象方法（self参数）、类方法（@classmethod）、静态方法（@staticmethod）、对象属性、类属性、多态。

### 代码

```python
import random

class User:
    # 类属性
    __count = 0

    def __init__(self, token, id=None, type=0):
        self._token = token
        self._id = id
        # 0 for student, 1 for teacher
        self._type = type

        self.__count += 1

    @classmethod
    def getUserCount(cls):
        return cls.__count

    @staticmethod
    def printUsersClassInfo():
        print("The User Class has three subclasses:\n" 
              "Student Teacher Manager\n"
              "Student can import the subjects and scores,\n"
              "Teacher can import the subject he/she teaches,\n"
              "Manager can log the student and teacher's data.\n")

    def getUserId(self):
        return self._id

    def setUserId(self, id):
        self._id = id

    def getUserType(self):
        return self._type
    
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
    def showList(cls):
        for student in cls.__students:
            print(f"ID:{student['id']} token:{student['token']}")

    def getStudentSubjects(self):
        return self._subjects

    def addStudentSubject(self, subjectName, score=0):
        self._subjects[subjectName] = int(score)

    def setStudentSubject(self, subjectName, score):
        for subject in self._subjects:
            if subject["name"] == subjectName:
                subject["score"] = score
                break

    def getAverageScore(self):
        sumScore = 0
        for subject in self._subjects:
            sumScore += subject
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
    def showList(cls):
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
                return False
        self._students.append({
            "student": student,
            "score": 0
        })
        student.addStudentSubject(self._subject, 0)


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
    Student.showList()
    print(f"老师总数为{tcount}")
    print(f"老师列表如下")
    Teacher.showList()

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

```

## 代码说明

### 类
基类：User

两个子类：Student和Teacher

本类主要用于统计用户的成绩信息，可以提问与回答问题。

### 属性

成员属性：用户类包含着ID，token，subject等关于基本信息的成员变量。

类属性：类变量包含对该类创建对象个数和内容的统计。

### 方法

成员方法：

包含几个对成员变量的**getter**和**setter**

老师类的`askStudentQues`，可向学生提问，等

学生类的`ansTeacherQues`，可回答老师问题；`getAverageScore`可计算学科平均分，等

类方法：

`getUserCount`，`getStudentCount`，`getTeacherCount`等只需要访问类变量count来查看当前类的创建数量。

两个子类均有`showList`方法，用于展示用户列表，此处可体现多态。

静态方法：

User类下的`printUsersClassInfo`可输出该类的描述信息，并不使用本类的属性或方法。

### 测试运行

输入学生和老师的信息，来创建两个列表；将所有学生循环导入老师的班级中。

随机选择老师来向某个同学提问，输入问题内容，并给出答案，回答正确可加分。









