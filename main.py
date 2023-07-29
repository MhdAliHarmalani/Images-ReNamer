# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 21:46:50 2023

@author: Mhd Ali Harmalani
"""

import os
import tkinter.filedialog

import tkinter as tk
from PIL import Image, ImageTk


class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("Image ReNamer")
        self.master.geometry("1200x600")

        self.image_folder = ""
        self.images = []
        self.current_image_index = 0

        self.create_widgets()

    def create_widgets(self):
        # Create a label with your name, email, and phone number
        self.contact_label = tk.Label(self.master, text="Developed by Eng. Mohammad Ali Harmalani\nmhdaliharmalani@gmail.com\n+963962400125")
        self.contact_label.pack(pady=10)
        # Create the Choose Folder button
        self.choose_folder_button = tk.Button(self.master, text="Choose Folder", command=self.choose_folder)
        self.choose_folder_button.pack(pady=10)
        
        # Create a label for the Read Me information
        self.readme_label = tk.Label(self.master, text="""
                                    Read Me:\n\n
                                    1. Click on the Choose Folder button to select a folder containing image files.\n
                                    2. Use the Prev and Next buttons or the Left and Right arrow keys to navigate through the images in the folder.\n
                                    3. Type the fixed name in "Default Name Starting" text box, then type the rest of name in "Rename To" text box.\n
                                    4. Click on the Rename button or press Enter key to apply the new name.\n
                                    5. Click on the Change Folder button or press Ctrl+n to select a different folder.\n\n
                                    Shortcuts:\n
                                    - "Ctrl+n": Choose Folder or Change Folder button.  \n
                                    - Left arrow key: Previous image.  \n
                                    - Right arrow key: Next image.  \n
                                    - "Ctrl+r": Select the text box.  \n
                                    - "Ctrl+d": Select the Default Name Starting text box.  \n
                                    - Enter key: Rename image.
                                    """, justify="left", anchor="w")
        self.readme_label.pack(pady=10)
        
        # Bind Ctrl+n to Choose Folder button
        self.master.bind("<Control-n>", lambda event: self.choose_folder_button.invoke())
        
        # Create a label to show the current image name
        self.current_image_label = tk.Label(self.master, text="")
        self.current_image_label.pack()
        
        # Create an error label
        self.error_label = tk.Label(self.master, text="", fg="red")
        self.error_label.pack()
        
        # Bind r key to select the text box
        try:
            self.master.bind("<Control-r>", lambda event: self.select_text_box())
            self.master.bind("<Control-d>", lambda event: self.select_text_box_default())
        except:
            pass

        # Bind a function to the root window to cancel the focus on the text box
        self.master.bind("<Button-1>", lambda event: self.cancel_focus(event))
        
    def choose_folder(self):
        # Open a file dialog to choose the image folder
        self.image_folder = tk.filedialog.askdirectory()
        # Get a list of all the image files in the folder
        self.images = [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        if len(self.images) == 0:
            self.error_label.config(text="Error: There are no images in the folder.")
            return
        else:
            self.error_label.config(text="")
        
        self.contact_label.destroy()
        self.readme_label.destroy()
        
        # Destroy the Choose Folder button
        self.choose_folder_button.destroy()
        # Create the Change Folder button
        self.change_folder_button = tk.Button(self.master, text="Change Folder", command=self.change_folder)
        self.change_folder_button.pack(pady=10)
        # Bind Ctrl+n to Change Folder button
        self.master.bind("<Control-n>", lambda event: self.change_folder_button.invoke())
        # Create the Previous and Next buttons
        self.prev_button = tk.Button(self.master, text="Prev", command=self.show_previous_image)
        self.prev_button.pack(side="left", padx=10, pady=10)
        # Bind left arrow key to Prev button
        self.master.bind("<Left>", lambda event: self.show_previous_image())
        self.next_button = tk.Button(self.master, text="Next", command=self.show_next_image)
        self.next_button.pack(side="right", padx=10, pady=10)
        # Bind right arrow key to Next button
        self.master.bind("<Right>", lambda event: self.show_next_image())
        # Create the Image Label
        self.image_label = tk.Label(self.master)
        self.image_label.pack()
        # Create a frame for text_box, text_box_default, and rename_button
        self.bottom_frame = tk.Frame(self.master)
        self.bottom_frame.pack(side="bottom", pady=10)
        
        # Create the Text Entry box text_box_defulte
        self.text_box_default_label = tk.Label(self.bottom_frame)
        self.text_box_default_label.pack(side="left", padx=10)
        self.text_box_default_label.config(text="Default Name Starting")
        self.text_box_default = tk.Entry(self.bottom_frame)
        self.text_box_default.pack(side="left", padx=10)
        
        # Create the Text Entry box
        self.text_box_label = tk.Label(self.bottom_frame)
        self.text_box_label.pack(side="left", padx=10)
        self.text_box_label.config(text="Rename to")
        self.text_box = tk.Entry(self.bottom_frame)
        self.text_box.pack(side="left", padx=10)
        
        # Create the Rename button
        self.rename_button = tk.Button(self.bottom_frame, text="Rename", command=self.rename_image)
        self.rename_button.pack(side="left", padx=10)
        # Bind Enter key to Rename button
        self.text_box.bind("<Return>", lambda event: self.rename_image())
        # Bind a function to set focus on the text box when it is clicked
        self.text_box.bind("<Button-1>", lambda event: self.select_text_box())
        self.text_box_default.bind("<Button-1>", lambda event: self.select_text_box_default())
        # Display the first image
        self.show_image()

    def change_folder(self):
        # Open a file dialog to choose the image folder
        new_image_folder = tk.filedialog.askdirectory()
        new_images = [os.path.join(new_image_folder, f) for f in os.listdir(new_image_folder) if f.endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        if len(new_images) != 0:
            self.image_folder = new_image_folder
            # Get a list of all the image files in the folder 
            self.images = new_images
            del new_image_folder
            del new_images
            # Reset the current image index
            self.current_image_index = 0
            # Display the first image
            self.show_image()
        else:
            self.error_label.config(text="Error: There are no images in the folder.")
            root.after(6000, self.hide_error_message) # Hide the error message after 3 seconds
        
    def show_image(self):
        # Load the current image and display it
        image = Image.open(self.images[self.current_image_index])
        image = image.resize((700, 550))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        # Update the text box with the current file name without extension
        file_name, ext = os.path.splitext(os.path.basename(self.images[self.current_image_index]))
        self.text_box.delete(0, tk.END)
        # self.text_box.insert(0, file_name)
        # Update the label with the current image name
        self.current_image_label.config(text=f"Current Image: {file_name}{ext}")
    
    
    def show_previous_image(self):
        # Decrement the currentimage index and show the previous image
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.show_image()

    def show_next_image(self):
        # Increment the current image index and show the next image
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            self.show_image()

    def rename_image(self):
        # Get the new name of the image from the text box
        new_name = self.text_box_default.get().strip() + self.text_box.get().strip() 
        # Check if the text box is empty
        if not new_name:
            self.error_label.config(text="Error: Please enter a new name for the image.")     
            root.after(3000, self.hide_error_message) # Hide the error message after 3 seconds
            return
        # Get the file extension of the current image
        _, ext = os.path.splitext(self.images[self.current_image_index])
        # Check if the new name already exists in the folder
        new_path = os.path.join(self.image_folder, new_name + ext)
        if new_path in self.images:
            self.error_label.config(text="Error: The name is already exists in the folder.")
            root.after(3000, self.hide_error_message) # Hide the error message after 3 seconds
            return
        # Rename the file with the new name and the same extension
        os.rename(self.images[self.current_image_index], new_path)
        # Update the list of image paths with the new path
        self.images[self.current_image_index] = new_path
        
        file_name, ext = os.path.splitext(os.path.basename(self.images[self.current_image_index]))
        self.current_image_label.config(text=f"Current Image: {file_name}{ext}")
        # Print the success message in the error label in green color
        self.error_label.config(text="The operation was successful.", fg="green")
        root.after(1000, self.hide_error_message) # Hide the error message after 3 seconds
        
        
    def select_text_box(self):
        # Set the focus on the text box to enable renaming by keyboard input
        self.text_box.focus_set()
    
    def select_text_box_default(self):
        # Set the focus on the text box to enable renaming by keyboard input
        self.text_box_default.focus_set()

    def cancel_focus(self, event):
        try:
            # Check if the event was triggered outside the text box
            if event.widget != self.text_box and event.widget != self.text_box_default:
                # Set the focus to the root window to cancel the focus on the text box
                self.master.focus_set()
        except:
            self.master.focus_set()
            
    def hide_error_message(self):
        self.error_label.config(text="")
        self.error_label.config(fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewer(root)
    root.mainloop()