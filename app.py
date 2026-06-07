import streamlit as st

# 1. COMPREHENSIVE CAR DATABASE (ALPHABETIZED WITH META ATTRIBUTES)
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

class ForzaMetaDragTuner:
    def __init__(self, weight, front_dist, torque, redline, drive_type, gears, target_track):
        self.weight = weight
        self.front_dist = front_dist / 100.0 if front_dist > 1.0 else front_dist
        self.rear_dist = 1.0 - self.front_dist
        self.torque = torque
        self.redline = redline
        self.drive_type = drive_type.upper()
        self.gear_count = gears
        self.track = target_track

    def compute_meta_tune(self):
        # --- TAB 1: TIRES ---
        if self.drive_type == "FWD":
            tires = {"Front Tire Pressure": "15.0 PSI (Max Launch Patch)", "Rear Tire Pressure": "45.0 PSI (Min Drag)"}
        elif self.drive_type == "RWD":
            tires = {"Front Tire Pressure": "45.0 PSI (Min Drag)", "Rear Tire Pressure": "15.0 PSI (Max Launch Patch)"}
        else:
            tires = {"Front Tire Pressure": "22.0 PSI (Balanced Grab)", "Rear Tire Pressure": "15.0 PSI (Squat Traction)"}

        # --- TAB 2: GEARING ---
        track_modifiers = {"1/4 Mile": 1.15, "1 KM": 0.95, "1/2 Mile": 0.85}
        mod = track_modifiers.get(self.track, 1.0)
        base_fd = 2.80 + (self.torque / 750.0)
        final_drive = round(max(2.20, min(base_fd * mod, 6.10)), 2)
        
        ratios = []
        first_gear = round(3.80 - (self.torque / 500.0), 2)
        first_gear = max(2.20, min(first_gear, 4.50))
        ratios.append(first_gear)
        
        decay = 0.74 - (self.gear_count * 0.005)
        current = first_gear
        for i in range(1, self.gear_count):
            current *= (decay + (i * 0.015))
            ratios.append(round(max(0.40, current), 2))
            
        gearing = {"Final Drive": final_drive}
        for idx, r in enumerate(ratios, 1):
            gearing[f"Gear {idx}"] = r

        # --- TAB 3: ALIGNMENT ---
        alignment = {
            "Front Camber": "0.0° (Max Straightline)",
            "Rear Camber": "-0.5° (Compensates for Launch Squat)",
            "Front Toe": "0.0°", "Rear Toe": "0.0°",
            "Front Caster": "7.0° (High Velocity Stability)"
        }

        # --- TAB 4: ANTI-ROLL BARS ---
        arbs = {"Front ARB": "1.0 (Loose - Free Extension)", "Rear ARB": "65.0 (Maximum Stiffness - Stops Twist)"}

        # --- TAB 5: SPRINGS ---
        f_spring = ((600.0 - 50.0) * self.front_dist) + 50.0
        r_spring = ((1200.0 - 200.0) * self.rear_dist) + 200.0
        springs = {
            "Front Springs": f"{round(f_spring, 1)} lb/in (Soft - Lift)",
            "Rear Springs": f"{round(r_spring, 1)} lb/in (Stiff - Load)",
            "Front Ride Height": "Maximum (Promotes Squat)",
            "Rear Ride Height": "Minimum (Keeps CG Low)"
        }

        # --- TAB 6: DAMPING ---
        damping = {
            "Front Rebound": "20.0 (Holds Front Up)", "Rear Rebound": "1.0 (Quick Extension)",
            "Front Bump": "1.0 (Instant Nose Rise)", "Rear Bump": "20.0 (Stops Bottoming Out)"
        }

        # --- TAB 7 & 8: AERO / BRAKES ---
        aero = {"Front Aero": "Minimum Downforce", "Rear Aero": "Minimum Downforce"}
        brakes = {"Brake Balance": "50%", "Brake Pressure": "100%"}

        # --- TAB 9: DIFFERENTIAL ---
        if self.drive_type == "AWD":
            diff = {
                "Front Accel": "100%", "Front Decel": "0%",
                "Rear Accel": "100%", "Rear Decel": "0%",
                "Center Torque Bias": "75% Rear (Optimizes Launch)"
            }
        elif self.drive_type == "RWD":
            diff = {"Rear Accel": "100%", "Rear Decel": "0%"}
        else:
            diff = {"Front Accel": "100%", "Front Decel": "0%"}

        return {
            "TIRES": tires, "GEARING": gearing, "ALIGNMENT": alignment,
            "ANTI-ROLL BARS": arbs, "SPRINGS": springs, "DAMPING": damping,
            "AERO & BRAKES": {**aero, **brakes}, "DIFFERENTIAL": diff
        }

# --- SCREEN RENDERING LAYER ---
st.set_page_config(page_title="Personal Forza 6 Drag Tuner", layout="wide")
st.title("🏁 My Personal Meta Drag Tuning Suite")

st.header("1. Target Configuration")
search_query = st.text_input("Type here to filter cars (e.g., 'Mustang', 'BMW'):", "").strip().lower()

all_cars = list(CAR_DATABASE.keys())
preset_cars = [c for c in all_cars if c != "Custom / Manual Entry"]
preset_cars.sort()
filtered_cars = ["Custom / Manual Entry"] + [car for car in preset_cars if search_query in car.lower()]

selected_car = st.selectbox("Select Your Car:", filtered_cars)
defaults = CAR_DATABASE[selected_car]

track_choice = st.radio(
    "Choose Target Dragstrip Length:",
    ["1/4 Mile", "1 KM", "1/2 Mile"],
    horizontal=True
)

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.header("2. Vehicle Parameters")
    weight = st.number_input("Weight (lbs)", value=defaults["weight"], step=50)
    dist = st.slider("Front Weight Distribution (%)", min_value=30, max_value=70, value=defaults["dist"])
    torque = st.number_input("Peak Torque (lb-ft)", value=defaults["torque"], step=10)
    redline = st.number_input("Redline RPM", value=defaults["redline"], step=500)
    
    dt_options = ["AWD", "RWD", "FWD"]
    drive_type = st.selectbox("Drivetrain Layout", dt_options, index=dt_options.index(defaults["drive"]))
    gears = st.slider("Transmission Gear Count", min_value=4, max_value=10, value=defaults["gears"])

with col2:
    st.header(f"3. In-Game Tune ({track_choice})")
    tuner_engine = ForzaMetaDragTuner(weight, dist, torque, redline, drive_type, gears, track_choice)
    tune_specs = tuner_engine.compute_meta_tune()
    
    ui_tabs = st.tabs(list(tune_specs.keys()))
    for idx, (tab_name, data_dict) in enumerate(tune_specs.items()):
        with ui_tabs[idx]:
            st.subheader(f"{tab_name} Settings")
            for param, val in data_dict.items():
                st.metric(label=param, value=str(val))
