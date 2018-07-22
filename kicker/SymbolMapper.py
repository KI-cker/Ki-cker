class SymbolMapper(object):

    def __init__(self):
        self.symbolmap = {0: '0', 1: '+', -1: '-'}

    @staticmethod
    def normalize(value):
        return 0 if value == 0 else value / abs(value)

    def inputs2symbols(self, inputs):
        return map(
            lambda value: self.symbolmap[SymbolMapper.normalize(value)], inputs)
