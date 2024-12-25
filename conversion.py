import math

def clamp(v, low=0, high=255):
    return v

def srgb_transfer_function(a):
    return 12.92 * a if a <= 0.0031308 else 1.055 * math.pow(a, 1 / 2.4) - 0.055

def srgb_transfer_function_inv(a):
    return math.pow((a + 0.055) / 1.055, 2.4) if a > 0.04045 else a / 12.92

def linear_srgb_to_oklab(r, g, b):
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b

    l_ = math.cbrt(l)
    m_ = math.cbrt(m)
    s_ = math.cbrt(s)

    return [
        0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
        1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
        0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_,
    ]

def oklab_to_linear_srgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b

    l = l_ ** 3
    m = m_ ** 3
    s = s_ ** 3

    return [
        clamp(4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s),
        clamp(-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s),
        clamp(-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s),
    ]

def toe(x):
    k_1 = 0.206
    k_2 = 0.03
    k_3 = (1 + k_1) / (1 + k_2)
    return 0.5 * (k_3 * x - k_1 + math.sqrt((k_3 * x - k_1) ** 2 + 4 * k_2 * k_3 * x))

def toe_inv(x):
    k_1 = 0.206
    k_2 = 0.03
    k_3 = (1 + k_1) / (1 + k_2)
    return (x ** 2 + k_1 * x) / (k_3 * (x + k_2))

def compute_max_saturation(a, b):
    if -1.88170328 * a - 0.80936493 * b > 1:
        k0, k1, k2, k3, k4 = 1.19086277, 1.76576728, 0.59662641, 0.75515197, 0.56771245
        wl, wm, ws = 4.0767416621, -3.3077115913, 0.2309699292
    elif 1.81444104 * a - 1.19445276 * b > 1:
        k0, k1, k2, k3, k4 = 0.73956515, -0.45954404, 0.08285427, 0.12541070, 0.14503204
        wl, wm, ws = -1.2684380046, 2.6097574011, -0.3413193965
    else:
        k0, k1, k2, k3, k4 = 1.35733652, -0.00915799, -1.15130210, -0.50559606, 0.00692167
        wl, wm, ws = -0.0041960863, -0.7034186147, 1.7076147010

    S = k0 + k1 * a + k2 * b + k3 * a ** 2 + k4 * a * b

    k_l = 0.3963377774 * a + 0.2158037573 * b
    k_m = -0.1055613458 * a - 0.0638541728 * b
    k_s = -0.0894841775 * a - 1.2914855480 * b

    for _ in range(1):  # Optional iteration for convergence
        l_ = 1 + S * k_l
        m_ = 1 + S * k_m
        s_ = 1 + S * k_s

        l = l_ ** 3
        m = m_ ** 3
        s = s_ ** 3

        l_dS = 3 * k_l * l_ ** 2
        m_dS = 3 * k_m * m_ ** 2
        s_dS = 3 * k_s * s_ ** 2

        f = wl * l + wm * m + ws * s
        f1 = wl * l_dS + wm * m_dS + ws * s_dS

        S -= f / f1

    return S

def find_cusp(a, b):
    S_cusp = compute_max_saturation(a, b)

    rgb_at_max = oklab_to_linear_srgb(1, S_cusp * a, S_cusp * b)
    L_cusp = (1 / max(rgb_at_max)) ** (1/3)
    C_cusp = L_cusp * S_cusp

    return L_cusp, C_cusp

def find_gamut_intersection(a, b, L1, C1, L0, cusp=None):
    if cusp is None:
        cusp = find_cusp(a, b)

    if (L1 - L0) * cusp[1] - (cusp[0] - L0) * C1 <= 0:
        t = cusp[1] * L0 / (C1 * cusp[0] + cusp[1] * (L0 - L1))
    else:
        t = cusp[1] * (L0 - 1) / (C1 * (cusp[0] - 1) + cusp[1] * (L0 - L1))

        dL = L1 - L0
        dC = C1

        k_l = +0.3963377774 * a + 0.2158037573 * b
        k_m = -0.1055613458 * a - 0.0638541728 * b
        k_s = -0.0894841775 * a - 1.2914855480 * b

        l_dt = dL + dC * k_l
        m_dt = dL + dC * k_m
        s_dt = dL + dC * k_s

        for _ in range(3):
            L = L0 * (1 - t) + t * L1
            C = t * C1

            l_ = L + C * k_l
            m_ = L + C * k_m
            s_ = L + C * k_s

            l = l_ ** 3
            m = m_ ** 3
            s = s_ ** 3

            ldt = 3 * l_dt * l_ ** 2
            mdt = 3 * m_dt * m_ ** 2
            sdt = 3 * s_dt * s_ ** 2

            ldt2 = 6 * l_dt ** 2 * l_
            mdt2 = 6 * m_dt ** 2 * m_
            sdt2 = 6 * s_dt ** 2 * s_

            r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s - 1
            r1 = 4.0767416621 * ldt - 3.3077115913 * mdt + 0.2309699292 * sdt
            r2 = 4.0767416621 * ldt2 - 3.3077115913 * mdt2 + 0.2309699292 * sdt2

            u_r = r1 / (r1 ** 2 - 0.5 * r * r2)
            t_r = -r * u_r

            g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s - 1
            g1 = -1.2684380046 * ldt + 2.6097574011 * mdt - 0.3413193965 * sdt
            g2 = -1.2684380046 * ldt2 + 2.6097574011 * mdt2 - 0.3413193965 * sdt2

            u_g = g1 / (g1 ** 2 - 0.5 * g * g2)
            t_g = -g * u_g

            b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s - 1
            b1 = -0.0041960863 * ldt - 0.7034186147 * mdt + 1.7076147010 * sdt
            b2 = -0.0041960863 * ldt2 - 0.7034186147 * mdt2 + 1.7076147010 * sdt2

            u_b = b1 / (b1 ** 2 - 0.5 * b * b2)
            t_b = -b * u_b

            t_r = t_r if u_r >= 0 else float('inf')
            t_g = t_g if u_g >= 0 else float('inf')
            t_b = t_b if u_b >= 0 else float('inf')

            t += min(t_r, t_g, t_b)

    return t


