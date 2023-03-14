from tkinter import ttk, filedialog
import tkinter
from PIL import ImageTk, Image, ImageDraw
from TreeviewFrame import TreeviewFrame
import os
import Tooltip as Tooltip
import BinaryImageZigzagHomology
import cv2 as cv2
import shutil

class App:

    def __init__(self):
        # Tkinter GUI initialization and properties
        self.root = tkinter.Tk()
        self.root.minsize(width=100, height=100)
        self.root.resizable(width=0, height=0)
        self.root.title("ZigZag persistence for image processing")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.content = tkinter.Frame(self.root)
        self.GUI()
        self.content.grid(column=0, row=0)
        self.root.mainloop()


    def GUI(self):
        # Parameters initialitation
        self.interval_length = tkinter.IntVar(value=1)
        self.generator_min_length = tkinter.IntVar(value=1)
        self.generator_max_length = tkinter.IntVar(value=100)
        self.num_images = 10

        ###########
        # TOOLBAR #
        ###########
        toolbar = ttk.Frame(self.content)
        toolbar.grid(row=0, column=0, sticky="nwse", padx=10, pady=10)


        openImages = Image.open(r'icons/open-images.png')
        openImages = openImages.resize((72, 72), Image.LANCZOS)
        openImages = ImageTk.PhotoImage(openImages)
        openImagesButton = ttk.Button(toolbar, image=openImages, style='flat.TButton', command=self.open_images)
        openImagesButton.image = openImages
        Tooltip.CreateToolTip(openImagesButton, text='Open images')
        openImagesButton.grid(row=0, column=0)

        openVideo = Image.open(r'icons/open-video.png')
        openVideo = openVideo.resize((72, 72), Image.LANCZOS)
        openVideo = ImageTk.PhotoImage(openVideo)
        openVideoButton = ttk.Button(toolbar, image=openVideo, style='flat.TButton')
        openVideoButton.image = openVideo
        Tooltip.CreateToolTip(openVideoButton, text='Open video')
        openVideoButton.grid(row=0, column=1)

        save_images = Image.open(r'icons/save_images.png')
        save_images = save_images.resize((72, 72), Image.LANCZOS)
        save_images = ImageTk.PhotoImage(save_images)
        save_images_Button = ttk.Button(toolbar, image=save_images, style='flat.TButton', command=self.save_images)
        save_images_Button.image = save_images
        Tooltip.CreateToolTip(save_images_Button, text='Save images')
        save_images_Button.grid(row=0, column=2)

        save_generators = Image.open(r'icons/save_generators.png')
        save_generators = save_generators.resize((72, 72), Image.LANCZOS)
        save_generators = ImageTk.PhotoImage(save_generators)
        save_generators_Button = ttk.Button(toolbar, image=save_generators, style='flat.TButton')
        save_generators_Button.image = save_generators
        Tooltip.CreateToolTip(save_generators_Button, text='Save generators')
        save_generators_Button.grid(row=0, column=3)

        ###########
        # Options #
        ###########

        options = ttk.Labelframe(self.content, text="Options")
        options.grid(row=1, column=1, sticky = "news", padx=10, pady=10)

        dimensiones = ttk.Labelframe(options, text="Dimensions")
        dimensiones.grid(row=0, column=0, sticky="we", padx=10, pady=10)
        self.checkbox_n0_value = tkinter.BooleanVar(value="True")
        self.checkbox_n1_value = tkinter.BooleanVar(value="True")
        checkbox_n0 = ttk.Checkbutton(dimensiones, text="n = 0", variable=self.checkbox_n0_value)
        checkbox_n1 = ttk.Checkbutton(dimensiones, text="n = 1", variable=self.checkbox_n1_value)
        checkbox_n0.grid(row=0, column=0, padx=10, pady=10)
        checkbox_n1.grid(row=1, column=0, padx=10, pady=10)

        parameters = ttk.Labelframe(options, text="Parameters")
        parameters.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        IntervalLabel = ttk.Label(parameters, text="Interval length")
        IntervalSpinBox = ttk.Spinbox(parameters, from_=1.0, to=self.num_images, increment=1, textvariable=self.interval_length)

        IntervalLabel.grid(row=0, column=0, sticky="w", padx=10, pady=10)
        IntervalSpinBox.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        generator_min_lenth_Label = ttk.Label(parameters, text="Generators min length")
        generator_min_lenth_SpinBox = ttk.Spinbox(parameters, from_=1.0, increment=1, to=9999999,
                                      textvariable=self.generator_min_length)

        generator_min_lenth_Label.grid(row=1, column=0, sticky="w", padx=10, pady=10)
        generator_min_lenth_SpinBox.grid(row=1, column=1, sticky="e", padx=10, pady=10)

        generator_max_lenth_Label = ttk.Label(parameters, text="Generators max length")
        generator_max_lenth_SpinBox = ttk.Spinbox(parameters, from_=1, increment=1, to=9999999,
                                      textvariable=self.generator_max_length)

        generator_max_lenth_Label.grid(row=2, column=0, sticky="w", padx=10, pady=10)
        generator_max_lenth_SpinBox.grid(row=2, column=1, sticky="e", padx=10, pady=10)

        generators = ttk.Labelframe(options, text="Generators")
        generators.grid(row=2, column=0, sticky="we", padx=10, pady=10)

        self.show_generators = tkinter.BooleanVar()
        checkbox_show_generators = ttk.Checkbutton(generators, text="Show Generators", variable=self.show_generators)
        checkbox_show_generators.grid(row=0, column=0, sticky="news", padx=10, pady=10)

        ###########
        # Run button #
        ###########

        run_Button = ttk.Button(options, text="Run", style='flat.TButton', width=40, command=self.run)
        run_Button.grid(row=3, column=0, padx=10, pady=10, ipady=10)

        Tooltip.CreateToolTip(run_Button, padx=60, pady=50, text='Run zigzag persistence')

        ###############
        # Information #
        ###############

        self.info_string = tkinter.StringVar(value="No results currently. Click on the tool bar\nto open images or videos.")

        information_label = ttk.Labelframe(options, text="Information")
        information_label.grid(row=4, column=0, sticky="wes", padx=10, pady=10)
        information= ttk.Label(information_label, textvariable=self.info_string)
        information.grid(padx=10, pady=10, ipady=100)


        ############
        # Treeview #
        ############
        treeview_frame_container = ttk.Labelframe(self.content, text="Result")
        treeview_frame_container.grid(row=1, column=0, sticky="news", padx=10, pady=10)

        self.treeview_frame = TreeviewFrame(treeview_frame_container)
        self.treeview_frame.treeview.config(columns=("A"))

        # Setup column heading
        self.treeview_frame.treeview.heading('#0', text='Image', anchor='center')
        self.treeview_frame.treeview.heading('#1', text='File name', anchor='center')
        #treeview_frame.treeview.heading('#2', text=' B', anchor='center')
        # #0, #01, #02 denotes the 0, 1st, 2nd columns
        s = ttk.Style()
        self.factor_multiplication = 4
        factor_multiplication = self.factor_multiplication # I'M LAZY

        s.configure('Treeview', rowheight=54*factor_multiplication)
        # Setup column
        self.treeview_frame.treeview.column("#0", minwidth=0, width=90*factor_multiplication)
        self.treeview_frame.treeview.column('A', anchor='center', width=200)


        ######################
        # Toolbar edit order #
        ######################

        toolbar_order = ttk.Frame(self.content)
        toolbar_order.grid(row=2, column=0, sticky="nwse", padx=10, pady=10)

        move_up_Button = ttk.Button(toolbar_order, text="Move up", style='flat.TButton', command = self.move_up)
        move_up_Button.grid(row=0, column=0, padx=10, pady=10)

        move_down_Button = ttk.Button(toolbar_order, text="Move down", style='flat.TButton', command = self.move_down)
        move_down_Button.grid(row=0, column=1, padx=10, pady=10)

        delete_Button = ttk.Button(toolbar_order, text="Delete", style='flat.TButton', command = self.delete)
        delete_Button.grid(row=0, column=2, padx=10, pady=10)

        ######################
        #     Tab Control    #
        ######################

        self.tabControl = ttk.Notebook(self.content)
        self.tab0 = None
        self.tab1 = None

        ######################
        #    Aux variables   #
        ######################
        self.dimensions = []
        self.images_opencv = []

        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)


    # On closing: delete the temporal files
    def on_closing(self):
        remove_file('.aux_zigzag0.jpg')
        remove_file('.aux_zigzag1.jpg')
        remove_file('.aux_zigzag0.txt')
        remove_file('.aux_zigzag1.txt')
        self.root.destroy()

    def run(self):
        self.info_string.set("Computing the zigzag persistence.\nPlease wait.")
        # Empiezo a calcular.
        self.dimensions = []
        if self.checkbox_n0_value.get():
            self.dimensions.append(0)
        if self.checkbox_n1_value.get():
            self.dimensions.append(1)

        if not self.checkbox_n0_value.get() and not self.checkbox_n1_value.get():  # If n=0 or n=1 (nothing to compute)
            self.info_string.set("Error: you must select at least one dimension")
        elif not self.images_opencv: # If the list of images is empty
            self.info_string.set("Error: no images (open images or a video)")
        else: # Then, compute:
            self.info_string.set("Computing. Please wait.")
            BinaryImageZigzagHomology.imageListZigzagPlotBar(imageList=self.images_opencv, dimensions=self.dimensions,
                                                             interval_l=self.interval_length.get(), gen_l1=self.generator_min_length.get(),
                                                             gen_l2=self.generator_max_length.get(), printGenerators=self.show_generators.get())


            self.info_string.set("Finished!\n\n\n\nSave the barcodes and/or the generators pressing\nthe corresponding buttons in the toolbar.")
            ## Create tab
            self.treeview_frame.grid_forget()
            self.forget_existing_tabs() # Forget existing tabs


            if 0 in self.dimensions:
                self.tab0 = ttk.Frame(self.content)
                self.tabControl.add(self.tab0, text='n = 0')
                image0 = Image.open(".aux_zigzag0.jpg")
                image0 = ImageTk.PhotoImage(image0)

                tab_label0 = ttk.Label(self.tab0, image=image0)
                tab_label0.image = image0
                tab_label0.grid(column=0, row=0, padx=30, pady=30)
            if 1 in self.dimensions:
                self.tab1 = ttk.Frame(self.content)
                self.tabControl.add(self.tab1, text='n = 1')
                image1 = Image.open(".aux_zigzag1.jpg")
                image1 = ImageTk.PhotoImage(image1)

                tab_label1 = ttk.Label(self.tab1, image=image1)
                tab_label1.image = image1
                tab_label1.grid(column=0, row=0, padx=30, pady=30)

            self.tabControl.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    def update_list_images(self):
        new_images_opencv = []
        new_file_path = []

        # We iterate the current tree. We must update the self.images_opencv list in order to have the images in
        # the same order as the tree.
        for child in self.treeview_frame.treeview.get_children():
            image_name = self.treeview_frame.treeview.item(child)["values"][0]
            index_image = index_containing_substring(self.file_paths_images, image_name)
            new_images_opencv.append(self.images_opencv[index_image]) # Add to the new position the image
            new_file_path.append(self.file_paths_images[index_image])

        self.file_paths_images = new_file_path
        self.images_opencv = new_images_opencv

        # To print the current order
        # for child in self.treeview_frame.treeview.get_children():
        #     print(self.treeview_frame.treeview.item(child)["values"])[0]

    def move_up(self):
        rows = self.treeview_frame.treeview.selection()
        for row in rows:
            self.treeview_frame.treeview.move(row, self.treeview_frame.treeview.parent(row), self.treeview_frame.treeview.index(row)-1)
        self.update_list_images()

    def move_down(self):
        rows = self.treeview_frame.treeview.selection()
        for row in reversed(rows):
            self.treeview_frame.treeview.move(row, self.treeview_frame.treeview.parent(row), self.treeview_frame.treeview.index(row)+1)
        self.update_list_images()

    def delete(self):
        rows = self.treeview_frame.treeview.selection()
        for row in rows:
            self.treeview_frame.treeview.delete(row)
        self.update_list_images()

    def forget_existing_tabs(self):
        # We forget the previous existing tabs:
        if self.tab0 is not None:
            self.tabControl.forget(self.tab0)
            self.tab0 = None
        if self.tab1 is not None:
            self.tabControl.forget(self.tab1)
            self.tab1 = None

    def open_images(self):
        # Delete all (in case it was not empty)
        for i in self.treeview_frame.treeview.get_children():
            self.treeview_frame.treeview.delete(i)

        self.tabControl.grid_forget() # Para que vuelva a aparecer las miniaturas, en caso de que hayamos pulsado Run antes.
        # Nos cargamos también las tabs existentes.
        self.forget_existing_tabs()


        self.file_paths_images = list(filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.pbm")]))
        self.images_miniature = []
        self.images_opencv = []

        for image_path in self.file_paths_images:
            image_miniature = Image.open(image_path)
            image_miniature = image_miniature.resize((76 * self.factor_multiplication, 48 * self.factor_multiplication),
                                                     Image.LANCZOS)
            image_miniature = ImageTk.PhotoImage(image_miniature)
            self.images_miniature.append(image_miniature)
            image_name = os.path.basename(image_path)

            self.treeview_frame.treeview.insert('', 'end', image=image_miniature,
                                           value=(image_name, ))
            image = cv2.imread(image_path, 0)
            self.images_opencv.append(image)

    def save_images(self):
        if not self.dimensions:
            self.info_string.set("Error: no dimensions selected or zigzag persistence not computed")
        else:
            for i in self.dimensions:
                title = "Name for image in dimension " + str(i)
                name = '.aux_zigzag'+str(i)+'.jpg'
                file_name = filedialog.asksaveasfilename(defaultextension=".jpg", title=title, filetypes=[("JPG file", "*.jpg")])
                shutil.copy(name, file_name)

    def save_generators(self):
        if not self.dimensions:
            self.info_string.set("Error: no dimensions selected or zigzag persistence not computed")
        else:
            for i in self.dimensions:
                title = "Name for text file for generators in dimension " + str(i)
                name = '.aux_zigzag'+str(i)+'.txt'
                file_name = filedialog.asksaveasfilename(defaultextension=".txt", title=title, filetypes=[("Text file", "*.txt")])
                shutil.copy(name, file_name)


def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1

def remove_file(file_name):
    try:
        os.remove(file_name)
    except OSError:
        pass


if __name__ == "__main__":
    App()
