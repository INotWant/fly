import time
import logging
from tkinter import *
from tkinter import messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

showLogger = {"draw": False}


class View:

    def __init__(self, timeInterval, aircrafts, xLim=(0, 100), yLim=(0, 100), zLim=(0, 100)):
        self.timeInterval = timeInterval
        self.aircrafts = aircrafts
        self.afterHandler = None

        self._xLim = xLim
        self._yLim = yLim
        self._zLim = zLim

        self.root = Tk()
        self.root.title("FLY")
        self.root.geometry('700x700')
        self.frame = Frame(self.root, bg="#ffffff")
        self.frame.place(x=0, y=0, width=700, height=700)

        self.fig = plt.figure(figsize=(6, 6))
        self.ax = Axes3D(self.fig)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().place(x=0, y=0)

    def start(self):
        def drawTrack():
            startTime = time.time()
            self.ax.clear()
            self.ax.set_xlim(self._xLim[0], self._xLim[1])
            self.ax.set_ylim(self._yLim[0], self._yLim[1])
            self.ax.set_zlim(self._zLim[0], self._zLim[1])
            self.ax.axis("off")
            self.ax.view_init(0, 0)
            if showLogger.get("draw"):
                logger.info("[draw] cost time0: %s", int((time.time() - startTime) * 1000))
            xs, ys, zs = [], [], []
            for aircraft in self.aircrafts:
                x, y, z = aircraft.getTrackCoordinates()
                xs.append(x)
                ys.append(y)
                zs.append(z)
            if showLogger.get("draw"):
                logger.info("[draw] cost time1: %s", int((time.time() - startTime) * 1000))
            self.ax.scatter(xs, ys, zs, c="coral", s=5)
            self.canvas.draw()
            self.afterHandler = self.root.after(self.timeInterval, drawTrack)
            if showLogger.get("draw"):
                logger.info("[draw] cost time2: %s", int((time.time() - startTime) * 1000))

        drawTrack()

        def on_closing():
            self.root.after_cancel(self.afterHandler)
            answer = messagebox.askokcancel("退出", "确定退出吗?")
            if answer:
                plt.close('all')
                self.root.destroy()
            else:
                self.root.after(self.timeInterval, drawTrack)

        self.root.protocol("WM_DELETE_WINDOW", on_closing)
        self.root.mainloop()
