import sys
import os
import cv2
import numpy as np


def parse_args():

    if len(sys.argv) is not 4:
        print('3 arguments are required. \nThe path to the video file, '
              'the macro block size, and the motion threshold.')
        sys.exit(1)

    video_file = sys.argv[1]

    macro_block_size = sys.argv[2]

    if not macro_block_size.isdigit():
        print('macro block size must be a positive integer - using default [5]')
        macro_block_size = 5
    else:
        macro_block_size = int(macro_block_size)

    motion_threshold = sys.argv[3]

    if not motion_threshold.isdigit():
        print('motion threshold must be a positive integer - using default [25]')
        motion_threshold = 25
    else:
        motion_threshold = int(motion_threshold)

    return video_file, macro_block_size, motion_threshold


def get_output_file_path(video_file_path):

    path_to_folder = os.path.dirname(video_file_path)
    file_name = os.path.basename(video_file_path)
    output_file_name = os.path.splitext(file_name)[0] + '_out.mkv'

    return os.path.join(path_to_folder, output_file_name)


def calculate_ssd(block1, block2):
    return np.sqrt(np.sum((block1 - block2) ** 2))


def find_best_reference_block_match(cur_block, current_frame_row, current_frame_col, macro_block_size, reference_frame):

    smallest_ssd = sys.maxsize
    x_coord = -1
    y_coord = -1

    for row in range(current_frame_row - macro_block_size, current_frame_row + macro_block_size * 2, macro_block_size):
        for col in range(current_frame_col - macro_block_size, current_frame_col + macro_block_size * 2, macro_block_size):

            ref_block = reference_frame[row: row + macro_block_size, col: col + macro_block_size]

            if cur_block.shape == ref_block.shape:

                ssd = calculate_ssd(cur_block, ref_block)

                if ssd < smallest_ssd:
                    smallest_ssd = ssd
                    x_coord = col + int(round(macro_block_size / 2))
                    y_coord = row + int(round(macro_block_size / 2))

    return smallest_ssd, x_coord, y_coord


def draw_point(img, x, y):
    cv2.circle(img, (x, y), 1, (0, 0, 255), -1)


def main():

    video_file_path, macro_block_size, motion_threshold = parse_args()

    video_capture = cv2.VideoCapture(video_file_path)

    if not video_capture.isOpened():
        print('failed to open video')
        sys.exit(1)

    output_file_path = get_output_file_path(video_file_path)

    video_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    video_writer = cv2.VideoWriter(output_file_path,
                                   cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                   video_fps,
                                   (video_width, video_height))

    current_frame_available, current_frame = video_capture.read()

    if not current_frame_available:
        print('failed to read frames from video')
        sys.exit(1)

    reference_frame_available, reference_frame = video_capture.read()

    while reference_frame_available:

        current_frame_drawable = current_frame

        for row in range(0, video_height, macro_block_size):
            for col in range(0, video_width, macro_block_size):

                cur_block = current_frame[row: row + macro_block_size, col: col + macro_block_size]

                ssd, x_coord, y_coord = find_best_reference_block_match(cur_block,
                                                                        row, col,
                                                                        macro_block_size,
                                                                        reference_frame)

                if motion_threshold <= ssd:
                    draw_point(current_frame_drawable, x_coord, y_coord)

        cv2.imshow('Motion Estimation', current_frame_drawable)

        video_writer.write(current_frame_drawable)

        if cv2.waitKey(30) & 0xff == ord('q'):
            break

        current_frame = np.copy(reference_frame)
        reference_frame_available, reference_frame = video_capture.read()

    video_capture.release()
    video_writer.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
