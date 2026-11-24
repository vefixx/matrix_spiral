import asyncio
from matrix.matrix import get_matrix

TARGET_URL = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"


async def main():
    data = await get_matrix(TARGET_URL)
    print(data)


if __name__ == "__main__":
    asyncio.run(main())