def get_ST_max(a_, b_, cusp=None):
    if not cusp:
        cusp = find_cusp(a_, b_)
    
    L = cusp[0]
    C = cusp[1]
    return [C / L, C / (1 - L)]

def get_ST_mid(a_, b_):
    S = 0.11516993 + 1 / (
        7.44778970 + 4.15901240 * b_
        + a_ * (
            -2.19557347 + 1.75198401 * b_
            + a_ * (
                -2.13704948 - 10.02301043 * b_
                + a_ * (-4.24894561 + 5.38770819 * b_ + 4.69891013 * a_)
            )
        )
    )

    T = 0.11239642 + 1 / (
        1.61320320 - 0.68124379 * b_
        + a_ * (
            0.40370612 + 0.90148123 * b_
            + a_ * (
                -0.27087943 + 0.61223990 * b_
                + a_ * (0.00299215 - 0.45399568 * b_ - 0.14661872 * a_)
            )
        )
    )

    return [S, T]

def get_Cs(L, a_, b_):
    cusp = find_cusp(a_, b_)
    
    C_max = find_gamut_intersection(a_, b_, L, 1, L, cusp)
    ST_max = get_ST_max(a_, b_, cusp)
    
    S_mid = get_ST_mid(a_, b_)[0]
    T_mid = get_ST_mid(a_, b_)[1]
    
    k = C_max / min(L * ST_max[0], (1 - L) * ST_max[1])
    
    C_a = L * S_mid
    C_b = (1 - L) * T_mid
    
    C_mid = 0.9 * k * math.sqrt(math.sqrt(1 / (1 / (C_a ** 4) + 1 / (C_b ** 4))))
    
    C_a = L * 0.4
    C_b = (1 - L) * 0.8
    
    C_0 = math.sqrt(1 / (1 / (C_a ** 2) + 1 / (C_b ** 2)))
    
    return [C_0, C_mid, C_max]


def okhsl_to_srgb(h, s, l):
    if l >= 1:
        return [255, 255, 255]
    elif l <= 0:
        return [0, 0, 0]

    a_ = math.cos(2 * math.pi * h)
    b_ = math.sin(2 * math.pi * h)
    L = toe_inv(l)

    Cs = get_Cs(L, a_, b_)
    C_0, C_mid, C_max = Cs

    if s < 0.8:
        t = 1.25 * s
        k_0 = 0
        k_1 = 0.8 * C_0
        k_2 = (1 - k_1 / C_mid)
    else:
        t = 5 * (s - 0.8)
        k_0 = C_mid
        k_1 = 0.2 * C_mid * C_mid * 1.25 * 1.25 / C_0
        k_2 = (1 - (k_1) / (C_max - C_mid))

    C = k_0 + t * k_1 / (1 - k_2 * t)

    rgb = oklab_to_linear_srgb(L, C * a_, C * b_)
    return [
        255 * srgb_transfer_function(rgb[0]),
        255 * srgb_transfer_function(rgb[1]),
        255 * srgb_transfer_function(rgb[2]),
    ]

