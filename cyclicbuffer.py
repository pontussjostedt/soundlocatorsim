class CyclicBuffer:
    def __init__(self, length) -> None:
        self.length = length
        self.data = [0 for _ in range(length)]
        self._offset = -1
        self._iter_index = 0

    def offer(self, element: int) -> None:
        self._offset += 1
        self.data[self._offset % self.length] = element

    
    def __getitem__(self, index: int) -> int:
        return self.data[self._cycle_index(index)]


    def _cycle_index(self, index: int) -> int:
        print(f"index used: {(index + self._offset) % self.length}")
        return (-1 * index + self._offset) % self.length
    
    def __iter__(self) -> list[int]:
        return _CycleIter(self.data, self.length, self._offset)
    
    def last(self) -> int:
        return self.data[self._offset % self.length]
    

class _CycleIter:
    def __init__(self, data, length, _offset) -> None:
        self.data = data
        self.length = length
        self.iter_pos = 0
        self._offset = _offset

    def __next__(self):
        if -1 * self.iter_pos < self.length:
            out = self.data[(self.iter_pos + self._offset) % self.length]
            self.iter_pos -= 1
            return out
        else:
            raise StopIteration
    

if __name__ == "__main__":
    buffer = CyclicBuffer(4)
    buffer.offer(1)
    buffer.offer(2)
    buffer.offer(3)
    buffer.offer(4)
    buffer.offer(5)

    for x in buffer:
        print(x)

    print(f"last: {buffer.last()}")


    print(f"Using index {[buffer[x] for x in range(4)]}")
    print(*CyclicBuffer(4))