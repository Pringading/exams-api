import pytest
from src.utils.utils import data_to_dict_list


class TestDataToDictList:
    """Testing data_to_dict_list function from src/utils/utils.py"""

    @pytest.mark.it('Testing returns list of dictionaries.')
    def test_returns_list_of_dicts(self):
        """Testing returns a list of dictionaries"""

        test_data = [[1, 2], [2, 3], [3, 4]]
        test_columns = [{"name": "column 1"}, {"name": "column 2"}]
        result = data_to_dict_list(test_data, test_columns)
        assert isinstance(result, list)
        for row in result:
            assert isinstance(row, dict)

    @pytest.mark.it('Testing returns expected data.')
    def test_returns_expected_data(self):
        """Testing returned list contains expected data."""

        test_data = [[1, 2], [2, 3], [3, 4]]
        test_columns = [{"name": "column 1"}, {"name": "column 2"}]
        expected = [
            {"column 1": 1, "column 2": 2},
            {"column 1": 2, "column 2": 3},
            {"column 1": 3, "column 2": 4}
        ]
        result = data_to_dict_list(test_data, test_columns)
        assert result == expected
