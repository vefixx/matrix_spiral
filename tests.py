import pytest
from aioresponses import aioresponses

from matrix.matrix import (
    MatrixDownloadError,
    MatrixFormatError,
    get_matrix,
    parse_matrix,
    spiral_traversal,
)


def test_parse_formatted_table():
    raw_data = """
    | 10 20 30 |
    | 40 50 60 |
    | 70 80 90 |
    """
    target = [
        [10, 20, 30],
        [40, 50, 60],
        [70, 80, 90],
    ]
    assert parse_matrix(raw_data) == target


def test_spiral_walk():
    grid = [
        [10, 20, 30, 40],
        [50, 60, 70, 80],
        [90, 100, 110, 120],
        [130, 140, 150, 160],
    ]
    expected_sequence = [
        10, 50, 90, 130,
        140, 150, 160,
        120, 80, 40,
        30, 20,
        60, 100, 110, 70,
    ]
    assert spiral_traversal(grid) == expected_sequence


def test_single_element():
    assert spiral_traversal([[5]]) == [5]


def test_empty_input_raises():
    with pytest.raises(MatrixFormatError):
        parse_matrix("")


def test_rectangular_input_raises():
    data = "1 2 3\n4 5 6"
    with pytest.raises(MatrixFormatError):
        parse_matrix(data)


def test_non_numeric_raises():
    data = "1 2\n3 abc"
    with pytest.raises(MatrixFormatError):
        parse_matrix(data)


@pytest.mark.asyncio
async def test_successful_download_and_parse():
    target_url = "https://example.com/matrix.txt"
    mock_payload = "1 2\n3 4"

    with aioresponses() as mocked_responses:
        mocked_responses.get(target_url, status=200, body=mock_payload)
        actual_result = await get_matrix(target_url)

    assert actual_result == [1, 3, 4, 2]


@pytest.mark.asyncio
async def test_download_failure_raises():
    target_url = "https://example.com/matrix.txt"

    with aioresponses() as mocked_responses:
        mocked_responses.get(target_url, status=500)
        with pytest.raises(MatrixDownloadError):
            await get_matrix(target_url)