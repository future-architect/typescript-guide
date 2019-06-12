# coding:utf-8
from docutils import nodes, utils
from sphinx.util.nodes import split_explicit_title
from sphinx import addnodes
from sphinx.writers.latex import LaTeXTranslator
from six import u

def numdoc_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for making latex ref to the doc head."""
    env = inliner.document.settings.env
    
    text = utils.unescape(text)
    has_explicit, title, target = split_explicit_title(text)
    
    pnode = nodes.inline(rawtext, title, classes=['xref','doc'])
    pnode['reftarget'] = target

    return [pnode], []

def visit_inline(self, node):
    # type: (nodes.Node) -> None
    classes = node.get('classes', [])
    if classes in [['menuselection'], ['guilabel']]:
        self.body.append(r'\sphinxmenuselection{')
        self.context.append('}')
    elif classes in [['accelerator']]:
        self.body.append(r'\sphinxaccelerator{')
        self.context.append('}')
    elif classes in [['xref','doc']] and not self.in_title:
        self.body.append(ur'第\DUrole{%s}{' % ','.join(classes))
        self.context.append(u'}章')
    elif classes and not self.in_title:
        self.body.append(r'\DUrole{%s}{' % ','.join(classes))
        self.context.append('}')
    else:
        self.context.append('')

def setup(app):
    app.add_role('numdoc', numdoc_role)
    LaTeXTranslator.visit_inline = visit_inline