def srgb_to_okhsl(r, g, b):
    lab = linear_srgb_to_oklab(
        srgb_transfer_function_inv(r / 255),
        srgb_transfer_function_inv(g / 255),
        srgb_transfer_function_inv(b / 255)
    )

    C = math.sqrt(lab[1] * lab[1] + lab[2] * lab[2])
    a_ = lab[1] / C
    b_ = lab[2] / C

    L = lab[0]
    h = 0.5 + 0.5 * math.atan2(-lab[2], -lab[1]) / math.pi

    Cs = get_Cs(L, a_, b_)
    C_0, C_mid, C_max = Cs

    if C < C_mid:
        k_0 = 0
        k_1 = 0.8 * C_0
        k_2 = (1 - k_1 / C_mid)

        t = (C - k_0) / (k_1 + k_2 * (C - k_0))
        s = t * 0.8
    else:
        k_0 = C_mid
        k_1 = 0.2 * C_mid * C_mid * 1.25 * 1.25 / C_0
        k_2 = (1 - (k_1) / (C_max - C_mid))

        t = (C - k_0) / (k_1 + k_2 * (C - k_0))
        s = 0.8 + 0.2 * t

    l = toe(L)
    return [h, s, l]

def okhsv_to_srgb(h, s, v):
    a_ = math.cos(2 * math.pi * h)
    b_ = math.sin(2 * math.pi * h)

    ST_max = get_ST_max(a_, b_)
    S_max, S_0, T = ST_max[0], 0.5, ST_max[1]
    k = 1 - S_0 / S_max

    L_v = 1 - s * S_0 / (S_0 + T - T * k * s)
    C_v = s * T * S_0 / (S_0 + T - T * k * s)

    L = v * L_v
    C = v * C_v

    L_vt = toe_inv(L_v)
    C_vt = C_v * L_vt / L_v

    L_new = toe_inv(L)
    C = C * L_new / L
    L = L_new

    rgb_scale = oklab_to_linear_srgb(L_vt, a_ * C_vt, b_ * C_vt)
    scale_L = math.cbrt(1 / max(rgb_scale[0], rgb_scale[1], rgb_scale[2], 0))

    L *= scale_L
    C *= scale_L

    rgb = oklab_to_linear_srgb(L, C * a_, C * b_)
    return [
        255 * srgb_transfer_function(rgb[0]),
        255 * srgb_transfer_function(rgb[1]),
        255 * srgb_transfer_function(rgb[2]),
    ]

def srgb_to_okhsv(r, g, b):
    lab = linear_srgb_to_oklab(
        srgb_transfer_function_inv(r / 255),
        srgb_transfer_function_inv(g / 255),
        srgb_transfer_function_inv(b / 255)
    )

    C = math.sqrt(lab[1] * lab[1] + lab[2] * lab[2])
    a_ = lab[1] / C
    b_ = lab[2] / C

    L = lab[0]
    h = 0.5 + 0.5 * math.atan2(-lab[2], -lab[1]) / math.pi

    ST_max = get_ST_max(a_, b_)
    S_max, S_0, T = ST_max[0], 0.5, ST_max[1]
    k = 1 - S_0 / S_max

    t = T / (C + L * T)
    L_v = t * L
    C_v = t * C

    L_vt = toe_inv(L_v)
    C_vt = C_v * L_vt / L_v

    rgb_scale = oklab_to_linear_srgb(L_vt, a_ * C_vt, b_ * C_vt)
    scale_L = math.cbrt(1 / max(rgb_scale[0], rgb_scale[1], rgb_scale[2], 0))

    L /= scale_L
    C /= scale_L

    C = C * toe(L) / L
    L = toe(L)

    v = L / L_v
    s = (S_0 + T) * C_v / ((T * S_0) + T * k * C_v)

    return [h, s, v]

def hex_to_rgb(hex):
    if hex.startswith("#"):
        hex = hex[1:]

    if len(hex) == 3:  # e.g., #RGB
        r = int(hex[0], 16) / 15 * 255
        g = int(hex[1], 16) / 15 * 255
        b = int(hex[2], 16) / 15 * 255
        return [r, g, b]

    if len(hex) == 6:  # e.g., #RRGGBB
        r = int(hex[0:2], 16)
        g = int(hex[2:4], 16)
        b = int(hex[4:6], 16)
        return [r, g, b]

    if len(hex) == 1:  # e.g., #A
        a = int(hex[0], 16) / 15 * 255
        return [a, a, a]

    if len(hex) == 2:  # e.g., #AA
        a = int(hex[0:2], 16)
        return [a, a, a]

    return None

def rgb_to_hex(r, g, b):
    def component_to_hex(x):
        hex = (max(0,min(255,round(x)))).to_bytes(1, 'big').hex()
        return hex if len(hex) == 2 else '0' + hex

    return f"#{component_to_hex(r)}{component_to_hex(g)}{component_to_hex(b)}"

def merge(col1,col2,amount):
    lerp = lambda a, b, t : a + (b-a) * t
    return [lerp(a, b, amount) for a, b in zip(col1, col2)]

# Test
# conv = srgb_to_okhsl(255,128,64)
# print(conv[0]*360, conv[1], conv[2])
# print(okhsl_to_srgb(*srgb_to_okhsl(255,128,64)))