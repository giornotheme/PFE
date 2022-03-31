from __future__ import division

from math import ceil
from socket import AF_INET, SOCK_DGRAM, socket
from struct import pack
from datetime import datetime
from sys import argv, exit
from cv2 import IMWRITE_JPEG_QUALITY, VideoCapture, destroyAllWindows, imencode, cvtColor, Laplacian, CV_16U, CV_64F, COLOR_RGB2GRAY, mean, Sobel, VideoWriter, VideoWriter_fourcc, CAP_PROP_FRAME_WIDTH, CAP_PROP_FRAME_HEIGHT, CAP_PROP_FPS, CAP_V4L
import threading
import os

"""
class FrameSegment(object):
    """
    #Object to break down image frame segment
    #if the size of image exceed maximum datagram size
    """
    MAX_DGRAM = 2 ** 16

    # extract 64 bytes in case UDP frame overflown
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64

    def __init__(self, port=12345, remote='127.0.0.1', quality=100):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.quality = [
            int(IMWRITE_JPEG_QUALITY), quality
        ]
        self.port = port
        self.addr = remote
        self.isFocusing = False

    def udp_frame(self, img):
        """
        #Compress image and Break down
        #into data segments
        """

        compress_img = imencode(
            '.jpg', img, self.quality
        )[1]

        dat = compress_img.tobytes()
        size = len(dat)
        count = ceil(size / self.MAX_IMAGE_DGRAM)
        start = 0

        while count:
            end = min(
                size, start + self.MAX_IMAGE_DGRAM
            )
            self.sock.sendto(
                pack("B", count) + dat[start:end],
                (
                    self.addr,
                    self.port
                )
            )
            start = end
            count -= 1

    def quit(self, *largs):
        self.sock.close()
"""

def focusing(val):
  value = (val << 4) & 0x3ff0
  data1 = (value >> 8) & 0x3f
  data2 = value & 0xf0
  print("focus value: {}".format(val))
  os.system("i2cset -y 0 0x0c %d %d" % (data1,data2))

"""	
def sobel(img):
	img_gray = cvtColor(img, COLOR_RGB2GRAY)
	img_sobel = Sobel(img_gray, CV_16U,1,1)
	return mean(img_sobel)[0]
"""
def laplacian(img):
	img_gray = cvtColor(img, COLOR_RGB2GRAY)
	img_laplacian = Laplacian(img_gray, CV_16U)
	return mean(img_laplacian)[0]

def needFocus(img, camera):
  needFocus = False
  gray = cvtColor(img, COLOR_RGB2GRAY)
  lap = Laplacian(gray, CV_64F).var()
  if lap < 20 and camera.isFocusing == False:
    needFocus = True
  return needFocus

def autofocus(frame, camera):
  print("Start focusing")
  camera.isFocusing = True
  
  max_index = 10
  max_value = 0.0
  last_value = 0.0
  dec_count = 0
  focal_distance = 10
  
  while True:
      #Adjust focus
  		focusing(focal_distance)
  		#Take image and calculate image clarity
  		val = laplacian(frame)
  		#Find the maximum image clarity
  		if val > max_value:
  			max_index = focal_distance
  			max_value = val
  			
  		#If the image clarity starts to decrease
  		if val < last_value:
  			dec_count += 1
  		else:
  			dec_count = 0
  		#Image clarity is reduced by six consecutive frames
  		if dec_count > 6:
  			break
  		last_value = val
  		
  		#Increase the focal distance
  		focal_distance += 15
  		if focal_distance > 1000:
  			break
  
  #Adjust focus to the best
  focusing(max_index)
  camera.isFocusing = False
  print("max index = %d,max value = %lf" % (max_index, max_value))
"""
def main(fs, cap, videoOut):
    """
    #Top level main function 
    """
    print("Sending video data...")

    while (cap.isOpened()):
      ret, frame = cap.read()

      # if frame is read correctly
      if ret:
        fs.udp_frame(frame)
        videoOut.write(frame)
        if needFocus(frame, fs):
          x = threading.Thread(target=autofocus, args=(frame,fs,))
          x.start()

    cap.release()
    videoOut.release()
    destroyAllWindows()
    fs.quit()


if __name__ == "__main__":

    if len(argv) != 7:
      print("Not enough arguments! Exemple usage: python3 sender.py {Remote IP} {UDP Port} {Image Quality} {Video Width} {Video Height} {Video FPS}")
      exit(0)

    remote = argv[1]
    port = int(argv[2])
    quality = int(argv[3])
    video_width = int(argv[4])
    video_height = int(argv[5])
    video_fps = int(argv[6])

    fs = FrameSegment(port, remote, quality)
    cap = VideoCapture(-1, CAP_V4L)
    cap.set(CAP_PROP_FRAME_WIDTH, video_width)
    cap.set(CAP_PROP_FRAME_HEIGHT, video_height)
    cap.set(CAP_PROP_FPS, video_fps)

    videoOut = VideoWriter('output_' + datetime.now().strftime("%d-%m-%Y %Hh%Mm") + '.mp4', VideoWriter_fourcc(*'avc1'), float(video_fps), (video_width,video_height))

    try:
      main(fs, cap, videoOut)
    except KeyboardInterrupt:
        print('Video script interrupted, saving and ending program...')
        try:
            cap.release()
            videoOut.release()
            destroyAllWindows()
            fs.quit()
            exit(0)
        except SystemExit:
            cap.release()
            videoOut.release()
            destroyAllWindows()
            fs.quit()
            exit(0)
"""