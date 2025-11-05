# DrumScribe-AI

This project was also used for a Deep Learning for Audio Signal course project and I did some slides for it, check them here (they are in Spanish but the amount of text is so small that I'm sure anyone can understand it).

https://docs.google.com/presentation/d/e/2PACX-1vRZMLv54Lwds3XjPzL-EkvlxaNIu4ZqrGLiD8GjuV42B5Cri0M5aMMj-cHX-8UGUVEaHpDuh8Z1HQRC/pub

## Data Processing

### Audio Sample Rate

For this project, audio files are resampled to **22050 Hz** during preprocessing. This is a common sample rate in audio machine learning, offering a balance between capturing essential frequency information and computational efficiency. According to the Nyquist theorem, this rate allows for the representation of frequencies up to 11025 Hz, which covers the most critical range for drum transcription while reducing data size compared to higher rates like 44100 Hz.
