import time

class TypingStatistics:
    def __init__(self):
        self.start_time = 0.0
        self.end_time = 0.0
        self.total_keystrokes = 0
        self.errors = 0
        self.is_running = False
        
        # Pause / Resume support
        self.is_paused = False
        self.pause_start_time = 0.0
        self.total_paused_duration = 0.0

    def start(self):
        """ Start the typing timer. """
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            self.is_paused = False
            self.total_paused_duration = 0.0

    def stop(self):
        """ Stop the typing timer. """
        if self.is_running:
            if self.is_paused:
                self.resume()
            self.end_time = time.time()
            self.is_running = False

    def pause(self):
        """ Pause the typing session timer. """
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.pause_start_time = time.time()

    def resume(self):
        """ Resume the typing session timer. """
        if self.is_running and self.is_paused:
            self.total_paused_duration += time.time() - self.pause_start_time
            self.pause_start_time = 0.0
            self.is_paused = False

    def toggle_pause(self) -> bool:
        """ Toggles between pause and resume. Returns True if now paused, False otherwise. """
        if self.is_paused:
            self.resume()
            return False
        else:
            self.pause()
            return True

    def record_keystroke(self, is_correct: bool):
        """ Record a single keystroke and update error count if needed. """
        if self.is_paused:
            return
        self.total_keystrokes += 1
        if not is_correct:
            self.errors += 1

    def get_elapsed_time(self) -> float:
        """ Calculate elapsed active time in seconds (excluding paused periods). """
        if not self.is_running and self.start_time == 0.0:
            return 0.0

        current_paused = 0.0
        if self.is_paused and self.pause_start_time > 0.0:
            current_paused = time.time() - self.pause_start_time

        if self.is_running:
            raw_elapsed = time.time() - self.start_time
        else:
            raw_elapsed = self.end_time - self.start_time

        active_time = raw_elapsed - (self.total_paused_duration + current_paused)
        return max(0.0, active_time)

    def get_wpm(self) -> int:
        """ 
        Calculate Net Words Per Minute (Net WPM). 
        Standard formula: ((Total Keystrokes / 5) - Errors) / Time in Minutes.
        Smoothed for the first 2 seconds to avoid erratic initial spikes.
        """
        elapsed = self.get_elapsed_time()
        if elapsed < 2.0 or self.total_keystrokes == 0:
            return 0
        
        minutes = elapsed / 60.0
        gross_wpm = (self.total_keystrokes / 5.0) / minutes
        net_wpm = gross_wpm - (self.errors / minutes)
        
        return max(0, int(round(net_wpm)))

    def get_cpm(self) -> int:
        """ 
        Calculate Net Characters Per Minute (Net CPM).
        Standard formula: (Total Keystrokes - Errors) / Time in Minutes.
        """
        elapsed = self.get_elapsed_time()
        if elapsed < 2.0 or self.total_keystrokes == 0:
            return 0
            
        minutes = elapsed / 60.0
        correct_chars = max(0, self.total_keystrokes - self.errors)
        net_cpm = correct_chars / minutes
        return max(0, int(round(net_cpm)))

    def get_accuracy(self) -> float:
        """ Calculate typing accuracy percentage. """
        if self.total_keystrokes == 0:
            return 100.0
        
        correct = self.total_keystrokes - self.errors
        accuracy = (correct / self.total_keystrokes) * 100.0
        return round(accuracy, 1)

    def get_current_stats(self) -> dict:
        """ Return all statistics as a dictionary. """
        return {
            "wpm": self.get_wpm(),
            "cpm": self.get_cpm(),
            "accuracy": self.get_accuracy(),
            "errors": self.errors,
            "time": round(self.get_elapsed_time(), 1),
            "is_paused": self.is_paused
        }
