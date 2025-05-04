# TASK.md

## 📊 Project Workflow Visualization

This diagram illustrates the overall workflow, showing the progression through milestones and the relationships between different components.

```mermaid
graph TD
    subgraph "Milestone 1: Data Acquisition & Exploration"
        A[Setup Environment & Repo] --> B(Download/Acquire E-GMD Data);
        B --> C{Notebook 1: Dataset Exploration};
        C -- Creates --> D[Train/Val/Test Splits & Subset Metadata];
    end

    subgraph "Milestone 2: Feature Engineering"
        D --> E{Notebook 2: Feature Engineering};
        E -- Extracts/Aligns --> F[Processed Features & Targets];
        F --> G[Data Pipeline / Loader];
    end

    subgraph "Milestone 3: Model Development & Training"
        G --> H{Notebook 3: Model Development};
        H -- Defines/Uses --> I(Model Architecture);
        H -- Trains --> J[Trained Model Checkpoints];
    end

    subgraph "Milestone 3.5: Transfer Learning"
        J --> TL{Notebook 4: Transfer Learning};
        TL -- Uses --> PTM[Pre-trained Audio/Image Models];
        TL -- Produces --> TLM[Enhanced Model Checkpoints];
    end

    subgraph "Milestone 4: Inference & Evaluation"
        J --> K{Notebook 5: Inference & Evaluation};
        TLM --> K;
        K -- Generates --> L[Transcribed MIDI Files];
        K -- Calculates --> M[Evaluation Metrics & Plots];
        K -- Compares --> COMP[Baseline vs Transfer Learning];
    end

    subgraph "Milestone 5: Code Modularization"
        C --> N[src/data_handling.py];
        E --> O[src/feature_extraction.py];
        E --> P[src/midi_utils.py];
        H --> Q[src/model.py];
        TL --> QTL[src/transfer_models.py];
        K --> R[src/evaluation.py];
        N & O & P & Q & QTL & R --> S[scripts/train.py];
        N & O & P & Q & QTL & R --> T[scripts/transcribe.py];
    end

    subgraph "Milestone 6: Documentation & Presentation"
        U[Update README, Docs, Examples];
        V[Prepare Presentation & Demo];
    end

    %% Dependencies between milestones/outputs
    D --> E;
    F --> G;
    G --> H;
    I --> H;
    J --> K;
    L --> V;
    M --> V;
    S & T --> U;

    %% Linking Notebooks to Modules (Refinement Step)
    C -.-> N;
    E -.-> O;
    E -.-> P;
    H -.-> Q;
    K -.-> R;

    style D fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#ccf,stroke:#333,stroke-width:2px
    style TLM fill:#ccf,stroke:#333,stroke-width:2px
    style L fill:#cfc,stroke:#333,stroke-width:2px
    style M fill:#cfc,stroke:#333,stroke-width:2px
    style COMP fill:#cfc,stroke:#333,stroke-width:2px
```

**Explanation:**

1.  **Milestones 1-4 (Notebook Focus):** The core workflow starts with data acquisition and exploration (Notebook 1), moves to feature engineering (Notebook 2), then model development (Notebook 3), and finally inference/evaluation (Notebook 4). Key outputs like data splits, processed features, and trained models link these stages.
2.  **Milestone 5 (Modularization):** This milestone refactors the logic developed in the notebooks into reusable Python modules (`src/`) and command-line scripts (`scripts/`). The dashed lines indicate that the code originates from the notebooks.
3.  **Milestone 6 (Final Touches):** Documentation and presentation build upon the completed code and results.

---

## 💾 Milestone 1: Dataset Acquisition & Exploration

- [x] **Project Setup**

  - [x] Create and configure Python virtual environment
  - [x] Install core dependencies (librosa, numpy, matplotlib, pytorch, etc.)
  - [x] Create proper directory structure for data organization
  - [x] Set up version control and initial repository

- [x] **E-GMD Dataset Acquisition**

  - [x] Download the E-GMD dataset (or a portion of it)
  - [x] Understand dataset structure and organization
  - [x] Set up metadata handling for audio-MIDI pairs

- [x] **Notebook 1: Dataset Exploration & Subsetting**
  - [x] Create notebook `notebooks/01_dataset_exploration.ipynb`
  - [x] Explore E-GMD structure: audio files, MIDI annotations, metadata
  - [x] Visualize examples of audio waveforms and corresponding MIDI
  - [x] Develop strategy for creating a manageable subset
  - [x] Implement subset extraction pipeline
  - [x] Create balanced train/validation/test splits
  - [x] Generate dataset statistics and visualizations

## 🔍 Milestone 2: Feature Engineering & Data Preparation

- [x] **Notebook 2: Feature Engineering**

  - [x] Create notebook `notebooks/02_feature_engineering.ipynb`
  - [x] Implement audio preprocessing (resampling, normalization)
  - [x] Extract Mel spectrograms with different parameters
  - [x] Visualize spectrograms and compare configurations
  - [x] Extract onset and velocity information from MIDI files
  - [x] Align audio features with MIDI ground truth
  - [x] Create and save training examples

- [x] **Data Pipeline Development**
  - [x] Create efficient data loader for batched processing
  - [x] Implement on-the-fly data augmentation
  - [x] Develop feature caching mechanism for faster training

## 🏗️ Milestone 3: Model Development & Training

- [x] **Notebook 3: Model Development**

  - [x] Create notebook `notebooks/03_model_development.ipynb`
  - [x] Design model architecture for both onset and velocity prediction
  - [x] Implement model in PyTorch
  - [x] Define appropriate loss functions
  - [x] Create training loop with metrics tracking
  - [x] Implement validation procedure
  - [x] Visualize training progress
  - [x] Save model checkpoints

- [x] **Model Refinement**
  - [x] Experiment with different architectures
  - [x] Tune hyperparameters
  - [x] Implement early stopping and learning rate scheduling
  - [x] Evaluate model performance on validation set

### 🔁 Milestone 3.5: Transfer Learning

- [ ] **Notebook 4: Transfer Learning**
  - [ ] Create notebook `notebooks/04_transfer_learning.ipynb`
  - [ ] Research and implement audio-specific pre-trained models
  - [ ] Optional: Implement image recognition pre-trained models (since we work with mel spectrograms)
  - [ ] Develop staged fine-tuning pipeline:
    - [ ] Initial training with frozen layers
    - [ ] Gradual unfreezing of layers
  - [ ] Adapt architecture to work with mel spectrograms
  - [ ] Compare performance with base model

## 📊 Milestone 4: Inference & Evaluation

- [ ] **Notebook 5: Inference & Evaluation**

  - [ ] Create notebook `notebooks/05_inference_evaluation.ipynb`
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
