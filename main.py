from tkinter import ttk, filedialog
import tkinter
from PIL import ImageTk, Image, ImageDraw
from TreeviewFrame import TreeviewFrame
import os
import Tooltip as Tooltip


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
        self.generator_max_length = tkinter.IntVar(value=1)
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

        ###########
        # Options #
        ###########

        options = ttk.Labelframe(self.content, text="Options")
        options.grid(row=1, column=1, sticky = "news", padx=10, pady=10)

        dimensiones = ttk.Labelframe(options, text="Dimensions")
        dimensiones.grid(row=0, column=0, sticky="we", padx=10, pady=10)
        self.checkbox_n0_value = tkinter.BooleanVar()
        self.checkbox_n1_value = tkinter.BooleanVar()
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

        move_up_Button = ttk.Button(toolbar_order, text="Move up", style='flat.TButton', command= self.move_up)
        move_up_Button.grid(row=0, column=0, padx=10, pady=10)

        move_down_Button = ttk.Button(toolbar_order, text="Move down", style='flat.TButton', command= self.move_down)
        move_down_Button.grid(row=0, column=1, padx=10, pady=10)

        delete_Button = ttk.Button(toolbar_order, text="Delete", style='flat.TButton', command= self.delete)
        delete_Button.grid(row=0, column=2, padx=10, pady=10)

        ######################
        #     Tab Control    #
        ######################

        self.tabControl = ttk.Notebook(self.content)

    def run(self):
        self.info_string.set("Computing the zigzag persistence.\nPlease wait.")


        self.info_string.set("Finished!\n\n\n\nSave the barcodes and/or the generators pressing\nthe corresponding buttons in the toolbar.")
        ## Create tab
        self.treeview_frame.grid_forget()

        self.tabControl.grid(row=1, column=0)
        tab1 = ttk.Frame(self.content)
        tab2 = ttk.Frame(self.content)

        self.tabControl.add(tab1, text='n = 0')
        self.tabControl.add(tab2, text='n = 1')
        self.tabControl.grid(sticky="nsew", padx=10, pady=10)

        ttk.Label(tab1,
                  text="Welcome to \
                  GeeksForGeeks").grid(column=0,
                                       row=0,
                                       padx=30,
                                       pady=30)
        ttk.Label(tab2,
                  text="Lets dive into the\
                  world of computers").grid(column=0,
                                            row=0,
                                            padx=30,
                                            pady=30)


    def move_up(self):
        rows = self.treeview_frame.treeview.selection()
        for row in rows:
            self.treeview_frame.treeview.move(row, self.treeview_frame.treeview.parent(row), self.treeview_frame.treeview.index(row)-1)

    def move_down(self):
        rows = self.treeview_frame.treeview.selection()
        for row in reversed(rows):
            self.treeview_frame.treeview.move(row, self.treeview_frame.treeview.parent(row), self.treeview_frame.treeview.index(row)+1)

    def delete(self):
        rows = self.treeview_frame.treeview.selection()
        for row in rows:
            self.treeview_frame.treeview.delete(row)

    def open_images(self):
        # Borramos todo (por si acaso había cosas de antes)
        for i in self.treeview_frame.treeview.get_children():
            self.treeview_frame.treeview.delete(i)

        self.tabControl.grid_forget() # Para que vuelva a aparecer, en caso de que hayamos pulsado Run antes.

        self.file_paths_images = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        self._imgs = []

        for image_path in self.file_paths_images:
            image_miniature = Image.open(r'icons/example.jpg')
            image_miniature = image_miniature.resize((76 * self.factor_multiplication, 48 * self.factor_multiplication),
                                                     Image.LANCZOS)
            image_miniature = ImageTk.PhotoImage(image_miniature)
            self._imgs.append(image_miniature)
            image_name = os.path.basename(image_path)

            self.treeview_frame.treeview.insert('', 'end', image=image_miniature,
                                           value=(image_name, ))


# https://www.youtube.com/watch?v=tvXFpMGlHPk


        # results = ttk.Labelframe(self.content, text="Result")
        # results.grid(row=1, column=0)
        #
        # image_result = Image.open('ur.jpg')
        # image_result = ImageTk.PhotoImage(image_result)
        # resultsLabel = ttk.Label(results, image=image_result, width=300)
        # resultsLabel.image = image_result
        # resultsLabel.grid()
        #
        #
        #






if __name__ == "__main__":
    App()
