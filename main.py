"""VideoSlim - Video compression tool using FFmpeg.

Simple wrapper that delegates to the transcoding module.
This is the main entry point for the application.
"""

import transcoding


def main() -> None:
    """Main entry point - delegates to transcoding module."""
    transcoding.main()


if __name__ == "__main__":
    main()