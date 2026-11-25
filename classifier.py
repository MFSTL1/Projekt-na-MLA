import mediapipe as mp
import cv2
from torchvision.transforms import v2
import multiprocessing

#import multiprocessing
#UWAGA ZAMIAST DATASETU V2 MA BYĆ NASZ DATASET

stop_event = multiprocessing.Event() # thread do zatrzymywania przechwytywania obrazu
frame_queue = multiprocessing.Queue(maxsize=2)

def pictureLoader(fileName): # obsługa zdjęć z plików obrazu
    return 0

def videoLoader(fileName): #obsługa plików video, które nie są strumieniem na żywo z kamery
    return 0

def videoStreamLoader(codec, stop_event): # + fileName do pliku video??
    cam = cv2.VideoCapture(0)
    #frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    #frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # ograniczenie do danych, sprawdzić czy nie ucina tylko do lewego górnego rogu
    frame_width = 640
    frame_height = 480
    cam.set(cv2.CAP_PROP_FPS, 20) # 20fps czyli +- 40ms między klatkami
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

    while True:
        ret, frame = cam.read()

        # Write the frame to the output file
        out.write(frame)

        # Display the captured frame
        cv2.imshow('Camera', frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) == ord('q') or stop_event: # lub stop_event, zatrzymujemy screen capture
            break

    # Release the capture and writer objects
    cam.release()
    out.release()
    cv2.destroyAllWindows()

class klasyfikator(): #tutaj trenowanie i klasyfikacja osobno od pobierania obrazu
    def __init__():
        return 0  
    def train():
        return 0

    def classificatorWorker(): #obsługuje pętlę wykrywania i klasyfikacji na podstawie obrazu
        return 0

def handler():
    #handler obsługuje wątki i jest wywoływany w main
    #p1 jako nasz główny proces + klasyfikator, p2 jako przechwytywanie obrazu z kamery
    newKlasyfikator = klasyfikator(stop_event)
    p1 = multiprocessing.process(target=newKlasyfikator.classificatorWorker, args=("mpv4",stop_event))
    p2 = multiprocessing.process(target=videoStreamLoader, args=())
    p1.start()
    p2.start()
    p1.join()
    p2.join()



