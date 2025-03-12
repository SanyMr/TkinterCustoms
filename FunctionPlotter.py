import tkinter as tk
from tkinter import ttk
import math
import tkinter.messagebox
import uuid

class FunctionPlotter(tk.Frame):
    def __init__(self, master=None, app=None, width=400, height=300, x_range=(-10, 10), y_range=(-10, 10), title="Function Plot", **kwargs):
        super().__init__(master, **kwargs)
        self.app = app
        self.width = width
        self.height = height
        self.x_range = x_range
        self.y_range = y_range
        self.title = title
        self.curves = []  # List to store multiple curves (function, name, color)
        self.grid_spacing = 1  # Distance between grid lines
        self.init_ui()
        
        # Create a unique ID for this plotter
        self.id = str(uuid.uuid4())[:8]
        
    def init_ui(self):
        # Create a frame for the header with title and check button
        self.header_frame = tk.Frame(self)
        self.header_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        # Create selection variable
        self.selected_var = tk.BooleanVar(value=False)
        
        # Check button for selection
        self.select_check = tk.Checkbutton(self.header_frame, variable=self.selected_var, 
                                          command=self.on_select_changed)
        self.select_check.pack(side=tk.LEFT, padx=5)
        
        # Create a title label
        self.title_label = tk.Label(self.header_frame, text=self.title, font=("Arial", 10, "bold"))
        self.title_label.pack(side=tk.LEFT, fill=tk.X, padx=5)
        
        # Canvas for plotting
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas.bind("<Configure>", self.resize)
        # Border for selection
        self.configure(relief=tk.GROOVE, borderwidth=1)
        
        # Initial plot with empty axes
        self.draw_grid()
    
    def find_app(self, widget):
        while widget is not None:
            if hasattr(widget, 'select_plotter'):
                return widget
            widget = widget.master
        return None

        
    def on_select_changed(self):
        app = self.find_app(self)
        if app is not None:
            is_selected = self.selected_var.get()
            if is_selected:
                app.select_plotter(self)
            else:
                if app.selected_plotter == self:
                    self.selected_var.set(True)
    
    def set_selected(self, is_selected):
        self.selected_var.set(is_selected)
        self.configure(
            relief=tk.RAISED if is_selected else tk.GROOVE,
            borderwidth=3 if is_selected else 1
        )
        
    def draw_grid(self):
        self.canvas.delete("all")  # Clear canvas
        
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        # If canvas hasn't been drawn yet, use the initial values
        if width <= 1:
            width, height = self.width, self.height
        
        # Draw grid lines
        x_min, x_max = self.x_range
        y_min, y_max = self.y_range
        
        # Calculate pixel per unit
        x_scale = width / (x_max - x_min)
        y_scale = height / (y_max - y_min)
        
        # Vertical grid lines (x-axis)
        x = x_min
        while x <= x_max:
            canvas_x = (x - x_min) * x_scale
            # Draw light gray grid lines
            if abs(x) > 0.01:  # Not the y-axis
                self.canvas.create_line(canvas_x, 0, canvas_x, height, fill="#E0E0E0", dash=(2, 4))
            # Draw x-axis labels
            if abs(x) >= self.grid_spacing or abs(x) < 0.01:
                self.canvas.create_text(canvas_x, height - 10, text=str(round(x, 1)), fill="gray")
            x += self.grid_spacing
        
        # Horizontal grid lines (y-axis)
        y = y_min
        while y <= y_max:
            canvas_y = height - (y - y_min) * y_scale  # Invert y-coordinate
            # Draw light gray grid lines
            if abs(y) > 0.01:  # Not the x-axis
                self.canvas.create_line(0, canvas_y, width, canvas_y, fill="#E0E0E0", dash=(2, 4))
            # Draw y-axis labels
            if abs(y) >= self.grid_spacing or abs(y) < 0.01:
                self.canvas.create_text(10, canvas_y, text=str(round(y, 1)), fill="gray", anchor=tk.W)
            y += self.grid_spacing
        
        # Draw x-axis
        if y_min <= 0 <= y_max:
            y_axis_pos = height - (0 - y_min) * y_scale
            self.canvas.create_line(0, y_axis_pos, width, y_axis_pos, fill="black", width=2)
            self.canvas.create_text(width - 20, y_axis_pos - 10, text="x", fill="black")
        
        # Draw y-axis
        if x_min <= 0 <= x_max:
            x_axis_pos = (0 - x_min) * x_scale
            self.canvas.create_line(x_axis_pos, 0, x_axis_pos, height, fill="black", width=2)
            self.canvas.create_text(x_axis_pos + 10, 20, text="y", fill="black")
        
        # Draw all existing curves
        for func, name, color in self.curves:
            self.plot_function(func, name, color)
        
        # Draw legend
        self.draw_legend()
    
    def draw_legend(self):
        if not self.curves:
            return
        
        # Calculate legend position and dimensions
        legend_width = 120
        legend_height = len(self.curves) * 20 + 10
        legend_x = self.canvas.winfo_width() - legend_width - 10
        legend_y = 10
        
        # Draw legend background
        self.canvas.create_rectangle(legend_x, legend_y, 
                                     legend_x + legend_width, legend_y + legend_height,
                                     fill="white", outline="gray")
        
        # Draw legend entries
        for i, (_, name, color) in enumerate(self.curves):
            y_pos = legend_y + 10 + i * 20
            # Draw line sample
            self.canvas.create_line(legend_x + 10, y_pos, legend_x + 30, y_pos, fill=color, width=2)
            # Draw curve name
            self.canvas.create_text(legend_x + 40, y_pos, text=name, fill="black", anchor=tk.W)
    
    def plot_function(self, func, name, color):
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        if width <= 1:
            width, height = self.width, self.height
            
        x_min, x_max = self.x_range
        y_min, y_max = self.y_range
        
        # Calculate pixel per unit
        x_scale = width / (x_max - x_min)
        y_scale = height / (y_max - y_min)
        
        # Number of points to plot
        num_points = width
        
        points = []
        for i in range(num_points):
            x = x_min + (x_max - x_min) * i / (num_points - 1)
            try:
                y = func(x)
                # Skip points outside the y-range
                if y < y_min or y > y_max:
                    if points:  # Add this check to avoid creating separate lines
                        self.canvas.create_line(points, fill=color, width=2)
                        points = []
                    continue
                
                canvas_x = (x - x_min) * x_scale
                canvas_y = height - (y - y_min) * y_scale  # Invert y-coordinate
                points.append(canvas_x)
                points.append(canvas_y)
            except (ValueError, ZeroDivisionError):
                # Handle discontinuities
                if points:
                    self.canvas.create_line(points, fill=color, width=2)
                    points = []
                
        # Draw the collected points
        if points:
            self.canvas.create_line(points, fill=color, width=2)
    
    def add_function(self, func, name=None, color=None):
        """Add a function to plot"""
        if name is None:
            name = f"Function {len(self.curves) + 1}"
        if color is None:
            colors = ["blue", "red", "green", "purple", "orange", "brown"]
            color = colors[len(self.curves) % len(colors)]
            
        self.curves.append((func, name, color))
        self.update_plot()
    
    def remove_function(self, index):
        """Remove a function by index"""
        if 0 <= index < len(self.curves):
            del self.curves[index]
            self.update_plot()
            return True
        return False
    
    def update_plot(self):
        """Update the plot with current settings"""
        self.draw_grid()
    
    def clear_all(self):
        """Clear all curves"""
        self.curves = []
        self.update_plot()
    
    def set_title(self, title):
        """Set the title of the plot"""
        self.title = title
        self.title_label.config(text=title)
    
    def set_ranges(self, x_range=None, y_range=None, grid_spacing=None):
        """Set the x and y ranges for the plot"""
        if x_range is not None:
            self.x_range = x_range
        if y_range is not None:
            self.y_range = y_range
        if grid_spacing is not None:
            self.grid_spacing = grid_spacing
        self.update_plot()
    
    def resize(self, event=None):
        """Handle resize events"""
        self.update_plot()


class MultiPlotterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multi-Function Plotter")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        self.selected_plotter = None
        self.plotters = []
        
        self.create_widgets()
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        # Create main frame that expands with window
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create top toolbar
        self.toolbar = tk.Frame(self.main_frame, height=40, bg="#f0f0f0")
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Add toolbar buttons
        self.add_btn = tk.Button(self.toolbar, text="Add Plot", command=self.add_plotter)
        self.add_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.delete_btn = tk.Button(self.toolbar, text="Delete Selected", command=self.delete_selected)
        self.delete_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create content area with two panes
        self.content = tk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.content.pack(fill=tk.BOTH, expand=True)
        
        # Left pane for plots (with scrolling)
        self.plot_container_frame = tk.Frame(self.content)
        self.content.add(self.plot_container_frame, width=800, stretch="always")
        
        # Create a canvas for scrolling
        self.plot_canvas = tk.Canvas(self.plot_container_frame, bg="#f5f5f5")
        self.plot_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to canvas
        self.plot_scrollbar = tk.Scrollbar(self.plot_container_frame, orient=tk.VERTICAL, command=self.plot_canvas.yview)
        self.plot_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.plot_canvas.configure(yscrollcommand=self.plot_scrollbar.set)
        
        # Create a frame inside the canvas to hold the plots
        self.plot_frame = tk.Frame(self.plot_canvas, bg="#f5f5f5")
        self.plot_canvas_window = self.plot_canvas.create_window((0, 0), window=self.plot_frame, anchor=tk.NW)
        
        # Right pane for configuration
        self.config_frame = tk.Frame(self.content, bg="#e8e8e8")
        self.content.add(self.config_frame, width=300)
        
        # Create configuration widgets
        self.create_config_widgets()
        
        # Bind scroll events
        self.plot_frame.bind("<Configure>", self.on_plot_frame_configure)
        self.plot_canvas.bind("<Configure>", self.on_canvas_configure)
        
    def create_config_widgets(self):
        # Label for configuration section
        tk.Label(self.config_frame, text="Plot Configuration", font=("Arial", 12, "bold"), 
                 bg="#e8e8e8").pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Frame for configuration controls
        config_controls = tk.Frame(self.config_frame, bg="#e8e8e8")
        config_controls.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Plot Title
        tk.Label(config_controls, text="Plot Title:", bg="#e8e8e8").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_var = tk.StringVar(value="Function Plot")
        title_entry = tk.Entry(config_controls, textvariable=self.title_var)
        title_entry.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)
        
        # X Range
        tk.Label(config_controls, text="X Range:", bg="#e8e8e8").grid(row=1, column=0, sticky=tk.W, pady=5)
        range_frame = tk.Frame(config_controls, bg="#e8e8e8")
        range_frame.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)
        
        self.x_min_var = tk.DoubleVar(value=-10)
        self.x_max_var = tk.DoubleVar(value=10)
        tk.Entry(range_frame, textvariable=self.x_min_var, width=6).pack(side=tk.LEFT, padx=2)
        tk.Label(range_frame, text="to", bg="#e8e8e8").pack(side=tk.LEFT, padx=2)
        tk.Entry(range_frame, textvariable=self.x_max_var, width=6).pack(side=tk.LEFT, padx=2)
        
        # Y Range
        tk.Label(config_controls, text="Y Range:", bg="#e8e8e8").grid(row=2, column=0, sticky=tk.W, pady=5)
        range_frame = tk.Frame(config_controls, bg="#e8e8e8")
        range_frame.grid(row=2, column=1, sticky=tk.W+tk.E, pady=5)
        
        self.y_min_var = tk.DoubleVar(value=-10)
        self.y_max_var = tk.DoubleVar(value=10)
        tk.Entry(range_frame, textvariable=self.y_min_var, width=6).pack(side=tk.LEFT, padx=2)
        tk.Label(range_frame, text="to", bg="#e8e8e8").pack(side=tk.LEFT, padx=2)
        tk.Entry(range_frame, textvariable=self.y_max_var, width=6).pack(side=tk.LEFT, padx=2)
        
        # Grid Spacing
        tk.Label(config_controls, text="Grid Spacing:", bg="#e8e8e8").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.grid_var = tk.DoubleVar(value=1.0)
        tk.Entry(config_controls, textvariable=self.grid_var, width=6).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Apply button
        self.apply_btn = tk.Button(config_controls, text="Apply Changes", command=self.apply_config)
        self.apply_btn.grid(row=4, column=0, columnspan=2, pady=10)
        self.apply_btn.config(state=tk.DISABLED)
        
        # Section for current functions
        tk.Label(config_controls, text="Current Functions", font=("Arial", 11, "bold"), 
                bg="#e8e8e8").grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        # Frame for function list
        self.function_list_frame = tk.Frame(config_controls, bg="#e8e8e8")
        self.function_list_frame.grid(row=6, column=0, columnspan=2, sticky=tk.W+tk.E, pady=5)
        
        # Section for adding functions
        tk.Label(config_controls, text="Add Function", font=("Arial", 11, "bold"), 
                bg="#e8e8e8").grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(20, 5))
        
        # Function entry
        tk.Label(config_controls, text="f(x) =", bg="#e8e8e8").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.func_var = tk.StringVar(value="math.sin(x)")
        self.func_entry = tk.Entry(config_controls, textvariable=self.func_var)
        self.func_entry.grid(row=8, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Function name
        tk.Label(config_controls, text="Name:", bg="#e8e8e8").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.func_name_var = tk.StringVar(value="")
        self.func_name_entry = tk.Entry(config_controls, textvariable=self.func_name_var)
        self.func_name_entry.grid(row=9, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Function color
        tk.Label(config_controls, text="Color:", bg="#e8e8e8").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.func_color_var = tk.StringVar(value="blue")
        self.func_color_combo = ttk.Combobox(config_controls, textvariable=self.func_color_var, 
                                          values=["blue", "red", "green", "purple", "orange", "brown"], 
                                          state="readonly")
        self.func_color_combo.grid(row=10, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Add function button
        self.add_func_btn = tk.Button(config_controls, text="Add Function", command=self.add_function)
        self.add_func_btn.grid(row=11, column=0, columnspan=2, pady=10)
        self.add_func_btn.config(state=tk.DISABLED)
        
        # Clear functions button
        self.clear_btn = tk.Button(config_controls, text="Clear All Functions", command=self.clear_functions)
        self.clear_btn.grid(row=12, column=0, columnspan=2, pady=5)
        self.clear_btn.config(state=tk.DISABLED)
        
        # Set column weights
        config_controls.columnconfigure(1, weight=1)
    
    def on_plot_frame_configure(self, event):
        """Update the scrollregion when the plot frame changes size"""
        self.plot_canvas.configure(scrollregion=self.plot_canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        """Resize the window inside the canvas when the canvas changes size"""
        # Update the width of the plot frame to fill the canvas
        self.plot_canvas.itemconfig(self.plot_canvas_window, width=event.width)
    
    def on_resize(self, event):
        """Handle window resize"""
        # Only process if it's the main window being resized
        if event.widget == self:
            # Update all plotters
            for plotter in self.plotters:
                plotter.resize()
    
    def add_plotter(self):
        title = f"Plot {len(self.plotters) + 1}"
        plotter = FunctionPlotter(self.plot_frame, app=self, title=title)
        plotter.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.plotters.append(plotter)
        plotter.add_function(lambda x: math.sin(x), "sin(x)", "blue")
        self.select_plotter(plotter)
    
    def delete_selected(self):
        """Delete the selected plotter"""
        if self.selected_plotter:
            # Remove from list
            self.plotters.remove(self.selected_plotter)
            # Destroy widget
            self.selected_plotter.destroy()
            # Clear selection
            self.selected_plotter = None
            # Disable config buttons
            self.apply_btn.config(state=tk.DISABLED)
            self.add_func_btn.config(state=tk.DISABLED)
            self.clear_btn.config(state=tk.DISABLED)
            # Clear function list
            self.update_function_list()
    
    def select_plotter(self, plotter):
        # Deselect all plotters first
        for p in self.plotters:
            if p != plotter:
                p.set_selected(False)
        
        # Update selected plotter reference
        self.selected_plotter = plotter
        
        if plotter:
            plotter.set_selected(True)
            self.update_config_fields(plotter)
            self.update_function_list()
            self.toggle_config_buttons(True)
        else:
            self.toggle_config_buttons(False)
            self.update_function_list()
    
    def update_function_list(self):
        for widget in self.function_list_frame.winfo_children():
            widget.destroy()
        
        if self.selected_plotter:
            for i, (_, name, color) in enumerate(self.selected_plotter.curves):
                self.create_function_entry(i, name, color)
    
    def create_function_entry(self, index, name, color):
        func_frame = tk.Frame(self.function_list_frame, bg="#e8e8e8")
        func_frame.pack(fill=tk.X, pady=2)
        
        color_indicator = tk.Frame(func_frame, width=10, height=10, bg=color)
        color_indicator.pack(side=tk.LEFT, padx=5)
        
        tk.Label(func_frame, text=name, bg="#e8e8e8").pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            func_frame, 
            text="X", 
            command=lambda idx=index: self.remove_function(idx),
            width=2, 
            relief=tk.FLAT
        ).pack(side=tk.RIGHT, padx=5)
    
    def remove_function(self, index):
        """Remove a function from the selected plotter"""
        if self.selected_plotter:
            if self.selected_plotter.remove_function(index):
                self.update_function_list()
    
    def apply_config(self):
        """Apply configuration to selected plotter"""
        if not self.selected_plotter:
            return
        
        try:
            # Get values from config
            title = self.title_var.get()
            x_min = self.x_min_var.get()
            x_max = self.x_max_var.get()
            y_min = self.y_min_var.get()
            y_max = self.y_max_var.get()
            grid_spacing = self.grid_var.get()
            
            # Validate ranges
            if x_min >= x_max:
                raise ValueError("X minimum must be less than X maximum")
            if y_min >= y_max:
                raise ValueError("Y minimum must be less than Y maximum")
            if grid_spacing <= 0:
                raise ValueError("Grid spacing must be positive")
            
            # Apply to plotter
            self.selected_plotter.set_title(title)
            self.selected_plotter.set_ranges(
                x_range=(x_min, x_max),
                y_range=(y_min, y_max),
                grid_spacing=grid_spacing
            )
        except ValueError as e:
            tk.messagebox.showerror("Invalid Input", str(e))
    
    def add_function(self):
        """Add a function to the selected plotter"""
        if not self.selected_plotter:
            return
        
        try:
            # Get function from entry
            func_str = self.func_var.get()
            name = self.func_name_var.get()
            color = self.func_color_var.get()
            
            # Use default name if empty
            if not name:
                name = f"Function {len(self.selected_plotter.curves) + 1}"
            
            # Create function
            func = lambda x: eval(func_str, {"math": math, "x": x})
            
            # Add to plotter
            self.selected_plotter.add_function(func, name, color)
            
            # Clear entries
            self.func_name_var.set("")
            
            # Update function list
            self.update_function_list()
        except Exception as e:
            tk.messagebox.showerror("Invalid Function", f"Error: {str(e)}")
    
    def clear_functions(self):
        """Clear all functions from the selected plotter"""
        if self.selected_plotter:
            self.selected_plotter.clear_all()
            self.update_function_list()

    def update_config_fields(self, plotter):
        self.title_var.set(plotter.title)
        self.x_min_var.set(plotter.x_range[0])
        self.x_max_var.set(plotter.x_range[1])
        self.y_min_var.set(plotter.y_range[0])
        self.y_max_var.set(plotter.y_range[1])
        self.grid_var.set(plotter.grid_spacing)
    
    def toggle_config_buttons(self, state):
        state = tk.NORMAL if state else tk.DISABLED
        self.apply_btn.config(state=state)
        self.add_func_btn.config(state=state)
        self.clear_btn.config(state=state)

if __name__ == "__main__":
    """app = MultiPlotterApp()
    app.mainloop()"""

    root = tk.Tk()

    plotter1 = FunctionPlotter(root, width=400, height=300, x_range=(-10, 10), y_range=(-10, 10), title="Function Plot")
    plotter1.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    plotter1.add_function(lambda x: math.sin(x), "sin(x)", "blue")

    plotter2 = FunctionPlotter(root, width=400, height=300, x_range=(-10, 10), y_range=(-10, 10), title="Function Plot")
    plotter2.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    plotter2.add_function(lambda x: math.cos(x), "cos(x)", "red")

    root.mainloop()
