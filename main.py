from tkinter import *
import tkinter.font as tkfont
import transnetv2
import os
import cv2
from PIL import Image, ImageTk
import utils


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.project_path = os.getcwd()
        self.video_file = StringVar(master, "test_data/bbc_02_clip.mp4")
        self.video_width = 360
        self.video_height = 288
        self.shot_width = int(self.video_width / 3)
        self.shot_height = int(self.video_height / 3)
        self.select_device = IntVar(master, 1)

        self.current_img = None
        self.current_frame_num = 0
        self.l_img_1 = None
        self.l_img_2 = None
        self.l_img_tmp_frame = None
        self.r_img_1 = None
        self.r_img_2 = None
        self.r_img_tmp_frame = None
        self.video_run_flag = False

        self.run_success = False
        self.predictions = None
        self.predictions_init = None
        self.scenes = None
        self.scenes_init = None
        self.truth_shots = None

        self.createWidgets()
        self.updateButtonStates(["black", "black", "gray", "black", "gray", "gray"])  # initial state
        self.pack()


    def say_hi(self):
            newWindow = Toplevel(self)

            newWindow.title("Tutorial")
            newWindow.geometry("900x380")

            self.t1 = Label(newWindow, text="Tutorial")
            self.t1["font"] = tkfont.Font(size=16, weight=tkfont.BOLD)
            self.t1.pack(padx=20, pady=20)

            texts = ["Files prepared: Original video (MP4 format recommended)\n",
                     "                         label files of SBD (Same directory as video. Named as \"VIDEO_NAME+.truth.txt\")\n",
                     "Process:   Input location of video file. (Need to provide relative path from current work directory) --> \n",
                     "                Select \"Device Select\" (Recommend default) --> Click \"Shot boundary detection\" --> \n",
                     "                Wait for the evaluation of the model (until `SBD success` appears in cmd) --> \n",
                     "                Click \"Visualize\" --> You can click \"Start\" or \"Pause\" while video is playing --> Click \"Quit\" "
                     ]
            for i in range(len(texts)):
                label = Label(newWindow, text=texts[i])
                label["font"] = tkfont.Font(size=12)
                label.pack(anchor=W, padx=20, pady=2)


    def run_TransnetV2(self):
        print("Running TransNet V2 evaluation ...")
        self.hint["text"] = "Running TransNet V2 evaluation, please wait..."
        self.hint.update()

        self.video_file.set(self.wg_video_file.get("0.0", "end").strip("\n"))  # update video_file
        path = self.project_path + "/" + str(self.video_file.get())

        if self.select_device.get() == 2:
            tf_device = "/cpu:0"
        elif self.select_device.get() == 3:
            tf_device = "/gpu:0"
        else:
            tf_device = ""

        self.predictions_init, self.scenes_init, self.run_success = transnetv2.main_process(
                [path], None, True, tf_device)

        if self.run_success:
            self.updateButtonStates(["black", "black", "black", "black", "gray", "gray"])  # ready to test state
            self.hint["text"] = "SBD success."
            self.hint.update()
            print("Evaluation finished. SBD success.")
        else:
            self.hint["text"] = "SBD failed."
            self.hint.update()
            print("Evaluation finished. SBD failed.")


    def createWidgets(self):
        self.wg_title_1 = Label(self)
        self.wg_title_1["text"] = "Visualization of Shot Boundary Detection based on TransNet V2"
        self.wg_title_1["font"] = tkfont.Font(size=18, weight=tkfont.BOLD)
        self.wg_title_1.grid(row=0, rowspan=1, column=0, columnspan=10, pady=15)

        self.wg_title_2 = Label(self)
        self.wg_title_2["text"] = "Author: Tomáš Souček     Modified: Shallwe"
        self.wg_title_2["font"] = tkfont.Font(size=16, weight=tkfont.BOLD)
        self.wg_title_2.grid(row=1, rowspan=1, column=0, columnspan=10, pady=15)

        self.hi_there = Button(self)
        self.hi_there["text"] = "Tutorial"
        self.hi_there["font"] = tkfont.Font(size=11)
        self.hi_there["command"] = self.say_hi        
        self.hi_there.grid(row=3, rowspan=2, column=1, columnspan=1, padx=15)

        self.wg_video_title = Label(self)
        self.wg_video_title["text"] = "Video file path"
        self.wg_video_title["font"] = tkfont.Font(size=12)
        self.wg_video_title.grid(row=2, rowspan=1, column=2, columnspan=1, padx=10)

        self.wg_video_file = Text(self, width=25, height=3, wrap=WORD, show=None)
        self.wg_video_file.insert('0.0', self.video_file.get())
        self.wg_video_file.grid(row=3, rowspan=3, column=2, columnspan=1, padx=5)

        self.wg_button_start = Button(self)
        self.wg_button_start["text"] = "Shot boundary detection"
        self.wg_button_start["font"] = tkfont.Font(size=11)
        self.wg_button_start["command"] = self.run_TransnetV2
        self.wg_button_start.grid(row=3, rowspan=2, column=3, columnspan=1, padx=10)

        self.wg_button_show = Button(self)
        self.wg_button_show["text"] = "Visualize"
        self.wg_button_show["font"] = tkfont.Font(size=11)
        self.wg_button_show["command"] = self.video_get
        self.wg_button_show.grid(row=3, rowspan=2, column=4, columnspan=1, padx=15)



        self.wg_device = Label(self)
        self.wg_device["text"] = "Device selection"
        self.wg_device["font"] = tkfont.Font(size=12)
        self.wg_device.grid(row=2, column=5, padx=5)

        self.wg_device_1 = Radiobutton(self, text='Default', variable=self.select_device, value=1).grid(row=3, column=5, padx=5)
        self.wg_device_2 = Radiobutton(self, text='Use CPU', variable=self.select_device, value=2).grid(row=4, column=5, padx=5)
        self.wg_device_3 = Radiobutton(self, text='Use GPU', variable=self.select_device, value=3).grid(row=5, column=5, padx=5)

        self.wg_button_quit = Button(self)
        self.wg_button_quit["text"] = "Quit"
        self.wg_button_quit["font"] = tkfont.Font(size=11)
        self.wg_button_quit["command"] = self.quit
        self.wg_button_quit.grid(row=3, rowspan=2, column=6, columnspan=1, padx=15)


        # Video playing part
        self.video_instr = Label(self)
        self.video_instr["text"] = "         Original Video   (3X speed)"
        self.video_instr["font"] = tkfont.Font(size=14)
        self.video_instr.grid(row=6, rowspan=1, column=3, columnspan=1, pady=5)

        self.video_window = Canvas(self, bg="white", width=self.video_width, height=self.video_height)
        self.video_window.grid(row=7, rowspan=4, column=2, columnspan=4, padx=10)

        self.video_start_button = Button(self, text='Start', width=5)
        self.video_start_button["font"] = tkfont.Font(size=11)
        self.video_start_button.grid(row=8, rowspan=1, column=1, columnspan=2, padx=5)
        self.video_start_button.bind("<ButtonRelease-1>", self.start_video)

        self.video_stop_button = Button(self, text='Pause', width=5)
        self.video_stop_button["font"] = tkfont.Font(size=11)
        self.video_stop_button.grid(row=9, rowspan=1, column=1, columnspan=2, padx=5)
        self.video_stop_button.bind("<ButtonRelease-1>", self.stop_video)

        self.sbd_l_instr = Label(self)
        self.sbd_l_instr["text"] = "True shot boundary"
        self.sbd_l_instr["font"] = tkfont.Font(size=14)
        self.sbd_l_instr.grid(row=11, rowspan=1, column=1, columnspan=3, pady=10)

        self.sbd_l_sb = Canvas(self, bg="white", width=self.shot_width*2+10, height=self.shot_height)
        self.sbd_l_sb.grid(row=12, rowspan=1, column=1, columnspan=3, padx=5)

        self.sbd_r_instr = Label(self)
        self.sbd_r_instr["text"] = "Detected shot boundary"
        self.sbd_r_instr["font"] = tkfont.Font(size=14)
        self.sbd_r_instr.grid(row=11, rowspan=1, column=4, columnspan=2, pady=10)

        self.sbd_r_sb = Canvas(self, bg="white", width=self.shot_width*2+10, height=self.shot_height)
        self.sbd_r_sb.grid(row=12, rowspan=1, column=4, columnspan=2, padx=5)

        self.sbd_prediction = Label(self)
        self.sbd_prediction["text"] = "SBD Prob:  0.0%"
        self.sbd_prediction["font"] = tkfont.Font(size=13)
        self.sbd_prediction.grid(row=13, rowspan=1, column=4, columnspan=2, pady=10)

        self.hint = Label(self)
        self.hint["text"] = ""
        self.hint["fg"] = "blue"
        self.hint["font"] = tkfont.Font(size=14)
        self.hint.grid(row=15, rowspan=1, column=0, columnspan=10, pady=10)



    def updateButtonStates(self, button_colors):
        buttons = [self.hi_there, self.wg_button_start, self.wg_button_show,
                   self.wg_button_quit, self.video_start_button, self.video_stop_button]
        for i in range(len(buttons)):
            buttons[i]["fg"] = button_colors[i]
            if button_colors[i] == "gray":
                buttons[i]['state'] = DISABLED
            else:
                buttons[i]['state'] = NORMAL


    def start_video(self, event):
        self.video_run_flag = True
        self.video_loop(self.cap)

    def stop_video(self, event):
        self.video_run_flag = False


    # Get Video Info
    def video_get(self):
        path = self.project_path + "/" + str(self.video_file.get())  # video file path
        self.cap = cv2.VideoCapture(path)  # get video through VideoCapture

        assert self.cap.isOpened() == True
        assert self.run_success == True

        self.truth_shots = utils.read_scenes(path + ".truth.txt", "\t")

        self.wait_time = 1000 / 3 / self.cap.get(5)  # set 3x speed
        self.video_run_flag = True

        self.hint["text"] = "Displaying result..."
        self.hint.update()
        # re-init
        self.current_frame_num = 0
        self.scenes = self.scenes_init
        self.predictions = self.predictions_init
        self.l_img_1 = None
        self.l_img_2 = None
        self.l_img_tmp_frame = None
        self.r_img_1 = None
        self.r_img_2 = None
        self.r_img_tmp_frame = None
        self.updateButtonStates(["black", "gray", "gray", "black", "black", "black"])  # testing state
        self.video_loop(self.cap)


    # Loop of Playing Video
    def video_loop(self, cap):
        ret, frame = cap.read()  # read a frame

        if ret:
            for _ in range(1):  # just for break
                # get image
                self.current_img = utils.print_tk_image(self.video_window, frame, self.video_width, self.video_height)

                # process prediction
                if self.scenes[0][0] == self.current_frame_num:
                    self.r_img_tmp_frame = frame
                elif self.scenes[0][1] == self.current_frame_num:
                    self.r_img_1 = utils.print_tk_image(self.sbd_r_sb, self.r_img_tmp_frame, self.shot_width, self.shot_height)
                    self.r_img_2 = utils.print_tk_image(self.sbd_r_sb, frame, self.shot_width, self.shot_height, pos_x=self.shot_width+10)
                    if len(self.scenes) <= 1:
                        break
                    self.scenes = self.scenes[1:]

                if self.truth_shots[0][0] == self.current_frame_num:
                    self.l_img_tmp_frame = frame
                elif self.truth_shots[0][1] == self.current_frame_num:
                    self.l_img_1 = utils.print_tk_image(self.sbd_l_sb, self.l_img_tmp_frame, self.shot_width, self.shot_height)
                    self.l_img_2 = utils.print_tk_image(self.sbd_l_sb, frame, self.shot_width, self.shot_height, pos_x=self.shot_width+10)
                    if len(self.truth_shots) <= 1:
                        break
                    self.truth_shots = self.truth_shots[1:]

                # get max prob of 4 frames to observe it easier
                if self.current_frame_num % 4 == 3:
                    pred_sbd = max([self.predictions[self.current_frame_num  ][0],
                                    self.predictions[self.current_frame_num-1][0],
                                    self.predictions[self.current_frame_num-2][0],
                                    self.predictions[self.current_frame_num-3][0]])
                    self.sbd_prediction["text"] = "            Probability:  {:5.1f}%".format(pred_sbd*100)

            self.current_frame_num += 1
            if self.video_run_flag:
                self.after(int(self.wait_time), lambda: self.video_loop(cap))  # make the loop here

        else:  # video finished
            self.hint["text"] = "Display ended."
            self.hint.update()
            self.updateButtonStates(["black", "black", "black", "black", "gray", "gray"])  # initial state




def main():
    root = Tk()
    root.geometry("1080x790+500+150")
    root.resizable(False, False)
    root.title("Visualizetion of Shot Boundary Detection based on TransNet V2")

    app = Application(master=root)
    app.mainloop()


    print("Program end.")



if __name__ == '__main__':
    main()
