import os
import uuid
import time
import platform
import threading
import logging
from typing import Dict, Any, List

from .storage import TelemetryStorage
from .network import TelemetryNetwork

logger = logging.getLogger(__name__)

# Official PostHog Credentials
POSTHOG_API_KEY = "phc_y2RBBdpRHnyQtCNUUi6v7bz7X6XPrR3xQTF7zjA9Kogk"
POSTHOG_HOST = "https://us.i.posthog.com"

class TelemetryService:
    """
    Main service orchestrating event tracking, storage, and network transmission.
    """
    def __init__(self, user_data_dir: str, app_version: str, language: str = "en", screen_reader: str = "Unknown", enabled: bool = True):
        self.enabled = enabled
        
        cache_file = os.path.join(user_data_dir, "telemetry_events.json")
        client_id_file = os.path.join(user_data_dir, "client_id.txt")
        
        self.storage = TelemetryStorage(cache_file)
        self.network = TelemetryNetwork(api_key=POSTHOG_API_KEY, host=POSTHOG_HOST)
        
        self.client_id = self._init_client_id(client_id_file)
        self.global_properties = self._gather_global_properties(app_version, language, screen_reader)
        
        self._lock = threading.Lock()
        self.events_queue: List[Dict[str, Any]] = self.storage.load()
        self.session_start_time = 0.0

        # Attempt to flush any offline events stored from previous sessions
        self.flush_async()

    def _init_client_id(self, file_path: str) -> str:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read().strip()
            except Exception as e:
                logger.error(f"Could not read client ID: {e}")
        
        new_id = str(uuid.uuid4())
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_id)
        except Exception as e:
            logger.error(f"Could not save new client ID: {e}")
        return new_id

    def _gather_global_properties(self, app_version: str, language: str, screen_reader: str) -> Dict[str, Any]:
        return {
            "os_platform": platform.system(),
            "os_release": platform.release(),
            "os_build": platform.version(),
            "app_version": app_version,
            "python_version": platform.python_version(),
            "language": language,
            "screen_reader": screen_reader
        }

    def track(self, event_name: str, properties: Dict[str, Any] = None):
        if not self.enabled:
            return

        event_data = {
            "event": event_name,
            "distinct_id": self.client_id,
            "timestamp": int(time.time()),
            "properties": {
                **self.global_properties,
                **(properties or {})
            }
        }
        
        with self._lock:
            self.events_queue.append(event_data)
        logger.debug(f"Telemetry event tracked: {event_name}")
        
        threading.Thread(target=self._save_cache, daemon=True).start()

    def start_session(self):
        self.session_start_time = time.time()
        self.track("app_started")

    def end_session(self):
        if self.session_start_time > 0:
            duration = int(time.time() - self.session_start_time)
            self.track("session_ended", {"duration_seconds": duration})
            
        self._save_cache()
        # Attempt one last flush before exit (synchronously to ensure it finishes)
        self._flush_sync()

    def flush_async(self):
        """ Spawns a background thread to upload events without blocking the UI. """
        if not self.enabled:
            return
        with self._lock:
            if not self.events_queue:
                return
        threading.Thread(target=self._flush_sync, daemon=True).start()

    def _flush_sync(self):
        """ Core upload logic. Clears local queue if network upload succeeds. """
        with self._lock:
            if not self.events_queue:
                return
            events_to_send = list(self.events_queue)
            
        success = self.network.send_events(events_to_send)
        if success:
            with self._lock:
                # Remove only the events that were successfully sent
                del self.events_queue[:len(events_to_send)]
            self._save_cache()

    def _save_cache(self):
        with self._lock:
            data_to_save = list(self.events_queue)
        self.storage.save(data_to_save)
