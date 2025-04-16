# Copyright 2024 cvpose
# Licensed under the Apache License, Version 2.0

import cv2
import mediapipe as mp
from virtual_landmark import VirtualLandmark, landmark, calculus as calc
from virtual_landmark import Connections, get_extended_pose_landmarks_style

# ==========================
# CUSTOM LANDMARK CLASS
# ==========================

class HelloWorld(VirtualLandmark):
    @landmark("MIDDLE_SHOULDER", connection=["RIGHT_SHOULDER", "LEFT_SHOULDER", "NECK"])
    def _middle_shoulder(self):
        return calc.middle(
            self[self.virtual_landmark.RIGHT_SHOULDER],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )

    @landmark("NECK", connection=["MIDDLE_SHOULDER", "NOSE"])
    def _neck(self):
        return calc.middle(
            self[self.virtual_landmark.NOSE],
            self[self.virtual_landmark.MIDDLE_SHOULDER],
        )

    @landmark("PROJECTION")
    def _norm(self):
        return calc.projection(
            self[self.virtual_landmark.LEFT_HIP],
            self[self.virtual_landmark.LEFT_KNEE],
            self[self.virtual_landmark.LEFT_SHOULDER],
        )

# ==========================
# MAIN EXECUTION (VIDEO)
# ==========================

def main():
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils

    # Start webcam capture
    cap = cv2.VideoCapture(0)  # Use a video file path if you prefer pre-recorded video

    with mp_pose.Pose(
        static_image_mode=False,
        model_complexity=2,
        enable_segmentation=False,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as pose:

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Ignoring empty frame.")
                break

            # Convert to RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Run pose detection
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                # Build extended landmarks
                landmarks = HelloWorld(results.pose_landmarks.landmark)
                connections = Connections(landmarks)
                landmark_style = get_extended_pose_landmarks_style(landmarks)

                # Draw landmarks on frame
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=landmarks.as_landmark_list(),
                    connections=connections.ALL_CONNECTIONS,
                    landmark_drawing_spec=landmark_style,
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(255, 255, 255), thickness=2
                    ),
                )

            # Show result
            cv2.imshow("Real-Time Pose Estimation", frame)

            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()