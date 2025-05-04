"""
MIDI processing utilities for drum transcription.
"""
import pretty_midi
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple


def extract_drum_events(midi_path: Path) -> Dict[int, List[Tuple[float, int]]]:
    """
    Extracts drum events from a MIDI file.

    Args:
        midi_path: Path to the MIDI file

    Returns:
        Dictionary mapping drum note numbers to lists of (onset_time, velocity) tuples
    """
    try:
        # Load MIDI file
        pm = pretty_midi.PrettyMIDI(str(midi_path))

        # Find drum tracks
        drum_events = {}

        for instrument in pm.instruments:
            if instrument.is_drum:
                for note in instrument.notes:
                    # Group by pitch (different drum sounds)
                    if note.pitch not in drum_events:
                        drum_events[note.pitch] = []

                    # Store onset time and velocity
                    drum_events[note.pitch].append((note.start, note.velocity))

        return drum_events
    except Exception as e:
        print(f"Error extracting drum events from {midi_path}: {e}")
        return {}


def align_spectrogram_with_midi(
    spec: np.ndarray,
    drum_events: Dict[int, List[Tuple[float, int]]],
    sr: int,
    hop_length: int,
    main_drums: List[int]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Aligns a spectrogram with MIDI drum events to create training labels.

    Args:
        spec: Log-mel spectrogram
        drum_events: Dictionary of drum events
        sr: Sample rate
        hop_length: Hop length used in spectrogram computation
        main_drums: List of MIDI note numbers for the main drums to track

    Returns:
        Tuple of (onset_target, velocity_target) arrays
    """
    # Get spectrogram dimensions
    n_frames = spec.shape[1]

    n_drums = len(main_drums)

    # Initialize target arrays
    onset_target = np.zeros((n_drums, n_frames), dtype=np.float32)
    velocity_target = np.zeros((n_drums, n_frames), dtype=np.float32)

    # For each tracked drum type
    for i, pitch in enumerate(main_drums):
        if pitch in drum_events:
            for time, velocity in drum_events[pitch]:
                # Convert time to frame index
                frame = int(time * sr / hop_length)

                # Skip if outside spectrogram range
                if 0 <= frame < n_frames:
                    onset_target[i, frame] = 1.0
                    velocity_target[i, frame] = velocity / \
                        127.0  # Normalize to 0-1

    return onset_target, velocity_target
