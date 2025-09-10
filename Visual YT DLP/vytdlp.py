import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import webbrowser
import json
import os
import sys

bitrate_map = {
    "128 kbps": "5", "160 kbps": "4", "192 kbps": "3", "256 kbps": "2", "320 kbps": "1"
}

def obtener_ruta_ytdlp():
    base = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__)
    exe_path = os.path.join(base, "yt-dlp.exe")
    if not os.path.exists(exe_path):
        messagebox.showerror("Error", "❌ No se encontró yt-dlp.exe en la carpeta del programa.")
        sys.exit(1)
    return exe_path

def obtener_playlist_info(link):
    try:
        ytdlp_path = obtener_ruta_ytdlp()
        result = subprocess.run([ytdlp_path, "--flat-playlist", "--dump-json", link],
            capture_output=True, text=True)
        return [json.loads(line) for line in result.stdout.strip().split("\n") if line]
    except:
        return []

def actualizar_formatos_por_modo():
    modo = combo_modo.get()
    if modo == "Audio":
        combo_formato['values'] = ["mp3", "m4a"]
        combo_formato.set("mp3")
        combo_bitrate.set("160 kbps")
    else:
        combo_formato['values'] = ["mp4", "webm"]
        combo_formato.set("webm")
        combo_calidad.set("720")

def mostrar_disclaimer():
    win = tk.Toplevel(root)
    win.title("Disclaimer Legal")
    win.geometry("520x360")
    win.configure(bg="#f2f2f2")
    win.resizable(False, False)

    texto = (
        "⚖️ Disclaimer Legal:\n\n"
        "visual yt-dlp no está afiliada oficialmente con yt-dlp ni sus desarrolladores. "
        "Esta herramienta únicamente facilita la interacción visual y no se responsabiliza "
        "por el funcionamiento interno de yt-dlp ni el contenido descargado mediante dicha herramienta.\n"
        "El uso queda bajo exclusiva responsabilidad del usuario."
    )
    ttk.Label(win, text=texto, wraplength=460, justify="left",
              font=("Segoe UI", 10), background="#f2f2f2", foreground="#555").pack(padx=20, pady=(20, 5))

    ttk.Label(win, text="🔗 Repositorio de visual yt-dlp:", font=("Segoe UI", 10, "bold"),
              background="#f2f2f2", foreground="#4a90e2").pack(pady=(10, 0))
    link1 = tk.Label(win, text="github.com/fedegure/VYTDLP", fg="blue", cursor="hand2",
                     font=("Segoe UI", 10, "underline"), bg="#f2f2f2")
    link1.pack()
    link1.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/fedegure/VYTDLP"))

    ttk.Label(win, text="🔗 Proyecto yt-dlp original:", font=("Segoe UI", 10, "bold"),
              background="#f2f2f2", foreground="#4a90e2").pack(pady=(10, 0))
    link2 = tk.Label(win, text="github.com/yt-dlp/yt-dlp", fg="blue", cursor="hand2",
                     font=("Segoe UI", 10, "underline"), bg="#f2f2f2")
    link2.pack()
    link2.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/yt-dlp/yt-dlp"))

    ttk.Button(win, text="Cerrar", command=win.destroy).pack(pady=(15, 20))

def actualizar_campos_por_modo(*args):
    actualizar_formatos_por_modo()
    modo = combo_modo.get()
    if modo == "Audio":
        label_bitrate.grid()
        combo_bitrate.grid()
        label_calidad.grid_remove()
        combo_calidad.grid_remove()
    else:
        label_calidad.grid()
        combo_calidad.grid()
        label_bitrate.grid_remove()
        combo_bitrate.grid_remove()

def elegir_directorio():
    return filedialog.askdirectory(title="Seleccionar carpeta de destino")

def actualizar_progreso(texto):
    label_progreso.config(text=texto)
    root.update_idletasks()

def descargar_individual(link):
    directorio = elegir_directorio()
    if not directorio:
        messagebox.showinfo("Cancelado", "No se seleccionó carpeta.")
        return
    ytdlp_path = obtener_ruta_ytdlp()
    modo = combo_modo.get()
    calidad = combo_calidad.get()
    formato = combo_formato.get()
    bitrate = combo_bitrate.get()
    actualizar_progreso("Descargando enlace directo...")
    comando = [ytdlp_path, "-o", os.path.join(directorio, "%(title)s.%(ext)s")]
    if modo == "Audio":
        comando += ["--extract-audio", "--audio-format", formato,
                    "--audio-quality", bitrate_map.get(bitrate, "5")]
        actualizar_progreso("Convirtiendo a audio...")
    else:
        comando += ["-S", f"height:{calidad}", "-f", "bv*+ba"]
        if formato == "mp4":
            comando += ["--recode-video", "mp4"]
        actualizar_progreso("Procesando video...")
    comando.append(link)
    subprocess.run(comando)
    actualizar_progreso("✅ Tarea completada")

def descargar_playlist(lista, seleccionados):
    directorio = elegir_directorio()
    if not directorio:
        messagebox.showinfo("Cancelado", "No se seleccionó carpeta.")
        return
    ytdlp_path = obtener_ruta_ytdlp()
    modo = combo_modo.get()
    calidad = combo_calidad.get()
    formato = combo_formato.get()
    bitrate = combo_bitrate.get()
    for i, video in enumerate(lista):
        if seleccionados[i].get():
            url = f"https://www.youtube.com/watch?v={video['id']}"
            titulo = video.get("title", f"video_{i+1}")
            prefijo = f"{i+1:03d}_"
            salida = f"{prefijo}{titulo}.%(ext)s"
            comando = [ytdlp_path, "-o", os.path.join(directorio, salida)]
            if modo == "Audio":
                comando += ["--extract-audio", "--audio-format", formato,
                            "--audio-quality", bitrate_map.get(bitrate, "5")]
                actualizar_progreso(f"{prefijo}{titulo} — Convirtiendo a audio...")
            else:
                comando += ["-S", f"height:{calidad}", "-f", "bv*+ba"]
                if formato == "mp4":
                    comando += ["--recode-video", "mp4"]
                actualizar_progreso(f"{prefijo}{titulo} — Procesando video...")
            comando.append(url)
            subprocess.run(comando)
    actualizar_progreso("✅ Playlist descargada")

