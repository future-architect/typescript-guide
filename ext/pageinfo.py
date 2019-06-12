# -*- coding: utf-8 -*-

from docutils.utils import column_width
from docutils import nodes


DOMAIN_NAME = 'pageinfo'
DEFAULT_PAGEINFO = {
    'char_count': 0,
    'half_char_count': 0,
    'full_char_count': 0,
    'ascii_count': 0,
    'nonascii_count': 0,
}


def doctree_resolved(app, doctree, docname):
    domain_data = app.env.domaindata.setdefault(DOMAIN_NAME, {})
    pageinfo = domain_data.setdefault(docname, DEFAULT_PAGEINFO.copy())

    for node in doctree.traverse(nodes.Text):
        text = node.astext()
        for c in text:
            if column_width(c) == 1:
                pageinfo['ascii_count'] += 1
                pageinfo['half_char_count'] += 1
                pageinfo['full_char_count'] += 0.5
            else:
                pageinfo['nonascii_count'] += 1
                pageinfo['half_char_count'] += 2
                pageinfo['full_char_count'] += 1
        pageinfo['char_count'] += len(text)


def html_page_context(app, pagename, templatename, context, doctree):
    if pagename:
        extras = app.env.domaindata.get(DOMAIN_NAME, {}).get(pagename, {})
        context.update(extras)


def setup(app):
    app.connect('doctree-resolved', doctree_resolved)
    app.connect('html-page-context', html_page_context)
