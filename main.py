"""VideoSlim - Video compression tool using FFmpeg.

Entry point that supports both CLI and GUI modes.
"""

import sys
import transcoding


def main() -> None:
    """Main entry point - CLI or GUI based on arguments."""
    # If no arguments, launch GUI
    if len(sys.argv) == 1:
        try:
            import gui
            gui.main()
        except ImportError:
            print("Error: tkinter GUI not available")
            print("Run with --help for command-line usage")
            sys.exit(1)
    else:
        # CLI mode
        transcoding.main()


if __name__ == "__main__":
    main()