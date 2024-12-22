# Audio Noise Reducer

A desktop application built with Python and Tkinter that reduces background noise from audio files using spectral noise reduction techniques.

## Features

- Support for multiple audio formats (WAV, MP3, OGG, FLAC, M4A)
- Adjustable noise reduction strength
- Real-time progress tracking
- Simple and intuitive user interface
- Automatic format conversion handling
- Cross-platform compatibility

## Screenshots

[Add screenshots of your application here]

## Installation

### Prerequisites

- Python 3.x
- FFmpeg (required for audio format conversion)

### Dependencies
pip install numpy
pip install scipy
pip install soundfile
pip install tkinter



### Running from Source

1. Clone the repository:
git clone https://github.com/arvind-git-code/noise_remover-desktop_App.git
cd noise-reducer



2. Install required packages:
pip install -r requirements.txt


3. Run the application:
python app.py



### Running the Executable

1. Download the latest release from the [Releases](link-to-releases) page
2. Extract the zip file
3. Run `app.exe`

## Building from Source

To create an executable:
pip install pyinstaller
pyinstaller --onefile -w app.py


The executable will be created in the `dist` directory.

## Usage

1. Launch the application
2. Click "Browse" to select an input audio file
3. Choose an output location and format
4. Adjust the noise reduction strength (1.0 is default)
5. Click "Reduce Noise" to process the audio
6. Wait for processing to complete
7. Find your processed audio file at the specified output location

## How It Works

The application uses spectral subtraction to reduce background noise:

1. Converts input audio to WAV format if necessary
2. Performs Short-Time Fourier Transform (STFT) on the audio
3. Estimates noise profile from the first 100ms of audio
4. Creates and applies a spectral mask to reduce noise
5. Performs inverse STFT to reconstruct the audio
6. Converts the processed audio to the desired output format

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- FFmpeg for audio format conversion
- SciPy for signal processing capabilities
- NumPy for numerical computations
- Tkinter for the graphical user interface

## Contact

arvindkumarlbs@gmail.com

Project Link: [https://github.com/arvind-git-code/noise_remover-desktop_App.git](https://github.com/arvind-git-code/noise_remover-desktop_App.git)

## Support

If you find this project helpful, please give it a ⭐️!
