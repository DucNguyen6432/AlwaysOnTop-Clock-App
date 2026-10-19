import tkinter as tk
from datetime import datetime
import math

class AlwaysOnTopClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Time Station Clock")
        self.root.geometry("320x370")
        self.root.configure(bg="#1a4971")
        
        # Giữ cửa sổ luôn nổi lên trên cùng (Always on Top)
        self.root.attributes("-topmost", True)
        
        # Canvas vẽ đồng hồ kim
        self.canvas = tk.Canvas(root, width=280, height=280, bg="#1a4971", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Label hiển thị ngày tháng
        self.date_label = tk.Label(root, text="", font=("Arial", 11, "bold"), fg="white", bg="#1a4971")
        self.date_label.pack()
        
        # Label hiển thị giờ điện tử
        self.time_label = tk.Label(root, text="", font=("Arial", 10), fg="#ffcc00", bg="#1a4971")
        self.time_label.pack()
        
        self.update_clock()

    def update_clock(self):
        self.canvas.delete("all")
        
        center_x = 140
        center_y = 140
        radius = 120
        
        # Vẽ vòng tròn viền vàng bên ngoài
        self.canvas.create_oval(center_x - radius, center_y - radius, 
                                center_x + radius, center_y + radius, 
                                outline="#f5b800", width=8)
        
        # Vẽ các số từ 1 đến 12
        for num in range(1, 13):
            angle = num * math.pi / 6 - math.pi / 2
            x = center_x + (radius - 28) * math.cos(angle)
            y = center_y + (radius - 28) * math.sin(angle)
            self.canvas.create_text(x, y, text=str(num), fill="#f5b800", font=("Arial", 12, "bold"))
            
        # Lấy thời gian hệ thống hiện tại
        now = datetime.now()
        hours = now.hour
        minutes = now.minute
        seconds = now.second
        
        # Tính góc cho các kim
        sec_angle = seconds * math.pi / 30 - math.pi / 2
        min_angle = minutes * math.pi / 30 + seconds * math.pi / 1800 - math.pi / 2
        hour_angle = (hours % 12) * math.pi / 6 + minutes * math.pi / 360 - math.pi / 2
        
        # Vẽ kim giờ (trắng)
        hx = center_x + 55 * math.cos(hour_angle)
        hy = center_y + 55 * math.sin(hour_angle)
        self.canvas.create_line(center_x, center_y, hx, hy, fill="white", width=5, capstyle=tk.ROUND)
        
        # Vẽ kim phút (trắng)
        mx = center_x + 80 * math.cos(min_angle)
        my = center_y + 80 * math.sin(min_angle)
        self.canvas.create_line(center_x, center_y, mx, my, fill="white", width=3, capstyle=tk.ROUND)
        
        # Vẽ kim giây (đỏ)
        sx = center_x + 95 * math.cos(sec_angle)
        sy = center_y + 95 * math.sin(sec_angle)
        self.canvas.create_line(center_x, center_y, sx, sy, fill="#ff3333", width=2)
        
        # Tâm đồng hồ (đỏ)
        self.canvas.create_oval(center_x - 5, center_y - 5, center_x + 5, center_y + 5, fill="#ff3333", outline="")

        # Cập nhật chữ Ngày & Giờ bên dưới
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M:%S %p")
        
        self.date_label.config(text=date_str)
        self.time_label.config(text=time_str)
        
        # Cập nhật lại sau mỗi 1000ms (1 giây)
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = AlwaysOnTopClock(root)
    root.mainloop()
