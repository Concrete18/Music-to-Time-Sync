# standard library
import datetime as dt

# third-party imports
from rich.console import Console
from rich.theme import Theme
import pyautogui


# rich console
custom_theme = Theme(
    {
        "primary": "bold deep_sky_blue1",
        "secondary": "bold pale_turquoise1",
        # error
        "info": "dim cyan",
        "warning": "bold magenta",
        "danger": "bold red",
    }
)
console = Console(theme=custom_theme)


def input_time():
    """
    ph
    """
    while True:
        msg = "Input your time in this format 'Hour:Mininute PM/AM'"
        end_time = input(msg)
        formatted_time = end_time
        input(f"Is this time correct?\n{formatted_time}")


def input_custom():
    """
    ph
    """
    song_length = input("How long is the media?")

    end_time = input_time()

    return song_length, end_time


def start(song_length, end_time) -> None:
    """
    ph
    """
    pyautogui.press("playpause")


def main():
    console.print("Media to Time Sync\n", style="primary")

    song_length, end_time = None, None
    use_saved = input("Do you want to use the saved media length and end time?")
    if use_saved:
        pass
    else:
        song_length, end_time = input_custom()
    song_length = input("How long is the media?")

    start(song_length, end_time)


if __name__ == "__main__":
    main()
