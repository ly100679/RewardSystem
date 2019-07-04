from enum import Enum

class ProjectType(Enum):
    project = '0'
    paper = '1'

class Education(Enum):
    college = '0'
    bachelor = '1'
    master = '2'
    doctor = '3'

class Category(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'

if __name__ == "__main__":
    print(Category.name)
    print(Category.value)