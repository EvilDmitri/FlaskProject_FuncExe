from patterns import patterns
import re


values = {}
html = []


def parse(filename):
    content = []
    with open(filename) as f:
        for line in f:
            if '\n' == line:
                pass
            else:
                content.append(line)

    with open(filename+'tmp', 'w') as fw:
        for line in content:
            if 'INPUTFIELD_TXT' in line:
                match = re.search(r'INPUTFIELD_TXT\((.+?)\)', content)
                text = match.grop(1).split(', ')
                values[name] = ''
                tag = '{desc} <input type="text" name="{name}">'.format(desc=text[1], name=text[0])
                html.append(tag)

                line = line.replace(a.group(0), a.group(1))

            fw.write(line)


def insert_values(filename):

    with open(filename) as fr:
        lines = fr.readlines()

    with open(filename, 'w') as fw:
        for line in lines:
            for key in values.iterkeys():
                if key in line:
                    line = line.replace(key, values[key])

            fw.write(line)



def show_html(filename):
    html = '''<form action="result">
                <br>
                <br>
<input type="submit" value="Submit">
</form>'''