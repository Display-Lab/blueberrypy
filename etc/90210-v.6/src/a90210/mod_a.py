import maya

def hello() -> str:
    now = maya.now()
    return "Hi there! It's " + now.iso8601()


if __name__ == '__main__':
    print(hello())