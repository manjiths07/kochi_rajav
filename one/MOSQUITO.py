import time
import numpy as np
import pyaudio
import pygame  # സൗണ്ട് പ്ലേ ചെയ്യാൻ വേണ്ടി

# Pygame mixer ഇനിഷ്യലൈസ് ചെയ്യുന്നു
pygame.mixer.init()

# ഓഡിയോ സെറ്റിങ്സ്
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048

# കൊതുകിന്റെ മൂളൽ ശബ്ദത്തിന്റെ സാധാരണ ഫ്രീക്വൻസി റേഞ്ച് (ഏകദേശം 400Hz മുതൽ 600Hz വരെ)
MOSQUITO_MIN_FREQ = 400
MOSQUITO_MAX_FREQ = 600

audio = pyaudio.PyAudio()

# മൈക്ക് സ്റ്റാർട്ട് ചെയ്യുന്നു
stream = audio.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    frames_per_buffer=CHUNK,
)

print(
    "🎧 Mosquito DJ System Live aanu! Kaathinarike kozhukkal varumbo"
    " nokkikollu..."
)
print("------------------------------------------------------------------")

last_played_time = 0

try:
  while True:
    # മൈക്കിൽ നിന്നുള്ള ഡാറ്റ റീഡ് ചെയ്യുന്നു
    data = np.frombuffer(
        stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16
    )

    # Fast Fourier Transform (FFT) ഉപയോഗിച്ച് ഫ്രീക്വൻസി അനലൈസ് ചെയ്യുന്നു
    fft_spectrum = np.fft.rfft(data)
    frequencies = np.fft.rfftfreq(fft_spectrum.size, 1 / RATE)
    amplitude = np.abs(fft_spectrum)

    # ഏറ്റവും കൂടുതൽ കേൾക്കുന്ന ആവൃതി (Peak Frequency) കണ്ടുപിടിക്കുന്നു
    peak_freq = frequencies[np.argmax(amplitude)]

    # കൊതുകിന്റെ ഫ്രീക്വൻസി റേഞ്ചിലാണോ എന്ന് ചെക്ക് ചെയ്യുന്നു
    if MOSQUITO_MIN_FREQ <= peak_freq <= MOSQUITO_MAX_FREQ:
      current_time = time.time()
      # ഒരേ കൊതുക് തുടർച്ചയായി സൗണ്ട് ഉണ്ടാക്കുമ്പോൾ പാട്ട് വീണ്ടും വീണ്ടും ഓവർലാപ്പ് ആവാതിരിക്കാൻ 3 സെക്കൻഡ് ഗ്യാപ്പ്
      if current_time - last_played_time > 3:
        print(
            f"\n🚨 [ALERT] Mosquito detected at {peak_freq:.2f} Hz! Drop the"
            " EDM Beat! 🎶🔥"
        )
        try:
          # കോഡ് സേവ് ചെയ്തിരിക്കുന്ന അതേ ഫോൾഡറിൽ 'edm_drop.mp3' എന്ന പേരിൽ ഒരു പാട്ട് വെക്കണം
          pygame.mixer.music.load("edm_drop.mp3")
          pygame.mixer.music.play()
        except:
          print("⚠️ 'edm_drop.mp3' ഫയൽ കണ്ടുപിടിക്കാൻ പറ്റിയില്ല!")

        last_played_time = current_time
    else:
      print(
          f"Listening... Current frequency: {peak_freq:.2f} Hz",
          end="\r",
          flush=True,
      )

except KeyboardInterrupt:
  print("\n🛑 System Stopped. Uranguvān samayamayi!")
  stream.stop_stream()
  stream.close()
  audio.terminate()