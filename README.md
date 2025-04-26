# DrumScribe-AI

## Data Processing

### Audio Sample Rate

For this project, audio files are resampled to **22050 Hz** during preprocessing. This is a common sample rate in audio machine learning, offering a balance between capturing essential frequency information and computational efficiency. According to the Nyquist theorem, this rate allows for the representation of frequencies up to 11025 Hz, which covers the most critical range for drum transcription while reducing data size compared to higher rates like 44100 Hz.
