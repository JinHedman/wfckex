from tkinter import *
from tkinter import ttk
from Input import *
from PIL import Image
from Rule_creation import *
from DrawFast import *
from WFC_color import *
import matplotlib.pyplot as plt
import random
import string
import os

class GUI:
    def __init__(self, run_test_wfc):
        self.get_files()
        self.testwfc = run_test_wfc

    def run(self):
        root = Tk()
        frm = ttk.Frame(root, padding=20)
        frm.grid()
        ttk.Label(frm, text="WFC").grid(column=0, row=0)

        self.btn_runtest = ttk.Button(frm, text="run test", command=self.testwfc, width=20, state=DISABLED)
        self.btn_runtest.grid(column=0, row=1)

        ttk.Label(frm, text="").grid(column=0, row=2)
        ttk.Label(frm, text="Draw size (x and y), and N").grid(column=0, row=3)
        self.entryX = ttk.Entry(frm,width=3)
        self.entryY = ttk.Entry(frm, width=3)
        self.entryX.insert(0, "15")
        self.entryY.insert(0, "15")
        self.entryX.grid(column=0, row=4)
        self.entryY.grid(column=0, row=5)

        self.entryN = ttk.Entry(frm, width=3)
        self.entryN.insert(0, "7,7")
        self.entryN.grid(column=0, row=6)



        self.btn_drawinput = ttk.Button(frm, text="draw input", command=self.inputbutton, width=20, state=NORMAL)
        self.btn_drawinput.grid(column=0, row=7)
        self.lbl_status = ttk.Label(frm, text="")
        self.lbl_status.grid(column=0, row=8)
        self.btn_runwfc = ttk.Button(frm, text="run WFC with map", command=self.wfc, width=20, state=DISABLED)
        self.btn_runwfc.grid(column=0, row=9)
        self.btn_save = ttk.Button(frm, text="Save map", command=self.savemap, width=20, state=DISABLED)
        self.btn_save.grid(column=0, row=10)
        ttk.Label(frm, text="").grid(column=0, row=11)

        self.cmb_maps = ttk.Combobox(frm,values=list(self.get_files().keys()))
        self.cmb_maps.grid(column = 0, row = 12)
        self.cmb_maps.bind("<<ComboboxSelected>>", self.cmb_select)


        self.btn_loadmap = ttk.Button(frm, text="load map", command=self.load_map, width=20, state=DISABLED)
        self.btn_loadmap.grid(column=0, row=13)
        self.btn_show = ttk.Button(frm, text="show loaded image", command=self.show_map, width=20, state=DISABLED)
        self.btn_show.grid(column=0, row=14)

        ttk.Label(frm, text="").grid(column=0, row=19)
        self.btn_quit = ttk.Button(frm, text="Quit", command=root.destroy, width=20)
        self.btn_quit.grid(column=0, row=20)

        root.mainloop()

    #When Draw map button is pressed,
    def inputbutton(self):
        self.resolution = [int(x) for x in self.entryN.get().split(",")]
        drawinput = draw_input((int(self.entryX.get()), int(self.entryY.get())), self.resolution)

        self.grid = drawinput.Input().transpose((1,0,2))
        self.lbl_status.config(text = "Costum map loaded")
        self.btn_runwfc["state"] = NORMAL
        self.btn_save["state"] = NORMAL
        self.btn_show["state"] = NORMAL

    # load map selected in combobox
    def load_map(self):
        path = self.get_files()[self.cmb_maps.get()]
        image = Image.open(path)
        array = np.array(image)
        self.grid = array
        self.lbl_status.config(text = self.cmb_maps.get() + " loaded")
        self.btn_runwfc["state"] = NORMAL
        self.btn_show["state"] = NORMAL
        #self.resolution = int(self.entryN.get().split(","))

    def cmb_select(self, changed):
        self.btn_loadmap["state"] = NORMAL

    def show_map(self):
        draw = DrawFast(self.grid.transpose((1,0,2)))
        draw.draw_once(self.grid.transpose((1,0,2)))

    def wfc(self):
        rulecreation = Rule_creation()
        self.resolution = [int(x) for x in self.entryN.get().split(",")]
        self.tiles, self.probability_list = rulecreation.create_set(self.grid, self.resolution)

        self.field = get_field((int(self.entryX.get()), int(self.entryY.get())), self.tiles)
        main_draw = DrawFast(convert_to_array_advance(self.field, self.tiles))
        main_draw.update(convert_to_array_advance(self.field, self.tiles))
        wfc = WFC_color(self.field, self.tiles, self.probability_list, main_draw)

    def savemap(self):
        im = Image.fromarray(self.grid)
        im.save("maps/map_" + self.get_random_string(3) + ".bmp")

    def get_random_string(self, length):
        # choose from all lowercase letter
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    def get_files(self):
        files = {}
        directory = 'maps'
        for file in os.scandir(directory):
            if file.is_file() and file.name.endswith(".bmp"):
                files[file.name] = file.path
        return files


