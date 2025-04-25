# DrumScribe-AI

## Overview

DrumScribe-AI is a Python-based system for automatic drum transcription that takes raw drum audio tracks (WAV/MP3) as input and outputs MIDI files representing the detected drum hits. The core of the system is a deep neural network that processes Mel-spectrograms to identify the onset times and types of core drum instruments (kick, snare, hi-hat).

## Project Structure

```
DrumScribe-AI/
├── data/               # Dataset storage
│   ├── processed/      # Preprocessed dataset files
│   └── raw/            # Original dataset files
├── docs/               # Documentation files
│   ├── planning.md     # Project architecture and planning
│   └── tasks.md        # Task list and progress tracking
├── models/             # Saved model weights and checkpoints
├── notebooks/          # Jupyter notebooks for development and experimentation
├── scripts/            # Utility scripts for training, inference, etc.
├── src/                # Source code
│   └── __init__.py
└── requirements.txt    # Project dependencies
```

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DrumScribe-AI
```

2. Create and activate a Python virtual environment:
```bash
# Using pyenv
pyenv virtualenv 3.11.11 drumscribe-ai
pyenv local drumscribe-ai

# Or using venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Coming soon as the project progresses.

## Features (Planned)

- Audio preprocessing with Librosa for feature extraction
- Deep learning model (CNN/CRNN) for drum onset detection and classification
- Post-processing to convert detected onsets to MIDI notes
- Support for the standard General MIDI (GM) mapping
- Initial target drum classes: Kick Drum, Snare Drum, Closed Hi-Hat

## Dependencies

- Python 3.8+
- PyTorch & TorchAudio
- Librosa, SoundFile
- NumPy
- MIDI I/O: mido or pretty_midi
- Matplotlib, seaborn
- JupyterLab/Notebook

## License

[License information to be added]

## Acknowledgements

- Based on research and methodologies in automatic drum transcription
- Utilizes public datasets such as ENST-Drums and IDMT-SMT-Drums
