"""
Utilities for generating MIDI from model predictions and visualization.
"""
import torch
import numpy as np
import pretty_midi
import matplotlib.pyplot as plt
import librosa
import tempfile
from pathlib import Path
import soundfile as sf
from IPython.display import Audio, display, HTML

from utils.audio import midi_to_audio


def predictions_to_midi(onset_frames, velocity_frames, threshold, frame_times, index_to_pitch_map, fixed_note_duration=0.1):
    """
    Convert model onset and velocity predictions to a MIDI file.

    Args:
        onset_frames: Tensor of onset probabilities [n_drums, n_frames]
        velocity_frames: Tensor of velocity predictions [n_drums, n_frames]
        threshold: Threshold for onset detection
        frame_times: Array of timestamps for each frame
        index_to_pitch_map: Map from drum indices to MIDI pitch numbers
        fixed_note_duration: Duration for each drum hit in seconds

    Returns:
        A PrettyMIDI object containing the drum notes
    """
    # Creates a MIDI object using pretty_midi
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(
        program=0, is_drum=True, name="Predicted Drums")
    n_drums, n_frames = onset_frames.shape
    binary_onsets = (onset_frames > threshold).float()
    masked_velocities = velocity_frames * binary_onsets

    # Go through each drum type
    for drum_idx in range(n_drums):
        # Find where the model predicted an onset
        onset_indices = torch.where(binary_onsets[drum_idx] == 1)[0]
        # Add a note for each detected onset
        for frame_idx in onset_indices:
            start_time = frame_times[frame_idx]
            end_time = start_time + fixed_note_duration
            # Convert predicted velocity (0-1) to MIDI velocity (1-127)
            velocity = int(
                masked_velocities[drum_idx, frame_idx].item() * 110) + 1
            velocity = max(1, min(velocity, 127))
            pitch = index_to_pitch_map.get(drum_idx)
            if pitch is None:
                continue  # Skip if drum index isn't mapped
            note = pretty_midi.Note(
                velocity=velocity, pitch=pitch, start=start_time, end=end_time)
            instrument.notes.append(note)

    pm.instruments.append(instrument)
    return pm


def visualize_and_listen(
    model,
    data_loader,
    device,
    threshold=0.5,
    num_samples=3,
    sr=22050,
    hop_length=512,
    soundfont_path=None,
    raw_audio_dir=None,
    drum_names=None,
    index_to_pitch_map=None
):
    """
    Shows plots and plays original audio vs predicted synthesized audio.
    """
    # Make sure model is in eval mode
    model.eval()
    samples_seen = 0

    # Check if we have the necessary files
    can_synthesize = soundfont_path is not None and Path(
        soundfont_path).exists()
    can_find_raw = raw_audio_dir is not None and Path(raw_audio_dir).exists()

    print(f"--- Starting Visualization & Listening ---")
    if not can_find_raw:
        print(f"WARNING: Raw audio directory not found. Cannot play original audio.")
    if not can_synthesize:
        print("WARNING: SoundFont not found. Cannot synthesize predicted MIDI.")

    # Create a temporary directory
    with torch.no_grad(), tempfile.TemporaryDirectory() as tmpdir:
        temp_dir_path = Path(tmpdir)

        # Process samples
        for batch in data_loader:
            if samples_seen >= num_samples:
                break

            # Get batch data
            inputs = batch["input"].to(device)
            onset_targets = batch["onset_target"]
            processed_file_paths = batch["file_paths"]

            # Get predictions
            onset_logits, velocity_preds = model(inputs)
            onset_logits, velocity_preds = onset_logits.cpu(), velocity_preds.cpu()
            onset_probs = torch.sigmoid(onset_logits)

            # Process each batch item
            for i in range(inputs.size(0)):
                if samples_seen >= num_samples:
                    break

                # Extract file info
                current_processed_path = Path(processed_file_paths[i])
                original_stem_with_prefix = current_processed_path.stem

                # Remove drummer prefix to match raw filenames
                first_underscore_index = original_stem_with_prefix.find('_')
                file_stem = original_stem_with_prefix[first_underscore_index +
                                                      1:] if first_underscore_index != -1 else original_stem_with_prefix

                print(
                    f"\n--- Sample {samples_seen + 1}/{num_samples} (Stem: {file_stem}) ---")

                # Get sample data
                input_spec = inputs[i].cpu()
                gt_onsets = onset_targets[i]
                pred_onset_probs = onset_probs[i]
                pred_velocities = velocity_preds[i]

                n_frames = input_spec.shape[1]
                frame_times = librosa.frames_to_time(
                    np.arange(n_frames), sr=sr, hop_length=hop_length)

                # Plot visualizations
                _plot_comparison(
                    input_spec, gt_onsets, pred_onset_probs, pred_velocities,
                    threshold, file_stem, drum_names, hop_length
                )

                # Play audio comparison
                if can_find_raw and can_synthesize:
                    _play_audio_comparison(
                        file_stem, raw_audio_dir, pred_onset_probs, pred_velocities,
                        threshold, frame_times, index_to_pitch_map, temp_dir_path,
                        soundfont_path, sr
                    )

                samples_seen += 1
                print("-" * 40)

    print(f"\n--- Visualization & Listening Finished ---")


