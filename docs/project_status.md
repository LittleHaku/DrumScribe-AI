# Project Status (as of 2025-04-26 22:22)

## Summary

This document provides a snapshot of the DrumScribe-AI project status to facilitate context sharing between development sessions.

## Current State

*   **Milestone 1: Dataset Acquisition & Exploration** - **COMPLETED**
    *   Project environment and repository setup are complete.
    *   The full E-GMD dataset was downloaded to `data/raw/`.
    *   A 10% subset, stratified by `drummer`, has been created.
        *   Subset audio/MIDI files are located in: `data/subset/`
        *   Subset metadata (including train/val/test splits) is saved at: `data/subset/subset_metadata.csv`
    *   Dataset exploration, subsetting logic, and split creation are documented in `notebooks/01_dataset_exploration.ipynb`.
    *   All related tasks in `docs/tasks.md` have been marked as complete.
    *   The high-level plan in `docs/planning.md` remains accurate.

## Key Outputs

*   `data/subset/`: Directory containing the 10% stratified data subset (audio and MIDI).
*   `data/subset/subset_metadata.csv`: Metadata for the subset, including `split_set` column ('train', 'validation', 'test').
*   `notebooks/01_dataset_exploration.ipynb`: Completed notebook detailing data loading, exploration, subsetting, and split creation.
*   `requirements.txt`: Updated with `scikit-learn`.

## Next Steps

*   Begin **Milestone 2: Feature Engineering & Data Preparation**.
*   Create and start working on `notebooks/02_feature_engineering.ipynb`.
    *   Focus on audio preprocessing (resampling, normalization).
    *   Implement Mel spectrogram extraction.
    *   Extract target features (onsets, velocities) from MIDI.
    *   Align audio features and MIDI targets.

## Project Structure (Top Level)

```
.
├── README.md
├── requirements.txt
├── data/
│   ├── raw/      # Full E-GMD dataset (potentially large, may be gitignored)
│   └── subset/   # 10% stratified subset with audio/MIDI and metadata
├── docs/
│   ├── planning.md
│   ├── tasks.md
│   └── project_status.md  # This file
├── notebooks/
│   └── 01_dataset_exploration.ipynb
├── scripts/
│   └── ... (Placeholder for future scripts)
└── src/
    └── ... (Placeholder for future source modules)
