import aerosandbox as asb
import aerosandbox.numpy as np

# =========================================================
# 1. CONSTANTS (From Week 6 / XFLR5 Data)
# =========================================================
S = 0.236          # m^2 : Surface Area
V_cruise = 14.5    # m/s : Cruise Speed
V_stall = 8.0      # m/s : Stall Speed

rho_foam = 19.22   # kg/m^3 : Wing foam density (from assignment instructions)
g = 9.81           # m/s^2 : Gravity

# Bounds for wingspan based on your 1.5m XFLR5 baseline
min_b = 0.8        # m : Minimum realistic wingspan
max_b = 2.5        # m : Maximum realistic wingspan

# =========================================================
# 2. SETUP TRACKING VARIABLES
# =========================================================
airfoils_to_test = ["naca0012", "naca0014", "naca2412", "naca4412"]

best_score = -np.inf
best_airfoil = None
best_span = 0
best_chord = 0

print("=" * 50)
print("Starting Airfoil Optimization")
print("=" * 50)

# =========================================================
# 3. OPTIMIZATION LOOP
# =========================================================
for af_name in airfoils_to_test:
    
    # Create a fresh optimization environment for each airfoil
    opti = asb.Opti()
    
    # --- Design Variables ---
    # The optimizer will test different wingspans and angles of attack
    b = opti.variable(init_guess=1.5, lower_bound=min_b, upper_bound=max_b)
    alpha = opti.variable(init_guess=3.0, lower_bound=-5, upper_bound=12)
    
    # --- Dependent Variables ---
    c = S / b  # Chord is dictated by the fixed Surface Area and variable span
    
    # --- Wing Weight Calculation ---
    airfoil = asb.Airfoil(af_name)
    # airfoil.area() is normalized. Multiply by c^2 to get true cross-sectional area
    cross_section_area = airfoil.area() * (c**2) 
    volume = cross_section_area * b
    weight = volume * rho_foam * g
    
    # --- Assemble Airplane Geometry ---
    # Building a simple rectangular wing using b and c
    wing = asb.Wing(
        symmetric=True,
        xsecs=[
            asb.WingXSec(
                xyz_le=[0, 0, 0], 
                chord=c, 
                airfoil=airfoil
            ),
            asb.WingXSec(
                xyz_le=[0, b / 2, 0], # Tip is at half-span because symmetric=True
                chord=c, 
                airfoil=airfoil
            )
        ]
    )
    airplane = asb.Airplane(wings=[wing])
    
# --- Aerodynamic Analysis (VLM) ---
    op_point = asb.OperatingPoint(
        velocity=V_cruise,
        alpha=alpha
    )
    
    vlm = asb.VortexLatticeMethod(
        airplane=airplane,
        op_point=op_point,
        spanwise_resolution=12,
        chordwise_resolution=4
    )
    
    aero = vlm.run()
    CL = aero["CL"]
    CD = aero["CD"]
    
    # --- Objective & Constraints ---
    # Objective: Maximize (CL/CD) / W. (We minimize the negative to achieve this)
    objective = (CL / CD) / weight
    opti.minimize(-objective)
    
    # Optional Stall Constraint: Ensure the wing can support the 827g mass at V_stall
    # (Assuming a max lift coefficient of ~1.2 for standard airfoils)
    # opti.subject_to(0.5 * 1.225 * (V_stall**2) * S * 1.2 >= (0.827 * g))
    
    # --- Solve ---
    try:
        # verbose=False keeps the terminal output clean
        sol = opti.solve(verbose=False) 
        
        # Extract optimized values
        score = sol.value(objective)
        opt_b = sol.value(b)
        opt_c = sol.value(c)
        
        print(f"[{af_name}] Success! Score: {score:.3f} | Span: {opt_b:.2f}m | Chord: {opt_c:.2f}m")
        
        # Check if this is our new winner
        if score > best_score:
            best_score = score
            best_airfoil = af_name
            best_span = opt_b
            best_chord = opt_c
            
    except Exception as e:
        print(f"[{af_name}] Optimization failed within bounds.")

# =========================================================
# 4. FINAL RESULTS
# =========================================================
print("=" * 50)
print(f"WINNING AIRFOIL: {best_airfoil}")
print(f"OPTIMAL SPAN:    {best_span:.2f} m")
print(f"OPTIMAL CHORD:   {best_chord:.2f} m")
print(f"MAX SCORE:       {best_score:.3f}")
print("=" * 50)