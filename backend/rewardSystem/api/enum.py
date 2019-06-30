from enum import Enum

class ProjectType(Enum):
    project = 'Project'
    paper = 'Paper'

class Education(Enum):
    college = 'college'
    bachelor = 'bachelor'
    master = 'master'
    doctor = 'doctor'

class Category(Enum):
    A = '机械与控制'
    B = '信息技术'
    C = '数理'
    D = '生命科学'
    E = '能源化工'
    F = '哲学社会科学'

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
