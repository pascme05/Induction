# Datei: drehfeld_snapshot.py
import numpy as np
import matplotlib.pyplot as plt

f = 50.0
omega = 2*np.pi*f
I_m = 1.0

theta_a = 0.0
theta_b = 2*np.pi/3
theta_c = 4*np.pi/3

def phase_vector(i, theta):
    return i * np.array([np.cos(theta), np.sin(theta)])

# gewählter Zeitpunkt (z.B. t = T/8)
t = (1.0 / f) / 8

ia = I_m * np.cos(omega*t)
ib = I_m * np.cos(omega*t - 2*np.pi/3)
ic = I_m * np.cos(omega*t - 4*np.pi/3)

v_a = phase_vector(ia, theta_a)
v_b = phase_vector(ib, theta_b)
v_c = phase_vector(ic, theta_c)
V = v_a + v_b + v_c

fig, ax = plt.subplots(figsize=(6,6))
ax.set_aspect('equal', 'box')
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.plot([0, v_a[0]], [0, v_a[1]], marker='o', label=f'Phase A: i={ia:.2f}')
ax.plot([0, v_b[0]], [0, v_b[1]], marker='o', label=f'Phase B: i={ib:.2f}')
ax.plot([0, v_c[0]], [0, v_c[1]], marker='o', label=f'Phase C: i={ic:.2f}')
ax.plot([0, V[0]], [0, V[1]], linewidth=3, label=f'Resultierender |V|={np.linalg.norm(V):.3f}')
ax.legend()
ax.grid(True)
ax.set_title(f'Drehfeld-Momentaufnahme bei t={t*1000:.1f} ms')
plt.show()
