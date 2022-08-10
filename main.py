import cv2 as cv
import numpy as np
import mediapipe as mp
from pynput.mouse import Button, Controller
from tkinter import *
import speech_recognition as sr
import threading
import time
import pyautogui as pa

rec = sr.Recognizer()

root = Tk()

altura_monitor = root.winfo_screenheight()
largura_monitor = root.winfo_screenwidth()

pmmx = (0 + largura_monitor) * 0.5
pmmy = (0 + altura_monitor) * 0.5

print(pmmx, pmmy)

sensi_x = 7
sensi_y = 10

mouse = Controller()

x, y = 1, 1

mp_face_mesh = mp.solutions.face_mesh
LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
# right eyes indices
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]

LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]
mouth1 = [0, 72, 12, 302]
mouth2 = [15, 85, 16, 315]

cap = cv.VideoCapture("https://192.168.0.110:8080/video")

first_value_y = []
first_value_x = []
on_off = 0
beginnerclick = 0
beginnerpress = 0
ganhox = None
ganhoy = None

var1 = 0
var2 = 0


def main():
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.1,
            min_tracking_confidence=0
    ) as face_mesh:
        while True:

            #  Variavies Globais
            global var1, var2, beginnerclick, on_off, ganhox, ganhoy, beginnerpress

            ret, frame = cap.read()
            if not ret:
                break

            frame = cv.flip(frame, 1)
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
                (m_cx, m_cy), m_radius = cv.minEnclosingCircle(mesh_points[mouth1])
                (m2_cx, m2_cy), m2_radius = cv.minEnclosingCircle(mesh_points[mouth2])
                (px, py), p_radius = cv.minEnclosingCircle(mesh_points[[52, 65, 66, 66]])

                point_m = (np.array([m_cx, m_cy], dtype=np.int32))
                point_m2 = (np.array([m2_cx, m2_cy], dtype=np.int32))
                pp = (np.array([px, py], dtype=np.int32))

                center_left = (np.array([l_cx, l_cy], dtype=np.int32))
                center_right = (np.array([r_cx, r_cy], dtype=np.int32))

                cv.circle(frame, center_left, int(l_radius * 0.1), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, center_right, int(r_radius * 0.1), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, point_m, int(l_radius * 0.3), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, point_m2, int(l_radius * 0.3), (255, 0, 255), 1, cv.LINE_AA)
                cv.circle(frame, pp, int(p_radius * 0.3), (255, 0, 255), 1, cv.LINE_AA)

                pointclick = center_right[1] - pp[1]
                pointpress = point_m2[1] - point_m[1]

                if beginnerclick == 0:
                    beginnerpoint = pointclick
                    beginnerclick = 1

                if pointclick >= beginnerpoint + 12:
                    var1 = 1

                else:
                    var1 = 0

                if beginnerpress == 0:
                    beginnerpress = pointpress
                    beginnerpress = 1

                if pointpress >= beginnerpress+60:
                    var2 = 1

                else:
                    var2 = 2

                cv.line(frame, point_m, point_m2, (255, 0, 0), 1)
                cv.line(frame, center_right, pp, (255, 0, 0), 1)

            x = ((l_cx + r_cx) * 0.5)
            y = ((l_cy + r_cy) * 0.5)

            if on_off == 0:
                first_value_x = x
                first_value_y = y
                on_off = 1

            if x < first_value_x and y < first_value_y:
                ganhox = first_value_x - x
                ganhoy = first_value_y - y

                x1 = (pmmx - (ganhox * sensi_x))
                y2 = (pmmy - (ganhoy * sensi_y))

                mouse.position = (x1, y2)

            if x < first_value_x and y > first_value_y:
                ganhox = first_value_x - x
                ganhoy = y - first_value_y

                x1 = (pmmx - (ganhox * sensi_x))
                y2 = (pmmy + (ganhoy * sensi_y))

                mouse.position = (x1, y2)

            if x > first_value_x and y < first_value_y:
                ganhox = x - first_value_x
                ganhoy = first_value_y - y

                x1 = (pmmx + (ganhox * sensi_x))
                y2 = (pmmy - (ganhoy * sensi_y))

                mouse.position = (x1, y2)

            if x > first_value_x and y > first_value_y:
                ganhox = x - first_value_x
                ganhoy = y - first_value_y
                x1 = (pmmx + (ganhox * sensi_x))
                y2 = (pmmy + (ganhoy * sensi_y))

                mouse.position = (x1, y2)

            cv.imshow('img', frame)
            key = cv.waitKey(1)

            if key == 27:
                var1 = 3
                var2 = 3
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
                    break

                elif texto == "pressionar":
                    pa.mouseDown()

                elif texto == "soltar":
                    pa.mouseUp()

                elif texto == "apertar" or texto == "despertar":
                    pa.click()

                elif texto == "abrir":
                    pa.click()
                    pa.click()

                elif texto == "enviar":
                    pa.press('enter')

                elif texto == "escrever":
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


def pressionar():
    while True:
        try:
            if var2 == 1:
                pa.mouseDown()
                time.sleep(0.3)

            elif var2 == 2:
                pa.mouseUp()
                time.sleep(0.3)

            elif var2 == 3:
                break


        except:
            time.sleep(0.00005)
            print("Falhou")
            pass


def click():
    while True:

        try:
            # Gastar memoria
            print("", end="")

            if var1 == 1:
                print("Clicou")
                pa.click()
                time.sleep(0.3)

            elif var1 == 3:
                break

            elif var1 == 0:
                time.sleep(0.00005)
                pass

        except:
            time.sleep(0.00005)
            pass




"""if __name__ == '__main__':
    threading.Thread(target=main).start()
    #  recvoice()

    time.sleep(0.5)
    threading.Thread(target=click).start()

    time.sleep(0.5)
    pressionar()




"""