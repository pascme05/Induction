# Datei: drehfeld_animation.py
# Benötigt: Python 3, numpy, matplotlib
# Optional (zum Speichern als mp4/gif): ffmpeg oder imagemagick installiert

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ------- Parameter ----------------
f = 50.0                 # Frequenz [Hz]
omega = 2 * np.pi * f
I_m = 1.0                # Spitzenwert (willkürlich)
n_frames = 120           # Anzahl Frames pro Periode (Animation flüssig = größer)
T = 1.0 / f
t_vals = np.linspace(0, T, n_frames, endpoint=False)

# räumliche Achsen (elektrische Winkel) der drei Wicklungen
theta_a = 0.0
theta_b = 2*np.pi/3
theta_c = 4*np.pi/3

# Phasenströme (Cosinus-Referenz)
def i_a(t): return I_m * np.cos(omega*t)
def i_b(t): return I_m * np.cos(omega*t - 2*np.pi/3)
def i_c(t): return I_m * np.cos(omega*t - 4*np.pi/3)

def phase_vector(i, theta):
    """Vektor (x,y) einer Phase mit Strom i auf Achse theta"""
    return i * np.array([np.cos(theta), np.sin(theta)])

# ------- Plotaufbau ----------------
fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal', 'box')
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Drehfeld-Zeiger (3-Phasen) — Raumzeiger-Simulation')

# winding axes (nur als gestrichelte Linien)
for th in (theta_a, theta_b, theta_c):
    ax.plot([0, 1.2*np.cos(th)], [0, 1.2*np.sin(th)], linestyle='dashed')

# Einheitskreis als Referenz
unit_circle = plt.Circle((0,0), 1.0, fill=False, linewidth=0.7)
ax.add_patch(unit_circle)

# Quiver-Objekte für die drei Phasenvektoren und den Resultierenden
q_phases = ax.quiver([0,0,0],[0,0,0],[0,0,0],[0,0,0], angles='xy', scale_units='xy', scale=1)
q_res = ax.quiver([0],[0],[0],[0], angles='xy', scale_units='xy', scale=1, width=0.02)

# Text für Zeit + Betrag
mag_text = ax.text(-1.35, 1.25, '', fontsize=10)

# Animationsfunktionen
def init():
    q_phases.set_UVC([0,0,0], [0,0,0])
    q_res.set_UVC([0],[0])
    mag_text.set_text('')
    return q_phases, q_res, mag_text

def animate(i_frame):
    t = t_vals[i_frame]
    ia = i_a(t); ib = i_b(t); ic = i_c(t)
    v_a = phase_vector(ia, theta_a)
    v_b = phase_vector(ib, theta_b)
    v_c = phase_vector(ic, theta_c)
    V = v_a + v_b + v_c
    V_norm = np.linalg.norm(V)
    q_phases.set_UVC([v_a[0], v_b[0], v_c[0]], [v_a[1], v_b[1], v_c[1]])
    q_res.set_UVC([V[0]], [V[1]])
    mag_text.set_text(f't = {t*1000:.1f} ms\n|Result| = {V_norm:.3f}')
    return q_phases, q_res, mag_text

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=n_frames, interval=80, blit=True)

# Anzeige im interaktiven Fenster (oder Jupyter)
# plt.show()

# Optional: speichern (benötigt ffmpeg oder imagemagick)
# anim.save('drehfeld.mp4', fps=30, bitrate=2000)
anim.save('drehfeld.gif', writer='imagemagick', fps=30)
