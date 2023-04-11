import numpy as np
import tifffile
from brian2 import *
from pyrho import Encoder

# Define the encoding parameters
num_neurons = 100
time_step = 0.1 * ms
thresh = 0.5

# Define the opsin-based neuron models
tau = 10 * ms
eqs = '''
dv/dt = -v/tau : 1
'''

# Create the neuron group
neuron_group = NeuronGroup(num_neurons, eqs, threshold='v > thresh', reset='v = 0', method='euler')
neuron_group.v = 0

# Load the input image
img = tifffile.imread('random_input.tif')

# Define the encoding parameters
num_neurons = 100
time_step = 0.1  # milliseconds
thresh = 0.5

# Initialize the encoder
encoder = Encoder(num_neurons=num_neurons, time_step=time_step, thresh=thresh)

# Encode the input image into a set of spike trains
spike_trains = []
for row in img:
    signal = row.astype(float) / 255  # normalize to [0, 1]
    output = neuron_group.run((len(signal) - 1) * time_step, namespace={'thresh': thresh, 'tau': tau, 'signal': signal})
    spikes = encoder.encode(output.v[0])
    spike_trains.append(spikes)

spike_trains = np.array(spike_trains)

# Save the spike trains to a file
np.save('spike_trains.npy', spike_trains)
