import os
from functools import partial
from pathlib import Path

from ruamel.yaml import YAML
from dictscanfold.dircmds import Actions

yaml = YAML()


def traverse_dictdir(doc, on_node=None, path=None, actions=None):
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
            traverse_dictdir(v, on_node=on_node, path=the_path, actions=actions)
        else:
            cmd = on_node(the_path, v, ntype='leaf')
            actions.append(cmd)
    return actions


def node_to_action(parent_ps, content, **kw):
    from dictscanfold import dircmds
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
    doc_h = read_doc_from_file(src)
    doc = doc_h[root]
    actions: Actions = traverse_dictdir(
        doc,
        on_node=partial(node_to_action, force_write=force_write),
        path=dest,
        actions=Actions()
    )
    return actions


def scanfold(src, dest='.', force_write=False, root='root',
             dry=False, bash_script=False):
    actions = scanfold_dry(src, dest=dest, force_write=force_write, root=root)
    if dry:
        return actions
    elif bash_script:
        return actions.make_bash_script()
    else:
        result = actions.exec_py_func()
        return result


if __name__ == '__main__':
    import fire
    fire.Fire()
