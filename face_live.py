import face_recognition
import cv2
import numpy as np
from os import mkdir, path, listdir, system
import uuid


# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a second sample picture and learn how to recognize it.
dir_path = path.dirname(path.realpath(__file__))
Linus_Torvalds_image = face_recognition.load_image_file(dir_path + "/faces/Linus_Torvalds.jpg")
Linus_Torvalds_encoding = face_recognition.face_encodings(Linus_Torvalds_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    Linus_Torvalds_encoding
]
known_face_names = [
    "Linus Torvalds"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []

faces_acquired = []
process_this_frame = True

frame_red = 0, 0, 255
frame_green = 0, 255, 0
frame_blue = 255, 0, 0

# Create target Directory
acquired_faces_path = path.join(dir_path, "acquired_faces")
try:
    mkdir(acquired_faces_path)
    print("[INFO] Created acquired faces directory")
except FileExistsError:
    print("[INFO] Acquired faces directory already exists... SKIPPING")

def save_data(face_encoding, name):
    known_face_encodings.append(face_encoding)
    known_face_names.append(name)
    faces_acquired.append(face_encoding)

    filename = path.join(acquired_faces_path, name)+".jpg"
    cv2.imwrite(filename, frame)

def preload_data(acquired_faces_path):
    faces = []
    names = []
    for face in listdir(acquired_faces_path):
        face_path = path.join(acquired_faces_path, face)
        if path.isfile(face_path):

            name = path.splitext(face)
            print('1')
            face_image = face_recognition.load_image_file(face_path)
            print('2')
            face_encoding = face_recognition.face_encodings(face_image)[0]
            faces.append(face_encoding)
            names.append(name[0])

    return faces, names

preload_data = preload_data(acquired_faces_path)
[known_face_encodings.append(name) for name in preload_data[0]]
[known_face_names.append(name) for name in preload_data[1]]

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

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
                save_data(face_encoding, name)

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

    # Display the resulting image
    # cv2.namedWindow('Video', frame)
    cv2.imshow('Video', frame)
    cv2.moveWindow('Video', 20, 20)
    system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "python" to true' ''') # To make window active

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
