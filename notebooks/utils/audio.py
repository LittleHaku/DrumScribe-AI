"""
Audio utilities for synthesis, playback and feature extraction.
"""
import subprocess
import tempfile
from pathlib import Path
import numpy as np
import librosa
from IPython.display import Audio, display, HTML

# Define default soundfont path
SOUNDFONT_PATH = Path("../soundfont/FluidR3_GM.sf2")


def midi_to_audio(midi_path, soundfont_path, output_wav_path, sr=22050):
    """Turn a MIDI file into WAV audio using FluidSynth."""
    midi_path = Path(midi_path)
    soundfont_path = Path(soundfont_path)
    output_wav_path = Path(output_wav_path)

    if not soundfont_path.exists():
        return False  # Need soundfont
    if not midi_path.exists():
        return False  # Need the midi file

    try:
        command = ['fluidsynth', '-ni', str(soundfont_path), str(midi_path),
                   '-F', str(output_wav_path), '-r', str(sr)]
        subprocess.run(command, check=True, capture_output=True,
                       text=True, timeout=30)  # Run command
        return True  # Success!
    except Exception as e:
        print(f"  -> FluidSynth failed: {e}")  # Print error if synth fails
        return False  # Failed


def play_audio_and_midi(audio_path, pm, sr=44100, soundfont_path=None):
    """
    Provides playback for both the original audio and synthesized MIDI using FluidSynth.

    Args:
        audio_path: Path to the audio file
        pm: PrettyMIDI object
        sr: Sample rate
        soundfont_path: Path to soundfont, uses default if None
    """
    # Load the audio file
    y, _ = librosa.load(audio_path, sr=sr)

    # Use default soundfont if none provided
    if soundfont_path is None:
        soundfont_path = SOUNDFONT_PATH
    soundfont_path = Path(soundfont_path)

    # Create temporary directory to store midi and wav files
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir_path = Path(tmpdir)

        # Create temporary file paths
        temp_midi_path = temp_dir_path / "temp_drum.mid"
        temp_wav_path = temp_dir_path / "temp_drum.wav"

        # Save the MIDI
        pm.write(str(temp_midi_path))

        # Check if we can synthesize
        can_synthesize = soundfont_path.exists()

        print("Original Audio Recording:")
        display(Audio(data=y, rate=sr))

        # Synthesize MIDI with FluidSynth
        if can_synthesize:
            print("\nSynthesizing MIDI with FluidSynth...")
            if midi_to_audio(temp_midi_path, soundfont_path, temp_wav_path, sr=sr):
                try:
                    # Load and play the synthesized audio
                    midi_audio, sr_midi = librosa.load(temp_wav_path, sr=sr)
                    print("\nSynthesized MIDI Drum Pattern:")
                    display(Audio(data=midi_audio, rate=sr_midi))
                except Exception as e:
                    print(f"Error loading synthesized audio: {e}")
            else:
                print("Failed to synthesize MIDI. Make sure FluidSynth is installed.")
        else:
            print(
                f"\nCannot synthesize MIDI: SoundFont not found at {soundfont_path}")
            print("Download a SoundFont file and update the soundfont_path parameter.")


def preprocess_audio(audio_path, target_sr):
    """
    Loads, resamples, and normalizes an audio file.

    Args:
        audio_path (Path): Path to the input audio file.
        target_sr (int): The target sample rate to resample to.

    Returns:
        Optional[np.ndarray]: The preprocessed audio as a NumPy array,
                             or None if loading fails.
    """
    try:
        # Load audio, resample to target_sr, convert to mono
        audio, sr = librosa.load(audio_path, sr=target_sr, mono=True)

        # Peak normalization
        max_abs_val = np.max(np.abs(audio))
        if max_abs_val > 0:
            audio_normalized = audio / (max_abs_val + 1e-8)
        else:
            audio_normalized = audio

        return audio_normalized
    except Exception as e:
        print(f"Error processing {audio_path}: {e}")
        return None


def compute_mel_spectrogram(
    y,
    sr,
    n_fft=2048,
    hop_length=512,
    n_mels=229,
    fmin=20.0,
    fmax=8000.0
):
    """
    Computes a log-mel spectrogram from audio data.

    Args:
        y: Audio time series
        sr: Sample rate
        n_fft: FFT window size
        hop_length: Hop length between frames
        n_mels: Number of mel bands
        fmin: Lowest frequency (Hz)
        fmax: Highest frequency (Hz)

    Returns:
        Log-mel spectrogram as a numpy array
    """
    # Compute mel spectrogram
    mel_spec = librosa.feature.melspectrogram(
        y=y,
        sr=sr,
        n_fft=n_fft,
        hop_length=hop_length,
        n_mels=n_mels,
        fmin=fmin,
        fmax=fmax
    )

    # Convert to log scale (dB)
    log_mel_spec = librosa.power_to_db(mel_spec, ref=np.max)

    return log_mel_spec
