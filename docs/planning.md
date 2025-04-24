# Planning: Automatic Drum Transcription (Notebook-Focused Development)

## Summary

This project aims to build a Python-based system, developed primarily within a **Jupyter Notebook** for assignment purposes, that takes a raw drum audio track (WAV/MP3 file) as input and outputs a corresponding MIDI file representing the detected drum hits. The core will be a deep neural network (initially a CNN or CRNN) processing Mel-spectrograms to identify the onset times and types of core drum instruments (e.g., kick, snare, hi-hat). A post-processing module converts detected onsets into MIDI notes using the standard General MIDI (GM) mapping with a **fixed velocity**. While developed in a notebook, the structure will follow logical sections (data handling, model, training, inference, post-processing) to facilitate potential future refactoring into Python modules for applications like a web UI.

---

## 1. Purpose & Vision

- **Objective**: Automate the transcription of recorded drum tracks into a standard symbolic format (MIDI) to assist musicians, producers, and educators.
- **Development Approach:** Implement the core functionality within one or more **Jupyter Notebooks** (`.ipynb`) for ease of development, visualization, and assignment submission.
- **Core Scope**: Accurately detect the **onset time** and **instrument class** for essential kit elements:
  - **Initial Target Classes:** Kick Drum, Snare Drum, Closed Hi-Hat.
- **Outcomes**:
  1. **MIDI Export**: Generate a standard General MIDI (GM) file (Channel 10) mapping detected instruments to their standard note numbers (e.g., Kick=36, Snare=38, Closed Hi-Hat=42) with a **fixed, pre-defined velocity** (e.g., 100).
  2. **PDF Notation (Optional Extension)**: Automated engraving via a MIDI-to-sheet music pipeline (e.g., using MuseScore).
  3. **Custom MIDI Mapping (Optional Extension)**: Allow users to provide a mapping file (e.g., JSON) to assign detected instruments to non-GM MIDI notes.
- **Future Goal:** The notebook implementation should be structured logically to allow relatively straightforward refactoring into separate Python (`.py`) modules for potential integration into a web application or more complex pipelines later.

---

## 2. System Architecture (Conceptual Sections within Notebook)

### 2.1 Data Ingestion & Preprocessing

- **Input**: Mono or stereo WAV/MP3 files containing isolated drum tracks or mixes where drums are prominent. Path to input files will be specified within the notebook or via simple variables.
- **Preprocessing Steps (Implemented as functions/cells):**
  - **Resampling**: Standardize audio to a consistent sample rate (e.g., 44.1 kHz or 22.05 kHz).
  - **Normalization**: Normalize audio amplitude (e.g., peak or RMS).
  - **Time–Frequency Transform**: Compute **Mel-spectrograms** (using STFT followed by Mel filterbank) as the primary input feature for the model. Log-amplitude scaling is recommended.
  - **Data Loading/Annotation Parsing:** Functions to load audio and corresponding ground truth MIDI/annotations, converting them into suitable formats (e.g., frame-wise labels) for training.

### 2.2 Model Core

- **Architecture Options (Defined as classes/functions):**
  - **Baseline: CNN**: Frame-wise multi-label classification on Mel-spectrogram patches/frames. Defined using PyTorch/TensorFlow within notebook cells.
  - **Advanced: CRNN**: CNN front-end + RNN (LSTM/GRU) backend.
- **Output**: Per-frame probability vector (shape: `[num_frames, num_classes]`), where each element `p(frame_i, class_j)` indicates the likelihood of instrument `j` being active in frame `i`.

### 2.3 Post-Processing & MIDI Generation

- **Onset Detection (Implemented as functions/cells):**
  - Apply a threshold to the probability outputs for each instrument class.
  - Perform peak-picking on the thresholded probabilities to find likely onset times (time stamps).
- **MIDI Generation (Implemented as functions/cells):**
  - For each detected onset `(timestamp, instrument_class)`:
    - Create a MIDI Note On message using `mido` or `pretty_midi`.
    - Map `instrument_class` to its standard GM note number.
    - Set a **fixed velocity**.
    - Set MIDI channel to 9 (standard drum channel).
    - Convert `timestamp` (seconds) to MIDI ticks.
  - Function to save the generated MIDI data to a file.

---

## 3. Constraints & Considerations

- **Development Environment:** Primarily **Jupyter Notebook**. Structure code logically within cells.
- **Simplicity First**: Focus on the initial target classes (Kick, Snare, Closed HH).
- **Velocity**: Explicitly **out of scope** for estimation; use fixed velocity.
- **Polyphony**: Model output allows simultaneous predictions; training data handling might simplify based on dataset characteristics.
- **Latency**: Batch (offline) processing within the notebook is the goal.
- **Data Availability**: Acknowledge limitations; plan for augmentation or synthetic data.
- **Evaluation Metrics**: Frame-level and crucial **Onset-level** metrics (F1, P, R with tolerance window) should be calculated and displayed within the notebook.

---

## 4. Tech Stack & Tools

### 4.1 Languages & Environments

- **Python 3.8+** with virtualenv or Conda.
- **Primary Development Tool:** **Jupyter Notebook (`.ipynb`)**. Code will be organized using Markdown headers and cells.

### 4.2 Core Libraries

- **Audio I/O & Processing**: `Librosa`, `SoundFile`.
- **Deep Learning**: `PyTorch` + `TorchAudio` **OR** `TensorFlow/Keras`.
- **Numerical**: `NumPy`.
- **MIDI I/O**: `mido` **or** `pretty_midi`.
- **Visualization**: `Matplotlib`, `seaborn` (used extensively within the notebook).
- **Notebook Environment:** `jupyterlab` or `notebook`.
- **Optional PDF**: `MuseScore` (command-line interface).

### 4.3 Project Structure & Management

- **Primary Artifact:** One or more `.ipynb` files containing the core logic, training, and inference steps.
- **Supporting Directory Structure:** Maintain a standard structure for organization outside the notebook:
  - `data/`: For raw and processed datasets.
  - `models/`: To save trained model checkpoints.
  - `output/`: To save generated MIDI files.
  - `docs/`: For planning documents (`PLANNING.md`, `TASKS.md`).
- **Version Control**: `Git` + `GitHub` (or similar) - Track changes to the notebook(s) and supporting files. Be mindful of large notebook diffs.
- **Task Tracking**: `docs/TASKS.md` outlining steps _within_ the notebook development process.

---

## 5. Data & Datasets

- **Primary Goal**: Obtain datasets with aligned audio drum recordings and ground truth MIDI annotations.
- **Public Datasets**: `ENST-Drums`, `IDMT-SMT-Drums`, etc.
- **Synthetic Data Generation**: Strategy using MIDI + VSTs.
- **Data Augmentation**: Techniques like time-stretching, pitch-shifting, noise addition.
- **Data Splits**: Define Training, Validation, Test sets (files managed outside the notebook, logic within).

---

## 6. Optional Extensions (Post-Core Functionality / Post-Assignment)

1. Expand Instrument Classes.
2. PDF Notation.
3. Custom MIDI Mapping.
4. Velocity Estimation.
5. **Refactor Notebook to `.py` Modules:** Prepare code for integration into other applications (like a web app).
6. Real-Time Transcription.
7. Web UI.
