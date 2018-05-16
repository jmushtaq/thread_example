class Hello():
    """ to test:
            python hello.py
    """
    def __init__(self, name):
        self.name = name

    def write(self):
        print('Hello {}'.format(self.name))

if __name__ == '__main__':
        Hello('friend').write()
