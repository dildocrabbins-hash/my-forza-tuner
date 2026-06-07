import streamlit as st

# 1. EXPANDED CAR DATABASE (SORTED AUTOMATICALLY)
CAR_DATABASE = {
    "Custom / Manual Entry": {"weight": 3200, "dist": 54, "torque": 550, "redline": 8000, "drive": "AWD", "gears": 6},
    "Acura RSX Type S (2002)": {"weight": 2780, "dist": 61, "torque": 142, "redline": 8200, "drive": "FWD", "gears": 6},
    "Alfa Romeo Giulia Quadrifoglio (2017)": {"weight": 3800, "dist": 50, "torque": 443, "redline": 7000, "drive": "RWD", "gears": 6},
    "Alpine A110 (2017)": {"weight": 2432, "dist": 44, "torque": 236, "redline": 6800, "drive": "RWD", "gears": 7},
    "Aston Martin DBS Superleggera (2019)": {"weight": 3730, "dist": 51, "torque": 664, "redline": 7200, "drive": "RWD", "gears": 8},
    "Aston Martin Vantage (2019)": {"weight": 3373, "dist": 50, "torque": 505, "redline": 7000, "drive": "RWD", "gears": 8},
    "Audi R8 V10 Plus (2016)": {"weight": 3483, "dist": 42, "torque": 413, "redline": 8500, "drive": "AWD", "gears": 7},
    "Audi RS 6 Avant (2021)": {"weight": 4700, "dist": 55, "torque": 590, "redline": 7000, "drive": "AWD", "gears": 8},
    "BMW M3 Competition (2021)": {"weight": 3890, "dist": 52, "torque": 479, "redline": 7200, "drive": "RWD", "gears": 8},
    "BMW M5 CS (2022)": {"weight": 4114, "dist": 54, "torque": 553, "redline": 7000, "drive": "AWD", "gears": 8},
    "Chevrolet Corvette Stingray (2020)": {"weight": 3650, "dist": 40, "torque": 470, "redline": 6600, "drive": "RWD", "gears": 8},
    "Chevrolet Corvette Z06 (2023)": {"weight": 3500, "dist": 40, "torque": 460, "redline": 8600, "drive": "RWD", "gears": 8},
    "Dodge Charger SRT Hellcat (2015)": {"weight": 4575, "dist": 56, "torque": 650, "redline": 6200, "drive": "RWD", "gears": 8},
    "Ferrari 488 Pista (2019)": {"weight": 3053, "dist": 42, "torque": 561, "redline": 8000, "drive": "RWD", "gears": 7},
    "Ford Mustang Dark Horse (2024)": {"weight": 3850, "dist": 53, "torque": 418, "redline": 7500, "drive": "RWD", "gears": 6},
    "Ford Mustang GTD (2024)": {"weight": 3500, "dist": 50, "torque": 564, "redline": 7500, "drive": "RWD", "gears": 8},
    "Honda Civic Type R (2021)": {"weight": 3121, "dist": 62, "torque": 295, "redline": 7000, "drive": "FWD", "gears": 6},
    "Lamborghini Huracán Evo (2020)": {"weight": 3135, "dist": 43, "torque": 443, "redline": 8500, "drive": "AWD", "gears": 7},
    "McLaren 720S Spider (2019)": {"weight": 3236, "dist": 42, "torque": 568, "redline": 8500, "drive": "RWD", "gears": 7},
    "Nissan GT-R Nismo (2020)": {"weight": 3865, "dist": 54, "torque": 481, "redline": 7000, "drive": "AWD", "gears": 6},
    "Porsche 911 GT3 RS (2023)": {"weight": 3268, "dist": 39, "torque": 342, "redline": 9000, "drive": "RWD", "gears": 7},
    "Toyota GR Supra (2020)": {"weight": 3400, "dist": 50, "torque": 365, "redline": 6500, "drive": "RWD", "gears": 8}
}

