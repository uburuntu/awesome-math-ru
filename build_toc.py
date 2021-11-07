"""Generate the table of contents and insert it at the top of README.md."""


import re


_HEADER_REGEX = r'([#]+) ([^\n]+)'
_PUNCTUATION_REGEX = r'[^\w\- ]'
_HEADER_TEMPLATE = '{indent}* [{name}](#{anchor})'
_START_TOC = '<!-- START_TOC -->'
_END_TOC = '<!-- END_TOC -->'


def _anchor(name):
    anchor = name.lower().replace(' ', '-')
    anchor = re.sub(_PUNCTUATION_REGEX, '', anchor)
    return anchor


def _parse_header(header):
    r = re.match(_HEADER_REGEX, header)
    if r:
        level = len(r.group(1))
        name = r.group(2)
        return level, _anchor(name), name


def _iter_headers(md):
    headers = (line for line in md.splitlines()
               if line.startswith('#'))
    for header in headers:
        yield header


def _get_header_item(header):
    level, anchor, name = _parse_header(header)
    indent = '    ' * max(0, level - 1)
    return _HEADER_TEMPLATE.format(**locals())


def _gen_items(md):
    for header in _iter_headers(md):
        item = _get_header_item(header)
        yield item


def _read_md(filename):
    with open(filename, 'r') as f:
        return f.read()


def gen_toc(filename):
    md = _read_md(filename)
    i = md.index(_START_TOC) + len(_START_TOC) + 2
    j = md.index(_END_TOC)
    with open(filename, 'w') as f:
        f.write(md[:i])
        for item in _gen_items(md):
            if 'Математический список' in item:
                continue
            if 'Содержание' in item:
                continue
            f.write(item + '\n')
        f.write('\n' + md[j:])


if __name__ == '__main__':
    filename = 'README.md'
    gen_toc(filename)
