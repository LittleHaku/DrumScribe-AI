# Planning

## Summary

We will build an Automatic Drum Transcription (ADT) system using the Expanded Groove MIDI Dataset (E-GMD), working with a notebook-first approach to clearly visualize and understand each step of the pipeline. Since the E-GMD dataset is quite large (90GB compressed, 132GB uncompressed), we'll develop strategies to work with manageable subsets for local development. Our model will predict both drum-hit onsets and velocities, outputting MIDI files that capture the dynamics of the original performances.

---

## 1) Dataset Strategy (E-GMD)

1. **Dataset Selection**
   - Use the Expanded Groove MIDI Dataset (E-GMD) from Magenta
   - E-GMD contains 444 hours of audio from 43 drum kits with human-performed velocity annotations
   - Dataset is available at: [https://magenta.tensorflow.org/datasets/e-gmd](https://magenta.tensorflow.org/datasets/e-gmd)

2. **Working with Large Dataset**
   - Create a subset extraction pipeline to select a manageable portion (~5-10GB)
   - Sample across different drum kits to maintain variety
   - Focus on a balanced subset of patterns with clear annotations

3. **Data Organization**
   - Extract audio in WAV format and corresponding MIDI files
   - Convert Roland drum mappings to a simplified General MIDI mapping
   - Focus on six core drum categories: Kick, Snare, Tom, HiHat, Crash, and Ride
   - Create metadata records connecting audio and MIDI pairs
   - Split into train/validation/test sets (70/15/15%)

---

## 2) Notebook-First Development Pipeline

1. **Notebook 1: Dataset Exploration & Subsetting**
   - Explore E-GMD dataset structure
   - Develop subset extraction strategy
   - Implement simplification of drum mappings (Roland → simplified GM)
   - Create a balanced, representative subset
   - Analyze audio and MIDI characteristics

2. **Notebook 2: Feature Engineering**
   - Convert audio to Mel spectrograms
   - Visualize different spectrogram parameters
   - Extract onset and velocity information from simplified MIDI
   - Align audio features with MIDI ground truth

3. **Notebook 3: Model Development**
   - Design CNN/CRNN architecture
   - Implement both onset and velocity prediction heads
   - Train with appropriate loss functions
   - Track and visualize learning progress

4. **Notebook 4: Inference & Evaluation**
   - Implement post-processing for predictions
   - Convert model outputs to MIDI
   - Compare with ground truth
   - Evaluate using F-measure, precision, recall, and velocity accuracy

---

## 3) Model Architecture

- **Input**: Log-Mel spectrogram of audio frames
- **Feature Extraction**:
  - Convolutional layers for spatial feature extraction
  - Optional: Recurrent layers for temporal modeling
- **Output Heads**:
  - Onset detection head with sigmoid activation (one output per simplified drum type)
  - Velocity prediction head with appropriate activation (linear/tanh)
- **Multi-task Learning**:
  - Joint training with weighted losses for both onsets and velocities

---

## 4) Implementation Plan

1. **Start with Notebooks**
   - Develop entire pipeline in Jupyter notebooks
   - Visualize each step for clarity and understanding
   - Establish working proofs of concept

2. **Gradual Modularization**
   - Extract core functions to Python modules
   - Create a consistent API between components
   - Maintain visualization capabilities

3. **Training & Inference Pipelines**
   - Create efficient data loaders for batch processing
   - Implement checkpointing and model saving
   - Develop a simple inference API for prediction

---

## 5) Evaluation & Presentation

- **Onset Metrics**: F-measure, precision, recall for hit detection
- **Velocity Metrics**: Mean absolute error, correlation with ground truth
- **Perceptual Evaluation**: Listen to generated MIDI against ground truth
- **Visualization**: Create onset/velocity alignment plots

---

## 6) Project Timeline

1. **Week 1**: Dataset exploration, subsetting, and preprocessing
2. **Week 2**: Feature engineering and initial model development
3. **Week 3**: Model refinement and training
4. **Week 4**: Evaluation, MIDI generation, and presentation preparation
