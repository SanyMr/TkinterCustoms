import tkinter as tk
import winsound 

class CustomMessageBox(tk.Toplevel):
    def __init__(self, parent, title="Alert", message="This is an alert!",
                 image_path="alert.png",
                 ignore_command=None, ignore_all_command=None, abort_command=None,
                 image_scale=2):
        super().__init__(parent)
        # Enable window decorations so the user sees the title bar with X.
        self.resizable(False, False)
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)

        # Create a frame for a border (optional styling)
        border_frame = tk.Frame(self, bd=2, relief="raised")
        border_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Create a content frame inside the border.
        content = tk.Frame(border_frame, padx=10, pady=10)
        content.pack()

        # Load and scale the alert image.
        try:
            self.alert_image = tk.PhotoImage(file=image_path)
            self.alert_image = self.alert_image.subsample(image_scale, image_scale)
            img_label = tk.Label(content, image=self.alert_image)
            img_label.grid(row=0, column=0, rowspan=2, padx=(0, 10))
        except Exception as e:
            print("Could not load image:", e)

        # Create and pack the message label.
        label = tk.Label(content, text=message, anchor="w", justify="left")
        label.grid(row=0, column=1, sticky="w")

        # Frame to hold the buttons.
        btn_frame = tk.Frame(content)
        btn_frame.grid(row=1, column=1, pady=(10, 0), sticky="e")

        # Assign provided commands or default ones.
        self.ignore_command = ignore_command if ignore_command else self.default_ignore
        self.ignore_all_command = ignore_all_command if ignore_all_command else self.default_ignore_all
        self.abort_command = abort_command if abort_command else self.default_abort

        # Create the buttons and assign their callbacks.
        ignore_btn = tk.Button(btn_frame, text="Ignore", width=10, command=self.ignore_command)
        ignore_all_btn = tk.Button(btn_frame, text="Ignore All", width=10, command=self.ignore_all_command)
        abort_btn = tk.Button(btn_frame, text="Abort", width=10, command=self.abort_command)

        ignore_btn.pack(side=tk.LEFT, padx=5)
        ignore_all_btn.pack(side=tk.LEFT, padx=5)
        abort_btn.pack(side=tk.LEFT, padx=5)

        # Center the messagebox over the parent window.
        self.update_idletasks()
        self.center(parent)
        # Make the dialog modal.
        self.grab_set()

    def center(self, parent):
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        width = self.winfo_width()
        height = self.winfo_height()
        x = parent_x + (parent_width // 2) - (width // 2)
        y = parent_y + (parent_height // 2) - (height // 2)
        self.geometry(f"+{x}+{y}")

    def on_close(self):
        # This is called when the user clicks the X button.
        # You could choose to call one of your commands here if desired.
        print("close button clicked!")
        self.destroy()

    def default_ignore(self):
        print("Default: Ignore pressed")

    def default_ignore_all(self):
        print("Default: Ignore All pressed")

    def default_abort(self):
        print("Default: Abort pressed")

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    def custom_ignore():
        print("Custom: Ignore action executed.")

    def custom_ignore_all():
        print("Custom: Ignore All action executed.")

    def custom_abort():
        print("Custom: Abort action executed.")

    msg_box = CustomMessageBox(
        root,
        title="Custom Alert",
        message="Alert! Something needs your attention.",
        image_path="danger.png",  # Ensure this file exists or adjust the path.
        image_scale=10,
        ignore_command=custom_ignore,
        ignore_all_command=custom_ignore_all,
        abort_command=custom_abort
    )
    
    
    root.mainloop()