def mostrar_seleccion_playlist(lista):
    win = tk.Toplevel(root)
    win.title("Seleccionar videos de playlist")
    win.geometry("700x500")
    win.configure(bg="#f2f2f2")
    estilo_lista = ttk.Style()
    estilo_lista.configure("Lista.TButton",
        background="#4a90e2", foreground="#ffffff",
        font=("Segoe UI", 9, "bold"), padding=6)
    estilo_lista.map("Lista.TButton",
        background=[("active", "#357ABD")],
        foreground=[("active", "#ffffff")])
    seleccion_playlist = tk.BooleanVar()
    seleccionados = [tk.BooleanVar() for _ in lista]
    def toggle_todo():
        valor = seleccion_playlist.get()
        for var in seleccionados:
            var.set(valor)
    ttk.Checkbutton(win, text="Seleccionar playlist completa",
        variable=seleccion_playlist, command=toggle_todo,
        style="TCheckbutton").pack(anchor="w", padx=10, pady=5)
    canvas = tk.Canvas(win, bg="#f2f2f2", highlightthickness=0)
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    for i, video in enumerate(lista):
        chk = ttk.Checkbutton(frame, text=f"{i+1:03d} - {video.get('title', 'Video')}",
            variable=seleccionados[i], style="TCheckbutton")
        chk.pack(anchor="w", padx=10, pady=2)
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    ttk.Button(win, text="Descargar seleccionados",
        command=lambda: [descargar_playlist(lista, seleccionados), win.destroy()],
        style="Lista.TButton").pack(pady=10)

def descargar():
    link = entry_link.get().strip()
    if "list=" in link:
        info = obtener_playlist_info(link)
        if info:
            mostrar_seleccion_playlist(info)
            return
    descargar_individual(link)
def detectar_version_yt_dlp():
    try:
        path = obtener_ruta_ytdlp()
        version = subprocess.check_output([path, "--version"], text=True).strip()
        return version
    except Exception:
        return "No detectada"

# 🖌 GUI principal
root = tk.Tk()
root.title("visual yt-dlp")
root.wm_title("visual yt-dlp")

try:
    root.iconbitmap("icon.ico")
except:
    print("⚠️ No se pudo cargar el ícono. Asegurate de que 'icon.ico' exista y sea válido.")

root.configure(bg="#f2f2f2")

estilo = ttk.Style()
estilo.theme_use("default")
estilo.configure("TLabel", foreground="#333", background="#f2f2f2", font=("Segoe UI", 10))
estilo.configure("TCheckbutton", background="#f2f2f2", font=("Segoe UI", 9))
estilo.configure("Custom.TButton",
    background="#4a90e2", foreground="#ffffff",
    font=("Segoe UI", 10, "bold"), padding=6)
estilo.map("Custom.TButton",
    background=[("active", "#357ABD"), ("disabled", "#cccccc")],
    foreground=[("active", "#ffffff")])

ttk.Label(root, text="🔗 LINK VIDEO o PLAYLIST").grid(row=0, column=0, padx=5, pady=5)
entry_link = ttk.Entry(root, width=60)
entry_link.grid(row=0, column=1, padx=5, pady=5)

ttk.Separator(root, orient="horizontal").grid(row=1, columnspan=2, sticky="ew", pady=10)

ttk.Label(root, text="⚙️ MODO DE DESCARGA").grid(row=2, column=0)
combo_modo = ttk.Combobox(root, values=["Video", "Audio"])
combo_modo.grid(row=2, column=1)
combo_modo.set("Video")
combo_modo.bind("<<ComboboxSelected>>", actualizar_campos_por_modo)

ttk.Label(root, text="📦 FORMATO SALIDA").grid(row=3, column=0)
combo_formato = ttk.Combobox(root)
combo_formato.grid(row=3, column=1)

label_calidad = ttk.Label(root, text="📺 CALIDAD VIDEO")
combo_calidad = ttk.Combobox(root, values=["144", "240", "360", "480", "720", "1080"])
label_calidad.grid(row=4, column=0)
combo_calidad.grid(row=4, column=1)

label_bitrate = ttk.Label(root, text="🎵 CALIDAD AUDIO")
combo_bitrate = ttk.Combobox(root, values=list(bitrate_map.keys()))
label_bitrate.grid(row=4, column=0)
combo_bitrate.grid(row=4, column=1)

ttk.Button(root, text="⬇️ DESCARGAR", command=descargar,
    style="Custom.TButton").grid(row=5, columnspan=2, pady=10)

label_progreso = ttk.Label(root, text="", font=("Segoe UI", 9, "italic"))
label_progreso.grid(row=6, columnspan=2, pady=5)
version_detectada = detectar_version_yt_dlp()
label_version = ttk.Label(root, text=f"Motor yt-dlp: v{version_detectada}", font=("Segoe UI", 9, "italic"))
label_version.grid(row=7, columnspan=2, pady=(0, 10))

actualizar_campos_por_modo()

btn_disclaimer = ttk.Button(root, text="Disclaimer", command=mostrar_disclaimer)
btn_disclaimer.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

root.mainloop()