from patterns import patterns
import re

class Value:
    def __init__(self):
        self.n_stroke = ''  # number of stroke in content
        self.id = ''        # name of element
        self.val = ''     # value from form


class Parser:

    def __init__(self):
        self.values = []    # List of all macro elements
        self.html = []      # HTML-tags from macros
        self.content = []   # List of lines in file
        self.results = []   # List of results received from form 'post'
        self.output = ''    # Type of output

    def clear(self):
        self.__init__()


    def load(self, filename):
        """Load all file content into list
        :param filename: name of file to parse
        """
        with open(filename) as f:
            for line in f:
                if '\n' == line:
                    pass
                else:
                    self.content.append(line)

    def get_macros(self):
        """
            Retrieve macros from file content and put them into html
            Replace macros with tag names
        """
        for number, line in enumerate(self.content):

            # for pattern in patterns.iterkeys():
            if 'INPUTFIELD_TXT' in line:

                # New value
                value = Value()

                # Find the content of macro
                match = re.search(r'INPUTFIELD_TXT\((.+?)\)', line)

                # Get array of user defined fields
                text = match.group(1).split(', ')

                # The name of user defined element (Maybe it should not be defined by user?)
                value.id = text[0]
                value.id = value.id[1:-1]   # and remove quotes

                value.n_stroke = number

                # Add new macro into final list
                self.values.append(value)

                # Get name of tag and remove quotes
                name = text[0]
                name = name[1:-1]

                # Paste fields into html-tag
                tag = '''{0} <input type="text" name="{1}">'''.format(text[1], name)

                # Add tag to html list
                self.html.append(tag)

                # Paste name of macro into line and line into the content
                self.content[number] = line.replace(match.group(0), value.id)

    def get_html(self, filename):

        form_open = '<form action="/result/{filename}" method=post>'.format(filename=filename.split('/')[-1])
        form_close = '<br><input type=submit value=Execute> </form>'

        self.load(filename)
        self.get_macros()

        html = '<br>'.join(self.html)

        html = form_open + html + form_close

        return html


    def insert_values(self):
        for value in self.values:
            line = self.content[value.n_stroke]
            self.content[value.n_stroke] = line.replace(value.id, value.val)


    def put_results(self, results):
        """ Put data in values
        :param results: dictionary with results from form response
        """

        for value in self.values:
            value.val = results[value.id]
            line = self.content[value.n_stroke]
            self.content[value.n_stroke] = line.replace(value.id, value.val)

        fw = open('temp/t.py', 'w')
        for line in self.content[:-1]:
            fw.write(line)
        fw.flush()
        fw.close()


        a = __import__('temp.t', fromlist=[])

        return str(a.t.c)



    def run(self):
        for value in self.values:
            pass






    def get_output(self):
        output = self.content[-1]

