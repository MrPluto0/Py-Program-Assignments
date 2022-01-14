class User:
    # 类属性
    __count = 0

    def __init__(self, token, id=None, type=0):
        self._token = token
        self._id = id
        # 0 for student, 1 for teacher, 2 for manager
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