class PersonalForzaTuner:
    def __init__(self, weight, front_dist, torque, redline, drive_type="AWD", gears=6):
        self.weight = weight
        self.front_dist = front_dist / 100.0 if front_dist > 1.0 else front_dist
        self.rear_dist = 1.0 - self.front_dist
        self.torque = torque
        self.redline = redline
        self.drive_type = drive_type.upper()
        self.gear_count = gears

    def compute_tune(self):
        tires = {"Front Pressure": "30.5 PSI", "Rear Pressure": "30.0 PSI"} if self.drive_type == "AWD" else \
                {"Front Pressure": "31.0 PSI", "Rear Pressure": "29.5 PSI"} if self.drive_type == "RWD" else \
                {"Front Pressure": "29.5 PSI", "Rear Pressure": "31.0 PSI"}
        
        final_drive = round(3.40 + (self.torque / 1100.0), 2)
        ratios = []
        first = max(2.60, min(round(4.10 - (self.torque / 450.0), 2), 4.30))
        ratios.append(first)
        decay = 0.76 - (self.gear_count * 0.008)
        current = first
        for i in range(1, self.gear_count):
            current *= (decay + (i * 0.018))
            ratios.append(round(max(0.50, current), 2))
        gearing = {"Final Drive": final_drive}
        for idx, r in enumerate(ratios, 1):
            gearing[f"Gear {idx}"] = r

        alignment = {"Front Camber": "-2.0°", "Rear Camber": "-1.2°", "Front Toe": "0.0°", "Rear Toe": "0.0°", "Caster": "6.4°"}

        f_arb = 1.0 + (64.0 * self.front_dist)
        r_arb = 1.0 + (64.0 * self.rear_dist)
        arbs = {"Front ARB": round(f_arb - 3.0, 1), "Rear ARB": round(r_arb + 2.0, 1)}

        f_spring = ((1200.0 - 100.0) * self.front_dist) + 100.0
        r_spring = ((1200.0 - 100.0) * self.rear_dist) + 100.0
        springs = {"Front Springs": f"{round(f_spring, 1)} lb/in", "Rear Springs": f"{round(r_spring, 1)} lb/in", "Front Ride Height": "4.2 in", "Rear Ride Height": "4.4 in"}

        f_reb = 1.0 + (19.0 * self.front_dist)
        r_reb = 1.0 + (19.0 * self.rear_dist)
        damping = {"Front Rebound": round(f_reb, 1), "Rear Rebound": round(r_reb, 1), "Front Bump": round(f_reb * 0.55, 1), "Rear Bump": round(r_reb * 0.55, 1)}

        if self.drive_type == "AWD":
            diff = {"Front Accel": "50%", "Front Decel": "0%", "Rear Accel": "85%", "Rear Decel": "30%", "Center Bias": "65% Rear"}
        elif self.drive_type == "RWD":
            diff = {"Rear Accel": "75%", "Rear Decel": "25%"}
        else:
            diff = {"Front Accel": "45%", "Front Decel": "10%"}

        return {"TIRES": tires, "GEARING": gearing, "ALIGNMENT": alignment, "ANTI-ROLL BARS": arbs, "SPRINGS": springs, "DAMPING": damping, "DIFFERENTIAL": diff}

st.set_page_config(page_title="Personal Forza 6 Tuner", layout="wide")
st.title("🏎️ My Personal Forza Horizon 6 Tuner")

st.header("Search & Select Vehicle")

# MOBILE NAVIGATION FIX: Add a real-time typing search filter box
search_query = st.text_input("Type here to filter cars (e.g., 'Mustang', 'BMW', 'Corvette'):", "").strip().lower()

# Get all keys, put Manual Entry at the top, and alphabetize the rest perfectly
all_cars = list(CAR_DATABASE.keys())
preset_cars = [c for c in all_cars if c != "Custom / Manual Entry"]
preset_cars.sort()

# Dynamically filter the list based on what the user types on their phone keyboard
filtered_cars = ["Custom / Manual Entry"] + [car for car in preset_cars if search_query in car.lower()]

selected_car = st.selectbox("Matching Results:", filtered_cars)
defaults = CAR_DATABASE[selected_car]

col1, col2 = st.columns(2)

with col1:
    st.header("Chassis & Engine Specs")
    weight = st.number_input("Weight (lbs)", value=defaults["weight"], step=50)
    dist = st.slider("Front Weight Distribution (%)", min_value=30, max_value=70, value=defaults["dist"])
    torque = st.number_input("Peak Torque (lb-ft)", value=defaults["torque"], step=10)
    redline = st.number_input("Redline RPM", value=defaults["redline"], step=500)
    
    dt_options = ["AWD", "RWD", "FWD"]
    drive_type = st.selectbox("Drivetrain Layout", dt_options, index=dt_options.index(defaults["drive"]))
    gears = st.slider("Transmission Gear Count", min_value=4, max_value=10, value=defaults["gears"])

with col2:
    st.header("Tab-by-Tab Configuration")
    engine = PersonalForzaTuner(weight, dist, torque, redline, drive_type, gears)
    tune_results = engine.compute_tune()
    
    ui_tabs = st.tabs(list(tune_results.keys()))
    for idx, (tab_name, data_dict) in enumerate(tune_results.items()):
        with ui_tabs[idx]:
            st.subheader(f"{tab_name} Settings")
            for param, val in data_dict.items():
                st.metric(label=param, value=str(val))
