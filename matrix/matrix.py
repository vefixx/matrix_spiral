from typing import List
import aiohttp


class MatrixDownloadError(Exception):
    pass


class MatrixFormatError(Exception):
    pass


def parse_matrix(text: str) -> List[List[int]]:
    matrix = []
    for line in text.splitlines():
        line = line.strip()
        if not line or all(c in '+-| ' for c in line):
            continue

        line = line.replace('|', ' ')
        try:
            row = list(map(int, line.split()))
        except ValueError:
            raise MatrixFormatError("Ожидались целые числа")

        if row:
            matrix.append(row)

    if not matrix:
        raise MatrixFormatError("Матрица пуста")

    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise MatrixFormatError("Матрица должна быть квадратной")

    return matrix


def spiral_traversal(mat: List[List[int]]) -> List[int]:
    result = []
    r_min, r_max = 0, len(mat) - 1
    c_min, c_max = 0, len(mat[0]) - 1

    while r_min <= r_max and c_min <= c_max:
        for r in range(r_min, r_max + 1):
            result.append(mat[r][c_min])
        c_min += 1

        for c in range(c_min, c_max + 1):
            result.append(mat[r_max][c])
        r_max -= 1

        if c_min <= c_max:
            for r in range(r_max, r_min - 1, -1):
                result.append(mat[r][c_max])
            c_max -= 1

        if r_min <= r_max:
            for c in range(c_max, c_min - 1, -1):
                result.append(mat[r_min][c])
            r_min += 1

    return result


async def get_matrix(url: str) -> List[int]:
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                content = await resp.text()
    except (aiohttp.ClientError, TimeoutError) as err:
        raise MatrixDownloadError("Не удалось получить данные") from err

    return spiral_traversal(parse_matrix(content))