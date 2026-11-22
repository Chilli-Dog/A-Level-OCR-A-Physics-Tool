import random
import math

C = 3e8

def sig(x, n=3):
    return float(f"{x:.{n}g}")

QUESTION_TYPES = {
    "Snell's Law ONE": {
        "question": "The speed of light in air is ~3.0×10⁸ m s⁻¹ and the speed of light in glass is {v}×10⁸ m s⁻¹. A ray of monochromatic light in glass strikes the glass-air boundary at an angle of {d}° to the boundary.\nWhat is the angle made to the normal by the ray of light leaving the boundary (light goes from glass to air)?",
        "vars": lambda: (
            lambda v: {
                "v": v,
                "d": random.randint(max(1, math.ceil(90 - math.degrees(math.asin(v / 3))) + 1), 89)
            }
        )(round(random.uniform(1.5, 2.5), 2)),
        "solve": lambda v, d: round(math.degrees(math.asin((C/(v*10**8)) * math.sin(math.radians(90 - d)))), 2)
    },
    "Snell's Law TWO": {
        "question": "A ray of monochromatic light is incident at the boundary between two transparent materials of refractive index n₁ and n₂ (going from n₂ to n₁). The critical angle θ is equal to {d}°.\nWhat is the ratio n₁/n₂?",
        "vars": lambda: {
            "d": random.randint(14, 89)
        },
        "solve": lambda d: round(math.sin(math.radians(d)), 2)
    },
    "Snell's Law THREE": {
        "question": "A narrow beam of unpolarised light is incident at the boundary between air and glass. The refractive index of air is 1.00 and the refractive index of the glass is {r}. The angle of incidence of the light is {d}°.\nCalculate the time t taken for the refracted light to travel a depth of {x} cm of glass.",
        "vars": lambda: {
            "r": round(random.uniform(1.3, 2.5), 2),
            "d": round(random.uniform(1.0, 89.0), 1),
            "x": round(random.uniform(0.5, 100.0), 1)
        },
        "solve": lambda r, d, x: sig(((x*math.cos(math.asin(math.sin(math.radians(d)/r))))*10**(-2)*r)/C, 1)
    },
    "Snell's Law FOUR": {
        "question": "Determine the wavelength λ of the light in glass. The refractive index is {r}, the wavelength in air is {w} m.",
        "vars": lambda: {
            "r": round(random.uniform(1.3, 2.5), 2),
            "w": round(random.uniform(1e-11, 1e5), 1)
        },
        "solve": lambda w, r: sig(w/r, 1)
    },
    "Snell's Law FIVE": {
        "question": "Light is incident on glass (with refractive index {r}) at an angle of {d}°. Determine the angle of refraction θ in the glass (from air).",
        "vars": lambda: {
            "d": random.randint(1, 89),
            "r": round(random.uniform(1.3, 2.5), 2)
        },
        "solve": lambda d, r: round(math.degrees(math.asin(math.sin(math.radians(d))/r)), 0)
    },
    "Snell's Law SIX": {
        "question": "The refractive index of scintillator crystal for visible light is {r}. The refractive index of air is 1.00.\nCalculate the critical angle C for this crystal.",
        "vars": lambda: {
            "r": round(random.uniform(1.2, 2.0), 2)
        },
        "solve": lambda r: round(math.degrees(math.asin(1/r)), 2)
    },
    "Snell's Law SEVEN": {
        "question": "Calculate the angle of refraction θ when the angle φ is {d}° where φ is the angle of incidence and n₂ is {x} times greater than n₁.",
        "vars": lambda: {
            "d": random.randint(1, 89),
            "x": round(random.uniform(1.0, 3.0), 1)
        },
        "solve": lambda d, x: round(math.degrees(math.asin(math.sin(math.radians(d))/x)), 1)
    },
    # time period things:
    "Time Period ONE": {
        "question": "Calculate the period T of a light wave in a vacuum with wavelength {w} m",
        "vars": lambda: {
            "w": round(random.uniform(1e-11, 1e5), 1)
        },
        "solve": lambda w: sig(w/C, 3)
    },

    # applied things:
    "ISS Power": {
        "question": "The ISS has arrays of solar cells on its wings. These solar cells charge batteries which power the ISS. The wings always face the Sun. Use the data below to calculate the average power delivered to the batteries:\nThe period of the ISS around the Earth is {t1} minutes.\nThe total area of the cells facing the solar radiation is {a} m².\n{p}% of the energy of the sunlight incident on the cells is stored in the batteries.\nThe intensity of solar radiation at the orbit of the ISS is {i} kW m⁻² outside of the Earth’s shadow and zero inside it.\nThe ISS passes through the Earth’s shadow for {t2} minutes during each orbit.",
        "vars": lambda: {
            "a": round(random.uniform(1000, 3000), 2),
            "i": round(random.uniform(0.8, 2.8), 1), # intensity
            "p": random.randint(2, 20), #percentage absorbed
            "t1": random.randint(80, 100),
            "t2": random.randint(30, 50)
        },
        "solve": lambda a, i, p, t1, t2: round((a * (i * 10**3) * p * (t1 - t2)) / (100 * t1), 2)
    },
}
