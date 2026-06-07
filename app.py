import streamlit as st

# 1. EMBEDDED CAR DATABASE (EASY TO EXPAND AT THE TOP)
CAR_DATABASE = {
    "Custom / Manual Entry": {
        "weight": 3200, "dist": 54, "torque": 550, "redline": 8000, "drive": "AWD", "gears": 6
    },
    "2024 Ford Mustang Dark Horse": {
        "weight": 3850, "dist": 53, "torque": 418, "redline": 7500, "drive": "RWD", "gears": 6
    },
    "2024 Ford Mustang GTD": {
        "weight": 3500, "dist": 50, "torque": 564, "redline": 7500, "drive": "RWD", "gears": 8
    },
    "2023 Chevrolet Corvette Z06": {
        "weight": 3500, "dist": 40, "torque": 460, "redline": 8600, "drive": "RWD", "gears": 8
    },
    "2021 Audi RS 6 Avant": {
        "weight": 4700, "dist": 55, "torque": 590, "redline": 7000, "drive": "AWD", "gears": 8
    },
    "2020 Chevrolet Corvette Stingray": {
        "weight": 3650, "dist": 40, "torque": 470, "redline": 6600, "drive": "RWD", "gears": 8
    },
    "2019 Aston Martin DBS Superleggera": {
        "weight": 3730, "dist": 51, "torque": 664, "redline": 7200, "drive": "RWD", "gears": 8
    },
    "2017 Alfa Romeo Giulia Quadrifoglio": {
        "weight": 3800, "dist": 50, "torque": 443, "redline": 7000, "drive": "RWD", "gears": 6
    },
    "2002 Acura RSX Type S": {
        "weight": 2780, "dist": 61, "torque": 142, "redline": 8200, "drive": "FWD", "gears": 6
    }
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

# ADD CAR SELECTOR BOX AT THE TOP
st.header("Select Your Vehicle")
selected_car = st.selectbox("Choose a car from the library to auto-fill specs:", list(CAR_DATABASE.keys()))
defaults = CAR_DATABASE[selected_car]

col1, col2 = st.columns(2)

with col1:
    st.header("Car Specs")
    # Form elements now dynamically bind to the selected car dictionary defaults
    weight = st.number_input("Weight (lbs)", value=defaults["weight"], step=50)
    dist = st.slider("Front Weight Distribution (%)", min_value=30, max_value=70, value=defaults["dist"])
    torque = st.number_input("Peak Torque (lb-ft)", value=defaults["torque"], step=10)
    redline = st.number_input("Redline RPM", value=defaults["redline"], step=500)
    
    # Calculate index positions for select boxes safely
    dt_options = ["AWD", "RWD", "FWD"]
    drive_type = st.selectbox("Drivetrain", dt_options, index=dt_options.index(defaults["drive"]))
    gears = st.slider("Transmission Gears", min_value=4, max_value=10, value=defaults["gears"])

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
