t = {
    'a': 5,
    'b': 6
}
def a(t):
    t['a'] = 11

t2 = 1

def b(t2):
    t2 = 12

if __name__ == "__main__":
    a(t)
    print(t)
    b(t2)
    print(t2)