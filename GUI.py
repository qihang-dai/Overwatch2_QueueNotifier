import tkinter as tk
import threading
from QueueWatcher import QueueWatcher
import time 
import tkinter.messagebox as messagebox
from datetime import datetime

class QueueWatcherGUI:
    def __init__(self):
        self.queue_watcher = QueueWatcher()
        self.root = tk.Tk()
        self.root.title("Overwatch Queue Watcher")
        self.root.iconbitmap("hollow.ico")
        self.root.geometry("600x450")
        self.root.resizable(False, False)
        self.root.configure(background="sky blue")

        # Create a frame to hold the widgets in the right column
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side="right", fill="both", expand=True)
        self.right_frame.configure(background="snow")

        #add current time status label
        self.time_label = tk.Label(self.right_frame, text="Current Time: ", font=("Arial", 10), bg="snow")
        self.time_label.pack()
        self.update_time()

        self.time_spent = 0
        self.time_spent_job = None

        #add Queue status label once start button is clicked
        self.queue_status_label = tk.Label(self.right_frame, text="Queue Time: ", font=("Arial", 12), bg="snow")
        self.queue_status_label.pack()

        # Add a text box to describe how the program works
        description_text = """Default set for Overwatch 1920x1080 resolution. click set position to see which pixel the program is looking at. set offset x and y to adjust the pixel position. click start to start the program."""
        self.description_box = tk.Text(self.right_frame, height=5, width=40, wrap="word", font=("Helvetica", 10), bg="snow", bd = 1)
        self.description_box.insert(tk.END, description_text)
        self.description_box.config(state="disabled")
        self.description_box.pack()

        # Add labels and input fields for the coordinates, receiver email, sender email, and sender password
        x_label = tk.Label(self.right_frame, text="X Coordinate:")
        x_label.pack()

        self.x_input = tk.Entry(self.right_frame)
        self.x_input.insert(0, "0")
        self.x_input.pack()

        y_label = tk.Label(self.right_frame, text="Y Coordinate:")
        y_label.pack()

        self.y_input = tk.Entry(self.right_frame)
        self.y_input.insert(0, "0")
        self.y_input.pack()

        receiver_label = tk.Label(self.right_frame, text="Receiver Email:")
        receiver_label.pack()

        self.receiver_input = tk.Entry(self.right_frame)
        self.receiver_input.pack()

        sender_label = tk.Label(self.right_frame, text="Sender Email:")
        sender_label.pack()

        self.sender_input = tk.Entry(self.right_frame)
        self.sender_input.insert(0, "queuefound@gmail.com")
        self.sender_input.pack()

        password_label = tk.Label(self.right_frame, text="Sender Password:")
        password_label.pack()

        self.password_input = tk.Entry(self.right_frame)
        self.password_input.insert(0, "*******")
        self.password_input.pack()

        # Add the Start, Stop, and Set Position buttons to the right frame
        self.start_button = tk.Button(self.right_frame, text="Start", command=self.start_queue_watcher)
        self.start_button.configure(bg="lightgreen", fg="black", activebackground="white")
        self.start_button.pack()

        self.stop_button = tk.Button(self.right_frame, text="Stop", command=self.stop_queue_watcher, state="disabled")
        self.stop_button.configure(bg="pink", fg="black", activebackground="white")
        self.stop_button.pack()

        self.set_position_button = tk.Button(self.right_frame, text="Set Position", command=self.set_position)
        self.set_position_button.configure(bg="lightyellow", fg="black", activebackground="white")
        self.set_position_button.pack()

        # Add a button to change the background image
        self.current_image_index = 2
        self.image_filenames = ["mercy.gif", "kiroko.gif", "hollow.png"]
        self.change_background_button = tk.Button(self.root, text="Change Background", command=self.change_background)
        self.change_background_button.configure(bg="white", fg="black", activebackground="white")
        self.change_background_button.pack(side="bottom")

        # add a feeling lucky button next to side of change background button
        self.feeling_lucky_button = tk.Button(self.root, text="Feeling Lucky", command=self.feeling_lucky)
        self.feeling_lucky_button.configure(bg="white", fg="black", activebackground="white")
        self.feeling_lucky_button.pack(side="bottom")


        # Add the image to the left of the window
        self.background_image = tk.PhotoImage(file="hollow.png")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.pack(side="left")

        #stop all thread when program is closed
        self.root.protocol("WM_DELETE_WINDOW", self.close_program)


    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_clock)  # update every second
    
    def update_time_spent(self):
        self.time_spent += 1
        self.queue_status_label.config(text="Queue Time: " + str(self.time_spent) + " seconds")
        self.time_spent_job = self.root.after(1000, self.update_time_spent)
    
    def clear_time_spent(self):
        self.time_spent = 0
        self.queue_status_label.config(text="Queue Time: " + str(self.time_spent) + " seconds")
        if self.time_spent_job is not None:
            self.root.after_cancel(self.time_spent_job)
    
    def feeling_lucky(self):
        messagebox.showinfo("Feeling Lucky", "You are feeling lucky today!")
        
    def close_program(self):
        self.queue_watcher.stop()
        self.root.destroy()
    
    def change_background(self):
        # Increment the current image index
        self.current_image_index = (self.current_image_index + 1) % len(self.image_filenames)

        # Load the new image and display it
        self.background_image = tk.PhotoImage(file=self.image_filenames[self.current_image_index])
        self.background_label.configure(image=self.background_image)

    def update_time(self):
        # Get the current time and format it
        current_time = time.strftime('%H:%M:%S')
        # Update the label text
        self.time_label.configure(text="Current time: " + current_time)
        # Schedule the next update in 1 second
        self.root.after(1000, self.update_time)
    
    #check whether the queuewatcher is running every 1 second
    def check_queue_watcher(self):
        if self.queue_watcher.is_queue_alive():
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
        else:
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
        self.root.after(1000, self.check_queue_watcher)

    def start_queue_watcher(self):
        #start count time spent
        self.update_time_spent()

        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        thread = threading.Thread(target=self.queue_watcher.run)
        thread.start()
        # print stop when thread is stopped, make button available
        print("stop")


    def stop_queue_watcher(self):
        self.clear_time_spent()
        self.stop_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.queue_watcher.stop()

    
    def set_position(self):
        self.start_button.config(state="normal")
        x = int(self.x_input.get())
        y = int(self.y_input.get())

        screenshot = self.queue_watcher.get_queueing_image()
        self.queue_watcher.set_position(screenshot, show=True, offset_x=x, offset_y=y)

    def set_email(self):
        receiver = self.receiver_input.get()
        sender = self.sender_input.get()
        password = self.password_input.get()

        self.queue_watcher.set_email(receiver, sender, password)
        
    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    gui = QueueWatcherGUI()
    gui.run()
