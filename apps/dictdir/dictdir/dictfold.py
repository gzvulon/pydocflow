import os
from functools import partial
from pathlib import Path

from dictdir import dircmds


def traverce_dir(path: Path, exceptions=None):
    exceptions = exceptions or [
        '.git',
        '.venv',
        'out',
        '.vscode',
        '.idea',
        '.egg',
        '.eggs',
        '.pytest_cache',
        '__pycache__',
        '.DS_Store'
    ]
    if path.is_file():
        if path.suffix in ['.yml', '.txt', '.cfg', '.spec', '.py', '.md', '.covrc', '.yapf'
                           ] or path.name in '.covrc':
            text = path.read_text()
            if '\n' in text:
                from ruamel.yaml.scalarstring import LiteralScalarString
                literal = LiteralScalarString
                text = literal(text)
            return text

    elif path.is_dir():
        rs = {}
        its = sorted(path.iterdir(), key=lambda x: '0' if x.is_dir() else '1' + str(x))
        for it in its:
            if it.name in exceptions:
                continue
            rs[it.name] = traverce_dir(it)
        return rs
    else:
        raise ValueError()



def traverse_dictdir(doc, on_node=None, path=None, actions=None):
    """Walk on directory descriptor doc invokes actions
    :param doc: directory descriptor
    :param on_node: function to call on each node
    :param path: current path in dirdoc
    :param actions: Actions list to fill
    :return: actions list
    """
    path = path or []
    actions = actions if actions is not None else []

    if isinstance(path, str):
        path = Path(path)
    if isinstance(path, Path):
        path = list(path.parts)

    for k, v in doc.items():
        the_path = path + [k]
        if isinstance(v, dict):
            cmd = on_node(the_path, v, ntype='node')
            actions.append(cmd)
            traverse_dictdir(v,
                             on_node=on_node,
                             path=the_path,
                             actions=actions)
        else:
            cmd = on_node(the_path, v, ntype='leaf')
            actions.append(cmd)
    return actions


def node_to_action(parent_ps, content, **kw):
    ntype = kw.pop('ntype')
    path_p = Path(os.path.join(*parent_ps))
    if ntype == 'leaf':
        cmd = dircmds.WriteIfNotPresent(path=path_p, content=content, **kw)
    elif ntype == 'node':
        cmd = dircmds.EnsureDir(path=path_p, **kw)
    else:
        raise ValueError(ntype)
    return cmd


def read_doc_from_file(path):
    from pathlib import Path
    from ruamel.yaml import YAML
    yaml = YAML()
    with Path(path).open() as fp:
        doc = yaml.load(fp)
        return doc


def scanfold_dry(src, dest='.', force_write=False, root='root'):
    """ Unfold single yaml or json into full dir structure
    :param src: path to dictdir
    :param dest: unpack to dest
    :param force_write: rewrite ini files
    :param root: root node in document
    :return:
    """
    if isinstance(src, str):
        doc_h = read_doc_from_file(src)
    elif isinstance(src, dict):
        doc_h = src
    else:
        raise ValueError(f"src type not allowed: {type(src)}")

    doc = doc_h[root] if root not in [None, 'None', 'no', '', False] else doc_h

    actions: dircmds.Actions = traverse_dictdir(doc,
                                                on_node=partial(
                                                    node_to_action,
                                                    force_write=force_write),
                                                path=dest,
                                                actions=dircmds.Actions())

    return actions


def scanfold(src,
             dest='.',
             force_write=False,
             root='root',
             dry=False,
             bash_script=False,
             bash_shell=False):
    actions = scanfold_dry(src, dest=dest, force_write=force_write, root=root)
    if dry:
        return actions
    elif bash_script:
        return actions.make_bash_script()
    elif bash_shell:
        return actions.exec_bash_shell()
    else:
        result = actions.exec_py_func()
        return result




def folddir(src):
    from ruamel.yaml import  YAML
    from ruamel.yaml.scalarstring import FoldedScalarString
    from ruamel.yaml.scalarstring import LiteralScalarString
    folded = FoldedScalarString
    literal = LiteralScalarString

    yaml = YAML()

    res = traverce_dir(src)
    p = Path('/Users/ivanne/wss/pers/pydocflow/dictdir/dictdir/out/0_cur')
    dp = p / 'ff.yml'
    yaml.dump(res, dp)
    return dp

def test__wer():
    p_test = Path('/Users/ivanne/wss/pers/pydocflow/dictdir/dictdir/data4tests/python_basic')
    dp = folddir(p_test)
    scanfold(str(dp), str(dp.parent), root=None)

#
# if __name__ == '__main__':
#     import fire
#     import dictdir
#     d = {method.__name__: method for method in dictdir.__all__}
#     fire.Fire(d)
