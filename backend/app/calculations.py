import numpy as np
from typing import List, Tuple

def integral(f, a: float, b: float, n: int = 10000) -> float:
    """Numerical integration using trapezoidal rule"""
    if a == b:
        return 0.0
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return np.trapz(y, x)

def square(x):
    """Fixed square function - returns x^2"""
    return x ** 2

def moment_calculation(f, a: float, b: float, c: float, n: int = 10000) -> float:
    """Calculate moment about point a"""
    def mom(x):
        return f(x) * (x - a)
    return integral(mom, b, c, n)

def calculate_structural_analysis(
    f1: List[List[float]],  # Point moments [[magnitude, location], ...]
    f2: List[List[float]],  # Point forces [[magnitude, location], ...]
    f3: List[List[float]],  # Constant force profiles [[magnitude, start, end], ...]
    f4: List[List[float]],  # Triangular force profiles [[magnitude, start, end], ...]
    a: float,  # Support 1 location
    b: float,  # Support 2 location
    length: float,  # Beam length
    G: float = 1.0,  # Modulus of elasticity
    I: float = 1.0   # Second moment of area
) -> Tuple[List[float], List[float], List[float], List[float], List[List[float]]]:
    """
    Calculate shear force, bending moment, slope, and deflection for a beam
    Returns: (V, BM, slope, deflection, reaction_forces)
    """
    
    # Initialize variables
    p = 0  # Sum of moments about support 1
    q = 0  # Sum of vertical forces
    
    # Process point moments
    for moment in f1:
        p += moment[0]
    
    # Process point forces
    for force in f2:
        p += force[0] * (force[1] - a)
        q += force[0]
    
    # Process constant force profiles
    for profile in f3:
        def f(x):
            return profile[0] * np.ones_like(x)
        p += moment_calculation(f, a, profile[1], profile[2], n=10000)
        q += integral(f, profile[1], profile[2], n=10000)
    
    # Process triangular force profiles
    for profile in f4:
        def f(x):
            return profile[0] / (profile[2] - profile[1]) * (x - profile[1])
        p += moment_calculation(f, a, profile[1], profile[2], n=10000)
        q += integral(f, profile[1], profile[2], n=10000)
    
    # Calculate reaction forces
    f2c = [force[:] for force in f2]  # Copy of original point forces
    
    r2 = p / (a - b)  # Reaction at support 2
    r1 = -q - r2      # Reaction at support 1
    
    # Add reactions to point forces for calculation
    f2.extend([[r1, a], [r2, b]])
    
    # Sort all loads by location
    f1.sort(key=lambda x: x[1])
    f2.sort(key=lambda x: x[1])
    f3.sort(key=lambda x: x[1])
    f4.sort(key=lambda x: x[1])
    
    # Create position array
    l = np.linspace(0, length, 1001)
    dl = l[1] - l[0]
    
    # Calculate shear force
    V = calculate_shear_force(f2, f3, f4, l, dl)
    
    # Calculate bending moment
    BM = calculate_bending_moment(f1, f2, f3, f4, l, dl)
    
    # Calculate slope and deflection
    slope, deflection = calculate_slope_and_deflection(BM, l, dl, a, b, G, I)
    
    return V, BM, slope, deflection, f2c

