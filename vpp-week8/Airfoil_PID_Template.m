%% Airfoil Angle-of-Attack PID Control
% Fixed-axis rotating airfoil with aerodynamic pitching moment
% and a vertical wind-gust disturbance.

clear; close all; clc;

%% Define physical parameters:

rho = 1.225; % Sea level air density [kg/m^3]
V = 15.0; % Freestream airspeed [m/s]
S = 0.25; % Reference area [m^2]
c = 0.20; % Mean chord [m]
Iyy = 0.25; % Pitch moment of inertia [kg*m^2]

%% Aerodynamic derivatives:

Cm_alpha = -0.80; % Static stability derivative [rad^-1]
Cm_delta = 1.0; % Control effectiveness [rad^-1]


%% Command and actuator limits

alpha_setpoint = deg2rad(3); % Desired angle-of-attack [rad]
delta_max = deg2rad(20); % Maximum actuator deflection [rad]
delta_min = -delta_max;

%% Wind-gust perturbation

gust_start_time = 5.0; % Gust begins at 5 seconds
gust_velocity = 0.5; %Vertical gust velocity [m/s]

%% Initial conditions

theta_0 = deg2rad(0);       % Initial pitch angle [rad]
theta_dot_0 = 0;            % Initial pitch rate [rad/s]
integral_error_0 = 0;       % Initial accumulated error

x0 = [theta_0;
      theta_dot_0;
      integral_error_0];

%% Timespan
tspan = [0, 12];

%% PID controller gains — tune these values

Kp = 0.0;
Ki = 0.0;
Kd = 0.0;

%% Tasks
% 1. Calculate the dynamic pressure and aerodynamic coefficients.
% 2. Convert the equation of motion into state-space form.
% 3. Implement the equations of motion in an ODE function.
% 4. Simulate the system using ode45.
% 5. Tune the PID gains and plot the system response.



