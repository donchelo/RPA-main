import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import sys
import json
import glob
from datetime import datetime
import queue
import time
from PIL import Image, ImageTk
import webbrowser

class RPALauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 AI4U | Launcher RPA TAMAPRINT")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Branding AI4U (rutas opcionales)
        self.brand_name = "AI4U"
        self.brand_tagline = "Automatización Inteligente para Ti!"
        self.brand_email = "hola@ai4u.com.co"
        self.brand_logo_path = os.path.join("assets", "ai4u_logo.png")
        self.brand_banner_path = os.path.join("assets", "ai4u_banner.png")
        self.brand_icon_path = os.path.join("assets", "ai4u.ico")
        self._image_refs = {}
        
        # Icono de la ventana si está disponible
        self._set_window_icon()
        
        # Variables de estado
        self.rpa_process = None
        self.is_running = False
        self.log_queue = queue.Queue()
        
        # Crear interfaz
        self.create_widgets()
        
        # Verificar requisitos al inicio
        self.check_requirements()
        
        # Iniciar hilo para procesar logs
        self.start_log_processor()
        
        # Actualizar estado de archivos JSON
        self.update_json_status()
    
    def create_widgets(self):
        # Título principal
        title_frame = ttk.Frame(self.root)
        title_frame.pack(pady=(12, 8), fill=tk.X)
        
        # Menú superior (Ayuda)
        self._create_menubar()
        
        # Intentar cargar banner o logo
        banner_photo = None
        if os.path.exists(self.brand_banner_path):
            banner_photo = self._load_image(self.brand_banner_path, max_size=(340, 80))
        logo_photo = None
        if banner_photo is None and os.path.exists(self.brand_logo_path):
            logo_photo = self._load_image(self.brand_logo_path, max_size=(80, 80))
        
        if banner_photo is not None:
            self._image_refs['banner_photo'] = banner_photo
            banner_label = ttk.Label(title_frame, image=banner_photo)
            banner_label.pack(side=tk.LEFT, padx=(0, 12))
        elif logo_photo is not None:
            self._image_refs['logo_photo'] = logo_photo
            logo_label = ttk.Label(title_frame, image=logo_photo)
            logo_label.pack(side=tk.LEFT, padx=(0, 12))
        
        # Bloque de textos de marca
        title_text_frame = ttk.Frame(title_frame)
        title_text_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        title_label = ttk.Label(
            title_text_frame,
            text=f"{self.brand_name} · Sistema RPA TAMAPRINT",
            font=("Arial", 20, "bold")
        )
        title_label.pack(anchor=tk.W)
        
        subtitle_label = ttk.Label(
            title_text_frame,
            text="Automatización de Órdenes SAP Business One",
            font=("Arial", 12)
        )
        subtitle_label.pack(anchor=tk.W, pady=(2, 0))
        
        tagline_label = ttk.Label(
            title_text_frame,
            text=self.brand_tagline,
            font=("Arial", 11, "italic")
        )
        tagline_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Correo clicable
        self._add_link_label(
            title_text_frame,
            text=self.brand_email,
            command=self._open_email
        ).pack(anchor=tk.W, pady=(4, 0))
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Frame izquierdo - Controles
        control_frame = ttk.LabelFrame(main_frame, text="Control del Sistema", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Estado del sistema
        self.status_label = ttk.Label(control_frame, text="Estado: Detenido", 
                                     font=("Arial", 12, "bold"), foreground="red")
        self.status_label.pack(pady=(0, 20))
        
        # Botón principal
        self.main_button = ttk.Button(control_frame, text="🚀 INICIAR RPA", 
                                     command=self.toggle_rpa, style="Accent.TButton")
        self.main_button.pack(pady=10, ipadx=20, ipady=10)
        
        # Información de archivos JSON
        json_frame = ttk.LabelFrame(control_frame, text="Archivos JSON", padding=5)
        json_frame.pack(fill=tk.X, pady=20)
        
        self.json_pending_label = ttk.Label(json_frame, text="Pendientes: 0")
        self.json_pending_label.pack(anchor=tk.W)
        
        self.json_processed_label = ttk.Label(json_frame, text="Procesados hoy: 0")
        self.json_processed_label.pack(anchor=tk.W)
        
        # Botón actualizar
        self.refresh_button = ttk.Button(json_frame, text="🔄 Actualizar", 
                                        command=self.update_json_status)
        self.refresh_button.pack(pady=(10, 0))
        
        # Estado de requisitos
        req_frame = ttk.LabelFrame(control_frame, text="Requisitos", padding=5)
        req_frame.pack(fill=tk.X, pady=20)
        
        self.req_python_label = ttk.Label(req_frame, text="Python: ✅")
        self.req_python_label.pack(anchor=tk.W)
        
        self.req_deps_label = ttk.Label(req_frame, text="Dependencias: ⏳")
        self.req_deps_label.pack(anchor=tk.W)
        
        self.req_tesseract_label = ttk.Label(req_frame, text="Tesseract: ⏳")
        self.req_tesseract_label.pack(anchor=tk.W)
        
        # Botón instalar dependencias
        self.install_deps_button = ttk.Button(req_frame, text="📦 Instalar Dependencias", 
                                            command=self.install_dependencies)
        self.install_deps_button.pack(pady=(10, 0))
        
        # Frame derecho - Logs
        log_frame = ttk.LabelFrame(main_frame, text="Logs del Sistema", padding=10)
        log_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Área de logs
        self.log_text = scrolledtext.ScrolledText(log_frame, height=25, width=60, 
                                                 state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Botones de log
        log_buttons_frame = ttk.Frame(log_frame)
        log_buttons_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(log_buttons_frame, text="🗑️ Limpiar Logs", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(log_buttons_frame, text="📁 Abrir Carpeta Logs", 
                  command=self.open_logs_folder).pack(side=tk.LEFT)
        
        # Barra inferior de marca
        self._create_brand_footer()
    
    def log_message(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        # Añadir al queue para procesamiento thread-safe
        self.log_queue.put(formatted_message)
    
    def start_log_processor(self):
        def process_logs():
            while True:
                try:
                    message = self.log_queue.get(timeout=0.1)
                    # Actualizar UI en hilo principal
                    self.root.after(0, self._append_log, message)
                except queue.Empty:
                    time.sleep(0.1)
        
        log_thread = threading.Thread(target=process_logs, daemon=True)
        log_thread.start()
    
    def _append_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def toggle_rpa(self):
        if self.is_running:
            self.stop_rpa()
        else:
            self.start_rpa()
    
    def start_rpa(self):
        try:
            # Verificar requisitos antes de iniciar
            if not self.check_requirements():
                self.log_message("No se pueden cumplir todos los requisitos", "ERROR")
                return
            
            # Verificar que existe main.py
            if not os.path.exists("main.py"):
                self.log_message("No se encontró main.py en el directorio actual", "ERROR")
                messagebox.showerror("Error", "No se encontró main.py en el directorio actual")
                return
            
            self.log_message("Iniciando sistema RPA...")
            
            # Iniciar proceso de Python
            self.rpa_process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                cwd=os.getcwd()
            )
            
            # Actualizar estado
            self.is_running = True
            self.status_label.config(text="Estado: Ejecutándose", foreground="green")
            self.main_button.config(text="⏹️ DETENER RPA")
            
            # Iniciar hilo para monitorear salida del proceso
            self.start_output_monitor()
            
            self.log_message("Sistema RPA iniciado correctamente", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Error al iniciar RPA: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"No se pudo iniciar el sistema RPA:\n{str(e)}")
    
    def stop_rpa(self):
        try:
            if self.rpa_process and self.rpa_process.poll() is None:
                self.log_message("Deteniendo sistema RPA...")
                self.rpa_process.terminate()
                
                # Esperar un poco para terminación limpia
                try:
                    self.rpa_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Forzar terminación si no responde
                    self.rpa_process.kill()
                    self.log_message("Proceso RPA forzado a terminar", "WARNING")
            
            # Actualizar estado
            self.is_running = False
            self.status_label.config(text="Estado: Detenido", foreground="red")
            self.main_button.config(text="🚀 INICIAR RPA")
            
            self.log_message("Sistema RPA detenido", "SUCCESS")
            
        except Exception as e:
            self.log_message(f"Error al detener RPA: {str(e)}", "ERROR")
    
    def start_output_monitor(self):
        def monitor_output():
            if self.rpa_process:
                for line in iter(self.rpa_process.stdout.readline, ''):
                    if line:
                        self.log_message(line.strip(), "RPA")
                
                # Proceso terminado
                if self.is_running:
                    self.root.after(0, self.on_process_ended)
        
        monitor_thread = threading.Thread(target=monitor_output, daemon=True)
        monitor_thread.start()
    
    def on_process_ended(self):
        self.is_running = False
        self.status_label.config(text="Estado: Detenido", foreground="red")
        self.main_button.config(text="🚀 INICIAR RPA")
        
        if self.rpa_process:
            return_code = self.rpa_process.poll()
            if return_code == 0:
                self.log_message("Sistema RPA terminado correctamente", "SUCCESS")
            else:
                self.log_message(f"Sistema RPA terminado con error (código: {return_code})", "ERROR")
    
    def check_requirements(self):
        all_good = True
        
        # Verificar Python
        try:
            python_version = sys.version
            self.req_python_label.config(text=f"Python: ✅ {sys.version.split()[0]}")
            self.log_message(f"Python detectado: {python_version.split()[0]}")
        except:
            self.req_python_label.config(text="Python: ❌")
            all_good = False
        
        # Verificar dependencias principales
        try:
            import cv2
            import PIL
            import schedule
            self.req_deps_label.config(text="Dependencias: ✅")
            self.log_message("Dependencias principales verificadas")
        except ImportError as e:
            self.req_deps_label.config(text="Dependencias: ❌")
            self.log_message(f"Faltan dependencias: {str(e)}", "WARNING")
            all_good = False
        
        # Verificar Tesseract
        tesseract_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
        ]
        
        tesseract_found = any(os.path.exists(path) for path in tesseract_paths)
        if tesseract_found:
            self.req_tesseract_label.config(text="Tesseract: ✅")
            self.log_message("Tesseract OCR encontrado")
        else:
            self.req_tesseract_label.config(text="Tesseract: ❌")
            self.log_message("Tesseract OCR no encontrado", "WARNING")
            all_good = False
        
        return all_good
    
    def install_dependencies(self):
        self.log_message("Instalando dependencias...")
        
        def install():
            try:
                # Ejecutar pip install
                result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.log_message("Dependencias instaladas correctamente", "SUCCESS")
                    self.root.after(0, self.check_requirements)
                else:
                    self.log_message(f"Error instalando dependencias: {result.stderr}", "ERROR")
            except Exception as e:
                self.log_message(f"Error en instalación: {str(e)}", "ERROR")
        
        # Ejecutar en hilo separado para no bloquear UI
        install_thread = threading.Thread(target=install, daemon=True)
        install_thread.start()
    
    def update_json_status(self):
        try:
            # Contar archivos JSON pendientes
            json_files = glob.glob("data/outputs_json/*.json")
            pending_count = len(json_files)
            
            # Contar archivos procesados hoy
            processed_dir = "data/outputs_json/Procesados"
            processed_today = 0
            
            if os.path.exists(processed_dir):
                today = datetime.now().date()
                for file in os.listdir(processed_dir):
                    if file.endswith('.json'):
                        file_path = os.path.join(processed_dir, file)
                        file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).date()
                        if file_date == today:
                            processed_today += 1
            
            # Actualizar labels
            self.json_pending_label.config(text=f"Pendientes: {pending_count}")
            self.json_processed_label.config(text=f"Procesados hoy: {processed_today}")
            
            # Log de actualización
            self.log_message(f"Estado JSON actualizado - Pendientes: {pending_count}, Procesados hoy: {processed_today}")
            
        except Exception as e:
            self.log_message(f"Error actualizando estado JSON: {str(e)}", "ERROR")
    
    def clear_logs(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log_message("Logs limpiados")
    
    def open_logs_folder(self):
        try:
            if os.path.exists("logs"):
                os.startfile("logs")
            else:
                self.log_message("Carpeta de logs no encontrada", "WARNING")
        except Exception as e:
            self.log_message(f"Error abriendo carpeta logs: {str(e)}", "ERROR")
    
    def on_closing(self):
        if self.is_running:
            if messagebox.askokcancel("Salir", "El sistema RPA está ejecutándose. ¿Deseas detenerlo y salir?"):
                self.stop_rpa()
                time.sleep(1)  # Dar tiempo para limpieza
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Mensaje inicial
        self.log_message("Launcher RPA TAMAPRINT iniciado")
        self.log_message("Haga clic en 'INICIAR RPA' para comenzar el procesamiento")
        
        # Iniciar loop principal
        self.root.mainloop()

    # === Utilidades de branding ===
    def _set_window_icon(self):
        try:
            if os.path.exists(self.brand_icon_path):
                # Preferir .ico en Windows
                self.root.iconbitmap(self.brand_icon_path)
                return
        except Exception:
            pass
        # Fallback: si hay logo PNG, usarlo como icono
        try:
            if os.path.exists(self.brand_logo_path):
                icon_img = self._load_image(self.brand_logo_path, max_size=(32, 32))
                if icon_img is not None:
                    self._image_refs['icon_img'] = icon_img
                    self.root.iconphoto(True, icon_img)
        except Exception:
            pass

    def _load_image(self, path: str, max_size=(72, 72)):
        """Carga una imagen y la reescala manteniendo relación de aspecto."""
        try:
            img = Image.open(path).convert("RGBA")
            img.thumbnail(max_size, Image.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def _add_link_label(self, parent, text: str, command):
        label = tk.Label(parent, text=text, fg="#1E6BF1", cursor="hand2", font=("Arial", 10, "underline"))
        label.bind("<Button-1>", lambda e: command())
        label.bind("<Enter>", lambda e: label.config(fg="#0B53D6"))
        label.bind("<Leave>", lambda e: label.config(fg="#1E6BF1"))
        return label

    def _open_email(self):
        try:
            webbrowser.open(f"mailto:{self.brand_email}?subject=Soporte%20RPA%20{self.brand_name}")
        except Exception:
            messagebox.showinfo("Contacto", f"Escríbenos a: {self.brand_email}")

    def _create_menubar(self):
        menubar = tk.Menu(self.root)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Acerca de AI4U", command=self._show_about)
        help_menu.add_command(label="Contacto", command=self._open_email)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        self.root.config(menu=menubar)

    def _show_about(self):
        message = (
            f"{self.brand_name} — {self.brand_tagline}\n\n"
            "Automatizamos procesos en SAP Business One con RPA, visión por computadora y OCR.\n\n"
            f"Contacto: {self.brand_email}"
        )
        messagebox.showinfo("Acerca de AI4U", message)

    def _create_brand_footer(self):
        sep = ttk.Separator(self.root, orient=tk.HORIZONTAL)
        sep.pack(fill=tk.X, pady=(6, 0))
        footer = ttk.Frame(self.root)
        footer.pack(fill=tk.X, pady=(4, 8))
        left = ttk.Label(footer, text=f"{self.brand_name} · {self.brand_tagline}", font=("Arial", 10))
        left.pack(side=tk.LEFT)
        right_container = ttk.Frame(footer)
        right_container.pack(side=tk.RIGHT)
        self._add_link_label(right_container, self.brand_email, self._open_email).pack(side=tk.RIGHT)

if __name__ == "__main__":
    app = RPALauncher()
    app.run()