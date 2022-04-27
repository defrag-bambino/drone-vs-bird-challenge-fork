import argparse
import os
import tqdm
import cv2

# this function takes a video file and an output dir and writes the frames to the output dir
# it uses opencv to read the video file and extract the frames
# it then writes the frames to the output dir
def vid_to_frames(vid_file, output_dir, image_name_prefix):
    # check if output dir exists, if not create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # save a outfile list
    outfile_list = []

    # read the video file
    vidcap = cv2.VideoCapture(vid_file)

    # get the total number of frames
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    # get the fps
    fps = vidcap.get(cv2.CAP_PROP_FPS)

    # get the width and height of the video
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("Converting video of width and height: " + str(width) + " and " + str(height) + " and fps: " + str(fps) + " and total frames: " + str(total_frames) + " to frames in " + output_dir) 

    # loop thorugh all the frames
    for i in tqdm.tqdm(range(total_frames)):
        # extract the frame
        success, image = vidcap.read()

        # check if the frame was extracted successfully
        if success:
            image_path = os.path.join(output_dir, image_name_prefix + "_frame%d.jpg" % i)
            # write the frame to the output dir
            cv2.imwrite(image_path, image)
            outfile_list.append(image_path)
        else:
            # if the frame was not extracted successfully, break the loop
            break

    # return the list of outfile paths
    return outfile_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a video to frames")
    parser.add_argument("--input_video", help="Input video file")
    parser.add_argument("--output_dir", help="Output directory for frames")
    parser.add_argument("--image_name_prefix", help="Prefix for the image name")
    args = parser.parse_args()

    # call the vid_to_frames function
    vid_to_frames(args.input_video, args.output_dir, args.image_name_prefix)