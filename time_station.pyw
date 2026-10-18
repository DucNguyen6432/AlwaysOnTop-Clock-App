"""
Time Station - always-on-top analog clock widget
-------------------------------------------------
Run:   double-click this file (needs Python from python.org installed)
Move:  drag with left mouse button
Menu:  right-click -> Opacity / Close
"""
import math
import tkinter as tk
from datetime import datetime

W, H = 300, 345
CX, CY = 150, 150          # clock centre
R_RING = 135               # gold ring radius
BG = "#0b3a66"             # dark blue face
GOLD = "#ffc20e"
TRANSPARENT = "#010101"    # used to cut out the corners


class Clock(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)          # no title bar
        self.attributes("-topmost", True)    # always on top
        self.attributes("-alpha", 0.95)
        self.configure(bg=BG)
        sw = self.winfo_screenwidth()
        self.geometry(f"{W}x{H}+{sw - W - 20}+20")   # top-right corner

        self.canvas = tk.Canvas(self, width=W, height=H, bg=BG,
                                highlightthickness=3, highlightbackground="#1f6fb5")
        self.canvas.pack()

        # drag to move
        self.canvas.bind("<ButtonPress-1>", self._start_move)
        self.canvas.bind("<B1-Motion>", self._do_move)

        # right-click menu
        self.menu = tk.Menu(self, tearoff=0)
        op = tk.Menu(self.menu, tearoff=0)
        for pct in (100, 90, 75, 50):
            op.add_command(label=f"{pct}%", command=lambda p=pct: self.attributes("-alpha", p / 100))
        self.menu.add_cascade(label="Opacity", menu=op)
        self.menu.add_separator()
        self.menu.add_command(label="Close", command=self.destroy)
        self.canvas.bind("<Button-3>", lambda e: self.menu.tk_popup(e.x_root, e.y_root))

        self.draw_static()
        self.tick()

    # ---------- moving ----------
    def _start_move(self, e):
        self._dx, self._dy = e.x, e.y

    def _do_move(self, e):
        self.geometry(f"+{self.winfo_x() + e.x - self._dx}+{self.winfo_y() + e.y - self._dy}")

    # ---------- drawing ----------
    def pt(self, angle_deg, length):
        a = math.radians(angle_deg)
        return CX + length * math.sin(a), CY - length * math.cos(a)

    def draw_static(self):
        c = self.canvas
        c.create_oval(CX - R_RING, CY - R_RING, CX + R_RING, CY + R_RING,
                      outline=GOLD, width=10, fill="#0d4478")
        for n in range(1, 13):
            x, y = self.pt(n * 30, 103)
            c.create_text(x, y, text=str(n), fill=GOLD, font=("Segoe UI", 14, "bold"))

    def tick(self):
        c = self.canvas
        c.delete("dynamic")
        now = datetime.now()
        h, m, s = now.hour % 12, now.minute, now.second + now.microsecond / 1e6

        hour_a = (h + m / 60 + s / 3600) * 30
        min_a = (m + s / 60) * 6
        sec_a = s * 6

        c.create_line(CX, CY, *self.pt(hour_a, 62), fill="white", width=6,
                      capstyle="round", tags="dynamic")
        c.create_line(CX, CY, *self.pt(min_a, 90), fill="white", width=3,
                      capstyle="round", tags="dynamic")
        c.create_line(*self.pt(sec_a + 180, 18), *self.pt(sec_a, 95), fill="#ff3b30",
                      width=2, tags="dynamic")
        c.create_oval(CX - 10, CY - 10, CX + 10, CY + 10, fill=GOLD, outline=GOLD,
                      tags="dynamic")

        date_txt = f"{now.strftime('%A, %B')} {now.day}, {now.year}"
        c.create_text(W // 2, 305, text=date_txt, fill="white",
                      font=("Segoe UI", 13, "bold"), tags="dynamic")
        c.create_text(W // 2, 328, text=now.strftime("%I:%M:%S %p").lstrip("0"),
                      fill=GOLD, font=("Segoe UI", 10), tags="dynamic")

        self.after(50, self.tick)


if __name__ == "__main__":
    Clock().mainloop()
