from jinja2 import Template

tem = Template("Hello {{name}}!")
print(tem.render(name="Ryan"))
