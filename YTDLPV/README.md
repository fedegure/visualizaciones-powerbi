📦 VYTDLP
Herramienta visual portable para descargar videos con yt-dlp, embebiendo ffmpeg y todos los recursos necesarios. Pensada para usuarios no técnicos: intuitiva, robusta y sin dependencias externas.

🎯 Características principales
- ✅ Interfaz profesional en azul/gris, con icono propio y branding coherente
- 🚫 Evita instalación de Python, librerías externas o configuraciones manuales
- 📂 Descargas directas a carpeta elegida por el usuario
- ⚙️ Progreso visual y retroalimentación clara
- 🔒 Incluye disclaimer legal sobre el uso ético de la herramienta

🧰 Requisitos
- 🖥️ Windows 10 o superior (64 bits)
- 📡 Conexión a internet
- 💾 Suficiente espacio en disco para los videos descargados

🚀 Cómo usar
- Ejecutar VYTDLP.exe
- Pegar el enlace del video
- Elegir carpeta de destino
- Presionar “Descargar” y esperar el progreso
🧪 En equipos sin Visual C++ Redistributable o ciertas DLLs, el ejecutable intenta resolver dependencias automáticamente.
⚠️ Si el antivirus lanza falso positivo, se recomienda marcar el archivo como seguro manualmente.


⚖️ Disclaimer legal
Este software utiliza componentes de código abierto:
- yt-dlp bajo Unlicense
- ffmpeg bajo GPL/LGPL
El propósito de VYTDLP es permitir la descarga de contenido público para uso personal, educativo o legítimo.
El usuario es responsable del uso que le dé a la herramienta. No se promueve el incumplimiento de derechos de autor, ni se almacenan o comparten videos por parte del desarrollador.

📁 Estructura del ejecutable
VYTDLP.exe
├─ assets/
│  ├─ yt-dlp.exe
│  └─ ffmpeg.exe
├─ icon.ico
├─ config/
│  └─ disclaimer.txt


Todos los binarios están empaquetados usando PyInstaller, respetando la portabilidad y funcionando sin Python instalado.

🖋 Autor
fedegure
Diseñador y desarrollador obsesionado con la calidad visual, legalidad y robustez técnica.
Este proyecto es parte de un proceso personal para demostrar cómo una herramienta técnica puede tener presentación profesional y experiencia impecable.
