import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

class PDFSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Splitter")
        self.root.geometry("400x300")
        self.root.configure(bg='sky blue')
        self.pdf_path = None

        # Set icon to a book icon (if available)
        try:
            self.root.iconbitmap('books.ico')  # Use 'books.ico' if you have an icon file
        except:
            pass

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        help_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Browse Button
        self.browse_btn = tk.Button(self.root, text="Browse PDF", command=self.browse_pdf, bg='grey', fg='white', font=('Arial', 12))
        self.browse_btn.pack(pady=10)

        # Page Count Label
        self.page_count_label = tk.Label(self.root, text="Pages: 0", bg='sky blue', fg='black', font=('Arial', 12))
        self.page_count_label.pack(pady=5)

        # Split Options
        self.option_var = tk.StringVar(value="1")
        self.option_frame = tk.Frame(self.root, bg='sky blue')
        self.option_frame.pack(pady=10)

        self.radio_every_page = tk.Radiobutton(self.option_frame, text="Split every page", variable=self.option_var, value="1", bg='sky blue', fg='black', font=('Arial', 10), command=self.update_entries)
        self.radio_every_page.grid(row=0, column=0, sticky='w')

        self.radio_every_n_pages = tk.Radiobutton(self.option_frame, text="Split every N pages", variable=self.option_var, value="2", bg='sky blue', fg='black', font=('Arial', 10), command=self.update_entries)
        self.radio_every_n_pages.grid(row=1, column=0, sticky='w')

        self.radio_by_range = tk.Radiobutton(self.option_frame, text="Split by ranges", variable=self.option_var, value="3", bg='sky blue', fg='black', font=('Arial', 10), command=self.update_entries)
        self.radio_by_range.grid(row=2, column=0, sticky='w')

        # Entry for N pages
        self.entry_n_pages = tk.Entry(self.option_frame, width=5)
        self.entry_n_pages.grid(row=1, column=1, padx=20)

        # Entry for ranges
        self.entry_ranges = tk.Entry(self.option_frame, width=20)
        self.entry_ranges.grid(row=2, column=1, padx=20)

        # Split Button
        self.split_btn = tk.Button(self.root, text="Split PDF", command=self.split_pdf, bg='grey', fg='white', font=('Arial', 12))
        self.split_btn.pack(pady=10)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bg='sky blue', fg='black', font=('Arial', 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.update_entries()

    def update_entries(self):
        option = self.option_var.get()
        self.radio_every_page.config(fg='black')
        self.radio_every_n_pages.config(fg='black')
        self.radio_by_range.config(fg='black')

        if option == "1":
            self.entry_n_pages.config(state='disabled')
            self.entry_ranges.config(state='disabled')
            self.radio_every_page.config(fg='dark blue')
            self.status_var.set("Selected Option: Split every page")
        elif option == "2":
            self.entry_n_pages.config(state='normal')
            self.entry_ranges.config(state='disabled')
            self.radio_every_n_pages.config(fg='dark blue')
            self.status_var.set("Selected Option: Split every N pages")
        elif option == "3":
            self.entry_n_pages.config(state='disabled')
            self.entry_ranges.config(state='normal')
            self.radio_by_range.config(fg='dark blue')
            self.status_var.set("Selected Option: Split by ranges")

    def browse_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            reader = PdfReader(self.pdf_path)
            self.page_count_label.config(text=f"Pages: {len(reader.pages)}")

    def split_pdf(self):
        if not self.pdf_path:
            messagebox.showerror("Error", "Please select a PDF file first.")
            return
        
        save_dir = filedialog.askdirectory()
        if not save_dir:
            return

        reader = PdfReader(self.pdf_path)
        total_pages = len(reader.pages)

        option = self.option_var.get()
        if option == "1":
            self.split_every_page(reader, save_dir)
        elif option == "2":
            try:
                n_pages = int(self.entry_n_pages.get())
                self.split_every_n_pages(reader, save_dir, n_pages)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number for N pages.")
        elif option == "3":
            try:
                ranges = self.entry_ranges.get()
                self.split_by_ranges(reader, save_dir, ranges)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid ranges.")

        messagebox.showinfo("Success", "PDF split successfully!")

    def split_every_page(self, reader, save_dir):
        for i in range(len(reader.pages)):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            output_filename = os.path.join(save_dir, f"{os.path.splitext(os.path.basename(self.pdf_path))[0]} - {i+1}.pdf")
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)

    def split_every_n_pages(self, reader, save_dir, n):
        for i in range(0, len(reader.pages), n):
            writer = PdfWriter()
            for j in range(i, min(i + n, len(reader.pages))):
                writer.add_page(reader.pages[j])
            output_filename = os.path.join(save_dir, f"{os.path.splitext(os.path.basename(self.pdf_path))[0]} - {i//n + 1}.pdf")
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)

    def split_by_ranges(self, reader, save_dir, ranges):
        range_list = ranges.split(',')
        for idx, r in enumerate(range_list):
            if '-' in r:
                start, end = map(int, r.split('-'))
            else:
                start = end = int(r)
            writer = PdfWriter()
            for i in range(start-1, end):
                writer.add_page(reader.pages[i])
            output_filename = os.path.join(save_dir, f"{os.path.splitext(os.path.basename(self.pdf_path))[0]} - {idx + 1}.pdf")
            with open(output_filename, "wb") as output_pdf:
                writer.write(output_pdf)

    def show_about(self):
        messagebox.showinfo("About", "PDF Splitter\n\nCreated by Fayez Eloraby\nMade with the help of Chat GPT")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
