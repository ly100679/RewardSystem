from enum import Enum

class ProjectType(Enum):
    project = '0'
    paper = '1'
    def switch(i):
        if i == 0:
            return ProjectType.project
        else:
            return ProjectType.paper

class Education(Enum):
    college = '0'
    bachelor = '1'
    master = '2'
    doctor = '3'
    def switch(i):
        if i == 0:
            return Education.college
        elif i == 1:
            return Education.bachelor
        elif i == 2:
            return Education.master
        elif i == 3:
            return Education.doctor

class Category(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    def switch(i):
        return Category[i]

class ProjectStatus(Enum):
    A = '未提交'
    B = '已提交'
    C = '审核中'
    D = '初审通过'
    E = '初审未通过'
    F = '评审中'
    G = '现场答辩'
    H = '未进入线下'
    I = '一等奖'
    J = '二等奖'
    K = '三等奖'

if __name__ == "__main__":
    s1 = 'B'
    s2 = 'A'
    tem = Category[s1].value
    print(tem)
    # print (t.name)