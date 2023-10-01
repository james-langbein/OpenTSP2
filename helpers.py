import numpy as np
import math
import cmath


def combinations_calculator(n, r=1):
    """Calculates number of combinations."""
    return int((math.factorial(n)) / (math.factorial(r) * math.factorial(n - r)))


def permutations_calculator(n, r=1):
    """Returns the full range of permutations for the instance's edges. This is used by the solve method to exhaust
    the permutations generator without going over the maximum number of permutations."""
    return int((math.factorial(n)) / (math.factorial(n - r)))


def angle(vertex, start, dest):
    """Calculates the signed angle between two edges with the same origin. Origin is the 'vertex' argument, 'start' is
    the end of the edge to calculate the angle from.
    Positively signed result means anti-clockwise rotation about the vertex."""
    def calc_radians(ab):
        if ab > math.pi:
            return ab + (-2 * math.pi)
        else:
            if ab < 0 - math.pi:
                return ab + (2 * math.pi)
            else:
                return ab + 0

    AhAB = math.atan2((dest.y - vertex.y), (dest.x - vertex.x))
    AhAO = math.atan2((start.y - vertex.y), (start.x - vertex.x))
    AB = AhAB - AhAO
    res = calc_radians(AB)
    # in between 0 - math.pi = do nothing, more than math.pi = +(-2 * math.pi), less than zero = do nothing
    # below is calc_radians() as a one-liner:
    # AB = math.degrees(AB + (-2 * math.pi if AB > math.pi else (2 * math.pi if AB < 0 - math.pi else 0)))

    return math.degrees(res)


def inner_soddy_center(A, B, C):

    class Node:
        def __init__(self, x, y):
            self.x = float(x)
            self.y = float(y)

        def __str__(self):
            strNode = self.x, self.y
            return str(strNode)

    def lineLength(line):
        x = (line[0].x - line[1].x) ** 2
        y = (line[0].y - line[1].y) ** 2
        z = x + y
        return cmath.sqrt(z)

    AB = [A, B]
    BC = [B, C]
    AC = [C, A]

    widthAB = lineLength(AB)
    widthBC = lineLength(BC)
    widthAC = lineLength(AC)

    radiusMatrixLHS = np.array([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    radiusMatrixRHS = np.array([widthAB, widthAC, widthBC])
    radiusA, radiusB, radiusC = np.linalg.solve(radiusMatrixLHS, radiusMatrixRHS)
    radiusInnerCircle = (radiusA * radiusB * radiusC) / (
                radiusB * radiusC + radiusA * (radiusB + radiusC) + 2 * cmath.sqrt(
            radiusA * radiusB * radiusC * (radiusA + radiusB + radiusC)))

    kA = 1 / radiusA
    kB = 1 / radiusB
    kC = 1 / radiusC
    kInner = 1 / radiusInnerCircle

    zkA = (A.x + A.y * 1j) * (kA)
    zkB = (B.x + B.y * 1j) * (kB)
    zkC = (C.x + C.y * 1j) * (kC)
    temp = zkA + zkB + zkC + 2 * cmath.sqrt(zkA * zkB + zkB * zkC + zkA * zkC)
    zkInner = temp / kInner
    innerSoddyCenter = Node(zkInner.real, zkInner.imag)

    return innerSoddyCenter


def inner_soddy_center2(A, B, C):
    """
    Returns a tuple of the x and y values for the Inner Soddy Center.
    """
    class Node:
        def __init__(self, x, y):
            self.x = float(x)
            self.y = float(y)

        def __str__(self):
            strNode = self.x, self.y
            return str(strNode)

    def lineLength(line):
        x = (line[0].x - line[1].x) ** 2
        y = (line[0].y - line[1].y) ** 2
        z = x + y
        return cmath.sqrt(z)

    A, B, C = Node(A.x, A.y), Node(B.x, B.y), Node(C.x, C.y)

    AB = [A, B]
    BC = [B, C]
    AC = [C, A]

    widthAB = lineLength(AB)
    widthBC = lineLength(BC)
    widthAC = lineLength(AC)

    radiusMatrixLHS = np.array([[1, 1, 0], [1, 0, 1], [0, 1, 1]])
    radiusMatrixRHS = np.array([widthAB, widthAC, widthBC])
    radiusA, radiusB, radiusC = np.linalg.solve(radiusMatrixLHS, radiusMatrixRHS)
    radiusInnerCircle = (radiusA * radiusB * radiusC) / (
                radiusB * radiusC + radiusA * (radiusB + radiusC) + 2 * cmath.sqrt(
            radiusA * radiusB * radiusC * (radiusA + radiusB + radiusC)))

    kA = 1 / radiusA
    kB = 1 / radiusB
    kC = 1 / radiusC
    kInner = 1 / radiusInnerCircle

    zkA = (A.x + A.y * 1j) * (kA)
    zkB = (B.x + B.y * 1j) * (kB)
    zkC = (C.x + C.y * 1j) * (kC)
    temp = zkA + zkB + zkC + 2 * cmath.sqrt(zkA * zkB + zkB * zkC + zkA * zkC)
    zkInner = temp / kInner
    innerSoddyCenter = (zkInner.real, zkInner.imag)

    return innerSoddyCenter
