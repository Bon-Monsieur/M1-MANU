# %%
import numpy as np
import matplotlib.pyplot as plt

# from mpl_toolkits.mplot3d import Axes3D


# Define the function (e.g., quadratic)
def func(x):
    # Example: simple quadratic form f(x) = 1/2 * x^T A x
    # A = np.eye(ndim)  # Identity matrix for simplicity
    # y = np.array([(abs(ndim//2-i)) for i in range(ndim)])
    y = [1, 2,1,1,1,1,1,1,1,1]
    return np.dot(x, y) * np.exp(-np.linalg.norm(x) ** 2)


def funcp(x):
    # y = [1, 2]
    y = [1, 2,1,1,1,1,1,1,1,1]
    return np.exp(-np.linalg.norm(x) ** 2) * (y - 2 * np.dot(x, y) * x)


def finite_difference_centered(f, x, eps):
    dim = x.size
    return np.array(
        [(f(x + eps * e_i) - f(x - eps * e_i)) / (2*eps) for e_i in np.eye(dim)]
    )

def finite_difference_forward(f, x, eps):
    dim = x.size
    return np.array([(f(x + eps * e_i) - f(x)) / eps for e_i in np.eye(dim)])


def finite_difference_backward(f, x, eps):
    dim = x.size
    return np.array([(f(x) - f(x - eps * e_i)) / eps for e_i in np.eye(dim)])

# def finite_difference_backward(f, x, eps):
#     # Implement the finite difference backward method
#     dim = x.size
#     I = np.eye(dim)
#     return np.array((f(x) - f(x - eps * I)) / eps)

# def finite_difference_forward(f, x, eps):
#     # Implement the finite difference forward method
#     dim = x.size
#     I = np.eye(dim)
#     return (f(x + eps * I) - f(x)) / eps

# def finite_difference_centered(f, x, eps):
#     # Implement the finite difference centered method
#     dim = x.size
#     I = np.eye(dim)
#     return np.array((f(x+ eps* I) - f(x)) / eps)


# %%


# Main program


# Define constants
ndim = 2  # Number of dimensions
rho = 0.01  # Initial step size (learning rate)
tol = 1e-6  # Tolerance for stopping criterion
max_iter = 1000  # Maximum number of iterations

# Store convergence histories
hist_func = []  # Stores function values
hist_grad_norm = []  # Stores norms of gradients
x_history = []  # Store x values

# Define admissible space (no bounds for now)

# Initialization
x = np.array([-0.6, -0.6]) + np.random.randn(ndim)  # Random starting point
print(x)
f = func(x)  # Initial function value
grad = funcp(x)  # Initial gradient
iter_count = 0

hist_func.append(f)
hist_grad_norm.append(np.linalg.norm(grad))
x_history.append(x.copy())

# cosine_restart():
# Loop over descent iterations
while np.linalg.norm(grad) > tol and iter_count < max_iter:
    # Calculate new iterate xn+1 using gradient descent step
    x = x - rho * grad

    # Recalculate function value and gradient
    f = func(x)
    grad = funcp(x)

    # Store convergence results
    hist_func.append(f)
    hist_grad_norm.append(np.linalg.norm(grad))
    x_history.append(x.copy())

    # Update step size rho if needed (adaptive learning rate can be added here)
    # rho *= 0.9  # Example adaptive step size reduction (optional)
    iter_count += 1

# Convert history lists to numpy arrays
x_history = np.array(x_history)
hist_func = np.array(hist_func)
print(hist_func.shape)
hist_grad_norm = np.array(hist_grad_norm)

# Plot convergence results
plt.figure(figsize=(12, 6))

# Plot function value convergence
plt.subplot(1, 2, 1)
plt.plot(hist_func / hist_func[0], label="Functional")
plt.title("Convergence of Functional")
plt.xlabel("Iterations")
plt.ylabel("J(x) / J(x0)")
plt.legend()

# Plot gradient norm convergence
plt.subplot(1, 2, 2)
plt.plot(hist_grad_norm / hist_grad_norm[0], label="Gradient Norm")
plt.title("Convergence of Gradient Norm")
plt.xlabel("Iterations")
plt.ylabel("||∇J(x)|| / ||∇J(x0)||")
plt.legend()

plt.tight_layout()
plt.show()


bounds = ((-3, 3), (-3, 3))

fig = plt.figure(figsize=(12, 6))
ax3d = fig.add_subplot(121)
axhmap = fig.add_subplot(122)
_X = np.linspace(*bounds[0], 100)
_Y = np.linspace(*bounds[1], 100)
X, Y = np.meshgrid(_X, _Y)
Z = np.vectorize(lambda x, y: func([x, y]))(X, Y)
print(Z.shape)
contourf = ax3d.contourf(X, Y, Z, levels=7)
ax3d.contour(X, Y, Z, levels=7, colors="white", linewidths=0.5)
ax3d.set_xlabel("X")
ax3d.set_ylabel("Y")
ax3d.set_title("Rastrigin Function: Level set plot")
print(x_history.T.shape)
axhmap.scatter(x_history.T[0, :], x_history.T[1, :])
ax3d.scatter(x_history.T[0, :], x_history.T[1, :])
ax3d.scatter(x_history.T[0, -1], x_history.T[1, -1])
fig.show()

# %%

x = np.array([1,-1,1,1,1,1,1,1,1,1])
EPS = np.logspace(-5,-11,num=2000)

plt.plot([np.linalg.norm((finite_difference_backward(func, x, eps) - funcp(x))) for eps in EPS],label="Backward")
plt.plot([np.linalg.norm((finite_difference_forward(func, x, eps) - funcp(x))) for eps in EPS],label="Forward")
plt.plot([np.linalg.norm((finite_difference_centered(func, x, eps) - funcp(x))) for eps in EPS],label="Centered")
plt.xscale('log')  # Log scale for x-axis
plt.yscale('log')  # Log scale for y-axis
plt.xlabel("Epsilon")
plt.ylabel("Norm of Difference")
plt.legend()
plt.title("Finite Difference Approximations vs True Gradient")
plt.show()

# %%
