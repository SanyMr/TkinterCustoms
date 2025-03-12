import tkinter as tk
from tkinter import ttk
import math
from plotter import FunctionPlotter
from scroll_frame import ScrollFrame

class PlotterApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Function Plotter Application")
        self.selected_plotter = None
        # Initialize config_widgets attribute
        self.config_widgets = []
        
        # Create the main panedwindow to divide left and right sections
        self.main_paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Create the left panel for function plots
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=2)  # Give more weight to the plotting area
        
        # Create the right panel for configuration options
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=1)
        
        # Set up the right panel with toolbar and scroll frame for configuration first
        # This ensures config_widgets is properly initialized before add_new_plotter calls update_config_panel
        self.setup_right_panel()
        
        # Set up the left panel with toolbar and scroll frame for plotters
        self.setup_left_panel()
        
    def setup_left_panel(self):
        # Create a frame for the toolbar at the top of the left panel
        self.left_toolbar_frame = ttk.Frame(self.left_frame)
        self.left_toolbar_frame.pack(fill=tk.X, side=tk.TOP)
        
        # Add some example toolbar buttons
        self.add_plotter_btn = ttk.Button(self.left_toolbar_frame, text="Add Plot", command=self.add_new_plotter)
        self.add_plotter_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.remove_plotter_btn = ttk.Button(self.left_toolbar_frame, text="Remove Plot", command=self.remove_selected_plotter)
        self.remove_plotter_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create the scroll frame for the plotters
        self.plotters_scroll_frame = ScrollFrame(self.left_frame)
        self.plotters_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # List to keep track of all plotters
        self.plotters = []
        
        # Add initial plotter
        self.add_new_plotter()
        
    def setup_right_panel(self):
        # Create a frame for the toolbar at the top of the right panel
        self.right_toolbar_frame = ttk.Frame(self.right_frame)
        self.right_toolbar_frame.pack(fill=tk.X, side=tk.TOP)
        
        # Add some example toolbar buttons
        self.apply_config_btn = ttk.Button(self.right_toolbar_frame, text="Apply Config", command=self.apply_configuration)
        self.apply_config_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.reset_config_btn = ttk.Button(self.right_toolbar_frame, text="Reset", command=self.reset_configuration)
        self.reset_config_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create the scroll frame for the configuration options
        self.config_scroll_frame = ScrollFrame(self.right_frame)
        self.config_scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # Add a label indicating no plotter is selected
        self.no_selection_label = ttk.Label(self.config_scroll_frame.viewPort, text="No plotter selected")
        self.no_selection_label.pack(pady=20)
        
        # Initialize configuration widgets list
        self.config_widgets = []
        # Initialize current_config dictionary
        self.current_config = {}
    
    def add_new_plotter(self):
        # Create a frame to hold the plotter and its selection button
        plotter_container = ttk.Frame(self.plotters_scroll_frame.viewPort)
        plotter_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add a selection button
        select_btn = ttk.Button(plotter_container, text="Select", 
                               command=lambda p=plotter_container: self.select_plotter(p))
        select_btn.pack(fill=tk.X, pady=(0, 5))
        
        # Create the function plotter
        plotter = FunctionPlotter(plotter_container, height=300, x_range=(-10, 10), y_range=(-10, 10), 
                                 title=f"Function Plot {len(self.plotters) + 1}")
        plotter.pack(fill=tk.BOTH, expand=True)
        
        # Add a default function
        if len(self.plotters) % 2 == 0:
            plotter.add_function(lambda x: math.sin(x), "sin(x)", "blue")
        else:
            plotter.add_function(lambda x: math.cos(x), "cos(x)", "red")
        
        # Store the plotter along with its container
        self.plotters.append((plotter_container, plotter, select_btn))
        
        # Select the newly added plotter
        self.select_plotter(plotter_container)
    
    def select_plotter(self, plotter_container):
        # Update the selected plotter
        for container, plotter, button in self.plotters:
            if container == plotter_container:
                self.selected_plotter = plotter
                button.configure(text="⭐ Selected")
            else:
                button.configure(text="Select")
        
        # Update the configuration panel
        self.update_config_panel()
    
    def remove_selected_plotter(self):
        if not self.selected_plotter or not self.plotters:
            return
        
        # Find and remove the selected plotter
        for i, (container, plotter, _) in enumerate(self.plotters):
            if plotter == self.selected_plotter:
                # Destroy the container which includes the plotter
                container.destroy()
                # Remove from our list
                self.plotters.pop(i)
                break
        
        # Update selected plotter
        self.selected_plotter = None if not self.plotters else self.plotters[0][1]
        
        # Update selection UI
        if self.plotters:
            self.select_plotter(self.plotters[0][0])
        else:
            self.update_config_panel()
    
    def update_config_panel(self):
        # Clear existing configuration widgets
        for widget in self.config_widgets:
            widget.destroy()
        self.config_widgets = []
        
        # If no plotter is selected, show the placeholder message
        if not self.selected_plotter:
            self.no_selection_label.pack(pady=20)
            return
        
        # Hide the placeholder message
        self.no_selection_label.pack_forget()
        
        # Create configuration options for the selected plotter
        title_label = ttk.Label(self.config_scroll_frame.viewPort, text="Plot Title:")
        title_label.pack(anchor=tk.W, padx=10, pady=(10, 0))
        
        title_entry = ttk.Entry(self.config_scroll_frame.viewPort)
        title_entry.insert(0, self.selected_plotter.title if hasattr(self.selected_plotter, 'title') else "Function Plot")
        title_entry.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        x_range_label = ttk.Label(self.config_scroll_frame.viewPort, text="X Range (min, max):")
        x_range_label.pack(anchor=tk.W, padx=10, pady=(10, 0))
        
        x_range_frame = ttk.Frame(self.config_scroll_frame.viewPort)
        x_range_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        x_min_entry = ttk.Entry(x_range_frame, width=10)
        x_min_entry.insert(0, "-10")
        x_min_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        x_max_entry = ttk.Entry(x_range_frame, width=10)
        x_max_entry.insert(0, "10")
        x_max_entry.pack(side=tk.LEFT)
        
        y_range_label = ttk.Label(self.config_scroll_frame.viewPort, text="Y Range (min, max):")
        y_range_label.pack(anchor=tk.W, padx=10, pady=(10, 0))
        
        y_range_frame = ttk.Frame(self.config_scroll_frame.viewPort)
        y_range_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        y_min_entry = ttk.Entry(y_range_frame, width=10)
        y_min_entry.insert(0, "-10")
        y_min_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        y_max_entry = ttk.Entry(y_range_frame, width=10)
        y_max_entry.insert(0, "10")
        y_max_entry.pack(side=tk.LEFT)
        
        # Add more configuration options as needed
        
        # Store the configuration widgets for later access
        self.config_widgets = [title_label, title_entry, x_range_label, x_range_frame, 
                             y_range_label, y_range_frame]
        
        # Store entry widgets for apply_configuration method
        self.current_config = {
            'title_entry': title_entry,
            'x_min_entry': x_min_entry,
            'x_max_entry': x_max_entry,
            'y_min_entry': y_min_entry,
            'y_max_entry': y_max_entry
        }
    
    def apply_configuration(self):
        if not self.selected_plotter or not hasattr(self, 'current_config'):
            return
        
        # Example of applying configuration - adapt to your FunctionPlotter implementation
        new_title = self.current_config['title_entry'].get()
        try:
            x_min = float(self.current_config['x_min_entry'].get())
            x_max = float(self.current_config['x_max_entry'].get())
            y_min = float(self.current_config['y_min_entry'].get())
            y_max = float(self.current_config['y_max_entry'].get())
            
            # Update the plotter with new configuration
            # Note: These methods will depend on your FunctionPlotter implementation
            if hasattr(self.selected_plotter, 'set_title'):
                self.selected_plotter.set_title(new_title)
            
            if hasattr(self.selected_plotter, 'set_ranges'):
                self.selected_plotter.set_ranges(x_min, x_max, y_min, y_max)
            
            # Redraw the plot
            if hasattr(self.selected_plotter, 'redraw'):
                self.selected_plotter.redraw()
            
        except ValueError:
            # Handle invalid input
            pass
    
    def reset_configuration(self):
        # Reset to default configuration
        if not self.selected_plotter:
            return
        
        self.update_config_panel()  # This will reset the form to current values

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")  # Set an initial size
    app = PlotterApplication(root)
    root.mainloop()
