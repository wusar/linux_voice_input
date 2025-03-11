# Real-time Voice Transcription and Pasting Tool

This is a Python-based real-time voice transcription utility. It leverages `pyaudio` for audio capture and `whisper` for speech recognition. The recognized text is then automatically copied to the clipboard and pasted into the active window.

## Features
- **Real-time Audio Recording**: Continuously captures audio input from the microphone.
- **Live Transcription**: Utilizes a pre-trained Whisper model to transcribe the audio on-the-fly.
- **Auto-copy and Paste**: Automatically copies the transcription results to the clipboard and pastes them into the current active window.
- **Automatic Termination**: Stops the program if it detects a long period of silence or if the recording time exceeds a set limit.

## Installation
Before running this project, you need to install the necessary Python libraries. You can install them using the following command:
```bash
pip install -r requirements.txt
```

## Usage
1. **Clone the Repository**:
   - Clone this project to your local machine using the following command:
   ```bash
   git clone https://github.com/wusar/linux_voice_input
   cd linux_voice_input
   ```
2. **Run the Program**:
   - Start the program by running the following command in the terminal:
   ```bash
   python main.py
   ```
   Once the program starts, it will begin listening to the microphone. When it detects speech, it will transcribe it in real-time and paste the results into the active window.

## Code Explanation
### Main Modules and Functions
- **Library Imports**: Imports essential libraries such as `pyaudio`, `wave`, and `whisper` for audio handling and speech recognition.
- **Model Loading**: Loads a pre-trained Whisper model using `whisper.load_model("base")`.
- **Streaming Decoding**: The `stream_decode` function converts audio data into text.
- **Audio Buffer and Parameter Setup**: Defines parameters like the audio buffer size, silence threshold, and maximum silence duration.
- **Microphone Callback**: The `callback` function processes each audio chunk, performs transcription, copy - paste operations, and monitors volume and recording duration.
- **Stream Initialization**: The `start_streaming` function initializes the `pyaudio` stream and starts listening to the microphone.

### Key Parameter Explanations
- `buffer_size`: The size of each audio block, set to 32000 samples (equivalent to 2 seconds by default).
- `silence_threshold`: A volume threshold used to determine if there is any speech input.
- `max_silence_duration`: The maximum amount of continuous silence allowed. The program will terminate if this limit is exceeded.

## Notes
- Ensure your microphone is functioning correctly before running the program.
- Since `pyautogui` is used for pasting, make sure the active window supports paste operations.
- Extended usage may consume significant system resources. Adjust the parameters as needed.

## Contribution
If you have suggestions for improvement or find any issues, please feel free to submit an issue or a pull request.

## License
This project is licensed under the [MIT License](LICENSE).