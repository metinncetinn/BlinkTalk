
# Blink-Based Interactive Question-Answer System

This project provides a novel way to interact with a computer by using eye blink detection to answer questions. The system integrates various technologies such as face mesh for eye blink detection, a database to store questions and answers, and a UDP server-client setup for communication.

## Features

- **Blink Detection**: Utilizes OpenCV and MediaPipe to detect blinks and interpret them as user inputs.
- **Database Integration**: Connects to an SQL Server database to store and retrieve questions and answers.
- **Text-to-Speech**: Converts answers to speech using the `gTTS` library.
- **Voice Recognition**: Uses the `speech_recognition` library to capture and recognize spoken questions.
- **UDP Communication**: Implements a UDP server-client setup for inter-process communication.
- **AI Response**: Producing answers to reviews that are not in the database with Google artificial intelligence.


### Requirements

- Python 3.7 or higher(Recommended 3.10)
- OpenCV
- MediaPipe
- NumPy
- pypyodbc
- gTTS
- speech_recognition
- pypyodbc

## Usage

1. **Start the UDP Server**: This will handle incoming requests and send appropriate responses.

    ```bash
    python udp_server.py
    ```

2. **Run the Main Application**: This application captures voice input, detects eye blinks, and interacts with the user.

    ```bash
    python main.py
    ```

3. **Interact with the System**: Speak into the microphone to ask a question, and use eye blinks to select the response.


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.
