"""
this class encapsulates stream reading functionality

LiveStream is RAII class

 -----------------------------------
    with LiveStream(url) as stream:
        stream.toJpeg(folderPath)
        stream.toMp4(folderPath)

"""

import platform
import cv2


class LiveStream:
    def __init__(self, url_, maxVideoFilesCount_ = 2, maxFramesPerVideoFile_ = 50, maxJpegFilesCount_ = 100):

        self.maxVideoFilesCount = maxVideoFilesCount_
        self.maxFramesPerVideoFile = maxFramesPerVideoFile_
        self.maxJpegFilesCount = maxJpegFilesCount_
        self.url = url_

    def __enter__(self):
        self.stream = cv2.VideoCapture(self.url)

        if not self.stream.isOpened():
            raise Exception("cannot open url:",self.url)

        self.fps = self.stream.get(cv2.CAP_PROP_FPS)
        self.wait_ms = int(1000 / self.fps)
        return self

    def __exit__(self, type, value, traceback):
        self.stream.release()
        cv2.destroyAllWindows()

    def toJpeg(self, folderPath):
        """
        converts input stream to jpeg files
        """
        if not self.stream:
            raise Exception("stream have not been initialised")

        print('[ saving stream as jpeg ... ] ')

        for imageIndex in range(self.maxJpegFilesCount):
            imageFileName = folderPath + "/hls_image_{}.jpg".format(imageIndex)

            ret, frame = self.stream.read()

            cv2.imwrite(imageFileName, frame)

            if platform.system() == 'Windows':
                cv2.imshow('frame', frame)
                if cv2.waitKey(self.wait_ms) & 0xFF == ord('q'):
                    break


    def toMp4(self, videoFolder):
        """
        converts input stream to mp4 files
        """
        if not self.stream:
            raise Exception("stream have not been initialised")

        print('[ saving stream as video ... ] ')

        for videoFileIndex in range(self.maxVideoFilesCount):
            videoFileName = videoFolder + "/hls_video_{}.mp4".format(videoFileIndex)

            # todo: loosing first frame, need to be rewritten
            ret, frame = self.stream.read()
            height, width, layers = frame.shape

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            videoWriter = cv2.VideoWriter(videoFileName, fourcc, int(self.fps), (width, height))

            for frameIndex in range(self.maxFramesPerVideoFile):
                ret, frame = self.stream.read()
                videoWriter.write(frame)

                if platform.system() == 'Windows':
                    cv2.imshow('frame', frame)
                    if cv2.waitKey(self.wait_ms) & 0xFF == ord('q'):
                        break

            videoWriter.release()
