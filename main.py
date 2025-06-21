# standard library
import datetime as dt
import json, time

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


def debug(song_length_delta, end_time):
    print("\nSong Length", song_length_delta)

    if isinstance(end_time, dt.datetime):
        print("End Time", end_time.strftime(r"%Y-%m-%d %H:%M:%S"))
        if dt.datetime.today().time() > end_time.time():
            print("Time has been passed")
        else:
            print("Time has not been passed")
    else:
        print("Invalid End Time")


def get_song_delta(media_length: str) -> dt.timedelta:
    hours, minutes, seconds = media_length.split(":")
    return dt.timedelta(
        hours=int(hours),
        minutes=int(minutes),
        seconds=int(seconds),
    )


def str_to_datetime(string: str) -> dt.datetime:
    return dt.datetime.strptime(string, "%I:%M:%S %p")


def load_saved() -> tuple[dt.timedelta | None, dt.datetime | None]:
    """
    ph
    """
    config_path = "saved_data.json"
    with open(config_path) as json_file:
        config_data = json.load(json_file)

    end_time_str = config_data.get("end_time", "")
    song_length_str = config_data.get("song_length", "")
    if not isinstance(end_time_str, str) or not isinstance(song_length_str, str):
        return None, None

    end_time = str_to_datetime(end_time_str)
    song_length_delta = get_song_delta(song_length_str)
    return song_length_delta, end_time


def if_yes(msg):
    response = input(msg)
    valid_yes = ["yes", "y", "yeah", "ya"]
    return response.lower() in valid_yes


def input_time():
    """
    ph
    """
    while True:
        msg = "\nInput your time in this format 'Hours:Minutes:Seconds PM/AM'\n"
        end_time_str = input(msg)
        try:
            end_time = dt.datetime.strptime(end_time_str, "%I:%M %p")
        except TypeError:
            print("That is not a valid time format")
            continue
        formatted_time = end_time
        if input(f"Is this time correct?\n{formatted_time}"):
            break


def input_custom():
    """
    ph
    """
    song_length = input("How long is the media/when do you want the time to sync to?")

    end_time = input_time()

    return song_length, end_time


def start(song_length_delta, end_time) -> None:
    """
    ph
    """
    start_time = end_time - song_length_delta

    STR_FORMAT = r"%I:%M:%S %p"
    start_time_str = start_time.strftime(STR_FORMAT)
    end_time_str = end_time.strftime(STR_FORMAT)
    console.print(f"\nStarting song at {start_time_str}")
    console.print(f"The Song will end at {end_time_str}")

    if start_time.time() < dt.datetime.now().time():
        print("Required start time has already passed")

    print()
    try:
        while True:
            cur_datetime = dt.datetime.now()
            if start_time.time() < cur_datetime.time():
                break
            time.sleep(1)
            str_time = cur_datetime.strftime(STR_FORMAT)
            print(f"\rCurrent Time: {str_time}", end="", flush=True)
        pyautogui.press("playpause")
        print("\nPlaying Media Now")
    except KeyboardInterrupt:
        print("\n\nCancelled Media to Time Sync")


def main():
    console.print("Media to Time Sync", style="primary")

    song_length_delta, end_time = None, None
    # use_saved = if_yes("\nDo you want to use the saved media length and end time?\n")
    use_saved = True
    if use_saved:
        song_length_delta, end_time = load_saved()
    else:
        song_length_delta, end_time = input_custom()

    start(song_length_delta, end_time)


if __name__ == "__main__":
    main()
