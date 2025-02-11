# Lingually

Lingually is a language-learning application built using Tkinter and integrates with Mistral AI to provide vocabulary management and profile-based language tracking.

## Features

- **Multi-profile support**: Create and switch between different language-learning profiles.
- **Vocabulary Management**: Add new words to your vocabulary and generate definitions using AI.
- **Custom Language Selection**: Choose learning and native languages for personalized experience.
- **User-Friendly UI**: Simple and intuitive graphical interface with easy navigation.
- **Configurable Display Settings**: Adjust the application’s resolution as needed.

## Installation

### Prerequisites

Ensure you have Python installed on your system.

### Steps

1. Clone the repository:
   ```
   git clone https://github.com/Mandelbroetchen/Lingually.git
   cd Lingually
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the environment variables:

   Create a `.env` file in the project root and add your Mistral AI API key:
   ```
   API_KEY=your_mistral_api_key
   ```

5. Run the application:
   ```
   python3 app.py
   ```

## Usage

- **Creating a Profile**: Upon first launch, you will be prompted to create a profile, selecting your preferred languages.
- **Adding Words**: Use the "Add Word" feature to store new vocabulary words and generate definitions.
- **Switching Profiles**: Navigate to the profile menu to switch between different user profiles.
- **Configuring Display Settings**: Adjust the resolution under the "Display" menu.

## File Structure

- `app.py` - Main application file that initializes the UI and manages user interaction.
- `utilities.py` - Contains helper functions such as contrast color calculations and language selection dialogs.
- `AddWordWin.py` - Handles adding new vocabulary words.
- `CreateProfileWin.py` - Manages profile creation.
- `SwitchProfileWin.py` - Allows switching between user profiles.
- `Toplevel.py` - A base class for modal windows.

## Contributing

1. Fork the repository.
2. Create a new branch: 
   ```
   git checkout -b feature-branch
   ```
3. Make your changes and commit:
   ```
   git commit -m "Description of changes"
   ```
4. Push the branch:
   ```
   git push origin feature-branch
   ```
5. Open a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Uses **Mistral AI** for language model integration.
- Built with **Tkinter** for the GUI.
