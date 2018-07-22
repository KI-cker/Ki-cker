from kicker.SymbolMapper import SymbolMapper


class ConsoleView(object):
    def __init__(self):
        self.header = "Current user input state:"
        self.pattern = "{0: <30}{1}     {2}     {3}     {4}"
        self.mapper = SymbolMapper()

    def renderView(self, inputs):
        mapped = self.mapper.inputs2symbols(inputs)
        rotation = mapped[1::2]
        translation = mapped[0::2]
        self.clearView()
        self.printHeader(inputs)
        self.printSeparator()
        self.printNewline(2)
        self.printRotation(rotation)
        self.printNewline(2)
        self.printTranslation(translation)
        self.printNewline(2)
        self.printSeparator()

    def printSeparator(self):
        print("-" * 60)

    def printHeader(self, inputs):
        print(self.header, inputs)

    def printRotation(self, rotation):
        print(self.pattern.format(" ", "G", "D", "M", "S"))
        self.printNewline(1)
        print(self.pattern.format("Rotation",
                                  rotation[0], rotation[1], rotation[2], rotation[3]))
        # print self.pattern.format("Rotation ", **rotation)

    def printTranslation(self, translation):
        print(self.pattern.format(" ", "G", "D", "M", "S"))
        self.printNewline(1)
        print(self.pattern.format("Translation ",
                                  translation[0], translation[1], translation[2], translation[3]))
        # print self.pattern.format("Translation", **translation)

    def printNewline(self, number):
        print("\n" * number,)

    def clearView(self):
        import os
        os.system('clear')
