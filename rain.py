import os
import cv2
import sys
import pygame
from tkinter import Tk, Label, Scale, HORIZONTAL
from PIL import Image, ImageTk

def get_resource_path(relative_path):
    """Returns the absolute path to the resource."""
    if getattr(sys, 'frozen', False):  # When running as an exe
        base_path = sys._MEIPASS
    else:  # When running in the development environment
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def play_rain():
    pygame.init()
    pygame.mixer.init()

    video_path = get_resource_path("resources/rain.mp4")
    audio_path = get_resource_path("resources/rain.mp3")
    icon_path = get_resource_path("resources/rain.ico")

    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play(-1) # -1 for infinite looping
    pygame.mixer.music.set_volume(0.5)

    root = Tk()
    root.title("Rain")
    root.iconbitmap(icon_path)
    root.geometry("400x400")

    label = Label(root, bg="Black")
    

    def update_volume(value):
        """Update the volume based on the slider value."""
        volume = int(value) / 100
        pygame.mixer.music.set_volume(volume)

    slider = Scale(
        root,
        from_=0,
        to=100,
        orient=HORIZONTAL,
        label="Volume",
        command=update_volume,
    )

    slider.set(50)
    slider.pack(side="bottom", fill="x", padx=10, pady=10)    
    label.pack(fill="both", expand=True)

    video = cv2.VideoCapture(video_path)

    def update_frame():
        ret, frame = video.read()
        if not ret:
            video.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = video.read()
        
        window_w = root.winfo_width()
        window_h = root.winfo_height()


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame, (window_w, window_h), interpolation=cv2.INTER_AREA)

        img = ImageTk.PhotoImage(Image.fromarray(frame_resized))
        label.config(image=img)
        label.image = img

        root.after(50, update_frame)
    
    update_frame()
    root.mainloop()

    video.release()
    pygame.mixer.music.stop()
    pygame.quit()


play_rain()