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
            Retrieve macros from file content
        """
        for number, line in enumerate(self.content):

            # for pattern in patterns.iterkeys():
            if 'INPUTFIELD_TXT' in line:

                # New value
                value = Value()

                # Find the content of macro
                match = re.search(r'INPUTFIELD_TXT\((.+?)\)', self.content)

                # Get array of user defined fields
                text = match.group(1).split(', ')

                # The name of user defined element (Maybe it should not be defined by user?)
                value.id = text.group(1)

                value.n_stroke = number

                # Add new macro into final list
                self.values.append(value)

                # Paste fields into html-tag
                tag = '{desc} <input type="text" name="{name}">'.format(desc=text[1], name=text[0])

                # Add tag to html list
                self.html.append(tag)

                # Paste name of macro into line and line into the content
                self.content[number] = line.replace(match.group(0), value.id)

    def get_html(self, filename):
        self.load(filename)
        self.get_macros()

        return self.html


    def insert_values(self):
        for value in self.values:
            line = self.content[value.n_stroke]
            self.content[value.n_stroke] = line.replace(value.id, value.val)


    def put_results(self, results):
        """ Put data in values
        :param results: dictionary with results from form response
        """
        for result in results.iterkey():



    def run(self):
        for value in self.values:
            pass






    def get_output(self):
        output = self.content[-1]





    def show_html(self, filename):
        html = '''<form action="result">
                    <br>
                    <br>
    <input type="submit" value="Submit">
    </form>'''