import obspython as obs
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OBSController:
    def __init__(self):
        self.obs_data = None
        self.obs_data_lock = threading.Lock()
        self.obs_data_cond = threading.Condition(self.obs_data_lock)
        self.obs_data_available = False
        self.obs_data_thread = threading.Thread(target=self.obs_data_thread_func)
        self.obs_data_thread.daemon = True
        self.obs_data_thread.start()

    def obs_data_thread_func(self):
        while True:
            with self.obs_data_lock:
                while not self.obs_data_available:
                    self.obs_data_cond.wait()
                self.obs_data_available = False
                obs_data = self.obs_data
                self.obs_data = None
            # Process obs_data here

    def start_obs_data_feed(self):
        """Start the OBS data feed."""
        self.obs_data_feed = obs.obs_frontend_add_event_callback(self.obs_event)
        self.obs_data_feed_thread = threading.Thread(target=self.obs_data_feed_thread_func)
        self.obs_data_feed_thread.daemon = True
        self.obs_data_feed_thread.start()

    def stop_obs_data_feed(self):
        """Stop the OBS data feed."""
        if self.obs_data_feed is not None:
            obs.obs_frontend_remove_event_callback(self.obs_data_feed)
            self.obs_data_feed = None

    def obs_event(self, event):
        """Handle OBS events."""
        if event.obs_event_type == obs.OBS_EVENT_TYPE_STREAMING_STARTED:
            self.obs_data_feed_thread_func()
        elif event.obs_event_type == obs.OBS_EVENT_TYPE_STREAMING_STOPPED:
            self.stop_obs_data_feed()

    def obs_data_feed_thread_func(self):
        while True:
            with self.obs_data_lock:
                self.obs_data = obs.obs_frontend_get_streaming_stats()
                self.obs_data_available = True
                self.obs_data_cond.notify_all()

    @staticmethod
    def safe_execute(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error executing {func.__name__}: {str(e)}")
            raise

    @staticmethod
    def start_recording():
        """Start recording."""
        OBSController.safe_execute(obs.obs_frontend_recording_start)

    @staticmethod
    def stop_recording():
        """Stop recording."""
        OBSController.safe_execute(obs.obs_frontend_recording_stop)

    @staticmethod
    def toggle_source_visibility(source_name):
        """Toggle the visibility of a source."""
        source = obs.obs_get_source_by_name(source_name)
        if source is not None:
            current_visibility = obs.obs_source_enabled(source)
            obs.obs_source_set_enabled(source, not current_visibility)
            obs.obs_source_release(source)

    @staticmethod
    def adjust_audio_level(source_name, volume):
        """Adjust the audio level of a source."""
        source = obs.obs_get_source_by_name(source_name)
        if source is not None:
            obs.obs_source_set_volume(source, volume)
            obs.obs_source_release(source)

    @staticmethod
    def set_transition(transition_name):
        """Set the current scene transition."""
        transition = obs.obs_frontend_get_current_transition()
        obs.obs_frontend_set_current_transition(transition_name)
        obs.obs_source_release(transition)

def script_properties():
    props = obs.obs_properties_create()
    obs.obs_properties_add_button(props, "start_recording", "Start Recording", OBSController.start_recording)
    obs.obs_properties_add_button(props, "stop_recording", "Stop Recording", OBSController.stop_recording)
    return props