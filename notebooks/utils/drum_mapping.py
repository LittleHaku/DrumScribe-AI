"""
Utilities for drum MIDI mapping and conversion.
"""
import pretty_midi
from pathlib import Path


def get_roland_to_simplified_category(pitch):
    """
    Convert Roland drum mapping to simplified drum categories.

    Args:
        pitch (int): MIDI pitch number in Roland mapping

    Returns:
        tuple: (new_pitch, category_name) with standardized pitch and category
    """
    # Define pitch mappings from Roland to simplified categories
    roland_to_simple = {
        # Kicks
        36: (36, "Kick"),

        # Snares
        38: (38, "Snare"),
        40: (38, "Snare"),  # Snare rim -> Snare
        37: (38, "Snare"),  # X-stick -> Snare

        # Toms
        48: (47, "Tom"),    # Tom 1 -> Tom
        50: (47, "Tom"),    # Tom 1 rim -> Tom
        45: (47, "Tom"),    # Tom 2 -> Tom
        47: (47, "Tom"),    # Tom 2 rim -> Tom
        43: (47, "Tom"),    # Tom 3 -> Tom
        58: (47, "Tom"),    # Tom 3 rim -> Tom

        # Hi-Hats
        46: (42, "HiHat"),  # HH Open -> HiHat
        26: (42, "HiHat"),  # HH Open Edge -> HiHat
        42: (42, "HiHat"),  # HH Closed -> HiHat
        22: (42, "HiHat"),  # HH Closed Edge -> HiHat
        44: (42, "HiHat"),  # HH Pedal -> HiHat

        # Crash Cymbals
        49: (49, "Crash"),  # Crash 1 -> Crash
        55: (49, "Crash"),  # Crash 1 Edge -> Crash
        57: (49, "Crash"),  # Crash 2 -> Crash
        52: (49, "Crash"),  # Crash 2 Edge -> Crash

        # Ride Cymbals
        51: (51, "Ride"),   # Ride -> Ride
        59: (51, "Ride"),   # Ride Edge -> Ride
        53: (51, "Ride")    # Ride Bell -> Ride
    }

    return roland_to_simple.get(pitch, (pitch, f"Unknown ({pitch})"))


def get_drum_name_simplified(pitch):
    """
    Get simplified drum name for visualization purposes.

    Args:
        pitch (int): MIDI pitch number

    Returns:
        str: Simplified drum name
    """
    _, category = get_roland_to_simplified_category(pitch)
    return category


def convert_midi_to_simplified_mapping(midi_path, output_path):
    """
    Converts a MIDI file from Roland drum mapping to simplified GM drum mapping.

    Args:
        midi_path: Path to the source MIDI file
        output_path: Path to save the converted MIDI file

    Returns:
        bool: True if conversion was successful, False otherwise
    """
    try:
        # Load the MIDI file
        pm = pretty_midi.PrettyMIDI(str(midi_path))

        # Process each instrument
        for instrument in pm.instruments:
            if instrument.is_drum:
                # Create a new list for converted notes
                new_notes = []

                # Process each note
                for note in instrument.notes:
                    # Get the new pitch using our mapping function
                    new_pitch, _ = get_roland_to_simplified_category(
                        note.pitch)

                    # Create a new note with the converted pitch
                    new_note = pretty_midi.Note(
                        velocity=note.velocity,
                        pitch=new_pitch,
                        start=note.start,
                        end=note.end
                    )
                    new_notes.append(new_note)

                # Replace the old notes with the new ones
                instrument.notes = new_notes

        # Save the modified MIDI file
        pm.write(str(output_path))
        return True

    except Exception as e:
        print(f"Error converting MIDI file: {e}")
        return False
