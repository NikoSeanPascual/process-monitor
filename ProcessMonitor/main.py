import tkinter as tk
import customtkinter as CTk
import subprocess
import threading
import time

BG_COLOR = "#0A1A0A"
ACCENT_COLOR = "#00FF41"
ROW_HOVER = "#1A331A"
FONT_MAIN = "Fixedsys"
FONT_FALLBACK = "Consolas"

CTk.set_appearance_mode("Dark")


class ProcessMonitor(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Niko's Processor Monitor | Hacker Style")
        self.geometry("850x700")
        self.configure(fg_color=BG_COLOR)

        self.processes = []
        self.row_widgets = []
        self.max_rows = 100

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.title_label = CTk.CTkLabel(
            self,
            text="SYSTEM_PROCESS_OVERRIDE",
            font=(FONT_MAIN, 32, "bold") if self.font_exists(FONT_MAIN) else (FONT_FALLBACK, 32, "bold"),
            text_color=ACCENT_COLOR
        )
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_ui())
        self.search_bar = CTk.CTkEntry(
            self,
            placeholder_text="SCANNING FOR TARGETS...",
            textvariable=self.search_var,
            font=(FONT_FALLBACK, 14),
            fg_color="#051005",
            border_color=ACCENT_COLOR,
            text_color=ACCENT_COLOR,
            placeholder_text_color="#006400",
            height=35
        )
        self.search_bar.grid(row=1, column=0, padx=30, pady=10, sticky="ew")

        self.header_frame = CTk.CTkFrame(self, fg_color="#0F260F", corner_radius=0, height=30)
        self.header_frame.grid(row=2, column=0, padx=20, sticky="ew")

        headers = [("NAME", 300), ("PID", 100), ("MEMORY USAGE", 120)]
        for text, width in headers:
            lbl = CTk.CTkLabel(self.header_frame, text=text, width=width, anchor="w",
                               font=(FONT_FALLBACK, 12, "bold"), text_color=ACCENT_COLOR)
            lbl.pack(side="left", padx=10)

        self.table_frame = CTk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            scrollbar_button_color=ACCENT_COLOR,
            scrollbar_button_hover_color="#008F11"
        )
        self.table_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")

        self.context_menu = tk.Menu(self, tearoff=0, bg="black", fg=ACCENT_COLOR, font=(FONT_FALLBACK, 10))
        self.context_menu.add_command(label="TERMINATE_PROCESS", command=self.kill_process)
        self.selected_pid = None

        self.setup_widget_pool()

        threading.Thread(target=self.fetch_processes_loop, daemon=True).start()
        self.refresh_ui()

    def font_exists(self, font_name):
        from tkinter import font
        return font_name in font.families()

    def setup_widget_pool(self):
        for i in range(self.max_rows):
            row_frame = CTk.CTkFrame(self.table_frame, fg_color="transparent", corner_radius=2)
            f = (FONT_MAIN, 16) if self.font_exists(FONT_MAIN) else (FONT_FALLBACK, 14)

            name_lbl = CTk.CTkLabel(row_frame, text="", width=300, anchor="w", font=f, text_color=ACCENT_COLOR)
            name_lbl.pack(side="left", padx=10)

            pid_lbl = CTk.CTkLabel(row_frame, text="", width=100, anchor="w", font=f, text_color=ACCENT_COLOR)
            pid_lbl.pack(side="left", padx=10)

            mem_lbl = CTk.CTkLabel(row_frame, text="", width=120, anchor="w", font=f, text_color=ACCENT_COLOR)
            mem_lbl.pack(side="left", padx=10)

            row_frame.bind("<Button-3>", lambda e, p=pid_lbl: self.show_context_menu(e, p))

            self.row_widgets.append({
                "frame": row_frame,
                "name": name_lbl,
                "pid": pid_lbl,
                "mem": mem_lbl
            })

    def show_context_menu(self, event, pid_label):
        text = pid_label.cget("text")
        if "ID:" in text:
            self.selected_pid = text.replace("ID:", "")
            self.context_menu.post(event.x_root, event.y_root)

    def kill_process(self):
        if self.selected_pid:
            try:
                subprocess.run(f"taskkill /F /PID {self.selected_pid}", shell=True, check=True)
                print(f"TERMINATED: {self.selected_pid}")
            except Exception as e:
                print(f"KILL_ERROR: {e}")

    def fetch_processes_loop(self):
        while True:
            try:
                raw = subprocess.check_output("tasklist /NH /FO CSV", shell=True)
                output = raw.decode('utf-8', errors='ignore').strip().split('\n')

                grouped = {}
                for line in output:
                    if not line.strip(): continue
                    p = [parts.strip().strip('"') for parts in line.split(',')]

                    if len(p) >= 5:
                        name = p[0]
                        try:
                            mem_str = p[4].replace(" K", "").replace(",", "")
                            mem = round(int(mem_str) / 1024, 2)
                            if name in grouped:
                                grouped[name]['Mem'] += mem
                                grouped[name]['Count'] += 1
                            else:
                                grouped[name] = {'Name': name, 'PID': p[1], 'Mem': mem, 'Count': 1}
                        except:
                            continue

                formatted = []
                for item in grouped.values():
                    name_display = f"> {item['Name']} [{item['Count']}]" if item['Count'] > 1 else f"> {item['Name']}"
                    formatted.append({
                        "Name": name_display.upper(),
                        "PID": item['PID'],
                        "Mem": item['Mem']
                    })

                self.processes = sorted(formatted, key=lambda x: x['Mem'], reverse=True)
            except Exception as e:
                print(f"FETCH_ERR: {e}")
            time.sleep(2.5)

    def refresh_ui(self):
        query = self.search_var.get().lower()
        filtered = [p for p in self.processes if query in p["Name"].lower()]

        for i in range(self.max_rows):
            row = self.row_widgets[i]
            if i < len(filtered):
                data = filtered[i]
                row["name"].configure(text=data["Name"])
                row["pid"].configure(text=f"ID:{data['PID']}")
                row["mem"].configure(text=f"{data['Mem']} MB")
                row["frame"].pack(fill="x", pady=1)
            else:
                row["frame"].pack_forget()

        self.after(1000, self.refresh_ui)


if __name__ == "__main__":
    app = ProcessMonitor()
    app.mainloop()