def calculate_shear_force(f2: List[List[float]], f3: List[List[float]], 
                         f4: List[List[float]], l: np.ndarray, dl: float) -> List[float]:
    """Calculate shear force along the beam"""
    i2 = i3 = i4 = -1
    l2, l3, l4 = len(f2), len(f3), len(f4)
    arr = [2, 3, 4]
    v = 0
    V = []
    
    for j in l[:-1]:
        for i in arr[:]:  # Create a copy to avoid modification during iteration
            if i == 2 and 2 in arr:
                if i2 + 1 == l2:
                    arr.remove(2)
                else:
                    if f2[i2 + 1][1] <= j:
                        v += f2[i2 + 1][0]
                        i2 += 1
                        if i2 + 1 == l2:
                            arr.remove(2)
                            break
            
            if i == 3 and 3 in arr:
                if i3 + 1 == l3:
                    arr.remove(3)
                    break
                if f3[i3 + 1][1] <= j:
                    v += f3[i3 + 1][0] * dl
                    if f3[i3 + 1][2] < j:
                        i3 += 1
                    if i3 + 1 == l3:
                        arr.remove(3)
                        break
            
            if i == 4 and 4 in arr:
                if i4 + 1 == l4:
                    arr.remove(4)
                    break
                if f4[i4 + 1][1] <= j:
                    t1, t2, t3 = f4[i4 + 1][0], f4[i4 + 1][1], f4[i4 + 1][2]
                    v += t1 / (t3 - t2) * (j - t2) * dl
                    if f4[i4 + 1][2] < j:
                        i4 += 1
                    if i4 + 1 == l4:
                        arr.remove(4)
                        break
        
        V.append(-v)
    
    V.append(-v)
    return V

def calculate_bending_moment(f1: List[List[float]], f2: List[List[float]],
                           f3: List[List[float]], f4: List[List[float]],
                           l: np.ndarray, dl: float) -> List[float]:
    """Calculate bending moment along the beam"""
    i1 = i2 = i3 = i4 = -1
    l1, l2, l3, l4 = len(f1), len(f2), len(f3), len(f4)
    g1 = g2 = g3 = g4 = 0
    arr = [1, 2, 3, 4]
    bm = 0
    BM = []

    for j in l[:-1]:
        for i in arr[:]:  # Create a copy to avoid modification during iteration
            if i == 1 and 1 in arr:
                if i1 + 1 != l1 and f1[i1 + 1][1] <= j:
                    bm -= f1[i1 + 1][0]
                    if i1 + 1 != l1:
                        i1 += 1

            if i == 2 and 2 in arr:
                bm += g2 * dl
                if i2 + 1 != l2 and f2[i2 + 1][1] <= j:
                    g2 += f2[i2 + 1][0]
                    if i2 + 1 != l2:
                        i2 += 1

            if i == 3 and 3 in arr:
                bm += g3 * dl
                if i3 + 1 != l3 and f3[i3 + 1][1] <= j:
                    g3 += f3[i3 + 1][0] * dl
                    if f3[i3 + 1][2] < j and i3 + 1 != l3:
                        i3 += 1

            if i == 4 and 4 in arr:
                bm += g4 * dl
                if i4 + 1 != l4 and f4[i4 + 1][1] <= j:
                    t1, t2, t3 = f4[i4 + 1][0], f4[i4 + 1][1], f4[i4 + 1][2]
                    g4 += t1 / (t3 - t2) * (j - t2) * dl
                    if f4[i4 + 1][2] < j and i4 + 1 != l4:
                        i4 += 1

        BM.append(bm)

    BM.append(bm)
    return BM

def calculate_slope_and_deflection(BM: List[float], l: np.ndarray, dl: float,
                                 a: float, b: float, G: float, I: float) -> Tuple[List[float], List[float]]:
    """Calculate slope and deflection from bending moment"""
    # Calculate slope by integrating bending moment
    slope = []
    da = 0
    for bm in BM:
        da += bm * dl
        slope.append(da)

    # Calculate deflection by integrating slope
    deflection = []
    da = 0
    for s in slope:
        da += s * dl
        deflection.append(da)

    # Find indices for support locations
    ai = bi = 0
    for i in range(len(l)):
        if abs(l[i] - a) < dl/2:
            ai = i
        if abs(l[i] - b) < dl/2:
            bi = i

    # Apply boundary conditions and material properties
    for i in range(len(l)):
        deflection[i] /= (G * I)
        slope[i] /= (G * I)

    # Apply support conditions (zero deflection at supports)
    if ai < len(deflection) and bi < len(deflection):
        c2 = (a * deflection[bi] - b * deflection[ai]) / (b - a) if b != a else 0
        c1 = (deflection[ai] - deflection[bi]) / (b - a) if b != a else 0

        for i in range(len(l)):
            deflection[i] += c1 * l[i] + c2
            slope[i] += c1

    return slope, deflection
