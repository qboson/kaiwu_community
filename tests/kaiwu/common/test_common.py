import numpy as np
import unittest
from kaiwu.common import JsonSerializableMixin


# Helper classes for testing
class AnotherTestClass(JsonSerializableMixin):
    def __init__(self):
        self.value = 10


class DemoClass(JsonSerializableMixin):
    def __init__(self):
        self.optimizer = "exclude_me"
        self.array = np.array([1, 2, 3])
        self.nested = AnotherTestClass()
        self.num = np.float64(5.5)
        self.sub_indices = [1, 2, 3]
        self.rng = np.random.default_rng()
        self.a_list = [AnotherTestClass(), AnotherTestClass()]


class Container(JsonSerializableMixin):
    def __init__(self):
        self.items = [AnotherTestClass(), AnotherTestClass()]


class MyTestCase(unittest.TestCase):

    # Tests for to_json_dict
    def test_to_json_dict_excludes_optimizer(self):
        obj = DemoClass()
        json_dict = obj.to_json_dict()
        assert '_optimizer' not in json_dict

    def test_to_json_dict_converts_numpy_array(self):
        obj = DemoClass()
        json_dict = obj.to_json_dict()
        assert json_dict['array'] == [1, 2, 3]
        assert json_dict['array$type'] == 'np.ndarray'

    def test_to_json_dict_handles_nested_objects(self):
        obj = DemoClass()
        json_dict = obj.to_json_dict()
        assert isinstance(json_dict['nested'], dict)
        assert json_dict['nested']['value'] == 10
        assert json_dict['nested$type'] == 'JsonSerializableMixin'

    def test_to_json_dict_converts_numpy_number(self):
        obj = DemoClass()
        json_dict = obj.to_json_dict()
        assert json_dict['num'] == 5.5
        assert isinstance(json_dict['num'], float)

    def test_to_json_dict_converts_sub_indices(self):
        obj = DemoClass()
        json_dict = obj.to_json_dict()
        assert json_dict['sub_indices'] == [1, 2, 3]

    def test_to_json_dict_saves_rng_state(self):
        obj = DemoClass()
        json_dict = obj.to_json_dict()
        assert 'rng' in json_dict

    def test_to_json_dict_handles_list_of_objects(self):
        container = Container()
        json_dict = container.to_json_dict()
        assert isinstance(json_dict['items'], list)
        assert all(isinstance(item, dict) for item in json_dict['items'])
        assert json_dict['items$type'] == 'list'

    def test_to_json_dict_excludes_custom_fields(self):
        obj = DemoClass()
        obj.some_field = "exclude_me"
        json_dict = obj.to_json_dict(exclude_fields=('some_field',))
        assert 'some_field' not in json_dict

    def test_to_json_dict_handles_sub_indices_none(self):
        obj = DemoClass()
        obj.sub_indices = None
        json_dict = obj.to_json_dict()
        assert 'sub_indices' in json_dict
        assert json_dict['sub_indices'] is None

    # Tests for load_json_dict
    def test_load_json_dict_restores_attributes(self):
        original = DemoClass()
        original.array = np.array([4, 5, 6])
        original.nested.value = 20
        original.num = np.float64(10.5)
        original.sub_indices = [4, 5, 6]
        original.rng = np.random.default_rng(42)

        json_dict = original.to_json_dict()

        new_obj = DemoClass()
        new_obj.load_json_dict(json_dict)

        assert np.array_equal(new_obj.array, original.array)
        assert new_obj.nested.value == original.nested.value
        assert new_obj.num == original.num
        assert new_obj.sub_indices == original.sub_indices

    def test_load_json_dict_with_list_of_objects_keeps_as_dicts(self):
        container = Container()
        json_dict = container.to_json_dict()
        new_container = Container()
        new_container.load_json_dict(json_dict)
        assert isinstance(new_container.items, list)
        assert all(isinstance(item, dict) for item in new_container.items)

    def test_load_json_dict_with_missing_type_assumes_raw_value(self):
        json_dict = {
            'array': [7, 8, 9],
            # Missing array$type
        }
        obj = DemoClass()
        obj.load_json_dict(json_dict)
        assert obj.array == [7, 8, 9]


if __name__ == '__main__':
    unittest.main()
