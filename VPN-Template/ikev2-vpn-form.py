from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('ikev2-temp.txt')

#create a dictionary with user input to pass the variables


output = template.render()
print(output)
