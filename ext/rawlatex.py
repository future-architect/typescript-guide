# coding:utf-8
from docutils import nodes, utils
from sphinx.util.nodes import split_explicit_title

def tex_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """Role for inserting latex code as is."""
    text = utils.unescape(text, restore_backslashes=True)
    has_explicit, texsnipet, target = split_explicit_title(text)
    
    pnode = nodes.raw(rawtext, texsnipet, format='latex')

    return [pnode], []

def setup(app):
    app.add_role('tex', tex_role)

