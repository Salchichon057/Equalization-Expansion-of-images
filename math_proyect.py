import cv2

import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

_MAX_SIZE = (200, 200)
_ALPHA = 1.5
_BETA = 10

class App(ttk.Window):
    def __init__(self):
        super().__init__(
            themename= 'flatly',
            position= [480,0],
            minsize= [960,1020],
            maxsize= [1020,1080])
        self.title('Frame Forge')
        self.geometry('960x1020')
        self.preview_img = None  # Variable to handle a reference to selected Image. Without it, the image will not
        # appear
        self.color_img = None 
        self.output_img = None
        self.filepath = ""
        self.img_to_process = None
        
        self.title_label = ttk.Label(
            self,
            text= 'FRAME FORGE',
            font= ('Franklin Gothic Medium',50, 'bold'),
            anchor='center',
            background= '#0B2447',
            foreground= '#fff'
            )

        # Title layout
        self.title_label.pack(expand= False, side='top' ,fill= 'both')

        # content frame
        self.content_frame = ttk.Frame(self , padding=10)
        frame_menu = ttk.Frame(self.content_frame )
        frame_image = ttk.Frame(self.content_frame, relief= 'groove')

        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.columnconfigure(1, weight=30)
        self.content_frame.rowconfigure(0, weight=1)

        # Content layout
        self.content_frame.pack(expand= True, fill='both')

        # widgets menu
        button_style = ttk.Style()
        button_style.configure('my.TButton', font=('Gill Sans MT', 15))

        select_button = ttk.Button(
            frame_menu,
            text= 'Seleccionar Imagen',
            style= 'my.TButton',
            command=lambda: __open_browse_files())

        equalize_button = ttk.Button(
            frame_menu,
            text= 'Ecualizar Imagen',
            style= 'my.TButton',
            command=lambda: __equalization_image())

        expand_button = ttk.Button(
            frame_menu,
            text= 'Expandir Imagen',
            style= 'my.TButton',
            command=lambda: __expand_image())
        
        
        notebook_data = ttk.Notebook(frame_menu, bootstyle= 'info')
        
        # Data Ecualización
        tab1 = ttk.Frame(notebook_data)
        label_data_eq = ttk.Label(
            tab1,
            text= 'La ecualización de histogramas \nes una técnica de procesamiento\nde imágenes que ajusta la \ndistribución de los valores \nde los píxeles para mejorar\nel contraste y la apariencia\nvisual de una imagen.\nLa técnica se basa en redistribuir\nlas frecuencias de los valores\nde los píxeles en el\nhistograma para expandir\nsu rango de tonalidades.\nEsta técnica es útil para\nmejorar imágenes con poca\ndefinición, con baja luminosidad\no con pobre contraste,\npero puede generar un\naspecto artificial o exagerado\nalgunas imágenes.',
            font=  ('Gill Sans MT',12),
            justify='left')
        
        # Data Expansion
        tab2 = ttk.Frame(notebook_data)
        label_data_exp = ttk.Label(
            tab2,
            text= 'La expansión de histogramas\nes una técnica para mejorar\nla calidad de las imágenes\nmediante la redistribución\n de los valores de los píxeles.\nSe ajusta la distribución\nde los valores en el histograma\npara expandir el rango\nde tonalidades y mejorar\nel contraste. Es útil para mejorar\nimágenes con un rango de \nvalores de píxeles comprimido\no con bajo contraste,\npero debe utilizarse con precaución\npara evitar artefactos o\nruido en la imagen.',
            font=  ('Gill Sans MT',12),
            justify='left')
        
        # Team member layout
        info_text = ttk.Label(
            frame_menu,
            text= 'Trabajo realizado por\n- Steve Roger Castillo Robles\n- Cristian Andrés Quito Igreda\n- Diego Martín Esquivel Aguayo\n- Gerald Patricio Serrano Uchuva\n- Jeramel Melissa Avila Saldaña',
            font= ('Perpetua ',13), 
            justify='left', 
            relief= 'flat',
            padding= 10,
            # background= '#A5D7E8',
            # foreground= '#0B2447',
            bootstyle = 'inverse success')

        frame_menu.columnconfigure(0, weight=1)
        frame_menu.rowconfigure(0, weight=1) # Select button
        frame_menu.rowconfigure(1, weight=1) # Equalize button
        frame_menu.rowconfigure(2, weight=1) # Expand button
        frame_menu.rowconfigure(3, weight=3) # Info Layout
        frame_menu.rowconfigure(4, weight=1) # Team menbers Layout

        # menu layout
        select_button.grid(column=0, row=0, sticky='nswe',padx=10, pady= 5)
        equalize_button.grid(column=0, row=1, sticky='nswe',padx=10, pady= 5)
        expand_button.grid(column=0, row=2, sticky='nswe',padx=10, pady= 5)
        
        label_data_eq.pack()
        label_data_exp.pack()
        notebook_data.add(tab1, text= 'Ecualización')
        notebook_data.add(tab2, text= 'Expansión')
        notebook_data.grid(column=0, row=3,sticky='nswe',padx=5)
        
        info_text.grid(column=0, row=4, padx=10, sticky='wes')
        
        frame_menu.grid(column= 0, row= 0, sticky='nswe')

        # Image widgets
        text1 = ttk.Label(
            frame_image,
            anchor= 'center',
            bootstyle = 'secondary',
            font= ('Segoe UI',15, 'bold'))
        label_color_img = ttk.Label(frame_image)
        
        text2 = ttk.Label(
            frame_image,
            anchor= 'center',
            bootstyle = 'secondary',
            font= ('Segoe UI',15, 'bold'))
        label_selected_img = ttk.Label(frame_image)
        
        text3 = ttk.Label(
            frame_image,
            anchor= 'center',
            bootstyle = 'secondary',
            font= ('Segoe UI',15, 'bold'))
        label_output_image = ttk.Label(frame_image)
        
        # Image layout
        text1.grid(column=0, row= 0 , columnspan=2, sticky='n',pady= 10)
        label_color_img.grid(column=0, row= 1 , columnspan=2)
        
        text2.grid(column=0, row= 2 , columnspan=2, sticky='s')
        label_selected_img.grid(column=0, row= 3, pady= 10)
        
        text3.grid(column=0, row= 4 , columnspan=2, sticky='s')
        label_output_image.grid(column=0, row= 5, pady= 10)

        # Image menu
        frame_image.columnconfigure(0, weight=1)
        frame_image.columnconfigure(1, weight=1)
        frame_image.rowconfigure(0, weight=1) # "Imagen seleccionada"
        frame_image.rowconfigure(1, weight=1) # imagen a color
        frame_image.rowconfigure(2, weight=1) # "Imagen a escala de grises"
        frame_image.rowconfigure(3, weight=1) # grayscale image & histogram
        frame_image.rowconfigure(4, weight=1) # "Imagen ecualizada|expandida"
        frame_image.rowconfigure(5, weight=1) # modified image
        
        # Image functions
        def __verify_selected_image() -> bool:
            if self.img_to_process is None:
                messagebox.showerror(message="Debe de seleccionar una imagen", title="Imagen no seleccionada")
                return False
            else:
                return True

        def __embed_histogram_plot_to_tkinter(img, frame: ttk.Frame, _row: int, _column: int) -> None:

            histogram = cv2.calcHist([img], [0], None, [256], [0, 256])

            # Making the plot for the histogram
            figure = Figure(dpi=50)
            axis = figure.add_subplot(111)
            axis.plot(histogram, color='gray')

            # Embedding plot of matplotlib to Tk
            canvas = FigureCanvasTkAgg(figure, frame)
            canvas.get_tk_widget().grid(row=_row, column=_column)

        def __embed_img_to_tkinter(img) -> None:
            im = Image.fromarray(img)
            im.thumbnail(_MAX_SIZE, Image.Resampling.LANCZOS)
            self.output_img = ImageTk.PhotoImage(image=im)
            label_output_image.config(image=self.output_img)

        def __open_browse_files():
            filepath = filedialog.askopenfilename(initialdir="/",
                                                    title="Select an image",
                                                    filetypes=[("Image files", ("*.jpg*", "*.png*", "*.jpeg*"))])
            self.filepath = filepath  # This is just for testing
            preview_img_loaded = Image.open(filepath)

            preview_img_loaded.thumbnail(_MAX_SIZE, Image.Resampling.LANCZOS)

            self.color_img = ImageTk.PhotoImage(preview_img_loaded)
            
            label_color_img.config(image=self.color_img)
            
            preview_img_loaded = preview_img_loaded.convert("L")

            self.preview_img = ImageTk.PhotoImage(preview_img_loaded)

            label_selected_img.config(image=self.preview_img)

            self.img_to_process = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
            
            text1['text'] = 'Imagen seleccionada'
            text2['text'] = 'Imagen a escala de grises'
            __embed_histogram_plot_to_tkinter(self.img_to_process, frame_image, 3, 1)

        def __equalization_image():
            if __verify_selected_image() is not True:
                return None

            img = cv2.equalizeHist(self.img_to_process)
            text3['text'] = 'Imagen Ecualizada'
            notebook_data.select(tab1)
            __embed_histogram_plot_to_tkinter(img, frame_image, 5, 1)
            __embed_img_to_tkinter(img)

        def __expand_image():
            if __verify_selected_image() is not True:
                return None
            img = cv2.convertScaleAbs(self.img_to_process, alpha=_ALPHA, beta=_BETA)
            text3['text'] = 'Imagen Expandida'
            notebook_data.select(tab2)
            __embed_histogram_plot_to_tkinter(img, frame_image, 5, 1)
            __embed_img_to_tkinter(img)

        frame_image.grid(column=1, row=0 , columnspan= 30 ,sticky='nsew')

myApp = App()
myApp.mainloop()