import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from datetime import datetime
import shutil
import re
import json

class BlogPostCreator:
    def __init__(self, master):
        self.master = master
        master.title("Advanced Blog Post Creator")
        master.geometry("800x900")

        self.uploaded_images = []
        self.image_sources = {}
        self.create_widgets()

    def create_widgets(self):
        # Main frame with scrollbar
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Title
        self.title_label = ttk.Label(self.scrollable_frame, text="Blog Post Title:")
        self.title_label.pack(pady=(10, 0))
        self.title_entry = ttk.Entry(self.scrollable_frame, width=70)
        self.title_entry.pack()

        # Podcast section
        self.podcast_label = ttk.Label(self.scrollable_frame, text="Podcast URL:")
        self.podcast_label.pack(pady=(10, 0))
        self.podcast_entry = ttk.Entry(self.scrollable_frame, width=70)
        self.podcast_entry.pack()

        # Sections
        self.sections_frame = ttk.Frame(self.scrollable_frame)
        self.sections_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        self.sections = []
        self.add_section()

        # Buttons
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Section", command=self.add_section).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Upload Images", command=self.upload_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Create Blog Post", command=self.create_blog_post).pack(side=tk.LEFT, padx=5)

        self.status_label = ttk.Label(self.scrollable_frame, text="")
        self.status_label.pack(pady=10)

    def add_section(self):
        section_frame = ttk.LabelFrame(self.sections_frame, text=f"Section {len(self.sections) + 1}")
        section_frame.pack(pady=5, padx=10, fill=tk.X)

        title_label = ttk.Label(section_frame, text="Section Title:")
        title_label.pack()
        title_entry = ttk.Entry(section_frame, width=60)
        title_entry.pack()

        content_label = ttk.Label(section_frame, text="Section Content:")
        content_label.pack()
        content_text = tk.Text(section_frame, height=5, width=70)
        content_text.pack()

        # Make content_text dynamically resizable
        content_text.bind("<KeyRelease>", lambda event: self.resize_text_widget(event, content_text))

        image_var = tk.StringVar(value="No image")
        image_dropdown = ttk.Combobox(section_frame, textvariable=image_var, values=["No image"])
        image_dropdown.pack()

        image_source_label = ttk.Label(section_frame, text="Image Source:")
        image_source_label.pack()
        image_source_entry = ttk.Entry(section_frame, width=60)
        image_source_entry.pack()

        self.sections.append({
            "title": title_entry,
            "content": content_text,
            "image": image_var,
            "dropdown": image_dropdown,
            "image_source": image_source_entry
        })

    def resize_text_widget(self, event, widget):
        lines = int(widget.index('end-1c').split('.')[0])
        widget.configure(height=min(max(5, lines), 20))

    def upload_images(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png *.gif")]
        filenames = filedialog.askopenfilenames(title="Select images", filetypes=filetypes)
        if filenames:
            self.uploaded_images.extend(filenames)
            self.status_label.config(text=f"{len(self.uploaded_images)} images uploaded")
            self.update_image_dropdowns()

    def update_image_dropdowns(self):
        image_options = ["No image"] + [os.path.basename(img) for img in self.uploaded_images]
        for section in self.sections:
            current_value = section["image"].get()
            section["dropdown"]["values"] = image_options
            if current_value not in image_options:
                section["image"].set("No image")

    def create_blog_post(self):
        title = self.title_entry.get()
        if not title:
            messagebox.showerror("Error", "Blog post title is required!")
            return

        slug = re.sub(r'[^\w\-]', '', title.lower().replace(' ', '-'))
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Create image directory and copy images
        img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "blog", slug)
        os.makedirs(img_dir, exist_ok=True)
        self.image_sources = {}
        for i, img in enumerate(self.uploaded_images):
            new_filename = f"{slug}-{i+1}{os.path.splitext(img)[1]}"
            shutil.copy(img, os.path.join(img_dir, new_filename))
            self.image_sources[new_filename] = self.sections[i+1]["image_source"].get()  # i+1 because the first section is the introduction

        # Save image sources
        with open(os.path.join(img_dir, "image_sources.json"), "w") as f:
            json.dump(self.image_sources, f)

        # Create new HTML file
        html_content = self.generate_html_content(title, date, slug)
        blog_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog")
        file_path = os.path.join(blog_dir, f"{slug}.html")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Update index.html
        self.update_index_html(title, slug, date)

        messagebox.showinfo("Success", f"Blog post created successfully!\nFile: {file_path}")
        self.master.destroy()

    def generate_html_content(self, title, date, slug):
        content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Marvin J. Largo</title>
    <link rel="stylesheet" href="../css/styles.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/js/all.min.js"></script>
