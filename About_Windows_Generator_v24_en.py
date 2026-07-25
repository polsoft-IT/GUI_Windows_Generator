import os
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import customtkinter as ctk
import webbrowser
from PIL import Image

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AboutDialog(ctk.CTkToplevel):
    def __init__(self, parent, logo_path, logo_size):
        super().__init__(parent)
        self.title("About - Generator")
        self.geometry("450x450")
        self.resizable(False, False)
        self.configure(fg_color="#1a1a1a")
        
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (450 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (450 // 2)
        self.geometry(f"450x450+{x}+{y}")
        
        self.grab_set()

        if logo_path and os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                img.thumbnail((logo_size, logo_size))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                ctk.CTkLabel(self, image=ctk_img, text="").pack(pady=(25, 10))
            except:
                self.show_default_icon()
        else:
            self.show_default_icon()

        ctk.CTkLabel(self, text="About Window Generator", font=("Arial", 20, "bold"), text_color="#ffffff").pack(pady=(5, 2))
        ctk.CTkLabel(self, text="Version v24.0.0", font=("Arial", 12), text_color="#808080").pack(pady=(0, 15))

        desc_text = "An advanced tool for visual design, real-time previewing, and generating clean, modern 'About' windows for the CustomTkinter library."
        ctk.CTkLabel(self, text=desc_text, font=("Arial", 13), text_color="#e0e0e0", wraplength=390, justify="center").pack(pady=10, padx=20)

        info_frame = ctk.CTkFrame(self, fg_color="#242424", corner_radius=8, width=390, height=100)
        info_frame.pack(pady=15, padx=20, fill="x")
        info_frame.pack_propagate(False)

        ctk.CTkLabel(info_frame, text="Author: Sebastian Januchowski", font=("Arial", 12, "bold"), text_color="#ffffff").pack(pady=(8, 2))
        ctk.CTkLabel(info_frame, text="Company: polsoft.ITS™ Group", font=("Arial", 11), text_color="#aaaaaa").pack(pady=1)

        links_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        links_frame.pack(pady=5)

        github_lbl = ctk.CTkLabel(links_frame, text="GitHub", font=("Arial", 11, "underline"), text_color="#3498db", cursor="hand2")
        github_lbl.pack(side="left", padx=10)
        github_lbl.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/polsoft-IT"))

        email_lbl = ctk.CTkLabel(links_frame, text="Send Email", font=("Arial", 11, "underline"), text_color="#3498db", cursor="hand2")
        email_lbl.pack(side="left", padx=10)
        email_lbl.bind("<Button-1>", lambda e: webbrowser.open("mailto:polsoft.its@mail.com"))

        ctk.CTkButton(self, text="Close", fg_color="#3a3a3a", text_color="#ffffff", hover_color="#4a4a4a", width=120, command=self.destroy).pack(pady=(10, 20), side="bottom")

    def show_default_icon(self):
        ctk.CTkLabel(self, text="ℹ", font=("Arial", 48), text_color="#3498db").pack(pady=(25, 10))


class AboutGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("About Window Generator v24 - Dynamic Links Edition")
        self.geometry("950x820")
        self.resizable(True, True)

        # Text data variables
        self.logo_path = ""
        self.app_name = ctk.StringVar(value="My Application")
        self.version = ctk.StringVar(value="v1.0.0")
        self.author = ctk.StringVar(value="Author: John Doe")
        self.description = ctk.StringVar(value="A short description of your awesome application. Resize the window with your mouse to see how the text wraps perfectly in the generated file.")
        
        # Dynamic list storing link data
        self.links = []

        # About window dimensions
        self.win_width = ctk.StringVar(value="400")
        self.win_height = ctk.StringVar(value="500")

        # Logo size
        self.logo_size = 80

        # Style dictionaries for standard fields
        self.font_sizes = {
            "app_name": 22, "version": 12, "description": 14, "author": 12
        }
        self.font_colors = {
            "app_name": "#ffffff", "version": "#808080", "description": "#ffffff", "author": "#aaaaaa"
        }
        
        self.bg_color = "#242424"
        self.btn_close_bg = "#3a3a3a"    
        self.btn_close_fg = "#ffffff"    
        
        self.active_field = "app_name"
        self.active_link_index = None

        self.drag_start_x = 0
        self.drag_start_y = 0
        self.drag_start_w = 400
        self.drag_start_h = 500
        
        self.inner_preview = None
        self.desc_label = None
        self._updating_from_entry = False
        
        for var in [self.app_name, self.version, self.author, self.description]:
            var.trace_add("write", lambda *args: self.update_preview())
            
        self.win_width.trace_add("write", self._on_entry_dimension_change)
        self.win_height.trace_add("write", self._on_entry_dimension_change)

        # Initialize default link (URL, display label)
        self.add_link_data("https://github.com/user", "Visit GitHub")

        self.setup_menubar()
        self.setup_ui()
        self.create_context_menu()

    def add_link_data(self, default_url="", default_label=""):
        var_url = ctk.StringVar(value=default_url)
        var_label = ctk.StringVar(value=default_label)
        
        var_url.trace_add("write", lambda *args: self.update_preview())
        var_label.trace_add("write", lambda *args: self.update_preview())
        
        link_item = {
            "var": var_url,
            "label_var": var_label,
            "size": 12,
            "color": "#3498db"
        }
        self.links.append(link_item)

    def setup_menubar(self):
        self.menubar = tk.Menu(self, bg="#2b2b2b", fg="#ffffff", activebackground="#34495e", activeforeground="#ffffff", bd=0)
        
        file_menu = tk.Menu(self.menubar, tearoff=0, bg="#2b2b2b", fg="#ffffff", activebackground="#34495e", activeforeground="#ffffff", bd=0)
        file_menu.add_command(label="Select Logo", command=self.load_logo)
        file_menu.add_command(label="Generate about.py File", command=self.generate_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="File", menu=file_menu)
        
        edit_menu = tk.Menu(self.menubar, tearoff=0, bg="#2b2b2b", fg="#ffffff", activebackground="#34495e", activeforeground="#ffffff", bd=0)
        edit_menu.add_command(label="Cut", command=lambda: self.focus_get().event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", command=lambda: self.focus_get().event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", command=lambda: self.focus_get().event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Bold (Unicode)", command=lambda: self.apply_unicode_style("bold"))
        edit_menu.add_command(label="Italic (Unicode)", command=lambda: self.apply_unicode_style("italic"))
        edit_menu.add_command(label="Underline", command=lambda: self.apply_unicode_style("underline"))
        edit_menu.add_command(label="Strikethrough", command=lambda: self.apply_unicode_style("strikethrough"))
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
        
        colors_menu = tk.Menu(self.menubar, tearoff=0, bg="#2b2b2b", fg="#ffffff", activebackground="#34495e", activeforeground="#ffffff", bd=0)
        colors_menu.add_command(label="Change Window Background Color", command=self.open_bg_color_picker)
        colors_menu.add_command(label="Change Close Button Color", command=self.open_close_bg_picker)
        colors_menu.add_command(label="Change Close Button Text Color", command=self.open_close_fg_picker)
        colors_menu.add_separator()
        colors_menu.add_command(label="Change Selected Text Field Color", command=self.open_color_picker_from_menu)
        self.menubar.add_cascade(label="Colors", menu=colors_menu)

        help_menu = tk.Menu(self.menubar, tearoff=0, bg="#2b2b2b", fg="#ffffff", activebackground="#34495e", activeforeground="#ffffff", bd=0)
        help_menu.add_command(label="About", command=self.show_about_dialog)
        self.menubar.add_cascade(label="Help", menu=help_menu)
        
        self.configure(menu=self.menubar)

    def show_about_dialog(self):
        AboutDialog(self, self.logo_path, self.logo_size)

    def _on_entry_dimension_change(self, *args):
        if not self._updating_from_entry:
            self.update_preview()

    def apply_unicode_style(self, style_type):
        widget = self.focus_get()
        if not widget: return
        if hasattr(widget, "_entry"): widget = widget._entry
        if not isinstance(widget, (tk.Entry, ctk.CTkEntry)): return

        try:
            first = widget.index("sel.first")
            last = widget.index("sel.last")
            selected_text = widget.get()[first:last]
        except tk.TclError:
            return

        transformed = ""
        if style_type == "bold":
            for char in selected_text:
                if 'a' <= char <= 'z': transformed += chr(ord(char) + 0x1D41A - ord('a'))
                elif 'A' <= char <= 'Z': transformed += chr(ord(char) + 0x1D400 - ord('A'))
                elif '0' <= char <= '9': transformed += chr(ord(char) + 0x1D7CE - ord('0'))
                else: transformed += char
        elif style_type == "italic":
            for char in selected_text:
                if 'a' <= char <= 'z': transformed += 'ℎ' if char == 'h' else chr(ord(char) + 0x1D44E - ord('a'))
                elif 'A' <= char <= 'Z': transformed += chr(ord(char) + 0x1D434 - ord('A'))
                else: transformed += char
        elif style_type == "underline":
            for char in selected_text: transformed += char + "\u0332"
        elif style_type == "strikethrough":
            for char in selected_text: transformed += char + "\u0336"

        widget.delete(first, last)
        widget.insert(first, transformed)

    def open_color_picker_from_menu(self):
        if self.active_field == "website" and self.active_link_index is not None:
            initial_color = self.links[self.active_link_index]["color"]
        else:
            initial_color = self.font_colors[self.active_field]
            
        color_code = colorchooser.askcolor(title="Select Text Color", initialcolor=initial_color)
        if color_code and color_code[1]:
            if self.active_field == "website" and self.active_link_index is not None:
                self.links[self.active_link_index]["color"] = color_code[1]
            else:
                self.font_colors[self.active_field] = color_code[1]
            self.update_preview()

    def create_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0, bg="#2b2b2b", fg="#ffffff", activebackground="#34495e", activeforeground="#ffffff", bd=0)
        self.context_menu.add_command(label="Cut", command=lambda: self.focus_get().event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Copy", command=lambda: self.focus_get().event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Paste", command=lambda: self.focus_get().event_generate("<<Paste>>"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Bold", command=lambda: self.apply_unicode_style("bold"))
        self.context_menu.add_command(label="Italic", command=lambda: self.apply_unicode_style("italic"))
        self.context_menu.add_command(label="Underline", command=lambda: self.apply_unicode_style("underline"))
        self.context_menu.add_command(label="Strikethrough", command=lambda: self.apply_unicode_style("strikethrough"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Color (Change Field Color)", command=self.open_color_picker_from_menu)
        
        self.bind_class("Entry", "<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def setup_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.edit_frame = ctk.CTkScrollableFrame(self, width=420, corner_radius=0)
        self.edit_frame.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(self.edit_frame, text="Window Configuration", font=("Arial", 20, "bold")).pack(pady=15)

        self.create_input(self.edit_frame, "App Name:", self.app_name, "app_name")
        self.create_input(self.edit_frame, "Version:", self.version, "version")
        self.create_input(self.edit_frame, "Author:", self.author, "author")
        self.create_input(self.edit_frame, "Description:", self.description, "description")
        
        self.links_container = ctk.CTkFrame(self.edit_frame, fg_color="transparent")
        self.links_container.pack(fill="x", pady=5)
        self.render_links_inputs()

        # --- STYLE ADJUSTMENT SECTION ---
        self.style_frame = ctk.CTkFrame(self.edit_frame, fg_color="#2b2b2b", corner_radius=8)
        self.style_frame.pack(fill="x", padx=20, pady=15)
        
        self.slider_label = ctk.CTkLabel(self.style_frame, text="Field Style [Title]: 22px", font=("Arial", 12, "bold"))
        self.slider_label.pack(anchor="w", padx=15, pady=(10, 2))
        
        controls_container = ctk.CTkFrame(self.style_frame, fg_color="transparent")
        controls_container.pack(fill="x", padx=15, pady=(0, 15))
        
        self.font_slider = ctk.CTkSlider(controls_container, from_=8, to=40, number_of_steps=32, command=self.on_slider_move)
        self.font_slider.set(self.font_sizes[self.active_field])
        self.font_slider.pack(fill="x", pady=(0, 10))

        self.logo_slider_label = ctk.CTkLabel(controls_container, text=f"Max Logo Size: {self.logo_size}px", font=("Arial", 11))
        self.logo_slider_label.pack(anchor="w", pady=(5, 2))
        
        self.logo_slider = ctk.CTkSlider(controls_container, from_=30, to=200, number_of_steps=170, command=self.on_logo_slider_move)
        self.logo_slider.set(self.logo_size)
        self.logo_slider.pack(fill="x", pady=(0, 15))
        
        buttons_row = ctk.CTkFrame(controls_container, fg_color="transparent")
        buttons_row.pack(fill="x", pady=(5, 0))
        buttons_row.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.btn_bg_color = ctk.CTkButton(buttons_row, text="Background", fg_color=self.bg_color, hover_color="#2c3e50", command=self.open_bg_color_picker)
        self.btn_bg_color.grid(row=0, column=0, sticky="ew", padx=(0, 2))

        self.btn_close_bg_picker = ctk.CTkButton(buttons_row, text="Button", fg_color=self.btn_close_bg, hover_color="#2c3e50", command=self.open_close_bg_picker)
        self.btn_close_bg_picker.grid(row=0, column=1, sticky="ew", padx=(2, 2))

        self.btn_close_fg_picker = ctk.CTkButton(buttons_row, text="Close", fg_color="#34495e", text_color=self.btn_close_fg, hover_color="#2c3e50", command=self.open_close_fg_picker)
        self.btn_close_fg_picker.grid(row=0, column=2, sticky="ew", padx=(2, 0))

        # --- DIMENSIONS SECTION ---
        ctk.CTkLabel(self.edit_frame, text="About Window Dimensions (drag with mouse on right):", font=("Arial", 12, "bold")).pack(pady=(10, 5))
        
        dim_frame = ctk.CTkFrame(self.edit_frame, fg_color="transparent")
        dim_frame.pack(fill="x", padx=20)
        dim_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        ctk.CTkLabel(dim_frame, text="Width:").grid(row=0, column=0, sticky="e", padx=(0, 5))
        self.entry_w = ctk.CTkEntry(dim_frame, textvariable=self.win_width, width=70)
        self.entry_w.grid(row=0, column=1, sticky="w", pady=5)
        
        ctk.CTkLabel(dim_frame, text="Height:").grid(row=0, column=2, sticky="e", padx=(15, 5))
        self.entry_h = ctk.CTkEntry(dim_frame, textvariable=self.win_height, width=70)
        self.entry_h.grid(row=0, column=3, sticky="w", pady=5)

        self.btn_logo = ctk.CTkButton(self.edit_frame, text="Select Logo", command=self.load_logo, fg_color="#34495e")
        self.btn_logo.pack(pady=15, padx=20, fill="x")

        ctk.CTkButton(self.edit_frame, text="Generate about.py File", fg_color="#2ecc71", hover_color="#27ae60", 
                      command=self.generate_file).pack(pady=10, padx=20, fill="x")

        # --- RIGHT PANEL: PREVIEW ---
        self.preview_container = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.preview_container.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.update_preview()

    def create_input(self, master, label_text, var, field_key):
        ctk.CTkLabel(master, text=label_text).pack(anchor="w", padx=20, pady=(5, 0))
        entry = ctk.CTkEntry(master, textvariable=var, width=360)
        entry.pack(padx=20, pady=(0, 5))
        entry.bind("<FocusIn>", lambda e: self.switch_active_field(field_key))

    def render_links_inputs(self):
        """Dynamically renders link input fields with №, +, and - buttons."""
        for widget in self.links_container.winfo_children():
            widget.destroy()

        for idx, link_item in enumerate(self.links):
            row_frame = ctk.CTkFrame(self.links_container, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=3)

            label_text = f"Link (URL) #{idx + 1}:"
            ctk.CTkLabel(row_frame, text=label_text).pack(anchor="w")

            input_action_row = ctk.CTkFrame(row_frame, fg_color="transparent")
            input_action_row.pack(fill="x")

            entry = ctk.CTkEntry(input_action_row, textvariable=link_item["var"], width=230)
            entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
            entry.bind("<FocusIn>", lambda e, i=idx: self.switch_active_field("website", i))

            # Yellow "№" button placed before the "+" button
            btn_alias = ctk.CTkButton(input_action_row, text="№", width=30, height=28, fg_color="#f1c40f", hover_color="#f39c12", text_color="#000000", font=("Arial", 12, "bold"), command=lambda i=idx: self.open_alias_dialog(i))
            btn_alias.pack(side="left", padx=2)

            btn_add = ctk.CTkButton(input_action_row, text="+", width=30, height=28, fg_color="#2ecc71", hover_color="#27ae60", command=self.add_link_field)
            btn_add.pack(side="left", padx=2)

            btn_remove = ctk.CTkButton(input_action_row, text="-", width=30, height=28, fg_color="#e74c3c", hover_color="#c0392b", command=lambda i=idx: self.remove_link_field(i))
            btn_remove.pack(side="left", padx=2)

    def open_alias_dialog(self, index):
        """Opens a small modal window to enter a custom display label instead of the full URL."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Set Link Label")
        dialog.geometry("350x150")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() // 2) - (350 // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (150 // 2)
        dialog.geometry(f"350x150+{x}+{y}")

        ctk.CTkLabel(dialog, text="Enter text to display instead of the URL:", font=("Arial", 12)).pack(pady=(15, 5))
        
        entry_alias = ctk.CTkEntry(dialog, textvariable=self.links[index]["label_var"], width=300)
        entry_alias.pack(pady=5)
        entry_alias.focus_set()

        def save_and_close():
            self.update_preview()
            dialog.destroy()

        ctk.CTkButton(dialog, text="Confirm", width=100, command=save_and_close).pack(pady=10)

    def add_link_field(self):
        if len(self.links) >= 5:
            messagebox.showwarning("Limit", "Maximum number of links is 5 for design aesthetics.")
            return
        self.add_link_data("https://", "")
        self.render_links_inputs()
        self.update_preview()

    def remove_link_field(self, index):
        if len(self.links) <= 1:
            messagebox.showwarning("Error", "At least one web link must remain.")
            return
        self.links.pop(index)
        self.active_link_index = None
        self.render_links_inputs()
        self.switch_active_field("app_name")
        self.update_preview()

    def switch_active_field(self, field_key, link_idx=None):
        self.active_field = field_key
        self.active_link_index = link_idx
        
        friendly_names = {
            "app_name": "Title", "version": "Version", 
            "description": "Description", "author": "Author", "website": f"Web Link #{link_idx+1 if link_idx is not None else 1}"
        }

        if field_key == "website" and link_idx is not None:
            current_size = self.links[link_idx]["size"]
        else:
            current_size = self.font_sizes[field_key]

        self.font_slider.set(current_size)
        self.slider_label.configure(text=f"Field Style [{friendly_names[field_key]}]: {current_size}px")
        self.update_preview()

    def on_slider_move(self, value):
        size = int(value)
        friendly_names = {
            "app_name": "Title", "version": "Version", 
            "description": "Description", "author": "Author", "website": f"Web Link #{self.active_link_index+1 if self.active_link_index is not None else 1}"
        }
        
        if self.active_field == "website" and self.active_link_index is not None:
            self.links[self.active_link_index]["size"] = size
        else:
            self.font_sizes[self.active_field] = size

        self.slider_label.configure(text=f"Field Style [{friendly_names[self.active_field]}]: {size}px")
        self.update_preview()

    def on_logo_slider_move(self, value):
        self.logo_size = int(value)
        self.logo_slider_label.configure(text=f"Max Logo Size: {self.logo_size}px")
        self.update_preview()

    def open_bg_color_picker(self):
        color_code = colorchooser.askcolor(title="Select About Window Background Color", initialcolor=self.bg_color)
        if color_code and color_code[1]:
            self.bg_color = color_code[1]
            self.btn_bg_color.configure(fg_color=color_code[1])
            self.update_preview()

    def open_close_bg_picker(self):
        color_code = colorchooser.askcolor(title="Select Close Button Color", initialcolor=self.btn_close_bg)
        if color_code and color_code[1]:
            self.btn_close_bg = color_code[1]
            self.btn_close_bg_picker.configure(fg_color=color_code[1])
            self.update_preview()

    def open_close_fg_picker(self):
        color_code = colorchooser.askcolor(title="Select Close Button Text Color", initialcolor=self.btn_close_fg)
        if color_code and color_code[1]:
            self.btn_close_fg = color_code[1]
            self.btn_close_fg_picker.configure(text_color=color_code[1])
            self.update_preview()

    def load_logo(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Supported Images", "*.ico *.png *.jpg *.jpeg *.gif")]
        )
        if file_path:
            self.logo_path = file_path
            self.btn_logo.configure(text=f"Logo: {os.path.basename(file_path)}")
            self.update_preview()

    def start_resize(self, event):
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        try:
            self.drag_start_w = int(self.win_width.get())
            self.drag_start_h = int(self.win_height.get())
        except ValueError:
            self.drag_start_w, self.drag_start_h = 400, 500

    def resize_width(self, event):
        delta_x = event.x_root - self.drag_start_x
        new_w = max(200, self.drag_start_w + delta_x)
        if self.inner_preview: self.inner_preview.configure(width=new_w)
        if self.desc_label: self.desc_label.configure(wraplength=new_w - 40)
        self._updating_from_entry = True
        self.win_width.set(str(new_w))
        self._updating_from_entry = False

    def resize_height(self, event):
        delta_y = event.y_root - self.drag_start_y
        new_h = max(200, self.drag_start_h + delta_y)
        if self.inner_preview: self.inner_preview.configure(height=new_h)
        self._updating_from_entry = True
        self.win_height.set(str(new_h))
        self._updating_from_entry = False

    def resize_both(self, event):
        delta_x = event.x_root - self.drag_start_x
        delta_y = event.y_root - self.drag_start_y
        new_w = max(200, self.drag_start_w + delta_x)
        new_h = max(200, self.drag_start_h + delta_y)
        if self.inner_preview: self.inner_preview.configure(width=new_w, height=new_h)
        if self.desc_label: self.desc_label.configure(wraplength=new_w - 40)
        self._updating_from_entry = True
        self.win_width.set(str(new_w))
        self.win_height.set(str(new_h))
        self._updating_from_entry = False

    def end_resize(self, event):
        self.update_preview()

    def update_preview(self):
        if not hasattr(self, 'preview_container'): return
        for widget in self.preview_container.winfo_children():
            widget.destroy()

        try:
            w = int(self.win_width.get()) if self.win_width.get() else 400
            h = int(self.win_height.get()) if self.win_height.get() else 500
        except ValueError:
            w, h = 400, 500

        preview_w = max(w, 200)
        preview_h = max(h, 200)

        self.inner_preview = ctk.CTkFrame(self.preview_container, width=preview_w, height=preview_h, 
                                     fg_color=self.bg_color, border_width=2, border_color="#3a3a3a")
        self.inner_preview.place(relx=0.5, rely=0.5, anchor="center")
        self.inner_preview.pack_propagate(False)

        title_bar = ctk.CTkFrame(self.inner_preview, fg_color="#1e1e1e", height=28, corner_radius=0)
        title_bar.pack(fill="x", side="top")
        title_bar.pack_propagate(False)
        ctk.CTkLabel(title_bar, text="About", font=("Arial", 11), text_color="#ccc").pack(side="left", padx=10)

        if self.logo_path and os.path.exists(self.logo_path):
            try:
                img = Image.open(self.logo_path)
                img.thumbnail((self.logo_size, self.logo_size))
                ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                ctk.CTkLabel(self.inner_preview, image=ctk_img, text="").pack(pady=15)
            except: pass

        ctk.CTkLabel(self.inner_preview, text=self.app_name.get(), 
                     font=("Arial", self.font_sizes["app_name"], "bold"), 
                     text_color=self.font_colors["app_name"]).pack(pady=5)
        
        ctk.CTkLabel(self.inner_preview, text=self.version.get(), 
                     font=("Arial", self.font_sizes["version"]), 
                     text_color=self.font_colors["version"]).pack()
        
        self.desc_label = ctk.CTkLabel(self.inner_preview, text=self.description.get(), 
                                       font=("Arial", self.font_sizes["description"]), 
                                       wraplength=preview_w-40, 
                                       text_color=self.font_colors["description"])
        self.desc_label.pack(pady=15)
        
        ctk.CTkLabel(self.inner_preview, text=self.author.get(), 
                     font=("Arial", self.font_sizes["author"], "italic"), 
                     text_color=self.font_colors["author"]).pack()
        
        ctk.CTkButton(self.inner_preview, text="Close", fg_color=self.btn_close_bg, 
                      text_color=self.btn_close_fg, state="disabled").pack(pady=15, side="bottom")

        # Draw links on preview (taking custom labels into account)
        for link_item in reversed(self.links):
            display_text = link_item["label_var"].get()
            if not display_text.strip():
                display_text = link_item["var"].get()

            ctk.CTkLabel(self.inner_preview, text=display_text, 
                         font=("Arial", link_item["size"]), 
                         text_color=link_item["color"]).pack(pady=3, side="bottom")

        edge_thickness = 7
        right_edge = tk.Frame(self.inner_preview, bg="", cursor="sb_h_double_arrow", width=edge_thickness)
        right_edge.place(relx=1.0, rely=0, relheight=1.0, anchor="ne")
        right_edge.bind("<Button-1>", self.start_resize)
        right_edge.bind("<B1-Motion>", self.resize_width)
        right_edge.bind("<ButtonRelease-1>", self.end_resize)

        bottom_edge = tk.Frame(self.inner_preview, bg="", cursor="sb_v_double_arrow", height=edge_thickness)
        bottom_edge.place(relx=0, rely=1.0, relwidth=1.0, anchor="sw")
        bottom_edge.bind("<Button-1>", self.start_resize)
        bottom_edge.bind("<B1-Motion>", self.resize_height)
        bottom_edge.bind("<ButtonRelease-1>", self.end_resize)

        corner_edge = tk.Frame(self.inner_preview, bg="", cursor="size_nw_se", width=edge_thickness*2, height=edge_thickness*2)
        corner_edge.place(relx=1.0, rely=1.0, anchor="se")
        corner_edge.bind("<Button-1>", self.start_resize)
        corner_edge.bind("<B1-Motion>", self.resize_both)
        corner_edge.bind("<ButtonRelease-1>", self.end_resize)

    def generate_file(self):
        dest_path = filedialog.asksaveasfilename(defaultextension=".py", initialfile="about.py")
        if not dest_path: return

        logo_code = ""
        if self.logo_path:
            safe_path = self.logo_path.replace("\\", "\\\\")
            logo_code = f"""
        try:
            img = Image.open(r"{safe_path}")
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=({self.logo_size}, {self.logo_size}))
            ctk.CTkLabel(self, image=ctk_img, text="").pack(pady=15)
        except: pass"""

        links_code = ""
        for item in reversed(self.links):
            url_val = item["var"].get()
            label_val = item["label_var"].get()
            
            # If label text is empty, use the full URL
            display_text = label_val if label_val.strip() else url_val
            size = item["size"]
            color = item["color"]
            
            links_code += f"""
        link_{id(item)} = ctk.CTkLabel(self, text="{display_text}", font=("Arial", {size}), text_color="{color}", cursor="hand2")
        link_{id(item)}.pack(pady=4, side="bottom")
        link_{id(item)}.bind("<Button-1>", lambda e: webbrowser.open("{url_val}"))"""

        code = f"""import customtkinter as ctk
import webbrowser
from PIL import Image

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, parent=None):
        if parent is None: super().__init__()
        else: super().__init__(parent)
        
        self.title("About")
        self.geometry("{self.win_width.get()}x{self.win_height.get()}")
        self.resizable(False, False)
        self.configure(fg_color="{self.bg_color}")
        
        self.update_idletasks()
        w = int("{self.win_width.get()}")
        h = int("{self.win_height.get()}")
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{{w}}x{{h}}+{{x}}+{{y}}")

        self.grab_set()
        {logo_code}
        
        ctk.CTkLabel(self, text="{self.app_name.get()}", font=("Arial", {self.font_sizes['app_name']}, "bold"), text_color="{self.font_colors['app_name']}").pack(pady=5)
        ctk.CTkLabel(self, text="{self.version.get()}", font=("Arial", {self.font_sizes['version']}), text_color="{self.font_colors['version']}").pack()
        ctk.CTkLabel(self, text="{self.description.get()}", font=("Arial", {self.font_sizes['description']}), wraplength={int(self.win_width.get() or 400)-40}, text_color="{self.font_colors['description']}").pack(pady=15)
        ctk.CTkLabel(self, text="{self.author.get()}", font=("Arial", {self.font_sizes['author']}, "italic"), text_color="{self.font_colors['author']}").pack()
        
        ctk.CTkButton(self, text="Close", fg_color="{self.btn_close_bg}", text_color="{self.btn_close_fg}", command=self.destroy).pack(pady=15, side="bottom")
        {links_code}

if __name__ == "__main__":
    root = ctk.CTk()
    root.withdraw()
    about = AboutWindow(root)
    about.protocol("WM_DELETE_WINDOW", root.quit)
    about.bind("<Destroy>", lambda e: root.quit() if e.widget == about else None)
    root.mainloop()
"""
        try:
            with open(dest_path, "w", encoding="utf-8") as f: f.write(code)
            messagebox.showinfo("Success", "Universal module about.py generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

if __name__ == "__main__":
    app = AboutGeneratorApp()
    app.mainloop()