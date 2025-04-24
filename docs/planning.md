# Planning: Automatic Drum Transcription

## Summary

This project aims to build a Python-based system that takes a raw drum audio track (WAV/MP3 file) as input and outputs a corresponding MIDI file representing the detected drum hits. The core will be a deep neural network (initially a CNN or CRNN) processing Mel-spectrograms to identify the onset times and types of core drum instruments (e.g., kick, snare, hi-hat). A post-processing module converts detected onsets into MIDI notes using the standard General MIDI (GM) mapping with a **fixed velocity**. Optional extensions include PDF notation generation via MuseScore and custom MIDI mapping.

---

## 1. Purpose & Vision

- **Objective**: Automate the transcription of recorded drum tracks into a standard symbolic format (MIDI) to assist musicians, producers, and educators.
- **Core Scope**: Accurately detect the **onset time** and **instrument class** for essential kit elements:
  - **Initial Target Classes:** Kick Drum, Snare Drum, Closed Hi-Hat. (Consider adding Open Hi-Hat if feasible within the timeframe).
- **Outcomes**:
  1. **MIDI Export**: Generate a standard General MIDI (GM) file (Channel 10) mapping detected instruments to their standard note numbers (e.g., Kick=36, Snare=38, Closed Hi-Hat=42) with a **fixed, pre-defined velocity** (e.g., 100).
  2. **PDF Notation (Optional Extension)**: Automated engraving via a MIDI-to-sheet music pipeline (e.g., using MuseScore).
  3. **Custom MIDI Mapping (Optional Extension)**: Allow users to provide a mapping file (e.g., JSON) to assign detected instruments to non-GM MIDI notes.

---

## 2. System Architecture

### 2.1 Data Ingestion & Preprocessing

- **Input**: Mono or stereo WAV/MP3 files containing isolated drum tracks or mixes where drums are prominent.
- **Preprocessing**:
  - **Resampling**: Standardize audio to a consistent sample rate (e.g., 44.1 kHz or 22.05 kHz).
  - **Normalization**: Normalize audio amplitude (e.g., peak or RMS).
  - **Time–Frequency Transform**: Compute **Mel-spectrograms** (using STFT followed by Mel filterbank) as the primary input feature for the model. Log-amplitude scaling is recommended.

### 2.2 Model Core

- **Architecture Options**:
  - **Baseline: CNN**: Frame-wise multi-label classification on Mel-spectrogram patches/frames. Each output neuron corresponds to an instrument class.
  - **Advanced: CRNN**: CNN front-end for feature extraction per frame + RNN (LSTM/GRU) backend to model temporal dependencies and improve onset localization.
- **Output**: Per-frame probability vector (shape: `[num_frames, num_classes]`), where each element `p(frame_i, class_j)` indicates the likelihood of instrument `j` being active in frame `i`. The model should be capable of predicting multiple instruments potentially active in the same frame (multi-label).

### 2.3 Post-Processing

- **Onset Detection**: Convert frame-wise probabilities into discrete onset events.
  - Apply a threshold to the probability outputs for each instrument class.
  - Perform peak-picking on the thresholded probabilities to find likely onset times (time stamps). Refinements like smoothing or using activation functions designed for onset detection might be explored.
- **MIDI Generation**:
  - For each detected onset `(timestamp, instrument_class)`:
    - Create a MIDI Note On message.
    - Map `instrument_class` to its standard GM note number (e.g., Snare -> 38).
    - Set a **fixed velocity** (e.g., 100).
    - Set MIDI channel to 9 (standard drum channel, often displayed as 10).
    - Convert `timestamp` (seconds) to MIDI ticks based on a chosen tempo/time signature (or assume a default).
  - Use libraries like `mido` or `pretty_midi`.

---

## 3. Constraints & Considerations

- **Simplicity First**: Focus on the initial target classes (Kick, Snare, Closed HH) before adding more.
- **Velocity**: Explicitly **out of scope** for estimation; use fixed velocity.
- **Polyphony**: The model _output_ should allow simultaneous predictions (multi-label per frame), but initial _training data_ might benefit from focusing on examples without perfectly overlapping onsets if available datasets are challenging.
- **Latency**: Batch (offline) processing is the goal. Real-time performance is an optional extension.
- **Data Availability**: Acknowledge limitations of public annotated drum datasets. Plan for potential need for data augmentation or using synthetic data (Section 5).
- **Evaluation Metrics**:
  - Frame-level: F1-score, Precision, Recall per instrument class.
  - **Onset-level**: **F1-score, Precision, Recall using a tolerance window (e.g., +/- 50ms)** around ground truth onsets. This is crucial for evaluating transcription quality.

---

## 4. Tech Stack & Tools

### 4.1 Languages & Environments

- **Python 3.8+** with virtualenv or Conda.
- **Jupyter Notebooks**: For exploration, visualization, and initial prototyping.
- **Python Scripts (`.py`)**: For reusable functions, training pipelines, and final inference script/module.

### 4.2 Core Libraries

- **Audio I/O & Processing**: `Librosa`, `SoundFile`.
- **Deep Learning**: `PyTorch` + `TorchAudio` **OR** `TensorFlow/Keras`.
- **Numerical**: `NumPy`.
- **MIDI I/O**: `mido` **or** `pretty_midi`.
- **Visualization**: `Matplotlib`, `seaborn`.
- **Optional PDF**: `MuseScore` (command-line interface for automation).

### 4.3 Project Structure & Management

- **Directory Structure**: Standard ML layout (e.g., `data/`, `src/`, `notebooks/`, `models/`, `scripts/`, `docs/`).
- **Version Control**: `Git` + `GitHub` (or similar).
- **Task Tracking**: `docs/TASKS.md` or project management tool.

---

## 5. Data & Datasets

- **Primary Goal**: Obtain datasets with aligned audio drum recordings and ground truth MIDI annotations.
- **Public Datasets**:
  - `ENST-Drums`: Includes separated stems and annotations (may require alignment checking).
  - `IDMT-SMT-Drums`: Another source for real drum recordings.
  - _(Search for others specifically providing audio-MIDI alignment for drums)_.
- **Synthetic Data Generation**:
  - **Strategy**: Use existing MIDI drum patterns (e.g., from `Lakh MIDI Dataset` filtered for drums, or purpose-created patterns).
  - Render these MIDI files to audio using high-quality drum VSTs/samplers (e.g., free samplers like Sitala, commercial ones if available) to create perfectly aligned (audio, MIDI) pairs.
- **Data Augmentation**: Apply techniques like time-stretching, pitch-shifting (small amounts), adding background noise, and varying gain to increase model robustness, especially if real data is scarce.
- **Data Splits**: Carefully define Training, Validation, and Test sets. Ensure no data leakage between sets (e.g., different recordings from the same drummer/session should ideally be in the same split).

---

## 6. Optional Extensions (Post-Core Functionality)

1. **Expand Instrument Classes**: Add Open Hi-Hat, Toms, Crash, Ride cymbals.
2. **PDF Notation**: Implement the MuseScore CLI pipeline (MIDI -> MusicXML -> PDF).
3. **Custom MIDI Mapping**: Implement loading of a JSON file to override default GM mapping.
4. **Velocity Estimation**: Modify the model or post-processing to estimate hit velocity.
5. **Real-Time Transcription**: Adapt model for low-latency processing (e.g., using TorchScript, ONNX Runtime).
6. **Web UI**: Build a simple Flask/FastAPI interface for audio upload and MIDI download.
