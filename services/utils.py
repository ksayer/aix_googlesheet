from typing import Generator


def list_chunks(lst: list, size: int = 10) -> Generator[list, None, None]:
    for i in range(0, len(lst), size):
        yield lst[i:i + size]
