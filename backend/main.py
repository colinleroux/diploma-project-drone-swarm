import requests
from fastapi import FastAPI, Request, Response
from mock.drone import TelloDrone
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import cv2
from starlette.responses import StreamingResponse
import socket

app = FastAPI()
drone = TelloDrone()
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust the allowed origins as needed
    allow_methods=["*"],  # Adjust the allowed methods as needed
    allow_headers=["*"],  # Adjust the allowed headers as needed
    allow_credentials=True,  # Adjust as needed if you are using cookies or sessions
)
# Set the address of the mock server
drone_server_address = ("localhost", 8999)

class CommandRequest(BaseModel):
    command: str


@app.post('/api/commands')
def handle_command(command_request: CommandRequest):
    # Send the command to the drone server
    command = command_request.command.encode('utf-8')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(command, drone_server_address)

    return {'message': f'Received command: {command.decode()}'}


@app.get("/takeoff")
def takeoff():
    drone.takeoff()
    return {"message": "Takeoff command sent"}

def generate_video_stream():
    # Open the video capture from the drone
    cap = cv2.VideoCapture(0)

    # Set the video frame size
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        if not ret:
            break

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)

        if not ret:
            break

        # Yield the frame as bytes
        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n'


@app.get("/video-stream")
def video_stream():
    # Generate the video stream
    return StreamingResponse(generate_video_stream(), media_type="multipart/x-mixed-replace; boundary=frame")
