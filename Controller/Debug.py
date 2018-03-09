from enum import Enum

print('File level scope')

class OuterClass:

    class InnerClass(Enum):
        V1 = 1,
        V2 = 2,
        V3 = 3

        # def __init__(self):
        #     print('__init(InnerClass)')


    def __init__(self):
        self.Value1 = OuterClass.InnerClass.V1
        self.Value2 = OuterClass.InnerClass.V2

    def TestMe(self, val1 = None):
        _val1 = OuterClass.InnerClass.V1


def main():
    c1 = OuterClass()
    c1.TestMe()

if __name__ == '__main__':
    print('__main()__')
    main()