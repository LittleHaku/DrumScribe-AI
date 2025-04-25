# Tasks

## Phase 1: Setup & Foundation

- [x] **1.1 Project Initialization**
  - [x] Create main project directory.
  - [x] Set up standard ML project structure (`data/`, `src/`, `notebooks/`, `models/`, `scripts/`, `docs/`).
  - [x] Initialize Git repository (`git init`).
  - [ ] Create remote repository (e.g., on GitHub) and push initial structure.
  - [ ] Create initial `README.md`.
- [x] **1.2 Environment Setup**
  - [x] Create Python virtual environment (e.g., `conda create ...` or `python -m venv ...`).
  - [x] Activate the environment.
  - [x] Create `requirements.txt` file.
  - [x] Install core dependencies (`numpy`, `librosa`, `soundfile`, `matplotlib`).
  - [x] Install chosen Deep Learning framework (`pytorch`+`torchaudio` OR `tensorflow`/`keras`).
  - [x] Install MIDI library (`mido` OR `pretty_midi`).
  - [x] Verify installations.
- [x] **1.3 Initial Documentation**
  - [x] Copy final `PLANNING.md` into `docs/`.
  - [x] Finalize this `TASKS.md` file.

---

## Phase 2: Data Handling & Preprocessing

- [ ] **2.1 Data Acquisition**
  - [ ] Download relevant public datasets (e.g., ENST-Drums, IDMT-SMT-Drums).
  - [ ] Organize downloaded data in the `data/raw/` directory.
  - [ ] _(Optional - if needed)_ Set up synthetic data generation:
    - [ ] Select source MIDI files (filter Lakh dataset or use others).
    - [ ] Select/install a drum VST/sampler.
    - [ ] Write script to render MIDI -> Audio using the sampler.
- [ ] **2.2 Data Loading & Preprocessing Implementation (`src/data_handling.py`)**
  - [ ] Implement function to load audio files (`librosa.load`).
  - [ ] Implement resampling function.
  - [ ] Implement audio normalization function.
  - [ ] Implement Mel-spectrogram computation (`librosa.feature.melspectrogram`). Ensure parameters (n_fft, hop_length, n_mels) are configurable. Use log-amplitude.
  - [ ] Implement function(s) to load and parse ground truth MIDI annotations.
    - [ ] Align MIDI events to audio time (consider dataset specifics).
    - [ ] Convert MIDI events into frame-wise target labels (multi-label binary vectors for Kick, Snare, Closed HH).
- [ ] **2.3 Dataset Representation (`src/dataset.py`)**
  - [ ] Implement PyTorch `Dataset` class (or TF equivalent):
    - [ ] Takes list of audio/annotation pairs.
    - [ ] `__getitem__` loads audio, preprocesses, computes spectrogram, loads/formats target labels.
    - [ ] Handles potential segmentation/windowing of long files.
  - [ ] Implement PyTorch `DataLoader` (or TF equivalent) for batching.
- [ ] **2.4 Data Splitting & Preparation**
  - [ ] Define strategy for splitting data into train, validation, test sets (ensure no leakage).
  - [ ] Prepare file lists or metadata files for each split.
  - [ ] _(Optional)_ Implement data augmentation strategies (add noise, time stretch, pitch shift). Integrate into `Dataset` class.

---

## Phase 3: Model Development (Core)

- [ ] **3.1 Model Architecture Definition (`src/model.py`)**
  - [ ] **Choose Initial Architecture**: Start with CNN baseline.
  - [ ] Implement CNN architecture:
    - [ ] Define convolutional layers (2D Conv).
    - [ ] Define activation functions (e.g., ReLU).
    - [ ] Define pooling layers.
    - [ ] Define final fully connected layers.
    - [ ] Define output layer with sigmoid activation for multi-label classification (output size = number of drum classes).
  - [ ] _(Later/Optional)_ Implement CRNN architecture (CNN feature extractor + LSTM/GRU layers).
- [ ] **3.2 Loss Function & Optimizer**
  - [ ] Choose and define loss function (e.g., `torch.nn.BCELoss` or `BCEWithLogitsLoss`).
  - [ ] Choose and configure optimizer (e.g., `torch.optim.Adam`).

---

## Phase 4: Training & Evaluation Pipeline

- [ ] **4.1 Training Script (`scripts/train.py`)**
  - [ ] Set up argument parsing (for hyperparameters, data paths, etc.).
  - [ ] Instantiate model, loss function, optimizer.
  - [ ] Instantiate `DataLoader` for train and validation sets.
  - [ ] Implement the main training loop:
    - [ ] Iterate through epochs and batches.
    - [ ] Move data to appropriate device (CPU/GPU).
    - [ ] Perform forward pass.
    - [ ] Calculate loss.
    - [ ] Perform backward pass (`loss.backward()`).
    - [ ] Update model weights (`optimizer.step()`).
    - [ ] Zero gradients (`optimizer.zero_grad()`).
  - [ ] Implement validation loop (run periodically, e.g., end of epoch):
    - [ ] Set model to evaluation mode (`model.eval()`).
    - [ ] Disable gradient calculation (`with torch.no_grad():`).
    - [ ] Iterate through validation data.
    - [ ] Calculate validation loss and metrics.
