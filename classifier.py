import torch
import torchvision
import cv2
from torchvision.transforms import v2
import multiprocessing
#import queue
#import asyncio
#import multiprocessing
#UWAGA ZAMIAST DATASETU V2 MA BYĆ NASZ DATASET

stop_event = multiprocessing.Event() # thread do zatrzymywania przechwytywania obrazu
frame_queue = multiprocessing.Queue(maxsize=2)

def videoStreamLoader(codec, stop_event): # + fileName do pliku video??
    cam = cv2.VideoCapture(0)
    #frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    #frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # ograniczenie do danych
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

def klasyfikator1(): # test ze strony do torchvision
    transform = v2.Compose([
        v2.ToImage(),
        v2.ToDtype(torch.float32, scale=True),
        v2.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    batch_size = 4

    trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
                                            download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                            shuffle=True, num_workers=2)

    testset = torchvision.datasets.CIFAR10(root='./data', train=False,
                                        download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                            shuffle=False, num_workers=2)

    classes = ('plane', 'car', 'bird', 'cat',
            'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

def handler():
    #p1 jako nasz główny proces + klasyfikator, p2 jako przechwytywanie obrazu z kamery
    
    p1 = multiprocessing.process(target=klasyfikator1,args=())
    p2 = multiprocessing.process(target=klasyfikator1, args=("mpv4",stop_event))
    p1.start()
    p2.start()
    p1.join()
    p2.join()




"""     # Image Classification
import torch
from torchvision.transforms import v2

H, W = 32, 32
img = torch.randint(0, 256, size=(3, H, W), dtype=torch.uint8)

transforms = v2.Compose([
    v2.RandomResizedCrop(size=(224, 224), antialias=True),
    v2.RandomHorizontalFlip(p=0.5),
    v2.ToDtype(torch.float32, scale=True),
    v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])
img = transforms(img) """

""" 
# Detection (re-using imports and transforms from above)
from torchvision import tv_tensors

img = torch.randint(0, 256, size=(3, H, W), dtype=torch.uint8)
boxes = torch.randint(0, H // 2, size=(3, 4))
boxes[:, 2:] += boxes[:, :2]
boxes = tv_tensors.BoundingBoxes(boxes, format="XYXY", canvas_size=(H, W))

# The same transforms can be used!
img, boxes = transforms(img, boxes)
# And you can pass arbitrary input structures
output_dict = transforms({"image": img, "boxes": boxes}) """