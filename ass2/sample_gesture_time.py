import numpy as np

GESTURE_TIME = 1.6

def random_gesture_times(duration: float, max_interval: float=1) -> None:
    time = 0
    gesture_times = []

    # gestures can start within duration, but end after -> (GESTURE_TIME *2) to avoid this
    while (time < duration - GESTURE_TIME):
        # random time from [end previous gesture, end previous gesture + max_interval)
        time_stamp = np.random.uniform(time, time + max_interval)
        gesture_times.append(time_stamp)
        time = time_stamp + GESTURE_TIME

    return gesture_times

def main():
    gesture_times = random_gesture_times(duration=30, max_interval=2)
    time_between_gestures = [gesture_times[idx] - gesture_times[idx - 1] - GESTURE_TIME
                             for idx in range(1, len(gesture_times))]

    print(gesture_times)
    print()
    print(time_between_gestures)

if __name__ == "__main__":
    main()
