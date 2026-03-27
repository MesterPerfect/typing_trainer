import time

class TypingStatistics:
    def __init__(self):
        self.start_time = 0.0
        self.end_time = 0.0
        self.total_keystrokes = 0
        self.errors = 0
        self.is_running = False

    def start(self):
        """ Start the typing timer. """
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True

    def stop(self):
        """ Stop the typing timer. """
        if self.is_running:
            self.end_time = time.time()
            self.is_running = False

    def record_keystroke(self, is_correct: bool):
        """ Record a single keystroke and update error count if needed. """
        self.total_keystrokes += 1
        if not is_correct:
            self.errors += 1

    def get_elapsed_time(self) -> float:
        """ Calculate elapsed time in seconds. """
        if not self.is_running and self.start_time == 0.0:
            return 0.0
        if self.is_running:
            return time.time() - self.start_time
        return self.end_time - self.start_time

    def get_wpm(self) -> int:
        """ 
        Calculate Net Words Per Minute (Net WPM). 
        Standard formula: ((Total Keystrokes / 5) - Errors) / Time in Minutes 
        """
        minutes = self.get_elapsed_time() / 60.0
        if minutes == 0 or self.total_keystrokes == 0:
            return 0
        
        gross_wpm = (self.total_keystrokes / 5.0) / minutes
        net_wpm = gross_wpm - (self.errors / minutes)
        
        # Ensure WPM does not drop below 0
        return max(0, int(net_wpm))

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
            "accuracy": self.get_accuracy(),
            "errors": self.errors,
            "time": round(self.get_elapsed_time(), 1)
        }
