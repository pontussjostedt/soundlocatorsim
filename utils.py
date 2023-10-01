import numpy as np

def shift_padd(arr: np.ndarray, shift: int) -> np.ndarray:
    if shift == 0:
        return arr
    elif shift > 0:
        return np.concatenate((np.zeros(shift, dtype=np.int32), arr[:-shift]))
    else:
        return np.concatenate((arr[-shift:], np.zeros(-shift, dtype=np.int32)))
    

def normalize(arr: np.ndarray, min_value, max_value) -> np.ndarray:
    return (arr - min_value) / (max_value - min_value)


if __name__ == "__main__":
    to_shift = np.array([1, 2, 3, 4, 5])
    print(shift_padd(to_shift, 0))
    print(shift_padd(to_shift, 2))
    print(shift_padd(to_shift, -2))