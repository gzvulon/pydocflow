from functools import partial

# ===Executors===


def exec_py_func(actions, **kw):
    changes = []
    for act in actions:
        func = act.render_py()
        change = func(**kw)
        changes.append(change)
    res = sum(changes)
    return res


def exec_bash_shell(actions, **kw):
    import os
    changes = []
    for act in actions:
        cmd = act.render_bash_shell()
        change = os.system(cmd)
        changes.append(change)
    res = sum(changes)
    return res


def make_bash_script(actions, **kw):
    changes = []
    for act in actions:
        cmd = act.render_bash_script()
        changes.append(cmd)
    res = "\n\n".join(changes)
    return res


class Actions(list):
    exec_py_func = exec_py_func
    exec_bash_shell = exec_bash_shell
    make_bash_script = make_bash_script


# ===Commands===


def write_if_new(path=None, content=None, force_write=False):
    from pathlib import Path
    pp = Path(path)
    if force_write or not pp.exists():
        pp.write_text(content)
        return 1
    return 0


class WriteIfNotPresent:
    def __init__(self, path=None, content=None, force_write=None):
        self.path = path
        self.content = content
        self.force_write = force_write

    def render_bash_shell(self, force_write=None, **kw):
        bash_write_text = f"cat << EOF > {self.path}\n{self.content}"
        prefix = " " if force_write else f"test -f {self.path} || "
        bash_cmd = prefix + bash_write_text
        return bash_cmd

    def render_bash_script(self, force_write=None, **kw):
        bash_cmd = self.render_bash_shell(force_write=force_write, **kw)
        return bash_cmd + '\nEOF'

    def render_py(self, force_write=None, **kw):

        py_cmd = partial(write_if_new, path=self.path,
                         content=self.content,
                         force_write=force_write)
        return py_cmd

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'


def ensure_dir(path=None, content=None, force_write=False):
    from pathlib import Path
    need_create = 0 if Path(path).exists() else 1
    Path(path).mkdir(parents=True, exist_ok=True)
    return need_create


class EnsureDir:
    def __init__(self, path=None, content=None, force_write=None):
        self.path = path
        self.content = content
        self.force_write = force_write

    def render_bash_shell(self, force_write=None, **kw):
        return f'mkdir -p {self.path}'

    def render_bash_script(self, force_write=None, **kw):
        return self.render_bash_shell(force_write=force_write, **kw)

    def render_py(self, force_write=None, **kw):
        py_cmd = partial(ensure_dir, path=self.path,
                         content=self.content,
                         force_write=force_write)
        return py_cmd

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'
