from docutils import nodes
from docutils.parsers.rst import Directive
#from sphinx.util.compat import make_admonition
from sphinx.locale import _

def setup(app):
    app.add_directive('customenv', CustomenvDirective)
    app.add_node(customenv, 
                 html=(visit_customenv_node, depart_customenv_node),
                 latex=(visit_latex_customenv_node, depart_latex_customenv_node),
                 text=(visit_customenv_node, depart_customenv_node))
    return {'version': '0.1'}

class customenv(nodes.Admonition, nodes.Element):
    pass

def visit_customenv_node(self, node):
    self.visit_admonition(node)

def depart_customenv_node(self, node):
    self.depart_admonition(node)

class CustomenvDirective(Directive):
    has_content = True
    required_arguments = 1
    
    def run(self):
      envname = self.arguments[0]
      env = make_admonition(
              customenv, self.name, [envname], self.options,
              self.content, self.lineno, self.content_offset, 
              self.block_text, self.state, self.state_machine)
      return env

def visit_latex_customenv_node(self, node):
    self.body.append('\n\\begin{customadmonition}')

def depart_latex_customenv_node(self, node):
    self.body.append('\\end{customadmonition}\n')

def make_admonition(node_class, name, arguments, options, content, lineno,
                    content_offset, block_text, state, state_machine):
    text = '\n'.join(content)
    admonition_node = node_class(text)
    if arguments:
        title_text = arguments[0]
        textnodes, messages = state.inline_text(title_text, lineno)
        admonition_node += nodes.title(title_text, '', *textnodes)
        admonition_node += messages
        if 'class' in options:
            classes = options['class']
        else:
            classes = ['admonition-' + nodes.make_id(title_text)]
        admonition_node['classes'] += classes
    state.nested_parse(content, content_offset, admonition_node)
    return [admonition_node]
