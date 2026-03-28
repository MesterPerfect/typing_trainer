import argparse

def parse_arguments():
    """ Parse command line arguments and return the parsed args object. """
    parser = argparse.ArgumentParser(
        description="Typing Trainer - Accessible typing tutor",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Logging Options Group
    log_group = parser.add_argument_group('Logging Options')
    log_group.add_argument(
        "--log-level", 
        type=str, 
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Override the default logging level"
    )
    log_group.add_argument(
        "--no-log-time", 
        action="store_true",
        help="Remove timestamps from log output"
    )

    # Application Options Group
    app_group = parser.add_argument_group('Application Options')
    app_group.add_argument(
        "--lang", 
        type=str, 
        choices=["en", "ar"],
        help="Force UI language (overrides user settings)"
    )
    app_group.add_argument(
        "--no-tts", 
        action="store_true",
        help="Disable Text-to-Speech engine completely"
    )

    return parser.parse_args()
