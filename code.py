# 2023 Skickar for Retia
#
# SPDX-License-Identifier: MIT

import audiocore
import board
import audiobusio
import neopixel
import analogio  # Import analogio for reading analog input values
import time
import random
import alarm  # Import alarm module for light sleep functionality

# Constants
MIN_PLAYBACK_TIME = 4.2  # Minimum playback time in seconds. Change this value as needed.
LDR_THRESHOLD = 50000  # Threshold value for LDR sensor to trigger audio playback
DEBOUNCE_TIME = 0.5  # Time in seconds to wait before checking the alarm condition again

# Initialize a strip of 11 NeoPixels on IO12
strip = neopixel.NeoPixel(board.IO12, 11, auto_write=False)
strip.fill((0, 0, 0))
strip.show()

# For ESP32-S2 mini module
audio = audiobusio.I2SOut(board.IO3, board.IO8, board.IO40)

while True:
    ldr = analogio.AnalogIn(board.IO14)  # Initialize the AnalogIn

    if ldr.value > LDR_THRESHOLD:  # Start playing if LDR value is over threshold and audio is not playing
        strip.fill((255, 0, 0))  # Set the entire strip to red
        strip.show()

        # Randomly pick between the audio files
        chosen_file = random.choice(["term5.wav", "term5.wav", "term5.wav", "term5.wav", "term5.wav", "term5.wav"])
        with open(chosen_file, "rb") as wave_file:
            wave = audiocore.WaveFile(wave_file)
            audio.play(wave)
            while audio.playing:
                pass  # Wait for the audio to finish playing

        strip.fill((0, 0, 0))  # Turn off the NeoPixels
        strip.show()

        ldr.deinit()  # Deinitialize the AnalogIn to save power and free up the pin

        time.sleep(DEBOUNCE_TIME)  # Debounce delay

    else:
        ldr.deinit()  # Deinitialize the AnalogIn to save power and free up the pin

        # Set up the pin alarm on the LDR sensor
        pin_alarm = alarm.pin.PinAlarm(pin=board.IO14, value=True, pull=True)

        # Put the board into light sleep until the LDR sensor value goes above the threshold
        alarm.light_sleep_until_alarms(pin_alarm)
