from typing import List
import aiohttp

class MatrixDownloadError(Exception):
    """Ошибка при скачивании матрицы."""
    pass

class MatrixFormatError(Exception):
    """Ошибка в формате матрицы."""
    pass

def parse_matrix(text: str) -> List[List[int]]:
    """Преобразует текст в квадратную матрицу."""
    matrix = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if set(line) <= set("+-| "):
            continue
        
        line = line.replace("|", " ")
        try:
            row = [int(number) for number in line.split()]
        except ValueError as error:
            raise MatrixFormatError("В матрице должны быть числа") from error
        
        if row:
            matrix.append(row)
            
    if not matrix:
        raise MatrixFormatError("Матрица пустая")
        
    size = len(matrix)
    for row in matrix:
        if len(row) != size:
            raise MatrixFormatError("Матрица должна быть квадратной")
            
    return matrix

def spiral_traversal(matrix: List[List[int]]) -> List[int]:
    """Обходит матрицу против часовой стрелки."""
    if not matrix:
        return []
        
    result = []
    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # 1. Вниз по левому краю.
        for row in range(top, bottom + 1):
            result.append(matrix[row][left])
        left += 1
        
        # 2. Вправо по нижнему краю.
        for column in range(left, right + 1):
            result.append(matrix[bottom][column])
        bottom -= 1
        
        # 3. Вверх по правому краю.
        if left <= right:
            for row in range(bottom, top - 1, -1):
                result.append(matrix[row][right])
            right -= 1
            
        # 4. Влево по верхнему краю.
        if top <= bottom:
            for column in range(right, left - 1, -1):
                result.append(matrix[top][column])
            top += 1
            
    return result

async def get_matrix(url: str) -> List[int]:
    """Скачивает матрицу и возвращает её обход по спирали."""
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                text = await response.text()
    except (aiohttp.ClientError, TimeoutError) as error:
        raise MatrixDownloadError("Не удалось скачать матрицу") from error
        
    matrix = parse_matrix(text)
    return spiral_traversal(matrix)