# Accessible Typing Trainer ⌨️🎧

A cross-platform, highly accessible typing tutor built with Python and PyQt6. This project is specifically engineered to be fully usable by visually impaired users, providing seamless integration with native screen readers and tactile audio feedback.

## ✨ Key Features

* **Universal Accessibility (TTS):** Native integration with screen readers across platforms (UniversalSpeech for NVDA/JAWS on Windows, and Speech-Dispatcher for Orca on Linux).
* **Tactile Audio Cues:** Real-time sound effects for correct keystrokes, errors, and lesson completion, reducing the reliance on verbose voice prompts.
* **Explorer Mode (Safe Discovery):** A dedicated mode for beginners to press any key and hear its name and finger placement. Features a "Safe Exit" system requiring three consecutive `Escape` presses to prevent accidental exits.
* **Guided Finger Prompts:** Step-by-step voice guidance telling the user exactly which finger to use for specific characters (Supports both English and Arabic layouts).
* **Advanced Typing Engine:** * Supports Character, Word, and Sentence modes.
    * Calculates **Net WPM** (Words Per Minute) and Accuracy by penalizing errors.
* **Lesson Editor:** Built-in interface to create, edit, and delete custom lessons or exams.
* **Bulletproof State Management:** JSON-based data storage for settings and results with built-in corruption shields and memory caching to minimize disk I/O.
* **Bilingual Support:** Default lessons and exams available in both English and Arabic.

## 🏗️ Architecture & Engineering

The project follows a clean **MVC / Service-Oriented Architecture** ensuring strict separation of concerns:
* `core/`: Contains the logical engines (`TypingEngine`, `ExplorerEngine`, `Statistics`).
* `services/`: Handles OS-level interactions (Audio, TTS engines, File I/O).
* `ui/`: Modular, reusable PyQt6 components and views managed by a `QStackedWidget` for single-page-application (SPA) flow.
* `models/`: Lightweight data structures using Python's `@dataclass`.
* `utils/`: Helper functions and a configured `RotatingFileHandler` for safe logging.

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MesterPerfect/typing_trainer.git
   cd typing_trainer
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Generate Audio Files (First Run Only):**
   ```bash
   python generate_sounds.py
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## ⌨️ Global Shortcuts

* `Enter` / `Return`: Start selected lesson.
* `Escape`: Return to the previous menu (or exit Explorer Mode with 3 presses).
* `F2`: Toggle Guided Voice Prompts.
* `F3`: Open Settings.
* `F4`: View Results.
* `F5 - F8`: Launch various Explorer Modes (Free, Arabic, English, Numbers).
* `F9`: Open Lesson Editor.

