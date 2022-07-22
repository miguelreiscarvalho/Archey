import cv2 as cv
import numpy as np
import mediapipe as mp
from pynput.mouse import Controller
from tkinter import *
import speech_recognition as sr
import threading
import time
import pyautogui as pa
import pygame

pygame.init()
pygame.mixer.music.load('executado.mp3')
pygame.mixer.music.play()
time.sleep(1)

rec = sr.Recognizer()

root = Tk()

altura_monitor = root.winfo_screenheight()
largura_monitor = root.winfo_screenwidth()

pmmx = (0 + largura_monitor) / 2
pmmy = (0 + altura_monitor) / 2

print(pmmx, pmmy)

sensi_x = 7
sensi_y = 10

mouse = Controller()

x, y = 1, 1

mp_face_mesh = mp.solutions.face_mesh
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
# right eyes indices
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

LEFT_IRIS = [x, 45, 4, 275]
RIGHT_IRIS = [y, 45, 4, 275]

cap = cv.VideoCapture(0)
first_value_y = []
#  cap.open("")

first_value_x = []
on_off = 0
ganhox = None
ganhoy = None


def main():
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.9,
            min_tracking_confidence=0.9
    ) as face_mesh:
        while True:
            global on_off
            global ganhox
            global ganhoy
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)
            if results.multi_face_landmarks:
                # print(results.multi_face_landmarks[0].landmark)
                mesh_points = np.array(
                    [np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in
                     results.multi_face_landmarks[0].landmark])

                (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[LEFT_IRIS])
                (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[RIGHT_IRIS])
                center_left = np.array([l_cx, l_cy], dtype=np.int32)

                center_right = np.array([r_cx, r_cy], dtype=np.int32)
                cv.circle(frame, center_left, int(l_radius / 1), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, center_right, int(r_radius / 1), (255, 0, 255), 1, cv.LINE_AA)

            x = int(((l_cx + r_cx) / 2))
            y = int(((l_cy + r_cy) / 2))

            if on_off == 0:
                first_value_x = x
                first_value_y = y
                on_off = 1

            if x < first_value_x and y < first_value_y:
                ganhox = first_value_x - x
                ganhoy = first_value_y - y

                x1 = int(pmmx - (ganhox * sensi_x))
                y2 = int(pmmy - (ganhoy * sensi_y))

                stringx = str(x1)

                stringx = stringx[:-1]
                stringx = stringx + "0"
                stringx = int(stringx)

                stringy = str(y2)

                stringy = stringy[:-1]
                stringy = stringy + "0"
                stringy = int(stringy)

                x1 = stringx

                y2 = stringy

                mouse.position = (x1, y2)

            if x < first_value_x and y > first_value_y:
                ganhox = first_value_x - x
                ganhoy = y - first_value_y

                x1 = int(pmmx - (ganhox * sensi_x))
                y2 = int(pmmy + (ganhoy * sensi_y))

                stringx = str(x1)

                stringx = stringx[:-1]
                stringx = stringx + "0"
                stringx = int(stringx)

                stringy = str(y2)

                stringy = stringy[:-1]
                stringy = stringy + "0"
                stringy = int(stringy)

                x1 = stringx

                y2 = stringy

                mouse.position = (x1, y2)

            if x > first_value_x and y < first_value_y:
                ganhox = x - first_value_x
                ganhoy = first_value_y - y

                x1 = int(pmmx + (ganhox * sensi_x))
                y2 = int(pmmy - (ganhoy * sensi_y))

                stringx = str(x1)

                stringx = stringx[:-1]
                stringx = stringx + "0"
                stringx = int(stringx)

                stringy = str(y2)

                stringy = stringy[:-1]
                stringy = stringy + "0"
                stringy = int(stringy)

                x1 = stringx

                y2 = stringy

                mouse.position = (x1, y2)

            if x > first_value_x and y > first_value_y:
                ganhox = x - first_value_x
                ganhoy = y - first_value_y
                x1 = int(pmmx + (ganhox * sensi_x))
                y2 = int(pmmy + (ganhoy * sensi_y))

                stringx = str(x1)

                stringx = stringx[:-1]
                stringx = stringx + "0"
                stringx = int(stringx)

                stringy = str(y2)

                stringy = stringy[:-1]
                stringy = stringy + "0"
                stringy = int(stringy)

                x1 = stringx

                y2 = stringy

                mouse.position = (x1, y2)

            cv.imshow('img', frame)
            key = cv.waitKey(1)

            if key == 27:
                break


def recvoice():
    with sr.Microphone() as mic:
        while True:

            try:
                print(f": ", end="")
                audio = rec.listen(mic)
                texto = rec.recognize_google(audio, language="pt-BR")

                print(texto)

                if texto == "Desligar programa":
                    pygame.mixer.music.load('executado.mp3')
                    pygame.mixer.music.play()
                    time.sleep(1)
                    break

                elif texto == "pressionar":
                    pygame.mixer.music.load('executado.mp3')
                    pygame.mixer.music.play()
                    time.sleep(1)
                    pa.mouseDown()

                elif texto == "soltar":
                    pygame.mixer.music.load('executado.mp3')
                    pygame.mixer.music.play()
                    time.sleep(1)
                    pa.mouseUp()

                elif texto == "apertar" or texto == "despertar":
                    pygame.mixer.music.load('executado.mp3')
                    pygame.mixer.music.play()
                    time.sleep(1)
                    pa.click()

                elif texto == "abrir":
                    pygame.mixer.music.load('executado.mp3')
                    pygame.mixer.music.play()
                    time.sleep(1)
                    pa.click()
                    pa.click()

                elif texto == "enviar":
                    pygame.mixer.music.load('executado.mp3')
                    pygame.mixer.music.play()
                    time.sleep(1)
                    pa.press('enter')

                elif texto == "escrever":
                    pygame.mixer.music.load('escrever.mp3')
                    pygame.mixer.music.play()
                    time.sleep(1)

                    print("> ", end="")
                    audio = rec.listen(mic)
                    escrito = rec.recognize_google(audio, language="pt-BR")
                    pa.write(f"{escrito}")
                    print(escrito)

                else:
                    pass

                print("\n")

                print(time.time())


            except:
                pass


main()
#  threading.Thread(target=main).start()
#  recvoice()
time.sleep(1)
cap.release()
cv.destroyAllWindows()
