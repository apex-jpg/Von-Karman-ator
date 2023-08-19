import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.optimize import curve_fit

# Define parameters
nose_long = 0.2  # 200 mm length
rocket_wide = 0.06  # 60 mm outer diameter
x_resolution = 0.0001  # increase resolution for a smoother graph
C = 0

# Initialize an empty list to store radius values
r = []

# Calculate and store radius values
for X in np.arange(0, nose_long + x_resolution, x_resolution):
    x = X / nose_long
    h = np.arccos(1 - 2 * x)
    # Calculate the radius using Von Karman formula
    radius = np.sqrt((h - (1 / 2) * np.sin(2 * h) + (C * (np.sin(h) ** 3) * h)) / np.pi) * (rocket_wide * 2)
    r.append(radius)

# Define the Von Karman curve function for curve fitting
def von_karman(x, a, b, c):
    return a * (1 - np.exp(-b * x)) + c

# Initial guesses for parameters a, b, and c
initial_guesses = [1.0, 0.01, 1.0]

# Set bounds for parameter optimization
parameter_bounds = ([0, 0, 0], [np.inf, 10, np.inf])  # Example bounds, adjust as needed

# Perform the curve fit with initial parameter guesses and bounds
params, _ = curve_fit(von_karman, np.arange(0, nose_long + x_resolution, x_resolution), r, p0=initial_guesses, bounds=parameter_bounds)

# Generate the fitted radius values using the curve fit
fitted_r = von_karman(np.arange(0, nose_long + x_resolution, x_resolution), *params)

# Plot the fitted radius values
plt.plot(fitted_r)
plt.xlabel('Index')
plt.ylabel('Fitted Radius')
plt.title('Fitted Von Karman Nose Cone')
plt.show()

# Output the calculated radius values to a CSV file

output_file = "fitted_radius_values.csv"
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Index', 'Fitted Radius (m)'])  # Write header row
    for idx, radius in enumerate(fitted_r):
        writer.writerow([idx + 1, radius])  # Write data rows

print(f"Fitted radius values have been saved to '{output_file}'")
