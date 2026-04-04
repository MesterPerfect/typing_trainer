import logging
from datetime import datetime, timezone
from typing import List, Dict, Any

try:
    from posthog import Posthog
    POSTHOG_AVAILABLE = True
except ImportError:
    POSTHOG_AVAILABLE = False

logger = logging.getLogger(__name__)

class TelemetryNetwork:
    """ Handles sending batched telemetry events to the remote PostHog server. """
    
    def __init__(self, api_key: str, host: str):
        self.api_key = api_key
        self.host = host
        self.client = None

        if POSTHOG_AVAILABLE and self.api_key:
            try:
                # Initialize PostHog client as per official documentation
                self.client = Posthog(project_api_key=self.api_key, host=self.host)
                logger.info("PostHog telemetry client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize PostHog client: {e}")
        elif not POSTHOG_AVAILABLE:
            logger.warning("PostHog library is not installed. Telemetry will remain strictly local.")

    def send_events(self, events: List[Dict[str, Any]]) -> bool:
        """
        Attempts to upload a batch of events to PostHog.
        Returns True if successful, False if network/client fails.
        """
        if not events:
            return True
            
        if not self.client:
            return False

        try:
            for event in events:
                # PostHog expects datetime objects for historical timestamps
                dt_timestamp = None
                ts = event.get("timestamp")
                if ts:
                    dt_timestamp = datetime.fromtimestamp(ts, tz=timezone.utc)

                # Send event using posthog.capture
                self.client.capture(
                    distinct_id=event.get("distinct_id", "unknown_user"),
                    event=event.get("event", "unknown_event"),
                    properties=event.get("properties", {}),
                    timestamp=dt_timestamp
                )
            
            # Force flush to ensure events are sent immediately
            self.client.flush()
            logger.info(f"Successfully uploaded {len(events)} telemetry events to PostHog.")
            return True
            
        except Exception as e:
            logger.error(f"Failed to upload telemetry events: {e}")
            return False
