import casadi as ca
import numpy as np
import matplotlib.pyplot as plt

# define a MPC function
# Input: initial state, time horizon, penalty start;
# Return: the next time step, optimal sequence of states, optimal sequence of control actions

## make a function for ploting

def MPC_MC(x0, penalty_start, N):
    # Create non-convex optimization problem
    opti = ca.Opti()

    # Variables
    x = opti.variable(2, N + 1)  # State trajectory (position and velocity)
    u = opti.variable(1, N)  # Control trajectory (force)

    # Reward variable (no need to define this as an optimization variable, we will add it directly to the cost)
    reward_value = -1000  # Large reward for reaching the goal (negative cost)

    # Initialize the cost to 0
    cost = 0

    # Define the dynamics and cost function
    for k in range(N):
        # Mountain Car dynamics
        position_k = x[0, k]
        velocity_k = x[1, k]
        force_k = u[0, k]

        # Apply the Mountain Car dynamics model
        velocity_next = velocity_k + (0.0015 * force_k - 0.0025 * ca.cos(3 * position_k))
        position_next = position_k + velocity_next

        # Apply dynamics constraints
        opti.subject_to(x[0, k + 1] == position_next)
        opti.subject_to(x[1, k + 1] == velocity_next)

        # Reward for reaching the goal
        cost += reward_value * ca.fmax(0, x[0, k] - 0.45)  # Add reward if position exceeds 0.45

    # Add a cost for the last 30 states to be as close to the goal set (0.45) as possible
    for k in range(penalty_start, N + 1):
        cost += 10 * (x[0, k] - 0.45) ** 2  # Penalize deviation from the goal

    # Set the objective to minimize cost (which now includes both the reward and the last 30-state penalty)
    opti.minimize(cost)

    # State constraints
    for k in range(N):
        opti.subject_to(x[0, k] >= -1.2)  # Minimum position
        opti.subject_to(x[0, k] <= 0.6)  # Maximum position
        opti.subject_to(x[1, k] >= -0.07)  # Minimum velocity
        opti.subject_to(x[1, k] <= 0.07)  # Maximum velocity

        # Control input bounds
        opti.subject_to(u[0, k] >= -1.0)
        opti.subject_to(u[0, k] <= 1.0)

    # Initial state constraint
    opti.subject_to(x[:, 0] == x0)

    # Set solver (IPOPT for nonlinear problems)
    opti.solver('ipopt')

    # Solve the optimization problem
    sol = opti.solve()

    # Extract the solution
    x_opt = sol.value(x)
    u_opt = sol.value(u)

    return x_opt, u_opt



# Define position and velocity ranges
position_range = np.arange(-0.5, -0.4, 0.001)  # Position from -0.3 to -0.05 with step 0.02
velocity_range = np.arange(-0.04, 0.04, 0.01)  # Velocity from 0.0 to 0.05 with step 0.01

# Generate all combinations of position and velocity
# Parameters
N = 110  # Time horizon
penalty_start = N - 30  # Start penalizing from this step
#x0 = np.array([0.2, 0])  # Example initial state
initial_states = [np.array([position, velocity]) for position in position_range for velocity in velocity_range]

# Loop through initial states and solve the MPC problem for each one
success_init_state = []; failed_init_state = []
success_init_action = []; failed_init_action = []
for i, x0 in enumerate(initial_states):
    x_opt, u_opt = MPC_MC(x0, penalty_start, N)
    # print(f"Optimal state trajectory for x0 = {x0}:\n", x_opt)
    # print(f"Optimal control trajectory for x0 = {x0}:\n", u_opt)
    if x_opt[0, -1] > 0.45:
        success_init_state.append(x0)
        success_init_action.append(u_opt)
    else:
        failed_init_state.append(x0)
        failed_init_action.append(u_opt)



pos_list = x_opt[0,:]
#position = [item[0] for item in x_opt]
plt.plot(pos_list)
plt.title("State List Plot")
plt.xlabel("Index")
plt.ylabel("Position Value")
plt.show()




