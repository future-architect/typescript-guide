from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.locale import _

def frontmatter(name, arguments, options, content, lineno,
                content_offset, block_text, state, state_machine):
    return [nodes.raw(
        '',
        r"""
\include{tobiraura}
\frontmatter
\setcounter{page}{3}
""",
        format='latex')]

def mainmatter(name, arguments, options, content, lineno,
               content_offset, block_text, state, state_machine):
    return [nodes.raw(
        '',
        r"""
\withintoctrue
\tableofcontents
\withintocfalse
\mainmatter
""",
        format='latex')]

def backmatter(name, arguments, options, content, lineno,
              content_offset, block_text, state, state_machine):
    return [nodes.raw(
        '',
        r"""
\backmatter
""",
        format='latex')]

def appendix(name, arguments, options, content, lineno,
              content_offset, block_text, state, state_machine):
    return [nodes.raw(
        '',
        r"""
\appendix
""",
        format='latex')]

def setup(app):
    app.add_directive('frontmatter', frontmatter, 1, (0, 0, 0))
    app.add_directive('mainmatter', mainmatter, 1, (0, 0, 0))
    app.add_directive('appendix', appendix, 1, (0, 0, 0))
    app.add_directive('backmatter', backmatter, 1, (0, 0, 0))
