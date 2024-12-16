import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt

def load_csv():
    """Load a CSV file and display its columns."""
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            global df
            df = pd.read_csv(file_path)
            column_listbox.delete(0, tk.END)
            for column in df.columns:
                column_listbox.insert(tk.END, column)
            messagebox.showinfo("File Loaded", f"CSV file loaded successfully: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

def plot_chart():
    """Plot chart based on selected X and Y columns."""
    try:
        x_column = x_var.get()
        y_column = y_var.get()
        if x_column and y_column:
            plt.figure(figsize=(10, 6))
            plt.plot(df[x_column], df[y_column], marker='o')
            plt.title(f'{y_column} vs {x_column}', fontsize=14)
            plt.xlabel(x_column, fontsize=12)
            plt.ylabel(y_column, fontsize=12)
            plt.grid(True)
            plt.show()
        else:
            messagebox.showwarning("Selection Error", "Please select both X and Y columns.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to plot chart: {e}")

# Create the main application window
root = tk.Tk()
root.title("CSV Plotter")

# Add buttons and labels
frame = tk.Frame(root)
frame.pack(pady=10)

load_button = tk.Button(frame, text="Load CSV", command=load_csv, width=20)
load_button.grid(row=0, column=0, padx=10)

x_label = tk.Label(frame, text="Select X Column:")
x_label.grid(row=1, column=0, pady=5)

x_var = tk.StringVar(root)
x_dropdown = tk.OptionMenu(frame, x_var, ())
x_dropdown.grid(row=1, column=1)

y_label = tk.Label(frame, text="Select Y Column:")
y_label.grid(row=2, column=0, pady=5)

y_var = tk.StringVar(root)
y_dropdown = tk.OptionMenu(frame, y_var, ())
y_dropdown.grid(row=2, column=1)

plot_button = tk.Button(frame, text="Plot Chart", command=plot_chart, width=20)
plot_button.grid(row=3, column=0, columnspan=2, pady=10)

# Add a listbox to display CSV columns
column_frame = tk.Frame(root)
column_frame.pack(pady=5)

column_listbox = tk.Listbox(column_frame, height=10, width=50)
column_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

scrollbar = tk.Scrollbar(column_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

column_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=column_listbox.yview)

# Function to update dropdown menus
def update_dropdowns(*args):
    x_dropdown["menu"].delete(0, "end")
    y_dropdown["menu"].delete(0, "end")
    for col in df.columns:
        x_dropdown["menu"].add_command(label=col, command=tk._setit(x_var, col))
        y_dropdown["menu"].add_command(label=col, command=tk._setit(y_var, col))

# Bind listbox updates to update dropdowns
column_listbox.bind("<<ListboxSelect>>", update_dropdowns)

# Run the application
root.mainloop()