#
# # Create non-convex optimization problem
# opti = ca.Opti()
#
# # Parameters
# N = 110  # Time horizon
# #dt = 0.05  # Time step
# penalty_start = N - 30  # Start penalizing from this step
#
# # Variables
# x = opti.variable(2, N+1)  # State trajectory (position and velocity)
# u = opti.variable(1, N)    # Control trajectory (force)
#
# # Reward variable (no need to define this as an optimization variable, we will add it directly to the cost)
# reward_value = -1000  # Large reward for reaching the goal (negative cost)
#
# # Initialize the cost to 0
# cost = 0
#
# # Define the dynamics and cost function
# for k in range(N):
#     # Mountain Car dynamics
#     position_k = x[0, k]
#     velocity_k = x[1, k]
#     force_k = u[0, k]
#
#     # Apply the Mountain Car dynamics model
#     velocity_next = velocity_k + (0.0015 * force_k - 0.0025 * ca.cos(3 * position_k))
#     position_next = position_k + velocity_next
#
#     # Apply dynamics constraints
#     opti.subject_to(x[0, k+1] == position_next)
#     opti.subject_to(x[1, k+1] == velocity_next)
#
#     # Reward for reaching the goal
#     cost += reward_value * ca.fmax(0, x[0, k] - 0.45)  # Add reward if position exceeds 0.45
#
# # Add a cost for the last 30 states to be as close to the goal set (0.45) as possible
# for k in range(penalty_start, N+1):
#     cost += 10 * (x[0, k] - 0.45) ** 2  # Penalize deviation from the goal
#
# # Set the objective to minimize cost (which now includes both the reward and the last 30-state penalty)
# opti.minimize(cost)
#
# # State constraints
# for k in range(N):
#     opti.subject_to(x[0, k] >= -1.2)  # Minimum position
#     opti.subject_to(x[0, k] <= 0.6)   # Maximum position
#     opti.subject_to(x[1, k] >= -0.07)  # Minimum velocity
#     opti.subject_to(x[1, k] <= 0.07)   # Maximum velocity
#
#     # Control input bounds
#     opti.subject_to(u[0, k] >= -1.0)
#     opti.subject_to(u[0, k] <= 1.0)
#
# # Initial state constraint
# x0 = np.array([0.2, 0])  # Example initial state
# opti.subject_to(x[:, 0] == x0)
#
# # Set solver (IPOPT for nonlinear problems)
# opti.solver('ipopt')
#
# # Solve the optimization problem
# sol = opti.solve()
#
# # Extract the solution
# x_opt = sol.value(x)
# u_opt = sol.value(u)
#
# print("Optimal state:", x_opt)
# print("Optimal control:", u_opt)
#
# pos_list = x_opt[0,:]
# #position = [item[0] for item in x_opt]
# plt.plot(pos_list)
# plt.title("State List Plot")
# plt.xlabel("Index")
# plt.ylabel("Position Value")
# plt.show()
#
#
#
# #################
# # 1st version of MPC by
# def solve_mpc_for_initial_state(x0):
#     # Create non-convex optimization problem
#     opti = ca.Opti()
#
#     # Parameters
#     N = 30  # Horizon length
#     #dt = 0.05  # Time step
#
#     # Variables
#     x = opti.variable(2, N+1)  # State trajectory (position and velocity)
#     u = opti.variable(1, N)  # Control trajectory (force)
#
#     # Cost matrices
#     Q = 0.001*np.eye(2)  # State cost matrix
#     R = 0.01 * np.eye(1)  # Control cost matrix (scaled down)
#
#     # Define the dynamics and cost function
#     cost = 0
#     for k in range(N):
#         # Cost function: quadratic cost on state and control
#         cost += ca.mtimes([x[:, k].T, Q, x[:, k]]) + ca.mtimes([u[:, k].T, R, u[:, k]])
#
#         # Mountain Car dynamics:
#         position_k = x[0, k]
#         velocity_k = x[1, k]
#         force_k = u[0, k]
#
#         # Apply the Mountain Car dynamics model
#         # velocity_next = velocity_k + (0.0015 * force_k - 0.0025 * ca.cos(3 * position_k)) * dt
#         # position_next = position_k + velocity_next * dt
#         velocity_next = velocity_k + (0.0015 * force_k - 0.0025 * ca.cos(3 * position_k))
#         position_next = position_k + velocity_next
#
#         # Apply dynamics constraints
#         opti.subject_to(x[0, k+1] == position_next)
#         opti.subject_to(x[1, k+1] == velocity_next)
#
#     # Terminal cost (penalize final state)
#     cost += ca.mtimes([x[:, N].T, Q, x[:, N]])
#
#     # Set the objective to minimize cost
#     opti.minimize(cost)
#
#     # State constraints
#     for k in range(N):
#         opti.subject_to(x[0, k] >= -1.2)  # Minimum position
#         opti.subject_to(x[0, k] <= 0.6)   # Maximum position
#         opti.subject_to(x[1, k] >= -0.07)  # Minimum velocity
#         opti.subject_to(x[1, k] <= 0.07)   # Maximum velocity
#         opti.subject_to(u[0, k] >= -1.0)   # Control input bounds
#         opti.subject_to(u[0, k] <= 1.0)
#
#     # Goal: reach a position of at least 0.45
#     opti.subject_to(x[0, N] >= 0.45)
#
#     # Apply initial state constraint
#     opti.subject_to(x[:, 0] == x0)
#
#     # Set solver (IPOPT for nonlinear problems)
#     p_opts = {"expand": True}
#     s_opts = {"max_iter": 5000, "tol": 1e-6}
#     opti.solver('ipopt', p_opts, s_opts)
#
#     # Solve the optimization problem
#     sol = opti.solve()
#
#     # Extract the solution
#     x_opt = sol.value(x)
#     u_opt = sol.value(u)
#
#     # Return the optimal state trajectory and control trajectory
#     return x_opt, u_opt
#
# # Define position and velocity ranges
# position_range = np.arange(-1, -0.06, 0.02)  # Position from -0.3 to -0.05 with step 0.02
# velocity_range = np.arange(-0.07, 0.07, 0.03)  # Velocity from 0.0 to 0.05 with step 0.01
#
# # Generate all combinations of position and velocity
# initial_states = [np.array([position, velocity]) for position in position_range for velocity in velocity_range]
#
# # Loop through initial states and solve the MPC problem for each one
# success_init_state = []
# success_init_action = []
# for i, x0 in enumerate(initial_states):
#     print(f"\nSolving MPC for initial state {x0}")
#     try:
#         x_opt, u_opt = solve_mpc_for_initial_state(x0)
#         print(f"Optimal state trajectory for x0 = {x0}:\n", x_opt)
#         print(f"Optimal control trajectory for x0 = {x0}:\n", u_opt)
#         success_init_state.append(x0)
#         success_init_action.append(u_opt)
#
#     except Exception as e:
#         print(f"Solver failed for initial state {x0}: {e}")
#
# print("here are states reach the points:", success_init_state)