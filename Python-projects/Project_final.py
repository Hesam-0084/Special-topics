import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import numpy as np
import tensorflow as tf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PIL import Image, ImageTk
import os
import tempfile

class ImageAnalyzerV3:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Analyzer V3")
        self.root.geometry("1000x800")

        self.paths = [None]*4
        self.data = []

        ttk.Style().theme_use("clam")

        bar = ttk.Frame(root)
        bar.pack(pady=10)

        ttk.Button(bar, text="Select Images", command=self.load).pack(side=tk.LEFT, padx=5)
        self.proc = ttk.Button(bar, text="Process", command=self.process, state=tk.DISABLED)
        self.proc.pack(side=tk.LEFT, padx=5)
        self.pdf = ttk.Button(bar, text="Export PDF", command=self.pdf_out, state=tk.DISABLED)
        self.pdf.pack(side=tk.LEFT, padx=5)

        self.img_lbls = []
        self.txt_lbls = []

        box = ttk.Frame(root)
        box.pack(fill=tk.BOTH, expand=True)

        for i in range(4):
            lf = ttk.LabelFrame(box, text=f"Image {i+1}")
            lf.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")

            im = ttk.Label(lf)
            im.pack()
            self.img_lbls.append(im)

            tx = ttk.Label(lf, text="Empty")
            tx.pack()
            self.txt_lbls.append(tx)

            box.columnconfigure(i%2, weight=1)
            box.rowconfigure(i//2, weight=1)

    def load(self):
        p = filedialog.askopenfilenames(filetypes=[("Images","*.png *.jpg *.jpeg")])
        if len(p) != 4:
            messagebox.showwarning("Error","Please select exactly 4 images")
            return

        self.paths = list(p)

        for i, x in enumerate(p):
            img = Image.open(x).convert("RGB")
            img.thumbnail((300,300))
            tk_img = ImageTk.PhotoImage(img)
            self.img_lbls[i].config(image=tk_img)
            self.img_lbls[i].image = tk_img
            self.txt_lbls[i].config(text=os.path.basename(x))

        self.proc.config(state=tk.NORMAL)

    def process(self):
        self.data.clear()

        for i, p in enumerate(self.paths):
            img = tf.image.convert_image_dtype(
                tf.image.decode_image(tf.io.read_file(p), channels=3, expand_animations=False),
                tf.float32
            )

            if i == 0:
                hsv = tf.image.rgb_to_hsv(img)
                h,s,v = tf.split(hsv, 3, axis=-1)
                h = tf.math.mod(h + 0.03, 1.0)
                out = tf.image.hsv_to_rgb(tf.concat([h,s,v], axis=-1))
                name = "Warm Tone"

            elif i == 1:
                hsv = tf.image.rgb_to_hsv(img)
                h,s,v = tf.split(hsv, 3, axis=-1)
                h = tf.math.mod(h + 0.2, 1.0)
                out = tf.image.hsv_to_rgb(tf.concat([h,s,v], axis=-1))
                name = "Cool Tone"

            elif i == 2:
                img_uint8 = tf.image.convert_image_dtype(img, tf.uint8)
                out_uint8 = tf.bitwise.right_shift(img_uint8, 4)
                out_uint8 = tf.bitwise.left_shift(out_uint8, 4)
                out = tf.image.convert_image_dtype(out_uint8, tf.float32)
                name = "Posterize / Reduced Colors"

            else:
                out = 1.0 - img
                out = tf.image.adjust_brightness(out, 0.1)
                out = tf.clip_by_value(out, 0.0, 1.0)
                name = "Negative + Bright"

            self.data.append((out, name))

            pil = tf.keras.preprocessing.image.array_to_img(out)
            pil.thumbnail((300,300))
            tk_img = ImageTk.PhotoImage(pil)
            self.img_lbls[i].config(image=tk_img)
            self.img_lbls[i].image = tk_img

            mean = tf.reduce_mean(out).numpy()
            self.txt_lbls[i].config(text=f"{name}\nMean:{mean:.3f}")

        self.pdf.config(state=tk.NORMAL)
        messagebox.showinfo("Done","Filters applied successfully!")

    def pdf_out(self):
        path = filedialog.asksaveasfilename(defaultextension=".pdf")
        if not path:
            return

        c = canvas.Canvas(path, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width/2, height-40, "Image Analyzer V3")

        y = height - 100

        for img, name in self.data:
            pil = tf.keras.preprocessing.image.array_to_img(img)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                pil.save(tmp.name)
                temp_path = tmp.name

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, name)
            c.drawImage(temp_path, 50, y-150, width=200, height=150)

            y -= 180
            os.remove(temp_path)

            if y < 200:
                c.showPage()
                y = height - 80

        c.save()
        messagebox.showinfo("Done","PDF exported successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    ImageAnalyzerV3(root)
    root.mainloop()
