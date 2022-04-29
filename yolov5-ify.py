from ast import parse
import os
import argparse
import cv2
import tqdm

from vid_to_frames import vid_to_frames




if __name__ == "__main__":
    # parse the args using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--videos_path", type=str, help="Path to the videos folder")
    parser.add_argument("--output_path", type=str, help="Path to the output folder. Will be created if it doesn't exist")
    parser.add_argument("--annotations_path", type=str, help="Path to the annotations folder")
    args = parser.parse_args()

    # normalize the paths
    vids_dir = os.path.normpath(args.videos_path)
    out_dir_imgs = os.path.join(os.path.normpath(args.output_path), "images")
    out_dir_lbls = os.path.join(os.path.normpath(args.output_path), "labels")
    annots_dir = os.path.normpath(args.annotations_path)

    #check if all the dirs exist, create the output dirs if they doesnt exist
    if not os.path.exists(vids_dir):
        print("Videos directory does not exist")
        exit()
    if not os.path.exists(out_dir_imgs):
        os.makedirs(out_dir_imgs, exist_ok=True)
    if not os.path.exists(out_dir_lbls):
        os.makedirs(out_dir_lbls, exist_ok=True)
    if not os.path.exists(annots_dir):
        print("Annotations directory does not exist")
        exit()

    # get the list of video files, they all have different file formats
    vid_files = [os.path.join(vids_dir, f) for f in os.listdir(vids_dir)]

    # loop through all the video files
    for vid_file in tqdm.tqdm(vid_files):
        # get the name of the video file and split away the extension and the path
        vid_name = os.path.basename(vid_file)
        vid_name_no_ext = os.path.splitext(vid_name)[0]
        # get the name of the corresponding annotations file
        annot_file = os.path.join(annots_dir, vid_name_no_ext + ".txt")
        # check if the annotations file exists
        if not os.path.exists(annot_file):
            print("Annotations file does not exist for video: " + vid_name)
            continue

        # get the list of frames from the video file
        frame_urls = vid_to_frames(os.path.join(vids_dir, vid_file), out_dir_imgs, vid_name_no_ext)
        # get the list of labels from the annotations file, the are line by line for each frame in the format:
        # framenum num_objs_in_frame obj1_x obj1_y obj1_w obj1_h obj1_class ...
        labels = [line.replace("\n", "") for line in open(annot_file, "r").readlines()]

        # check if the number of frames and labels are the same
        if len(frame_urls) != len(labels):
            print("Number of frames and labels are not the same for video: " + vid_name)
            continue

        # loop through all the labels
        for i, label in enumerate(labels):
            # get the number of objects in the frame
            num_objs = int(label.split(" ")[1])

            # create the label txt file for the frame, by replacing the 'images' in the frame_url[i] with 'labels' and replacing the extension with '.txt'
            lbl_file = os.path.join(out_dir_lbls, os.path.basename(frame_urls[i]).replace("images", "labels").replace(".jpg", ".txt"))

            # load the corresponding frame as an image
            img = cv2.imread(frame_urls[i])

            # loop through all the objects in the frame
            for obj in range(num_objs):
                # get the coordinates of the object and normalize them to image width and height
                x = int(label.split(" ")[2 + 5 * obj]) / img.shape[1]
                y = int(label.split(" ")[3 + 5 * obj]) / img.shape[0]
                w = int(label.split(" ")[4 + 5 * obj]) / img.shape[1]
                h = int(label.split(" ")[5 + 5 * obj]) / img.shape[0]
                # get the class of the object
                cls = label.split(" ")[6 + 5 * obj]
                if cls != "drone":
                    print("non-drone class found:", cls)

                # write the object to the label file in the format: cls,  x_center, y_center, width, height
                with open(lbl_file, "a") as f:
                    f.write("0 " + str(x + w / 2) + " " + str(y + h / 2) + " " + str(w) + " " + str(h) + "\n")







