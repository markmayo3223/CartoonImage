from tkinter import Toplevel, Button, RIGHT
import numpy as np
import cv2


class FilterFrame(Toplevel):

    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.original_image = self.master.processed_image
        self.filtered_image = None

        self.black_white_button = Button(master=self, text="Black White")
        self.gaussian_blur_button = Button(master=self, text="Gaussian Blur")
        self.edge_button = Button(master=self, text="Edge")
        self.cartoon_button = Button(master=self, text="Cartoon")

        self.cancel_button = Button(master=self, text="Cancel")
        self.apply_button = Button(master=self, text="Apply")

        self.black_white_button.bind("<ButtonRelease>", self.black_white_released)
        self.gaussian_blur_button.bind("<ButtonRelease>", self.gaussian_blur_button_released)
        self.edge_button.bind("<ButtonRelease>", self.edge_button_released)
        self.cartoon_button.bind("<ButtonRelease>", self.cartoon_button_released)
        self.apply_button.bind("<ButtonRelease>", self.apply_button_released)
        self.cancel_button.bind("<ButtonRelease>", self.cancel_button_released)

        self.black_white_button.pack()
        self.gaussian_blur_button.pack()
        self.edge_button.pack()
        self.cartoon_button.pack()
        self.cancel_button.pack(side=RIGHT)
        self.apply_button.pack()


    def black_white_released(self, event):
        self.black_white()
        self.show_image()

    def gaussian_blur_button_released(self, event):
        self.gaussian_blur()
        self.show_image()

    def edge_button_released(self, event):
        self.edge()
        self.show_image()

    def cartoon_button_released(self, event):
        self.cartoon()
        self.show_image()


    def apply_button_released(self, event):
        self.master.processed_image = self.filtered_image
        self.show_image()
        self.close()

    def cancel_button_released(self, event):
        self.master.image_viewer.show_image()
        self.close()

    def show_image(self):
        self.master.image_viewer.show_image(img=self.filtered_image)




    def black_white(self):
        self.filtered_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        self.filtered_image = cv2.cvtColor(self.filtered_image, cv2.COLOR_GRAY2BGR)


    def gaussian_blur(self):
        self.filtered_image = cv2.GaussianBlur(self.original_image, (41, 41), 0)

    def edge(self):
        self.filtered_image = cv2.Laplacian(self.original_image, -1, ksize=5)
        self.filtered_image = 255 - self.filtered_image
        ret, self.filtered_image = cv2.threshold(self.filtered_image, 150, 255, cv2.THRESH_BINARY)



    def cartoon(self):
        grayImage = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        grayImage = cv2.GaussianBlur(grayImage, (3, 3), 0)
        edgeImage = cv2.Laplacian(grayImage, -1, ksize=5)
        edgeImage = 255 - edgeImage
        ret, edgeImage = cv2.threshold(edgeImage, 150, 255, cv2.THRESH_BINARY)
        edgePreservingImage = cv2.edgePreservingFilter(self.original_image, flags=2, sigma_s=50, sigma_r=0.4)
        output = np.zeros(grayImage.shape)
        output = cv2.bitwise_and(edgePreservingImage, edgePreservingImage, mask=edgeImage)
        self.filtered_image = cv2.bitwise_and(edgePreservingImage, edgePreservingImage, mask=edgeImage)



    def close(self):
        self.destroy()
