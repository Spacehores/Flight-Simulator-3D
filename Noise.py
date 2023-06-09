import math
import pygame
import MyMath

p = [151, 160, 137, 91, 90, 15,
     131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23,
     190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33,
     88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166,
     77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244,
     102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196,
     135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123,
     5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42,
     223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
     129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97, 228,
     251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107,
     49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254,
     138, 236, 205, 93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180] * 2




def fade(t):
    return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)


def grad(hash_value, x, y):
    result = hash_value & 3
    if result == 0: return x + y
    if result == 1: return -x + y
    if result == 2: return x - y
    if result == 3: return -x - y
    return 0


def noise(x, y):
    xi = int(x) & 255
    yi = int(y) & 255
    g1 = p[p[xi] + yi]
    g2 = p[p[xi + 1] + yi]
    g3 = p[p[xi] + yi + 1]
    g4 = p[p[xi + 1] + yi + 1]

    xf = float(x - math.floor(x))
    yf = float(y - math.floor(y))

    d1 = grad(g1, xf, yf)
    d2 = grad(g2, xf - 1, yf)
    d3 = grad(g3, xf, yf - 1)
    d4 = grad(g4, xf - 1, yf - 1)

    u = fade(xf)
    v = fade(yf)

    x1_inter = MyMath.lerp(u, d1, d2)
    x2_inter = MyMath.lerp(u, d3, d4)
    y_inter = MyMath.lerp(v, x1_inter, x2_inter)
    clamped01 = (y_inter + 0.8123493) / (1 + 2 * 0.3123493);
    return pygame.math.clamp(clamped01, 0.0, 1.0)


def noiseFunction(x, y):
    iterations = 1
    frequency = 0.0721
    amplitude = (noise(4342 - x * 0.0521, 7654 - y * 0.0521) ** 2) * 10
    value = 0
    for i in range(iterations):
        amount = noise((x) * frequency, (y) * frequency)
        amount = 1.3 * (0.5 - abs(0.5 - amount))
        amount = pow(abs(amount), 1.15)
        amount *= amplitude
        value += amount
        amplitude = amplitude * 0.5
        frequency = frequency * 2

    water_amplitude = (noise(-743542 - x * 0.03221, -971654 - y * 0.03221) * 2) ** 4
    # water_amplitude = 1.3 * (0.5 - abs(0.5 - water_amplitude))
    value -= noise(x * 0.432, y * 0.432) * water_amplitude
    return value
