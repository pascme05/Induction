#######################################################################################################################
#######################################################################################################################
# Title:        Timedomain RL response
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
Diese Funktion berechnet die Sprungantwort eines RL Glieds
"""

#######################################################################################################################
# Import external libs
#######################################################################################################################
import numpy as np
import matplotlib.pyplot as plt

#######################################################################################################################
# Main
#######################################################################################################################
# ==============================================================================
# Parameter
# ==============================================================================
R = 1                                                                                                                    # Widerstand in Ohm
L = 1e-6                                                                                                                 # Induktivität in Henry
V = 5.0                                                                                                                  # Sprungspannung in Volt
t_max = 0.1                                                                                                              # Simulationsdauer in Sekunden
dt = 0.0001                                                                                                              # Zeitschritt in Sekunden
t_sprung = 0.02                                                                                                          # Zeitpunkt des Sprungs in Sekunden (kann angepasst werden)

# ==============================================================================
# Berechnung
# ==============================================================================
# Zeitarray
t = np.arange(0, t_max, dt)

# Sprungfunktion: V_in(t) = V für t >= t_sprung
V_in = V * (t >= t_sprung)  # Sprungspannung zum Zeitpunkt t_sprung

# Strom im RL-Schaltkreis für eine Sprungfunktion
# I(t) = (V / R) * (1 - exp(-R * (t - t_sprung) / L)) für t >= t_sprung
I = np.zeros_like(t)
for i, ti in enumerate(t):
    if ti >= t_sprung:
        I[i] = (V / R) * (1 - np.exp(-R * (ti - t_sprung) / L))

# Spannung über dem Widerstand: V_R = I * R
V_R = I * R

# Spannung über der Induktivität: V_L = V_in - V_R
V_L = V_in - V_R

# Ergebnisse plotten
plt.figure(figsize=(10, 8))


# ==============================================================================
# Plotting
# ==============================================================================
# Eingangsspannung (Sprungfunktion)
plt.subplot(3, 1, 1)
plt.plot(t, V_in, label='Eingangsspannung (Sprung)', color='blue')
plt.axvline(x=t_sprung, color='gray', linestyle='--', label=f'Sprung bei t = {t_sprung}s')
plt.xlabel('Zeit [s]')
plt.ylabel('Spannung [V]')
plt.title('Eingangsspannung (Sprungfunktion)')
plt.legend()
plt.grid(True)

# Strom durch den Schaltkreis
plt.subplot(3, 1, 2)
plt.plot(t, I, label='Strom I(t)', color='green')
plt.axvline(x=t_sprung, color='gray', linestyle='--', label=f'Sprung bei t = {t_sprung}s')
plt.xlabel('Zeit [s]')
plt.ylabel('Strom [A]')
plt.title('Strom im RL-Schaltkreis')
plt.legend()
plt.grid(True)

# Spannungen über R und L
plt.subplot(3, 1, 3)
plt.plot(t, V_R, label='Spannung über R', color='red')
plt.plot(t, V_L, label='Spannung über L', color='purple')
plt.axvline(x=t_sprung, color='gray', linestyle='--', label=f'Sprung bei t = {t_sprung}s')
plt.xlabel('Zeit [s]')
plt.ylabel('Spannung [V]')
plt.title('Spannung über Widerstand und Induktivität')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
