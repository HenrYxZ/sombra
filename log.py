from datetime import datetime


DATETIME_FORMAT = "%H:%M:%S %d-%m-%Y"


def start_of_animation():
    now = datetime.now()
    datetime_str = now.strftime(DATETIME_FORMAT)
    print("Started the animation at: {}".format(datetime_str))

def end_of_animation():
    now = datetime.now()
    datetime_str = now.strftime(DATETIME_FORMAT)
    print("Ended the animation at: {}".format(datetime_str))