import fire


def test__basic_model__init_with_params():
    from dictmodel import DictModel, DictField
    class MyModel(DictModel):
        int_field: int = DictField()
        str_field: str = DictField()
        dict_field: dict = DictField()
    
    mm = MyModel(
        int_field=3,
        str_field="sdf",
        dict_field={}
    )
    assert mm.int_field == 3
    assert mm.str_field == "sdf"
    assert mm.dict_field == {}


def test__basic_model__init_no_params():
    from dictmodel import DictModel, DictField
    class MyModel(DictModel):
        int_field: int = DictField()
        str_field: str = DictField()
        dict_field: dict = DictField()
    
    mm = MyModel()
    assert mm.int_field is None
    assert mm.str_field is None
    assert mm.dict_field is None


def test__basic_model__init_on_access_flag():
    """ Example:
    on_access flag is used to autocreate value for field using its type. 
    For custom constructors use default param with provided factory method
    """
    from dictmodel import DictModel, DictField
    class MyModel(DictModel):
        int_field: int = DictField(on_access=True)
        str_field: str = DictField(on_access=True)
        dict_field: dict = DictField(on_access=True)
    
    mm = MyModel()
    assert not mm.to_struct()
    mm.int_field += 1
    assert mm.int_field == 1
    assert mm.str_field == ""
    assert mm.dict_field == {}
    assert mm.to_struct()


def test__basic_model__init_default():
    """ Example:
    on_access flag is used to autocreate value for field using its type. 
    For custom constructors use default param with provided factory method
    """
    from dictmodel import DictModel, DictField
    from uuid import uuid4
    class MyModel(DictModel):
        int_field: int = DictField(default=lambda: 3)
        str_field: str = DictField(default=lambda: uuid4)
        dict_field: dict = DictField(default=dict)
    
    mm = MyModel()
    d1 = mm.to_struct()

    assert mm.int_field == 3
    assert mm.str_field
    assert mm.dict_field == {}


def test__to_yaml_str():
    from dictmodel import DictModel, DictField
    class MyModel(DictModel):
        f1 = DictField()
    
    model = MyModel(f1=dict(
        name='somename',
        items=[1,2,3]))
    yaml_str = model.to_yaml_str()
    lines =  yaml_str.split('\n')
    print(model.to_yaml_str())
    assert any('items: [1, 2, 3]' in line for line in lines)
    assert any('name: somename' in line for line in lines)


if __name__ == "__main__":
    # test_typing()
    # test__basic_model()
    # test__dict_types()
    fire.Fire()
