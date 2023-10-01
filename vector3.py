import math
class Vector3:
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __div__(self, scalar: 'Vector3') -> 'Vector3':
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    

    def __mul__(self, scalar: 'Vector3') -> 'Vector3':
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def mag(self) -> float:
        return math.sqrt(self.x * self.x + self.y*self.y + self.z * self.z)
    

    def dist(self, other: 'Vector3') -> float:
        return (self - other).mag()
    
    def normalized(self) -> 'Vector3':
        return self / self.mag
    
    def __repr__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"
    

    def __str__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"
    
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


if __name__ == "__main__":
    print(*Vector3(1, 2, 3))
    


    
