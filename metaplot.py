import numpy as np
import matplotlib.pyplot as plt

bohr_2_angstrom = 0.529177
kb = 8.6173303e-5 # eV * K^-1

temperature = 298.15                          #Change temperature according to your MD simulations!
colvar_path = "./ch3f-COLVAR.metadynLog"

# Load the colvar file
colvar_raw = np.loadtxt(colvar_path)

# Extract the two CVs
d1 = colvar_raw[:, 1] * bohr_2_angstrom
d2 = colvar_raw[:, 2] * bohr_2_angstrom

# Create a 2d histogram corresponding to the CV occurances
cv_hist = np.histogram2d(d1, d2, bins=50)
cv_hist = np.histogram2d(d1, d2, bins=50)

# probability from the histogram
prob = cv_hist[0]/len(d1)

# Free energy surface
fes = -kb * temperature * np.log(prob)

#print cv_hist[0]

# Save the image
extent = (np.min(cv_hist[1]), np.max(cv_hist[1]), np.min(cv_hist[2]), np.max(cv_hist[2]))
#extent = (np.min(cv_hist[1]), np.max(cv_hist[1]))
plt.figure(figsize=(8, 8))
plt.imshow(fes.T, extent=extent, aspect='auto', origin='lower', cmap='hsv')
cbar = plt.colorbar()
cbar.set_label("Free energy [eV]")
plt.xlabel("d1 [ang]")
plt.savefig("./fes.png", dpi=200)
plt.close()