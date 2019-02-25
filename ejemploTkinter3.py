# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 10:26:37 2019

@author: e-aespinosa
"""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk, Canvas
from tkinter import *
from scipy import ndimage
from tkinter import filedialog
from PIL import ImageTk

from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

s=0
#Fuente de los títulos#
LARGE_FONT=("Verdana", 20)
SMALL_FONT=("Verdana", 12)
##############################################################################
#Vector de imágenes#
VectImg=[]
VectComp=[]
VectImp=[]
VectOrig=[0, 0, 8, 1, 1, 2, 1]
##############################################################################
#Carga los modelos#
model1 = load_model('VacioNoVacio.h5')
model2 = load_model('Botella_Lata.h5')
model3 = load_model('Botella.h5')
model4 = load_model('Lata.h5')
##############################################################################
#Aplicación de escritorio#
class PlanogramApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, "neoris.ico")
        tk.Tk.wm_title(self, "Planogram Detection Demo")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames={}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        frame=self.frames[cont]
        frame.tkraise()
##############################################################################
#Primera página de la aplicación, contiene el menú de páginas#
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        #Título de la página
        label = tk.Label(self, text="Planogram Detection Algorithm Demo", font=LARGE_FONT)
        label.grid(row=0, column=1, pady=60, padx=150)
        ######################################################################
        #Instrucciones de la aplicación#
        label = tk.Label(self, text="First a new planogram image is needed. Upload one in the Planogram Page. Afterwards, define the segments that are required to predict in the Segment Page. Finally, go to the Engine Page and use the Run Prediction button for only one image, and Run Prediction Multiple for various images.", font=SMALL_FONT, wraplength=500)
        label.grid(row=1, column=1, pady=60, padx=150)
        ######################################################################
        #Botón para desplegar planograma#
        butt1 =  ttk.Button(self, text="Planogram Page",
                        command=lambda: controller.show_frame(PageOne))
        butt1.grid(row=2, column=1)
        ######################################################################
        #Botón para desplegar segmentación#
        butt1 =  ttk.Button(self, text="Segmentation Page",
                            command=lambda: controller.show_frame(PageTwo))
        butt1.grid(row=3, column=1)
        ######################################################################
        #Botón para desplegar motor#
        butt1 =  ttk.Button(self, text="Engine Page",
                            command=lambda: controller.show_frame(PageThree))
        butt1.grid(row=4, column=1)
        ######################################################################
#Segunda página de la aplicación, contiene la imagen del planograma#
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ######################################################################
        #Título de la página#
        label = tk.Label(self, text="Planogram Image", font=LARGE_FONT)
        label.grid(row=0, column=1, pady=60, padx=150)
        ######################################################################
        #Función para elgir imagen de planograma#
        def EscogeImagen():
            global image_rot
            #global image1
            imgpath =  filedialog.askopenfilename(initialdir = "/",
                                                title = "Select file",
                                                filetypes = (("jpeg files","*.jpg")\
                                                             ,("all files","*.*")))
            image = plt.imread(imgpath)
            image_rot = ndimage.rotate(image, -90)
            return image_rot
        ######################################################################
        #Botón para elegir imagen de planograma#
        button1 = ttk.Button(self, text="Choose file...",
                            command=EscogeImagen)
        button1.grid(row=1, column=0, padx=4, pady=4)
        ######################################################################
        #Mostrar Planograma#
        def PlanogramShow():
            global canvas
            #Canvas con el planograma
            f = Figure(figsize=(3,4), dpi=100)
            a = f.add_subplot(111)
            a.imshow(image_rot)
            a.axis('off')
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, rowspan=500, column=1, columnspan=2,
                                sticky=E)
            ##################################################################
        #Función que borra contenido del Canvas#
        #Botón para mostrar segmentación
        button2 = ttk.Button(self, text="Show Planogram",
                            command=PlanogramShow)
        button2.grid(row=2, column=0, padx=4, pady=4)
        ######################################################################
        #Botón para regresar a página principal#
        button3 = ttk.Button(self, text="Back to home",
                            command=lambda: controller.show_frame(StartPage))
        button3.grid(row=3, column=0, padx=4, pady=4)
        ######################################################################
        #Botón para desplegar la segmentación#
        button4 = ttk.Button(self, text="Segmentation Page",
                            command=lambda: controller.show_frame(PageTwo))
        button4.grid(row=4, column=0, padx=4, pady=4)
        ######################################################################
        #Botón para mostrar el motor#
        button5 = ttk.Button(self, text="Engine Page",
                            command=lambda: controller.show_frame(PageThree))
        button5.grid(row=5, column=0, padx=4, pady=4)       
        ######################################################################
#Tercera página de la aplicación, contiene la segmentación de la imagen#
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ######################################################################
        #Título de la página#
        label = tk.Label(self, text="Planogram Segmentation", font=LARGE_FONT)
        label.grid(row=0, column=1, columnspan=4, pady=60, padx=150)
        ######################################################################
        #Barras para meter parámetros#
        Label(self, text="X1 Coordinate").grid(row=1, column=0)
        x1 = Entry(self)
        x1.grid(row=1, column=1,)
        Label(self, text="X2 Coordinate").grid(row=2, column=0)
        x2 = Entry(self)
        x2.grid(row=2, column=1,)
        Label(self, text="Y1 Coordinate").grid(row=3, column=0)
        y1 = Entry(self)
        y1.grid(row=3, column=1,)
        Label(self, text="Y2 Coordinate").grid(row=4, column=0)
        y2 = Entry(self)
        y2.grid(row=4, column=1,)
       ###################################################################### 
       ######################################################################
	#Nueva función para mostrar planograma segmentado#
        def PlanogramUpdate():
            f = Figure(figsize=(2,3), dpi=100)
            a = f.add_subplot(111)
            a.imshow(image_rot)
            a.axis('off')
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            for i in range(0,len(VectImg)):
                oval = canvas.create_polygon(VectImp[4*i+1], VectImp[4*i+2],
                                   VectImp[4*i+3], VectImp[4*i+4], fill="red")
            canvas.get_tk_widget().grid(row=1, column=5, rowspan=500, columnspan=2,
                                sticky=E)
            ##################################################################
        #Mostrar imagen segmentada#
        def SegmentationShow():
            global image1
            global s
            #Segmentación de imagen
            image1 = image_rot[int(x1.get()):int(x2.get()), int(y1.get()):int(y2.get()), :]
            ##################################################################
            #Canvas para proyectar la imagen#
            s = s + 1
            f = Figure(figsize=(2,3), dpi=100)
            a = f.add_subplot(111)
            a.imshow(image1)
            a.axis('off')
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=5, rowspan=500, columnspan=2,
                                sticky=E)
            VectImg.append(image1)
            VectImp.append([int(x1.get()), int(y1.get()), int(x2.get()), int(y2.get())])
            #Botón para actualizar segmentación
            if s > 1:
                button5 = ttk.Button(self, text="Update Planogram",
                            command=PlanogramUpdate)
                button5.grid(row=6, column=0, padx=4, pady=4)
            ##################################################################
            return image1
            ##################################################################
        #Botón para regresar a página principal#
        button1 = ttk.Button(self, text="Back to home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=5, column=0, padx=4, pady=4)
        ######################################################################
        #Botón para desplegar planograma#
        button2 = ttk.Button(self, text="Planogram Page",
                            command=lambda: controller.show_frame(PageOne))
        button2.grid(row=5, column=1, padx=4, pady=4)
        ######################################################################
        #Botón para mostrar el motor#
        button3 = ttk.Button(self, text="Engine Page",
                            command=lambda: controller.show_frame(PageThree))
        button3.grid(row=5, column=2, padx=4, pady=4)
        ######################################################################
        #Botón para mostrar imagen segmentada#
        button4 = ttk.Button(self, text="Run Segmentation",
                            command=SegmentationShow)
        button4.grid(row=5, column=3, padx=4, pady=4)
        ######################################################################
#Cuarta página de la aplicación, contiene la predicción de la clase de la imagen#
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ######################################################################
        #Título de la imagen#
        label = tk.Label(self, text="Engine Core", font=LARGE_FONT)
        label.grid(row=0, column=1, pady=60, padx=150)
        ######################################################################
        #Botón para regresar a página principal#
        button1 = ttk.Button(self, text="Back to home",
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(row=4, column=0)
        ######################################################################
        #Botón para desplegar planograma#
        button2 = ttk.Button(self, text="Planogram Page",
                            command=lambda: controller.show_frame(PageOne))
        button2.grid(row=5, column=0)
        ######################################################################
        #Botón para desplegar la segmentación#
        button3 = ttk.Button(self, text="Segmentation Page",
                            command=lambda: controller.show_frame(PageTwo))
        button3.grid(row=6, column=0)
        ######################################################################
        #Función que predice la categoría a la que pertenece la imagen#
        def Prediccion():
            ##################################################################
            #Tratamiento de imagen para input de redes neuronales#
            image2 = cv2.resize(image1, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
            image2= img_to_array(image2)
            image2 = image2.reshape((1,image2.shape[0], image2.shape[1], image2.shape[2]))
            ##################################################################
            #Engine#
            vanova = model1.predict(image2)
            if np.argmax(vanova) == 0:
                label1 = "Not empty with: "
                botola = model2.predict(image2)
                if np.argmax(botola) == 0:
                    label2 = "A bottle of "
                    esbot = model3.predict(image2)
                    if  np.argmax(esbot) == 0:
                        label3 = "Coca Cola."
                    elif np.argmax(esbot) == 1:
                        label3 = "Coca Cola Light."
                    elif np.argmax(esbot) == 2:
                        label3 = "Apple Joya."
                    elif np.argmax(esbot) == 3:
                        label3 = "Pepsi."
                    elif np.argmax(esbot) == 4:
                        label3 = "Sprite."
                    elif np.argmax(esbot) == 5:
                        label3 = "Squirt."
                elif np.argmax(botola) == 1:
                    label2 = "Can of "
                    eslat = model4.predict(image2)
                    if  np.argmax(eslat) == 0:
                        label3 = "Arizona."
                    elif np.argmax(eslat) == 1:
                        label3 = "Boost."
                    elif np.argmax(eslat) == 2:
                        label3 = "Coca Cola."
                    elif np.argmax(eslat) == 3:
                        label3 = "Coca Cola Light."
                    elif np.argmax(eslat) == 4:
                        label3 = "Monster."
                    elif np.argmax(eslat) == 5:
                        label3 = "Rockstar."
                    elif np.argmax(eslat) == 6:
                        label3 = "VitaminWater."
                label = Label(self, text= "Prediction: "+label1+label2+label3)
                label.grid(row=1, column=2)
            elif np.argmax(vanova) == 1:
                label = Label(self, text= "The segmented space is empty.")
                label.grid(row=1, column=2)
        ######################################################################
        #Botón para determinar la predicción#
        button4 = ttk.Button(self, text="Run Prediction", command=Prediccion)
        button4.grid(row=1, column=0)
        ######################################################################
        #Engine para vector de imágenes#
        def Prediccion():
            ##################################################################
            #For para tratar cada imagen del vector VectImg#
            VectImg.reverse()
            for img in range(0,len(VectImg)):
            ##################################################################
                #Tratamiento de imagen para input de redes neuronales#
                image2 = cv2.resize(VectImg[img-1], dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
                image2= img_to_array(image2)
                image2 = image2.reshape((1,image2.shape[0], image2.shape[1], image2.shape[2]))
                ##################################################################
                #Engine#
                vanova = model1.predict(image2)
                if np.argmax(vanova) == 0:
                    label1 = "Not empty with: "
                    botola = model2.predict(image2)
                    if np.argmax(botola) == 0:
                        label2 = "A bottle of "
                        esbot = model3.predict(image2)
                        if  np.argmax(esbot) == 0:
                            label3 = "Coca Cola."
                            VectComp.append(8)
                        elif np.argmax(esbot) == 1:
                            label3 = "Coca Cola Light."
                            VectComp.append(9)
                        elif np.argmax(esbot) == 2:
                            label3 = "Apple Joya."
                            VectComp.append(11)
                        elif np.argmax(esbot) == 3:
                            label3 = "Pepsi."
                            VectComp.append(10)
                        elif np.argmax(esbot) == 4:
                            label3 = "Sprite."
                            VectComp.append(13)
                        elif np.argmax(esbot) == 5:
                            label3 = "Squirt."
                            VectComp.append(12)
                    elif np.argmax(botola) == 1:
                        label2 = "Can of "
                        eslat = model4.predict(image2)
                        if  np.argmax(eslat) == 0:
                            label3 = "Arizona."
                            VectComp.append(3)
                        elif np.argmax(eslat) == 1:
                            label3 = "Boost."
                            VectComp.append(4)
                        elif np.argmax(eslat) == 2:
                            label3 = "Coca Cola."
                            VectComp.append(1)
                        elif np.argmax(eslat) == 3:
                            label3 = "Coca Cola Light."
                            VectComp.append(2)
                        elif np.argmax(eslat) == 4:
                            label3 = "Monster."
                            VectComp.append(6)
                        elif np.argmax(eslat) == 5:
                            label3 = "Rockstar."
                            VectComp.append(5)
                        elif np.argmax(eslat) == 6:
                            label3 = "VitaminWater."
                            VectComp.append(7)
                    label = Label(self, text= "Prediction number "+str(img+1)+": "+label1+label2+label3)
                    label.grid(row=img+1, column=2)
                elif np.argmax(vanova) == 1:
                    label = Label(self, text= "Prediction number "+str(img+1)+": The segmented space is empty.")
                    label.grid(row=img+1, column=2)
                    VectComp.append(0)
        #Botón para determinar la predicción
        button5 = ttk.Button(self, text="Run Prediction multiple", command=Prediccion)
        button5.grid(row=2, column=0)
        ######################################################################
        #Función para comparar lo que es con lo que debería ser#
        def Comparacion():
            for i in range(0,len(VectOrig)):
                if VectOrig[i]==VectComp[i]:
                    label = Label(self, text= "Correcto")
                    label.grid(row=i+1, column=3)
                else:
                    label = Label(self, text= "Error")
                    label.grid(row=i+1, column=3)
                    ##########################################################
        #Botón para realizar la comparación de vectores#
        button5 = ttk.Button(self, text="Compare products with prediction", command=Comparacion)
        button5.grid(row=3, column=0)
        ######################################################################
         #Mostrar imagen segmentada#
        def SegmentationShow():
            global image1
            #Segmentación de imagen
            image1 = image_rot[int(x1.get()):int(x2.get()), int(y1.get()):int(y2.get()), :]
##############################################################################
#Ejecuta la aplicación#
app=PlanogramApp()
app.mainloop()