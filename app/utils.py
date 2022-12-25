def partition(arr, size):
    for i in range(0, len(arr), size):
        yield arr[i : i + size]
