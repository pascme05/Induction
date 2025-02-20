#######################################################################################################################
#######################################################################################################################
# Title:        Graphical Illustration of the Law of Induction
# Topic:        Fundamental Electrical Engineering
# File:         main
# Date:         04.02.2025
# Author:       Dr. Pascal A. Schirmer
# Version:      V.1.0
# Copyright:    Pascal Schirmer
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
# Function Description
#######################################################################################################################
"""
This function simulates the induced voltage in a conductor moving through a heterogeneous magnetic field.
"""

#######################################################################################################################
# Import external libs
#######################################################################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


#######################################################################################################################
# Global variables for animation control
#######################################################################################################################
paused = False
trace_history = []                                                                                                       # To store all induced voltage traces
current_trace = []                                                                                                       # To store the current induced voltage trace
current_time = []                                                                                                        # To store the current time values
coil_position = [1, -3]                                                                                                  # Initial coil position


#######################################################################################################################
# Global Fnc
#######################################################################################################################
# ==============================================================================
# Magnetic Field
# ==============================================================================
def magnetic_field(x, y, magnet_position, magnet_strength):
    # Magnet is modeled as a dipole at the given position
    magnet_x, magnet_y = magnet_position
    r_x = x - magnet_x
    r_y = y - magnet_y
    r = np.sqrt(r_x**2 + r_y**2)

    # Avoid division by zero (singularity) by adding a small offset
    r = np.clip(r, 0.1, None)  # Minimum distance of 0.1 to avoid singularity

    # Dipole field components (scaled by magnet strength)
    Bx = magnet_strength * 3 * r_x * r_y / r**5
    By = magnet_strength * (2 * r_y**2 - r_x**2) / r**5
    return Bx, By  # Return both Bx and By


# ==============================================================================
# Update Animation
# ==============================================================================
def update(frame):
    global coil_position, current_time, current_trace, trace_history, paused
    if paused:
        return

    # Time progresses uniformly
    t = frame * 0.1  # Time in seconds
    current_time.append(t)

    # Move the coil upward based on speed
    coil_position[1] += speed.get() / 100  # Adjust speed scaling for smoother motion

    # Reset the coil to the bottom if it leaves the upper frame
    if coil_position[1] > 3:
        coil_position[1] = -3  # Reset to the bottom
        trace_history.append((current_time.copy(), current_trace.copy()))  # Save the current trace
        current_time.clear()  # Reset time for the new trace
        current_trace.clear()  # Reset the current trace

    # Calculate the magnetic field at the coil's position
    Bx, By = magnetic_field(coil_position[0], coil_position[1], magnet_position, magnet_strength.get())
    B = np.sqrt(Bx**2 + By**2)  # Magnitude of the magnetic field

    # Calculate the magnetic flux through the coil
    coil_area = np.pi * (coil_size.get())**2  # Area of the coil
    flux = B * coil_area  # Magnetic flux (Φ = B * A)

    # Append the flux to the current_trace array
    current_trace.append(flux)

    # Calculate the gradient (induced EMF) only if there are at least 2 data points
    if len(current_trace) >= 2:
        emf = -np.gradient(current_trace)[-1]  # Faraday's Law: EMF = -dΦ/dt
        emf = np.clip(emf, -100, 100)  # Limit induced voltage to ±100 V
    else:
        emf = 0  # No EMF if there's only one data point

    # Clear previous plots
    ax1.clear()
    ax2.clear()

    # Draw the magnet at the center
    ax1.plot(magnet_position[0], magnet_position[1], 's', markersize=20, color='red', label='Magnet')

    # Draw the coil as a circle with adjustable size
    coil = plt.Circle((coil_position[0], coil_position[1]), coil_size.get(), color='black', fill=False, linewidth=2, label='Coil')
    ax1.add_patch(coil)

    # Calculate and plot magnetic field lines
    X, Y = np.meshgrid(np.linspace(-3, 3, 20), np.linspace(-3, 3, 20))
    Bx_field = np.zeros_like(X)
    By_field = np.zeros_like(Y)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Bx_field[i, j], By_field[i, j] = magnetic_field(X[i, j], Y[i, j], magnet_position, magnet_strength.get())
    ax1.streamplot(X, Y, Bx_field, By_field, color='blue', density=1.5, arrowsize=1, linewidth=1)

    # Set plot limits and labels for the first plot
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-3, 3)
    ax1.set_xlabel('X Position (m)')
    ax1.set_ylabel('Y Position (m)')
    ax1.set_title("Magnetic Field and Coil Motion")
    ax1.legend()
    ax1.grid(True)

    # Plot all induced voltage traces
    colors = plt.cm.viridis(np.linspace(0, 1, len(trace_history) + 1))  # Different colors for each trace
    for i, (time_values, trace_values) in enumerate(trace_history):
        ax2.plot(time_values, -np.gradient(trace_values), color=colors[i], label=f'Trace {i + 1}')

    # Plot the current induced voltage trace
    if len(current_trace) >= 2:
        ax2.plot(current_time, -np.gradient(current_trace), color=colors[-1], label='Current Trace')

    # Set adaptive y-limits for the induced voltage plot
    if len(current_trace) >= 2:
        emf_values = -np.gradient(current_trace)
        max_emf = max(np.abs(emf_values))  # Maximum absolute value of induced voltage
        y_limit = min(max_emf * 1.1, 100)  # Adaptive limit, capped at ±100 V
        ax2.set_ylim(-y_limit, y_limit)

    # Set plot limits and labels for the second plot
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Induced Voltage (ε) [V]')
    ax2.set_title("Induced Voltage Over Time (Faraday's Law)")
    ax2.legend()
    ax2.grid(True)

    # Draw the plots
    canvas.draw()


# ==============================================================================
# Pause/Resume Animation
# ==============================================================================
def toggle_pause():
    global paused
    paused = not paused
    pause_button.config(text="Resume" if paused else "Pause")


#######################################################################################################################
# Main
#######################################################################################################################
# Create the main window
root = tk.Tk()
root.title("Faraday's Law Visualization")

# Create a plot area with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 8))
fig.tight_layout(pad=4.0)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Initial positions
magnet_position = [0, 0]  # Magnet is fixed at the center

# Sliders for customization
ttk.Label(root, text="Coil Speed (m/s):").grid(row=1, column=0, padx=5, pady=5)
speed = tk.DoubleVar(value=1.0)
speed_slider = ttk.Scale(root, from_=0.0, to=5.0, variable=speed, orient="horizontal")
speed_slider.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Coil Radius (m):").grid(row=1, column=2, padx=5, pady=5)
coil_size = tk.DoubleVar(value=0.5)
coil_size_slider = ttk.Scale(root, from_=0.1, to=2.0, variable=coil_size, orient="horizontal")
coil_size_slider.grid(row=1, column=3, padx=5, pady=5)

ttk.Label(root, text="Magnet Strength (T):").grid(row=2, column=0, padx=5, pady=5)
magnet_strength = tk.DoubleVar(value=1.0)
magnet_strength_slider = ttk.Scale(root, from_=0.1, to=5.0, variable=magnet_strength, orient="horizontal")
magnet_strength_slider.grid(row=2, column=1, padx=5, pady=5)

# Pause/Resume button
pause_button = ttk.Button(root, text="Pause", command=toggle_pause)
pause_button.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

# Create an animation
ani = animation.FuncAnimation(fig, update, frames=100, interval=100, repeat=True)

# Run the application
root.mainloop()