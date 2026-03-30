# Accessible Typing Trainer ⌨️🎧

A cross-platform, highly accessible typing tutor built with Python and PySide6. This project is specifically engineered to be fully usable by visually impaired users, providing seamless integration with native screen readers, tactile audio feedback, and advanced TTS queuing.

---

## ✨ Key Features

### 🔊 Universal Accessibility (TTS)

* Native integration with screen readers across platforms:

  * **Windows:** UniversalSpeech (NVDA / JAWS)
  * **macOS:** AppleScript / VoiceOver
  * **Linux:** DBus / Speech-Dispatcher

### 🧠 Smart TTS Verbalization & Queuing

* Custom verbalizer ensures correct pronunciation of:

  * punctuation
  * math operators
  * Arabic diacritics (Tashkeel)
* Bypasses standard verbosity limitations
* Built-in queueing and debouncing to prevent overlapping speech during fast typing

### 🔍 Explorer Modes (Safe Discovery)

* Beginner-friendly modes to explore the keyboard:

  * Hear key names
  * Finger placement
  * Hardware function (modifiers, action keys)
* **Safe Exit System:** Requires 3 consecutive `Escape` presses to exit

### ✋ Guided Finger Prompts

* Step-by-step voice instructions
* Supports both Arabic and English keyboard layouts

### ⚡ Advanced Typing Engine

* Supports:

  * Character mode
  * Word mode
  * Sentence mode
* Calculates:

  * Net WPM (Words Per Minute)
  * Accuracy (with error penalties)

### 🔄 Smart Data Sync & Lesson Editor

* Built-in lesson editor
* "Smart Merge" algorithm:

  * Downloads new official lessons
  * Preserves user-created content

### ⬆️ Built-in OTA Updater

* Asynchronous update checker
* Screen-reader-friendly progress announcements
* Downloads updates from GitHub releases

### 🌍 Bilingual Support

* Full lesson coverage in:

  * English
  * Arabic
* Includes:

  * basic rows
  * numbers
  * punctuation
  * brackets
  * diacritics

---

## 🏗️ Architecture & Engineering

The project follows **Clean Architecture (MVC / Service-Oriented)** with a strong focus on SRP (Single Responsibility Principle) and performance.

### 📂 Project Structure

```text
core/       # TypingEngine, ExplorerEngine, Statistics
services/   # Audio, TTS, File I/O (with caching)
ui/         # PySide6 UI (SPA via QStackedWidget)
ui/typing/  # speech_handler, prompt_builder, verbalizer
models/     # @dataclass-based models
utils/      # Helpers + rotating logging system
```

### ⚙️ Engineering Highlights

* Decoupled logic for maintainability
* In-memory caching to reduce disk I/O
* Modular UI components
* RotatingFileHandler for safe logging

---

## 🚀 Installation & Usage

### 1️⃣ Clone the repository

```bash
git clone https://github.com/MesterPerfect/typing_trainer.git
cd typing_trainer
```

### 2️⃣ Create virtual environment & install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Generate audio files (first run only)

```bash
python generate_sounds.py
```

### 4️⃣ Run the application

```bash
python main.py
```

---

## ⌨️ Global Shortcuts

| Key            | Action                                          |
| -------------- | ----------------------------------------------- |
| Enter / Return | Start selected lesson                           |
| Escape         | Go back / Exit Explorer (3 presses)             |
| F2             | Toggle guided voice prompts                     |
| F3             | Open settings                                   |
| F4             | View results                                    |
| F5 – F8        | Explorer modes (Free, Arabic, English, Numbers) |
| F9             | Keyboard layout explorer / Lesson editor        |

### 📝 Editor Shortcuts

| Key      | Action      |
| -------- | ----------- |
| Ctrl + S | Save lesson |
| Ctrl + N | New lesson  |

---

## 🛠️ Command-Line Interface (CLI)

The application includes a flexible CLI for advanced users and developers.

### 📌 Basic Usage

```bash
python main.py [options]
```

### ⚙️ Available Options

#### 🔧 Logging Options

* `--log-level {DEBUG,INFO,WARNING,ERROR}`
* `--no-log-time`

#### 🧩 Application Options

* `--lang {en,ar}`
* `--no-tts`

### 💡 Examples

```bash
# Run with warnings only and clean logs
python main.py --log-level WARNING --no-log-time

# Launch in Arabic with TTS disabled
python main.py --lang ar --no-tts
```

---

## ❤️ Accessibility First

This project is built with accessibility as a **core principle**, not an afterthought. Every feature is designed to ensure a seamless experience for visually impaired users.

---

## 📄 License

*(Add your license here — e.g., MIT, GPL, etc.)*
