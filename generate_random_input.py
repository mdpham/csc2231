import numpy as np
import tifffile

# Generate a 100 x 100 random matrix
rand_matrix = np.random.rand(100, 100)

# Save the matrix as a TIFF file
tifffile.imwrite('random_input.tiff', rand_matrix)