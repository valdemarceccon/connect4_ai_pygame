def diagonals(arr: list[list[int]]) -> (list[int], list[int]):
    h, w = len(arr), len(arr[0])
    d1 = [[arr[h - p + q - 1][q]
           for q in range(max(p - h + 1, 0), min(p + 1, w))]
          for p in range(h + w - 1)]
    d2 = [[arr[p - q][q]
           for q in range(max(p - h + 1, 0), min(p + 1, w))]
          for p in range(h + w - 1)]
    return d1, d2


def get_columns(arr: list[list[int]]) -> list[list[int]]:
    return [[c for c in x] for x in map(list, zip(*arr))]


def is_sublist(list1, list2) -> bool:
    for x in range(len(list1)):
        if list1[x:x + len(list2)] == list2:
            return True
    return False
