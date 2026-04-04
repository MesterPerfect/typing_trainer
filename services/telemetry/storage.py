import os
import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TelemetryStorage:
    """ Handles saving and loading telemetry events to/from local disk. """
    
    def __init__(self, cache_file: str):
        self.cache_file = cache_file

    def save(self, events: List[Dict[str, Any]]):
        """ Writes the current event queue to the local JSON file. """
        if not events:
            return
            
        try:
            # Create a snapshot to prevent modification errors during saving
            queue_snapshot = list(events)
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(queue_snapshot, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save telemetry cache: {e}")

    def load(self) -> List[Dict[str, Any]]:
        """ Restores previously unsent events from the disk cache. """
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    events = json.load(f)
                logger.info(f"Loaded {len(events)} pending telemetry events from cache.")
                return events
            except Exception as e:
                logger.error(f"Failed to load telemetry cache: {e}")
        return []
