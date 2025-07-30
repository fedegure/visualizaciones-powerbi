import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import json
import os

bitrate_map = {
    "128 kbps": "5", "160 kbps": "4", "192 kbps": "3", "256 kbps": "2", "320 kbps": "1"
}

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

def obtener_playlist_info(link):
    try:
        result = subprocess.run(
            ["yt-dlp", "--flat-playlist", "--dump-json", link],
            capture_output=True, text=True
        )
        return [json.loads(line) for line in result.stdout.strip().split("\n") if line]
    except:
        return []

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

    modo = combo_modo.get()
    calidad = combo_calidad.get()
    formato = combo_formato.get()
    bitrate = combo_bitrate.get()

    actualizar_progreso("Descargando enlace directo...")

    comando = ["yt-dlp", "-o", os.path.join(directorio, "%(title)s.%(ext)s")]

    if modo == "Audio":
        comando += ["--extract-audio", "--audio-format", formato, "--audio-quality", bitrate_map.get(bitrate, "5")]
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

            comando = ["yt-dlp", "-o", os.path.join(directorio, salida)]

            if modo == "Audio":
                comando += ["--extract-audio", "--audio-format", formato, "--audio-quality", bitrate_map.get(bitrate, "5")]
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

    seleccion_playlist = tk.BooleanVar()
    seleccionados = [tk.BooleanVar() for _ in lista]

    def toggle_todo():
        valor = seleccion_playlist.get()
        for var in seleccionados:
            var.set(valor)

    ttk.Checkbutton(win, text="Seleccionar playlist completa", variable=seleccion_playlist, command=toggle_todo).pack(anchor="w", padx=10, pady=5)

    canvas = tk.Canvas(win)
    scrollbar = ttk.Scrollbar(win, orient="vertical", command=canvas.yview)
    frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for i, video in enumerate(lista):
        chk = ttk.Checkbutton(frame, text=f"{i+1:03d} - {video.get('title', 'Video')}", variable=seleccionados[i])
        chk.pack(anchor="w", padx=10, pady=2)

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    ttk.Button(win, text="Descargar seleccionados", command=lambda: [descargar_playlist(lista, seleccionados), win.destroy()]).pack(pady=10)

def descargar():
    link = entry_link.get().strip()
    if "list=" in link:
        info = obtener_playlist_info(link)
        if info:
            mostrar_seleccion_playlist(info)
            return
    descargar_individual(link)

# 🎨 GUI
root = tk.Tk()
root.title("YT-DLP Descargador Pro")

ttk.Label(root, text="LINK VIDEO o PLAYLIST").grid(row=0, column=0, padx=5, pady=5)
entry_link = ttk.Entry(root, width=60)
entry_link.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="MODO DE DESCARGA").grid(row=1, column=0)
combo_modo = ttk.Combobox(root, values=["Video", "Audio"])
combo_modo.grid(row=1, column=1)
combo_modo.set("Video")
combo_modo.bind("<<ComboboxSelected>>", actualizar_campos_por_modo)

ttk.Label(root, text="FORMATO SALIDA").grid(row=2, column=0)
combo_formato = ttk.Combobox(root)
combo_formato.grid(row=2, column=1)

label_calidad = ttk.Label(root, text="CALIDAD VIDEO")
combo_calidad = ttk.Combobox(root, values=["144", "240", "360", "480", "720", "1080"])
label_calidad.grid(row=3, column=0)
combo_calidad.grid(row=3, column=1)

label_bitrate = ttk.Label(root, text="CALIDAD AUDIO")
combo_bitrate = ttk.Combobox(root, values=list(bitrate_map.keys()))
label_bitrate.grid(row=3, column=0)
combo_bitrate.grid(row=3, column=1)

actualizar_campos_por_modo()

ttk.Button(root, text="INICIAR DESCARGA", command=descargar).grid(row=4, column=0, columnspan=2, pady=10)

label_progreso = ttk.Label(root, text="")
label_progreso.grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()