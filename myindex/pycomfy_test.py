from myindex.pycomfy import is_cfg_method, to_cfg_method, make_cfg_bond


class SimpleCfg:
    f_int: int
    f_str: str = 's'


def simple_method_sample(cfg: SimpleCfg):
    return f"{cfg.f_str}-{cfg.f_str}"


def test_is_cfg_method():
    x = is_cfg_method(SimpleCfg, simple_method_sample)
    assert x is True


def test__to_cfg_method__static_class():
    class MyCli:
        def __init__(self, cfg):
            self._cfg = cfg

        simple_method_sample = to_cfg_method(simple_method_sample)

    cfg = SimpleCfg()
    cfg.f_int = 3
    cli = MyCli(cfg)
    rv = cli.simple_method_sample()
    print(rv)


def test__to_cfg_method__dinamic_class_sample():
    cfg_class = SimpleCfg
    _name = f"{cfg_class.__name__}Cli"

    def ctor(self, cfg):
        self._cfg = cfg

    _dict = {
        "string_val": "this is val1",
        "int_val": 10,
        "__init__": ctor,
        "simple_method_sample": to_cfg_method(simple_method_sample),
    }
    MyCli = type(_name, (object,), _dict)

    cfg = SimpleCfg()
    cfg.f_str = '5'
    cli = MyCli(cfg)
    rv = cli.simple_method_sample()
    assert rv == '5-5'


def test__to_cfg_method__dinamic_class_full():
    MyCli = make_cfg_bond(SimpleCfg, globals())
    cfg = SimpleCfg()
    cfg.f_str = '5'
    cli = MyCli(cfg)
    rv = cli.simple_method_sample()
    assert rv == '5-5'


if __name__ == '__main__':
    import fire
    fire.Fire()
