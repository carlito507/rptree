import matplotlib.pyplot as plt
import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import write
from scipy.fft import rfft, rfftfreq, irfft

SAMPLE_RATE = 44100
DURATION = 5
N = SAMPLE_RATE * DURATION


def generate_sine_wave(frequency, duration, sample_rate):
    """Generate a sine wave with the given frequency and duration.
    """
    x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
    frequencies = x * frequency
    y = np.sin(frequencies * 2 * np.pi)
    return x, y


if __name__ == "__main__":
    x, y = generate_sine_wave(2, DURATION, SAMPLE_RATE)
    _, nice_tone = generate_sine_wave(400, DURATION, SAMPLE_RATE)
    _, bad_tone = generate_sine_wave(1000, DURATION, SAMPLE_RATE)
    mixed_tone = nice_tone + bad_tone
    normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)

    yf = rfft(normalized_tone)
    xf = rfftfreq(N, 1 / SAMPLE_RATE)

    points_per_freq = len(xf) / (SAMPLE_RATE / 2)
    target_idx = int(4000 * points_per_freq)

    yf[target_idx - 1 : target_idx + 2] = 0

    new_sig = irfft(yf)
    norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))

    plt.plot(new_sig[:1000])
    plt.show()
    write("mixed_tone.wav", SAMPLE_RATE, normalized_tone)
    write("clean.wav", SAMPLE_RATE, norm_new_sig)
