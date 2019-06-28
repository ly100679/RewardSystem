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