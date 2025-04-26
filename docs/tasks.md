# TASK.md

## 🚀 Milestone 1: Dataset Acquisition & Exploration

- [ ] **Project Setup**
  - [ ] Create and configure Python virtual environment
  - [ ] Install core dependencies (librosa, numpy, matplotlib, pytorch, etc.)
  - [ ] Create proper directory structure for data organization
  - [ ] Set up version control and initial repository

- [ ] **E-GMD Dataset Acquisition**
  - [ ] Download the E-GMD dataset (or a portion of it)
  - [ ] Understand dataset structure and organization
  - [ ] Set up metadata handling for audio-MIDI pairs

- [ ] **Notebook 1: Dataset Exploration & Subsetting**
  - [ ] Create notebook `notebooks/01_dataset_exploration.ipynb`
  - [ ] Explore E-GMD structure: audio files, MIDI annotations, metadata
  - [ ] Visualize examples of audio waveforms and corresponding MIDI
  - [ ] Develop strategy for creating a manageable subset
  - [ ] Implement subset extraction pipeline
  - [ ] Create balanced train/validation/test splits
  - [ ] Generate dataset statistics and visualizations

## 🔍 Milestone 2: Feature Engineering & Data Preparation

- [ ] **Notebook 2: Feature Engineering**
  - [ ] Create notebook `notebooks/02_feature_engineering.ipynb`
  - [ ] Implement audio preprocessing (resampling, normalization)
  - [ ] Extract Mel spectrograms with different parameters
  - [ ] Visualize spectrograms and compare configurations
  - [ ] Extract onset and velocity information from MIDI files
  - [ ] Align audio features with MIDI ground truth
  - [ ] Create and save training examples

- [ ] **Data Pipeline Development**
  - [ ] Create efficient data loader for batched processing
  - [ ] Implement on-the-fly data augmentation
  - [ ] Develop feature caching mechanism for faster training

## 🏗️ Milestone 3: Model Development & Training

- [ ] **Notebook 3: Model Development**
  - [ ] Create notebook `notebooks/03_model_development.ipynb`
  - [ ] Design model architecture for both onset and velocity prediction
  - [ ] Implement model in PyTorch
  - [ ] Define appropriate loss functions
  - [ ] Create training loop with metrics tracking
  - [ ] Implement validation procedure
  - [ ] Visualize training progress
  - [ ] Save model checkpoints

- [ ] **Model Refinement**
  - [ ] Experiment with different architectures
  - [ ] Tune hyperparameters
  - [ ] Implement early stopping and learning rate scheduling
  - [ ] Evaluate model performance on validation set

## 📊 Milestone 4: Inference & Evaluation

- [ ] **Notebook 4: Inference & Evaluation**
  - [ ] Create notebook `notebooks/04_inference_evaluation.ipynb`
  - [ ] Implement inference pipeline
  - [ ] Develop post-processing for predictions
  - [ ] Convert model outputs to MIDI
  - [ ] Calculate evaluation metrics (F-measure, MAE for velocity)
  - [ ] Create visualizations comparing predictions to ground truth
  - [ ] Generate audio renderings of predicted MIDI

- [ ] **Final Evaluation**
  - [ ] Evaluate best model on test set
  - [ ] Create comprehensive evaluation report
  - [ ] Compare with existing methods in literature

## 📦 Milestone 5: Code Modularization & Package Creation

- [ ] **Extract Core Functionality**
  - [ ] Create Python modules from notebook code:
    - [ ] `src/data_handling.py`: Dataset processing and loading
    - [ ] `src/feature_extraction.py`: Audio feature extraction
    - [ ] `src/midi_utils.py`: MIDI processing utilities
    - [ ] `src/model.py`: Model architecture definition
    - [ ] `src/evaluation.py`: Metrics and evaluation functions

- [ ] **Create Simple Interface**
  - [ ] Implement training script `scripts/train.py`
  - [ ] Create inference script `scripts/transcribe.py`
  - [ ] Add command-line options for key parameters

## 📚 Milestone 6: Documentation & Presentation

- [ ] **Project Documentation**
  - [ ] Update README.md with detailed instructions
  - [ ] Document API and usage examples
  - [ ] Add comments and docstrings to all code
  - [ ] Create demo notebook with end-to-end example

- [ ] **Prepare Class Presentation**
  - [ ] Create slides summarizing approach and results
  - [ ] Prepare audio examples comparing original and transcribed drums
  - [ ] Set up live demo
  - [ ] Document limitations and future work
