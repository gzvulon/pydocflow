from pathlib import Path
from pprint import pprint

from ruamel.yaml import YAML

yaml = YAML()


def traverse(doc, on_node=None, path=None):
    path = path or []
    if isinstance(path, str):
        path = [path]

    for k, v in doc.items():
        the_path = path + [k]
        if isinstance(v, dict):
            on_node(the_path, v, ntype='node')
            traverse(v, on_node=on_node, path=the_path)
        else:
            on_node(the_path, v, ntype='leaf')
    return path


def test__traverse_simple():
    doc = {'mf.txt': "", 'tmp': {'be.txt': '123d'}}
    actions = []

    def register(p, v, **kw):
        ntype = kw.pop('ntype')
        path_p = Path('/'.join(p))
        if ntype == 'leaf':
            cmd = f"touch {path_p}"
        elif ntype == 'node':
            cmd = f"mkdir -p {path_p}"
        else:
            raise ValueError(ntype)
        actions.append(cmd)

    traverse(doc, on_node=register, path='.')

    pprint(actions)


def test__traverse_smart(force_content=False):
    doc = {'mf.txt': "", 'tmp': {'be.txt': '123d'}}
    actions = []
    if force_content:
        prefix = " "
    else:
        prefix = "test -f file || "

    create_tmpl = """{prefix} cat << EOF > {file}
        {content}
        EOF
    """

    def register(p, v, **kw):
        ntype = kw.pop('ntype')
        path_p = Path('/'.join(p))
        if ntype == 'leaf':
            cmd = create_tmpl.format(prefix=prefix, file=path_p, content=v)
        elif ntype == 'node':
            cmd = f"mkdir -p {path_p}"
        else:
            raise ValueError(ntype)
        actions.append(cmd)

    traverse(doc, on_node=register, path='.')

    for cmd in actions:
        print(cmd)