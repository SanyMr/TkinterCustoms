import tkinter as tk
import platform

class ScrollFrame(tk.Frame):
    def __init__(self, parent, width=400, height=300, **kwargs):
        super().__init__(parent, **kwargs)
        self.width = width
        self.height = height
        # Set the size of this frame explicitly
        self.config(width=width, height=height)
        self.pack_propagate(False)
        
        # Create a canvas with the provided width and height
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff",
                                width=width, height=height)
        # Create an internal frame to hold child widgets
        self.viewPort = tk.Frame(self.canvas, background="#ffffff")
        # Create vertical scrollbar linked to the canvas
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        
        # Pack scrollbar and canvas
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        # Add the internal frame to the canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.viewPort, anchor="nw")
        
        # Bind events to update the scroll region
        self.viewPort.bind("<Configure>", self.onFrameConfigure)
        self.canvas.bind("<Configure>", self.onCanvasConfigure)
        
        # Bind mouse wheel scrolling events
        self.viewPort.bind('<Enter>', self.onEnter)
        self.viewPort.bind('<Leave>', self.onLeave)
    
    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame.'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def onCanvasConfigure(self, event):
        '''Adjust the inner frame's width to match the canvas width.'''
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def onMouseWheel(self, event):
        '''Cross-platform mouse wheel support.'''
        if platform.system() == 'Windows':
            self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")
        elif platform.system() == 'Darwin':
            self.canvas.yview_scroll(-1 * int(event.delta), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
    
    def onEnter(self, event):
        '''Bind mouse wheel when entering the viewPort.'''
        if platform.system() == 'Linux':
            self.canvas.bind_all("<Button-4>", self.onMouseWheel)
            self.canvas.bind_all("<Button-5>", self.onMouseWheel)
        else:
            self.canvas.bind_all("<MouseWheel>", self.onMouseWheel)
    
    def onLeave(self, event):
        '''Unbind mouse wheel when leaving the viewPort.'''
        if platform.system() == 'Linux':
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        else:
            self.canvas.unbind_all("<MouseWheel>")

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scrollable Frame Example")
    
    # Create a ScrollFrame with a fixed width and height
    scroll_frame = ScrollFrame(root, width=400, height=300)
    scroll_frame.pack(fill="both", expand=True)
    
    # Add some sample widgets to the scroll frame's viewPort
    for i in range(50):
        label = tk.Label(scroll_frame.viewPort, text=f"Label {i}", borderwidth=1, relief="solid")
        label.grid(row=i, column=0, padx=5, pady=5)
        btn = tk.Button(scroll_frame.viewPort, text=f"Button {i}")
        btn.grid(row=i, column=1, padx=5, pady=5)
    
    root.mainloop()
