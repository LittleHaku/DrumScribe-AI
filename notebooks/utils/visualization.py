"""
Visualization utilities for drum patterns and audio.
"""
import numpy as np
import matplotlib.pyplot as plt
from .drum_mapping import get_roland_to_simplified_category, get_drum_name_simplified


def plot_drum_piano_roll(
    pm,
    start_pitch=35,
    end_pitch=52,
    fs=100,
):
    """
    Plots a piano roll representation for simplified drum notes with distinct colors.

    Args:
        pm (pretty_midi.PrettyMIDI): The PrettyMIDI object
        start_pitch (int): The lowest MIDI pitch to include (default: 35)
        end_pitch (int): The highest MIDI pitch to include (default: 52)
        fs (int): Sampling frequency for the piano roll grid
    """
    # Define colors for each drum type
    drum_colors = {
        36: 'red',      # Kick
        38: 'blue',     # Snare
        42: 'green',    # HiHat
        47: 'purple',   # Tom
        49: 'orange',   # Crash
        51: 'yellow',   # Ride
    }

    # Find the drum instrument
    drum_instrument = None
    for instrument in pm.instruments:
        if instrument.is_drum:
            drum_instrument = instrument
            break

    if drum_instrument is None or len(drum_instrument.notes) == 0:
        print("No drum track found or the drum track has no notes.")
        duration = pm.get_end_time()
        plt.gca().set_xlim([0, duration])
        plt.gca().set_ylim([start_pitch, end_pitch])
        plt.title("Drum Piano Roll (No notes found)")
        return

    # Print notes found
    pitch_counts = {}
    for note in drum_instrument.notes:
        if start_pitch <= note.pitch <= end_pitch:
            if note.pitch not in pitch_counts:
                pitch_counts[note.pitch] = 0
            pitch_counts[note.pitch] += 1

    if pitch_counts:
        print("Detected drum hits:")
        for pitch, count in sorted(pitch_counts.items()):
            drum_name = get_drum_name_simplified(pitch)
            print(f"  {drum_name} (pitch {pitch}): {count} hits")

    # Create a clean figure with proper time axis
    duration = pm.get_end_time()
    plt.gca().set_xlim([0, duration])
    plt.gca().set_ylim([start_pitch - 0.5, end_pitch + 0.5])

    # Plot each note as a colored line for its duration
    for note in drum_instrument.notes:
        if start_pitch <= note.pitch <= end_pitch:
            # Map to simplified pitch
            simplified_pitch, _ = get_roland_to_simplified_category(note.pitch)

            # Get color (default to gray for unknown pitches)
            color = drum_colors.get(simplified_pitch, 'gray')

            # Plot horizontal line for note duration
            plt.hlines(
                y=simplified_pitch,
                xmin=note.start,
                xmax=note.end,
                colors=color,
                linewidth=4
            )

    # Set ticks and labels for simplified drum mapping
    simplified_drums = {
        36: "Kick",
        38: "Snare",
        42: "HiHat",
        47: "Tom",
        49: "Crash",
        51: "Ride"
    }

    # Create ticks at these pitches
    plt.yticks(list(simplified_drums.keys()))

    # Add drum names as text labels
    for pitch, name in simplified_drums.items():
        if start_pitch <= pitch <= end_pitch:
            plt.text(-0.5, pitch, name, ha="right", va="center")

    # Create a custom legend
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], color=drum_colors[pitch], lw=4, label=name)
        for pitch, name in simplified_drums.items()
        if pitch in drum_colors
    ]
    plt.legend(handles=legend_elements, loc='upper right')

    plt.ylabel("Drum Type")
    plt.xlabel("Time (s)")
    plt.title("Drum Piano Roll (Simplified Mapping)")
    plt.grid(True, alpha=0.3)
