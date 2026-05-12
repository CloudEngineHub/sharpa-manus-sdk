import os
import sys
import time

# import sharpa.so from SharpaWaveSDK python folder
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../python"))

from sharpa import SharpaWaveManager


def auto_detect_hand():
    print("Searching for devices...")
    manager = SharpaWaveManager.get_instance()
    time.sleep(1)

    while True:
        devices = manager.get_all_device_sn()
        if devices:
            print(f"Device found: {devices[0]}")
            return manager.connect(devices[0])
        print("No available devices found")
        time.sleep(1)


def main():
    hand = None
    started = False
    try:
        hand = auto_detect_hand()
        if hand is None:
            print("Failed to connect device.")
            return

        hand.start()
        started = True
        print("Reading joint angles every 1 second, Ctrl+C to stop.")

        while True:
            error, angles = hand.get_joint_position_degree()
            if error.code != 0:
                print(f"Read failed: {error.message}")
            else:
                print(",".join(f"{angle:.2f}" for angle in angles))
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExit by Ctrl+C.")
    finally:
        if hand is not None and started:
            hand.stop()
        SharpaWaveManager.get_instance().disconnect_all()
        print("Disconnected all devices.")


if __name__ == "__main__":
    main()
