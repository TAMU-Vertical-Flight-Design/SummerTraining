import aerosandbox as asb
import aerosandbox.numpy as np # we don't actually end up using this, but it may be helpful to see how aerosandbox has its own numpy wrapper
# for those that don't know, numpy is a python library for doing a lot of matrix math and linear algebra, which is very useful for aero calculations
# probably will end up being your most used module in college! (at least it was mine for sure)

'''
Week 4 Aerodynamics Summer Training: Aerosandbox Example Code

please make sure you have correctly set up your .venv and installed aerosandbox
see README.md for instructions

The point of this python script is for you to walk through the code and understand what it's doing
I understand you may not be familiar with the math behind it, but the goal is to understand what aerosandbox is doing
'''

######### Section 1: Flight Condition #########
# Define the operating point we're optimizing for (cruise)
# aerosandbox uses SI units unless otherwise specified

cruise_conditions = asb.OperatingPoint(
    atmosphere=asb.Atmosphere(altitude=150), # 150 m altitude
    velocity=30, # 30 m/s airspeed
    alpha=5, # 5 deg angle of attack
)
# now we have set our flight condition, this can be used in analysis for calculations




########## Section 2: Set Up the Optimizer #########
# Opti is the environment for optimization, all variables and constraints live here
optimization_environment = asb.Opti()

# we can now use this to optimization_environment.variable() to define design variables, and optimization_environment.subject_to() to define constraints



########## Section 3: Design Variables #########
# These are the wing parameters the optimizer is free to change, ie control parameters/independent variables

span = optimization_environment.variable(init_guess=10, lower_bound=3, upper_bound=20) # m
root_chord = optimization_environment.variable(init_guess=1.2, lower_bound=0.3, upper_bound=3.0) # m
tip_chord = optimization_environment.variable(init_guess=0.6, lower_bound=0.1, upper_bound=1.5) # m
twist_tip = optimization_environment.variable(init_guess=-2, lower_bound=-10, upper_bound=5) # deg (washout)
# the optimizer can change the values of these variables to find the best design, within the bounds specified



######## Section 4: Build the Airplane Geometry #########
# we will build up the airplane piece by piece:

# first airfoil
airfoil = asb.Airfoil("naca2412") # define the airfoil shape

# then wing
wing = asb.Wing(
    name="Main Wing",
    symmetric=True, # mirror across centerline → full span
    xsecs=[
        asb.WingXSec( # Root section ## WingXSec means "Wing Cross Section", X=Cross like on a traffic sign lol
            xyz_le=[0, 0, 0], # leading edge position of the root section
            chord=root_chord, # this is how we denote as root section
            twist=0, # root typically has no twist
            airfoil=airfoil,
        ),
        asb.WingXSec( # Tip section
            xyz_le=[
                0.25 * (root_chord - tip_chord), # quarter-chord sweep
                span / 2, # semi-span
                0
            ],
            chord=tip_chord, # this is how we denote as tip section
            twist=twist_tip, # here too
            airfoil=airfoil,
        ),
    ]
)

# then airplane
airplane = asb.Airplane(
    name="Optimized Wing",
    wings=[wing],
)



########## Section 5: Aerodynamic Analysis (VLM) #########
# now use Vortex Lattice Method (VLM) to analyze the airplane aerodynamics
# this is definitely new to y'all, if you want here's a good resource:
# https://en.wikipedia.org/wiki/Vortex_lattice_method
# Imo, Wikipedia is great for introductions to physics/aero topics

# VLM will solve for lift and induced drag (drag due to lift)

vlm = asb.VortexLatticeMethod(
    airplane=airplane,
    op_point=cruise_conditions,
    spanwise_resolution=12, # panels spanwise per half-wing
    chordwise_resolution=4, # panels chordwise
)

aero = vlm.run() # basically runs the analysis symbolically, this will return an object with all the results of the analysis
# no actual values yet!! remember, the control parameters haven't been solved for yet
# now we need to set up optimization and run


CL = aero["CL"] # lift coefficient
CD = aero["CD"] # drag coefficient (induced)

print(CL, CD, CL/CD)



########### Section 6: Constraints #########
# we can now define constraints on the design variables, to keep the optimizer from going crazy
# for example, we will use taper ratio (tip/root chord) to keep wing shape reasonable

taper_ratio = tip_chord / root_chord
optimization_environment.subject_to([ # .subject_to() sets the constraint
    taper_ratio >= 0.2, # minimum taper ratio
    taper_ratio <= 0.8 # maximum taper ratio
])



########## Find max L/D #########
# the way a lot of optimizers work is they only minimize, not maximize
# to get around this, you often set your objective to be the negative of what you want to maximize 
# L/D = CL/CD, so we will minimize -CL/CD to maximize L/D

# here, we set up what we want to minimize

optimization_environment.minimize(-CL / CD)



########### Section 8: Solve #########
# this is where the optimizer will try to find the best design, given the constraints and objective we set up

solution = optimization_environment.solve(verbose=False) # set verbose=True to see optimizer iterations



########### Section 9: Extract & Display Results #########
# now we can extract the results from the solution object and display them

opt_span = solution(span)
opt_root_chord = solution(root_chord)
opt_tip_chord = solution(tip_chord)
opt_twist = solution(twist_tip)
opt_CL = solution(CL)
opt_CD = solution(CD)
opt_LD = opt_CL / opt_CD

wing_area = 0.5 * (opt_root_chord + opt_tip_chord) * opt_span
aspect_ratio = opt_span ** 2 / wing_area

print("=" * 45)
print("Wing Optimization Results")
print("=" * 45)
print(f"Span: {opt_span:.2f} m")
print(f"Root chord: {opt_root_chord:.2f} m")
print(f"Tip chord: {opt_tip_chord:.2f} m")
print(f"Taper ratio: {opt_tip_chord/opt_root_chord:.3f}")
print(f"Tip twist: {opt_twist:.2f} deg")
print(f"Wing area: {wing_area:.2f} m²")
print(f"Aspect ratio: {aspect_ratio:.2f}")
print()
print(f'Old CL: {CL:.4f}')
print(f'Old CD (induced): {CD:.4f}')
print(f'Old L/D: {CL/CD:.2f}')
print()
print(f"New CL: {opt_CL:.4f}")
print(f"New CD (induced): {opt_CD:.4f}")
print(f"New L/D:  {opt_LD:.2f}")
print("=" * 45)