from flask_opencv_streamer.streamer import Streamer
import face_recognition
import cv2
import numpy as np
from os import mkdir, path, listdir, system, rmdir
import uuid
import logging
# import .settings as SETTING
from elasticsearch import Elasticsearch, ElasticsearchException
from datetime import datetime

from pprint import pprint

def streamer():
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []

    faces_acquired = []
    process_this_frame = True

    frame_red = 0, 0, 255
    frame_green = 0, 255, 0
    frame_blue = 255, 0, 0

    dir_path = path.dirname(path.realpath(__file__))
    acquired_faces_path = path.join(dir_path, "acquired_faces")

    port = 3030
    require_login = False

    #
    streamer = Streamer(port, require_login)


    # Create target Directory
    try:
        mkdir(acquired_faces_path)
        print("[INFO] Created acquired faces directory")
    except FileExistsError:
        print("[INFO] Acquired faces directory already exists... SKIPPING")

    # Open video device 0
    video_capture = cv2.VideoCapture(0)

    while True:
        main_stream(streamer, video_capture)

        if not streamer.is_streaming:
            streamer.start_streaming()

        cv2.waitKey(30)

def main_stream(streamer, video_capture):
    # temporary placing some varialbes definition here, move to settings later on
    frame_red = 0, 0, 255
    frame_green = 0, 255, 0
    frame_blue = 255, 0, 0

    # Load a second sample picture and learn how to recognize it.
    dir_path = path.dirname(path.realpath(__file__))
    Linus_Torvalds_image = face_recognition.load_image_file(dir_path + "/../faces/Linus_Torvalds.jpg")
    # Linus_Torvalds_image = face_recognition.load_image_file(dir_path + "/acquired_faces/4c46e336-8a3d-11e9-89b0-acde48001122.jpg")
    Linus_Torvalds_encoding = face_recognition.face_encodings(Linus_Torvalds_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        Linus_Torvalds_encoding
    ]
    known_face_names = [
        "Linus Torvalds"
    ]



    _, frame = video_capture.read()

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]


    process_this_frame = True
    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        # print([i[0] for i in known_face_encodings])

        for face_encoding in face_encodings:

            name = "Unknown"
            frame_color = frame_red

            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                frame_color = frame_green

                if face_recognition.compare_faces(faces_acquired, face_encoding):
                    frame_color = frame_blue
            else:
                # Face not recognized
                print('[INFO] Acquiring face')
                name = str(uuid.uuid1())
                frame_color = frame_red
                print(face_encoding)
                # save_data(face_encoding, name)
                save_data(face_encoding, name, frame)

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (frame_color), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (frame_color), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)



    streamer.update_frame(frame)


# Save image locally and on Elasticsearch
def save_data(face_encoding, name, frame):
    print('mock saving')
    # known_face_encodings.append(face_encoding)
    # known_face_names.append(name)
    # faces_acquired.append(face_encoding)
    #
    # # Savingimage locally
    # filename = path.join(acquired_faces_path, name)+".jpg"
    # pprint(filename)
    # cv2.imwrite(filename, frame)
    #
    # # Storing face point on Elasticsearch
    # encode_np_array = np.array(face_encoding)
    # try :
    #     es.index(   index=SETTING.ELASTICSEARCH_INDEX,
    #                 body={
    #                     'timestamp': datetime.now(),
    #                     'name': name,
    #                     'face_encoding': encode_np_array.tolist(),
    #                 }
    #             )
    #
    # except ElasticsearchException as es1:
    #     print('error es')


if __name__ == "__main__":
    print("main")
    streamer()