def _plot_comparison(input_spec, gt_onsets, pred_onset_probs, pred_velocities,
                     threshold, file_stem, drum_names, hop_length):
    """Plot spectrogram, ground truth and predictions side by side."""
    plt.figure(figsize=(15, 8))
    plt.suptitle(
        f"Transcription Comparison for: {file_stem}", fontsize=14, y=0.99)

    # Plot input spectrogram
    plt.subplot(3, 1, 1)
    plt.imshow(input_spec.numpy(), aspect='auto',
               origin='lower', cmap='viridis')
    plt.colorbar(label='Normalized Magnitude')
    plt.title('Input Mel Spectrogram')
    plt.ylabel('Mel Bin')
    plt.xticks([])

    # Plot ground truth
    plt.subplot(3, 1, 2)
    plt.imshow(gt_onsets.numpy(), aspect='auto',
               origin='lower', cmap='Reds', vmin=0, vmax=1)
    plt.colorbar(label='Onset (GT)')
    plt.title('Ground Truth Onsets')
    if drum_names:
        plt.yticks(np.arange(len(drum_names)), drum_names)
    plt.xticks([])

    # Plot predictions
    binary_onset_pred = (pred_onset_probs > threshold).float()
    masked_velocity_pred = pred_velocities * binary_onset_pred
    plt.subplot(3, 1, 3)
    plt.imshow(masked_velocity_pred.numpy(), aspect='auto',
               origin='lower', cmap='Blues', vmin=0, vmax=1)
    plt.colorbar(label='Velocity (Pred, 0-1)')
    plt.title(f'Predicted Onsets (Threshold={threshold:.2f}) & Velocities')
    if drum_names:
        plt.yticks(np.arange(len(drum_names)), drum_names)
    plt.xlabel(f'Time Frames (Hop Length = {hop_length})')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


def _play_audio_comparison(file_stem, raw_audio_dir, pred_onset_probs, pred_velocities,
                           threshold, frame_times, index_to_pitch_map, temp_dir_path,
                           soundfont_path, sr):
    """Play original and synthesized audio."""
    try:
        # Find original audio file
        found_wav = list(Path(raw_audio_dir).rglob(f"**/{file_stem}.wav"))
        found_mp3 = list(Path(raw_audio_dir).rglob(f"**/{file_stem}.mp3"))
        original_audio_path = found_wav[0] if found_wav else (
            found_mp3[0] if found_mp3 else None)

        if original_audio_path:
            print(f"Displaying original audio: {original_audio_path.name}")
            audio_orig, sr_orig = sf.read(original_audio_path)
            display(HTML(f"<b>Original Audio:</b>"))
            display(Audio(audio_orig.T, rate=sr_orig))
        else:
            print(f"Original audio not found for {file_stem}")

        # Synthesize prediction
        print("Synthesizing predicted MIDI...")
        pred_midi = predictions_to_midi(
            pred_onset_probs, pred_velocities, threshold, frame_times, index_to_pitch_map)

        pred_midi_path = temp_dir_path / f"{file_stem}_pred.mid"
        pred_midi.write(str(pred_midi_path))

        pred_wav_path = temp_dir_path / f"{file_stem}_pred.wav"

        if midi_to_audio(pred_midi_path, soundfont_path, pred_wav_path, sr=sr):
            audio_pred, sr_pred = sf.read(pred_wav_path)
            display(HTML(f"<b>Predicted MIDI (Synthesized):</b>"))
            display(Audio(audio_pred.T, rate=sr_pred))
        else:
            print("Failed to synthesize MIDI")

    except Exception as e:
        print(f"Error processing audio comparison: {e}")