</head>
<body>
    <header>
        <nav class="navbar">
            <a href="../index.html" class="brand">MarvinMTZ</a>
            <ul class="nav-menu">
                <li><a href="../index.html">Home</a></li>
                <li><a href="../index.html#about">About</a></li>
                <li><a href="../index.html#blog">Blog</a></li>
                <li><a href="../pages/contact.html">Contact</a></li>
            </ul>
            <div class="hamburger">
                <span class="bar"></span>
                <span class="bar"></span>
                <span class="bar"></span>
            </div>
        </nav>
    </header>

    <main>
        <article>
            <h1>{title}</h1>
            <p>By Marvin J. Largo | Published: {date}</p>

            <section id="introduction" class="section introduction">
                <h2>Introduction</h2>
                <p>{self.sections[0]["content"].get("1.0", tk.END).strip()}</p>
            </section>
            
            <section id="podcast" class="section podcast">
                <h2>Listen to the Podcast</h2>
                <p>Prefer to listen? Check out the podcast version of this article:</p>
                <div class="soundcloud-player">
                    <iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay"
                        src="{self.podcast_entry.get()}"></iframe>
                </div>
            </section>

            <section id="content" class="section content">
"""
        for i, section in enumerate(self.sections[1:], start=1):
            section_title = section["title"].get()
            section_content = section["content"].get("1.0", tk.END).strip()
            image = section["image"].get()

            if section_title:
                content += f"<h2>{section_title}</h2>\n"
            if image != "No image":
                img_filename = f"{slug}-{i}{os.path.splitext(image)[1]}"
                img_path = f"../images/blog/{slug}/{img_filename}"
                content += f'<img src="{img_path}" alt="{section_title}" style="width:100%; height:auto;">\n'
                if img_filename in self.image_sources:
                    content += f'<p class="image-source">Source: {self.image_sources[img_filename]}</p>\n'
            content += f"<p>{section_content}</p>\n"

        content += """
            </section>
        </article>
    </main>

    <footer>
        <div class="social-links">
            <a href="https://www.linkedin.com/in/marvinjlargo/" target="_blank"><i class="fab fa-linkedin"></i></a>
            <a href="https://www.youtube.com/@MarvinMtzWorld" target="_blank"><i class="fab fa-youtube"></i></a>
            <a href="https://github.com/marvinjlargo" target="_blank"><i class="fab fa-github"></i></a>
        </div>
        <p>&copy; 2024 Marvin J. Largo | All Rights Reserved</p>
    </footer>

    <script src="../js/main.js"></script>
</body>
</html>
"""
        return content

    def update_index_html(self, title, slug, date):
        index_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()

        blog_section = re.search(r'<div class="blog-grid">(.*?)</div>', content, re.DOTALL)
        if blog_section:
            new_article = f"""
                <article>
                    <h3>{title}</h3>
                    <p>Published on {date}</p>
                    <a href="blog/{slug}.html" class="read-more">Read More</a>
                </article>
"""
            updated_section = new_article + blog_section.group(1)
            content = content.replace(blog_section.group(0), f'<div class="blog-grid">{updated_section}</div>')

            with open(index_path, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlogPostCreator(root)
    root.mainloop()
