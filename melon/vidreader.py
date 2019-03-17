import cv2
import numpy as np


def read(video_file_path):
    # Create a VideoCapture object and read from input file
    capture = cv2.VideoCapture(video_file_path)
    fps = capture.get(cv2.CAP_PROP_FPS)
    num_frames = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = float(num_frames) / float(fps) * 1000  # in ms

    # input
    interval = 500

    m = int(duration // interval) + 1
    height = capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = capture.get(cv2.CAP_PROP_FRAME_WIDTH)

    X = np.empty(shape=(m, int(height), int(width), 3), dtype=np.float32)

    nr_frame = 0

    capture.set(cv2.CAP_PROP_POS_MSEC, 0)
    success, frame = capture.read()
    while success:
        # path_out = "~/Desktop/frames/"
        # cv2.imwrite(path_out + "frame%d.jpg" % nr_frame, frame)
        X[nr_frame, :, :, :] = frame.astype('float32')  # / 255.
        nr_frame += 1
        current_pos = nr_frame * interval
        capture.set(cv2.CAP_PROP_POS_MSEC, current_pos)
        success, frame = capture.read()

    # the_frames = np.array(frames)
    print(X.shape)


def main():
    path = "~/Desktop/sample.mp4"
    read(path)


if __name__ == "__main__":
    main()
