import face_recognition
import cv2
import os
import time
import sekurrity
# This is a super simple (but slow) example of running face recognition on live video from your webcam.
# There's a second example that's a little more complicated but runs faster.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
# obama_image = face_recognition.load_image_file("Andrew_Tio.jpg")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

known_faces = []
known_names = []
spotify_tracks = {
    "Unknown": "02DurCgOvDdX0uKEjqcl3W",
    "Andrew_Tio": "7ofFNEqVY1PUdrrL6iXthZ",
    "Raymond_Young": "2zYzyRzz6pRmhPzyfMEC8s"
}
# known = 'known'
# directory = os.fsencode(known)

# for file in os.listdir(directory):
#     filename = os.fsdecode(file)
#     if filename.endswith(".jpg"):
#         new_face = face_recognition.load_image_file(known + "/" + filename)
#         person_name = filename.replace(".jpg", "")
#         print("I know " + person_name)
#         known_names.append(person_name)
#         known_faces.append(face_recognition.face_encodings(new_face)[0])
#         # print(os.path.join(directory, filename))
#         continue
#     else:
#         continue

faces = sekurrity.get_all_faces()
for face in faces:
    known_names.append(face)
    known_faces.append(sekurrity.retrieve_face_encoding(face[0]))

match_not_found = True
capture_interval = 0
song_playing = False
unknown_counter = 0

def get_spotify_track(face):
    return face[3]

def get_name(face):
    return face[1]

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Find all the faces and face enqcodings in the frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        # See if the face is a match for the known face(s)
        results = face_recognition.compare_faces(known_faces, face_encoding)

        person = "Unknown"
        face = False
        for index, result in enumerate(results):
            if result:
                face = known_names[index]
                person = get_name(face)
                print("I see you " + person)
            else:
                unknown_counter += 1
            print("Unknown counter: {}".format(unknown_counter))
            if capture_interval == 0 and face and song_playing != get_spotify_track(face):
                os.system("osascript -e 'tell application \"spotify\" to play track \"spotify:track:" + get_spotify_track(face) + "\"'")
                song_playing = get_spotify_track(face)
                capture_interval = 15
                unknown_counter = 0
            if capture_interval == 0 and person == "Unknown" and unknown_counter > 3:
                os.system("osascript -e 'tell application \"spotify\" to play track \"spotify:track:02DurCgOvDdX0uKEjqcl3W\"'")
                os.system("osascript -e 'tell application \"spotify\" to set player position to 133'")
                unknown_counter = 0
                capture_interval = 15

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, person, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    if song_playing and capture_interval > 0:
        capture_interval -= 1

    print(capture_interval)
    # Display the resulting image
    cv2.imshow('Video', frame)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
