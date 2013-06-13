
keys_dict = {
    'text_input': '<input type="text" name="{name}">{desc}',
    'radiobutton': '<input type="radio" name="table" value="{desc}" checked>{desc}'
}


class Parser(object):
    def __init__(self):
        self.outputs = {}
        self.results = {}
        self.tags = []
        self.content = []

        self.fields = []

    def clear(self):
        self.__init__()

    def read_file(self, filename):
        with open(filename) as f:
            for line in f:
                if '\n' == line:
                    pass
                else:
                    self.content.append(line)

    def parse(self):
        def check_key(key):
            if key.startswith('output'):
                if key.startswith('output_text'):
                    value = key.strip().split(': ')[1]
                    self.outputs['text'] = value

            elif key.startswith('text'):
                try:
                    value = key.strip().split(': ')[1]
                    key = key.strip().split(': ')[0]
                    self.fields.append(value)
                except IndexError:
                    pass

                try:
                    tag = keys_dict[key].format(name=value, desc=value)
                    return tag
                except KeyError:
                    return

            elif key.startswith('radio'):
                try:
                    value = key.strip().split(': ')[1]
                    key = key.strip().split(': ')[0]
                except IndexError:
                    pass

                try:
                    tag = keys_dict[key].format(name=value, desc=value)
                    return tag
                except KeyError:
                    return

        for item in self.content:
            tag = check_key(item)
            if tag:
                self.tags.append(tag)

    def process(self, filename):
        self.read_file(filename)
        self.parse()

    def get_tags(self):
        return self.tags

    def get_outputs(self):
        return self.outputs



if __name__== '__main__':

    parser = Parser()
    parser.process('func.py')
    for tag in parser.get_tags():
        print tag
