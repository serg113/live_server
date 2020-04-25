"""
this class encapsulates stream reading functionality

LiveStream is RAII class,
it's current use case to prevent resource leaks
 -----------------------------------
    with LiveStream(url) as stream:
        stream.toJpeg(folderPath)
        stream.toMp4(folderPath)

"""

import cv2


class LiveStream:
    def __init__(self, url_, maxVideoFilesCount_ = 2, maxFramesPerVideoFile_ = 50, maxJpegFilesCount_ = 100):

        self.maxVideoFilesCount = maxVideoFilesCount_
        self.maxFramesPerVideoFile = maxFramesPerVideoFile_
        self.maxJpegFilesCount = maxJpegFilesCount_
        self.url = url_

    def __enter__(self):
        liveStream = cv2.VideoCapture(self.url)

        if liveStream.isOpened() is False:
            print('!!! Unable to open URL')
            raise Exception("cannot open url:",self.url)

        self.fps = liveStream.get(cv2.CAP_PROP_FPS)
        self.wait_ms = int(1000 / self.fps)
        self.stream = liveStream

        print('FPS:', self.fps)

        return self

    def __exit__(self, type, value, traceback):
        self.stream.release()

    def toJpeg(self, folderPath):
        """
        converts input stream to jpeg files
        """
        if not self.stream:
            raise Exception("stream have not been initialised")

        for imageIndex in range(self.maxJpegFilesCount):
            imageFileName = folderPath + "/hls_image_{}.jpg".format(imageIndex)

            ret, frame = self.stream.read()

            cv2.imwrite(imageFileName, frame)

    def toMp4(self, videoFolder):
        """
        converts input stream to mp4 files
        """
        if not self.stream:
            raise Exception("stream have not been initialised")

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

            videoWriter.release()
			