- [ ] **4.2 Evaluation Metrics Implementation (`src/evaluation.py`)**
  - [ ] Implement frame-level metrics calculation (Precision, Recall, F1 per class, Micro/Macro averages).
  - [ ] Implement **onset-level** metrics calculation:
    - [ ] Helper function to convert frame probabilities -> onset times (using thresholding/peak-picking from Phase 5).
    - [ ] Function to compare predicted onsets vs ground truth onsets within a tolerance window (e.g., +/- 50ms).
    - [ ] Calculate onset-based Precision, Recall, F1 per class.
- [ ] **4.3 Experiment Tracking & Checkpointing**
  - [ ] Implement logging (print to console, save to file).
  - [ ] _(Optional)_ Integrate TensorBoard or MLflow for visualizing loss/metrics.
  - [ ] Implement model checkpointing (save best model based on validation metric, e.g., validation F1).
- [ ] **4.4 Run Training**
  - [ ] Run initial training experiments on a small subset of data to debug.
  - [ ] Run full training experiment(s).
  - [ ] Analyze results, tune hyperparameters if necessary.

---

## Phase 5: Post-processing & MIDI Output

- [ ] **5.1 Inference Script/Function (`scripts/inference.py` or `src/inference.py`)**
  - [ ] Implement function to load a trained model checkpoint.
  - [ ] Implement function `predict(audio_path, model)`:
    - [ ] Loads audio.
    - [ ] Preprocesses audio (resample, normalize, Mel-spectrogram).
    - [ ] Feeds spectrogram through the loaded model (in `eval` mode).
    - [ ] Returns frame-wise probability outputs.
- [ ] **5.2 Onset Detection Logic (`src/postprocessing.py`)**
  - [ ] Implement function `probabilities_to_onsets(probabilities, threshold, frame_rate)`:
    - [ ] Apply threshold(s) to probabilities per instrument.
    - [ ] Implement peak-picking algorithm to find onset frames.
    - [ ] Convert onset frame indices to timestamps (seconds).
    - [ ] Return a list of `(timestamp, instrument_class)` tuples.
- [ ] **5.3 MIDI Generation (`src/midi_export.py`)**
  - [ ] Implement function `onsets_to_midi(onset_list, output_midi_path)`:
    - [ ] Define standard GM mapping (Kick=36, Snare=38, CHH=42, etc.).
    - [ ] Define **fixed velocity** (e.g., 100).
    - [ ] Use `mido` or `pretty_midi` to create a MIDI structure.
    - [ ] Add Note On messages for each detected onset, using the GM mapping and fixed velocity, on Channel 10 (index 9).
    - [ ] _(Optional)_ Add corresponding Note Off messages or handle note duration if needed.
    - [ ] Save the MIDI file.

---

## Phase 6: Integration & Testing

- [ ] **6.1 End-to-End Pipeline Script (`scripts/transcribe_drums.py`)**
  - [ ] Create a main script that takes an input audio file path and output MIDI file path as arguments.
  - [ ] Call functions from previous steps in sequence: `load_audio` -> `preprocess` -> `predict` -> `probabilities_to_onsets` -> `onsets_to_midi`.
- [ ] **6.2 Testing & Refinement**
  - [ ] Run the end-to-end script on examples from the validation and test sets.
  - [ ] Perform qualitative evaluation: Listen to original audio vs. generated MIDI playback.
  - [ ] Tune post-processing parameters (thresholds, peak-picking settings) based on evaluation metrics and listening tests.
- [ ] **6.3 Final Documentation**
  - [ ] Update `README.md` with instructions on how to set up the environment and run the transcription script.
  - [ ] Briefly document model architecture and results.

---

## Phase 7: Optional Extensions (If Time Permits)

- [ ] **7.1 Expand Instrument Classes**
  - [ ] Add Open Hi-Hat, Toms, Cymbals to target classes.
  - [ ] Update data annotation processing.
  - [ ] Update model output layer.
  - [ ] Retrain and re-evaluate.
- [ ] **7.2 PDF Notation Generation**
  - [ ] Install MuseScore.
  - [ ] Add step to convert generated MIDI -> MusicXML (using `pretty_midi` or external tool).
  - [ ] Add step to call MuseScore CLI to convert MusicXML -> PDF.
- [ ] **7.3 Custom MIDI Mapping**
  - [ ] Define JSON format for custom mapping.
  - [ ] Update `midi_export.py` to optionally load and use the custom mapping instead of GM default.
- [ ] **7.4 Velocity Estimation**
  - [ ] Modify model/post-processing to estimate velocity.
  - [ ] Update MIDI generation to use estimated velocity.
- [ ] **7.5 Real-Time Transcription**
  - [ ] Investigate model optimization (TorchScript/ONNX).
  - [ ] Adapt code for streaming audio input/output.
- [ ] **7.6 Web UI**
  - [ ] Build Flask/FastAPI backend.
  - [ ] Create simple HTML/JS frontend for upload/download.
