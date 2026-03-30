import subprocess
import threading
import queue
import logging
from .base import BaseTTS

logger = logging.getLogger(__name__)

class MacOSTTS(BaseTTS):
    def __init__(self):
        self.available = True
        self.speech_queue = queue.Queue()
        self.current_process = None
        
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def speak(self, text: str, interrupt: bool = False):
        if interrupt:
            self.stop()
            with self.speech_queue.mutex:
                self.speech_queue.queue.clear()
        self.speech_queue.put(text)

    def speak_char(self, char: str):
        if not char:
            return

        if char == " ":
            self.speak("space", interrupt=True)
        else:
            self.speak(char, interrupt=True)

    def stop(self):
        # Terminate the 'say' process if it is currently running
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
            except Exception:
                pass

    def _is_voiceover_running(self) -> bool:
        try:
            # Check if the VoiceOver process is active in the system
            output = subprocess.check_output(
                ['osascript', '-e', 'tell application "System Events" to (name of processes) contains "VoiceOver"'],
                text=True,
                stderr=subprocess.DEVNULL
            )
            return "true" in output.strip().lower()
        except Exception:
            return False

    def _process_queue(self):
        while True:
            text = self.speech_queue.get()
            if text is None:
                break
                
            try:
                if self._is_voiceover_running():
                    # Escape quotes and backslashes for AppleScript execution
                    escaped_text = text.replace('\\', '\\\\').replace('"', '\\"')
                    script = f'tell application "VoiceOver" to output "{escaped_text}"'
                    
                    # Execute the AppleScript to send speech directly to VoiceOver
                    subprocess.run(
                        ['osascript', '-e', script], 
                        check=True, 
                        capture_output=True, 
                        text=True
                    )
                else:
                    # Fallback to the native 'say' command if VoiceOver is off
                    self.current_process = subprocess.Popen(['say', text])
                    self.current_process.wait()
                    
            except subprocess.CalledProcessError as e:
                # Fallback to 'say' if AppleScript fails
                logger.debug(f"VoiceOver AppleScript failed, falling back to 'say'. Error: {e.stderr}")
                self.current_process = subprocess.Popen(['say', text])
                self.current_process.wait()
            except Exception as e:
                logger.error(f"macOS TTS error: {e}")
            
            self.speech_queue.task_done()

    def shutdown(self):
        self.stop()
        self.speech_queue.put(None)
        if self.worker_thread.is_alive():
            self.worker_thread.join(timeout=2)
