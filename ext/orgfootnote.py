from docutils import nodes
from sphinx.writers.latex import LaTeXTranslator

def visit_collected_footnote(self, node):
    # type: (nodes.Node) -> None
    self.in_footnote += 1
    if 'footnotetext' in node:
        self.body.append('\\footnotetext{')
    else:
        if self.in_parsed_literal:
            self.body.append('\\footnote{')
        else:
            self.body.append('\\footnote{')

def depart_collected_footnote(self, node):
    # type: (nodes.Node) -> None
    if 'footnotetext' in node:
        self.body.append('}\\ignorespaces ')
    else:
        if self.in_parsed_literal:
            self.body.append('}')
        else:
            self.body.append('}')
    self.in_footnote -= 1

def setup(app):
  LaTeXTranslator.visit_collected_footnote = visit_collected_footnote
  LaTeXTranslator.depart_collected_footnote = depart_collected_footnote
