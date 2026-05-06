"""VideoSlim GUI - Modern graphical interface using CustomTkinter."""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import transcoding
import os


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VideoSlimGUI:
    """Modern GUI for VideoSlim video compression tool."""
    
    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("VideoSlim - Video Compression Tool")
        self.root.geometry("600x610")
        self.root.resizable(True, True)
        self.root.minsize(600, 500)
        self.root.configure(fg_color="#1e1e2e")
        
        # Variables
        self.path_var = ctk.StringVar()
        self.vcodec_var = ctk.StringVar(value="hevc")
        self.acodec_var = ctk.StringVar(value="aac")
        self.crf_var = ctk.DoubleVar(value=28)
        self.recursive_var = ctk.BooleanVar(value=False)
        self.delete_var = ctk.BooleanVar(value=False)
        self.is_processing = False
        self.stop_event = threading.Event()
        self.total_files = 0
        self.current_file_index = 0
        
        # Build UI
        self._build_ui()
    
    def _build_ui(self):
        """Build the modern user interface."""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color=("#f5f5f5", "#2a2a2a"))
        header_frame.pack(fill="x", padx=0, pady=0)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="VideoSlim",
            font=("Helvetica", 10, "bold"),
            text_color="white"
        )
        title_label.pack(anchor="w", pady=(0, 0), padx=15)
        
        # Content frame with scrolling
        content_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # === FILE SELECTION ===
        file_frame = ctk.CTkFrame(content_frame, fg_color=("#f5f5f5", "#2a2a2a"), corner_radius=10)
        file_frame.pack(fill="x", pady=(0, 0))
        
        file_title = ctk.CTkLabel(file_frame, text="📁 Select Video", font=("Helvetica", 14, "bold"))
        file_title.pack(anchor="w", padx=15, pady=(0, 0))
        
        file_input_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_input_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        self.path_entry = ctk.CTkEntry(
            file_input_frame,
            textvariable=self.path_var,
            placeholder_text="Select a video file or folder...",
            height=40,
            font=("Helvetica", 11)
        )
        self.path_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        file_button_frame = ctk.CTkFrame(file_input_frame, fg_color="transparent")
        file_button_frame.pack(side="left", padx=0)
        
        ctk.CTkButton(
            file_button_frame,
            text="📄 File",
            command=self._browse_file,
            width=90,
            height=40,
            font=("Helvetica", 11, "bold"),
            corner_radius=8
        ).pack(side="left", padx=(0, 8))
        
        ctk.CTkButton(
            file_button_frame,
            text="📂 Folder",
            command=self._browse_folder,
            width=90,
            height=40,
            font=("Helvetica", 11, "bold"),
            corner_radius=8
        ).pack(side="left")
        
        # === CODEC SETTINGS ===
        codec_frame = ctk.CTkFrame(content_frame, fg_color=("#f5f5f5", "#2a2a2a"), corner_radius=10)
        codec_frame.pack(fill="x", pady=(0, 0))
        
        codec_title = ctk.CTkLabel(codec_frame, text="⚙️ Codec Settings", font=("Helvetica", 14, "bold"))
        codec_title.pack(anchor="w", padx=15, pady=(0, 0))
        
        # Video Codec
        vcodec_row = ctk.CTkFrame(codec_frame, fg_color="transparent")
        vcodec_row.pack(fill="x", padx=15, pady=(0, 0))
        
        ctk.CTkLabel(vcodec_row, text="Video Codec:", font=("Helvetica", 11, "bold"), width=120).pack(side="left", padx=(0, 10))
        ctk.CTkComboBox(
            vcodec_row,
            variable=self.vcodec_var,
            values=["hevc", "h264", "vp9", "av1"],
            state="readonly",
            width=150,
            height=35,
            font=("Helvetica", 11)
        ).pack(side="left", padx=(0, 30))
        
        ctk.CTkLabel(vcodec_row, text="Audio Codec:", font=("Helvetica", 11, "bold"), width=120).pack(side="left", padx=(0, 10))
        ctk.CTkComboBox(
            vcodec_row,
            variable=self.acodec_var,
            values=["aac", "mp3", "opus", "flac", "ac3"],
            state="readonly",
            width=150,
            height=35,
            font=("Helvetica", 11)
        ).pack(side="left")
        
        # CRF Slider
        crf_row = ctk.CTkFrame(codec_frame, fg_color="transparent")
        crf_row.pack(fill="x", padx=15, pady=(0, 0))
        
        crf_label = ctk.CTkLabel(crf_row, text="Quality (CRF):", font=("Helvetica", 11, "bold"), width=120)
        crf_label.pack(side="left", padx=(0, 0))
        
        self.crf_slider = ctk.CTkSlider(
            crf_row,
            from_=0,
            to=51,
            variable=self.crf_var,
            command=self._update_crf_label,
            width=200,
            height=8,
            button_length=20,
            button_corner_radius=8
        )
        self.crf_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.crf_label = ctk.CTkLabel(crf_row, text="28", font=("Helvetica", 11, "bold"), width=40)
        self.crf_label.pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(crf_row, text="(0=best, 51=worst)", font=("Helvetica", 11, "bold")).pack(side="left")
        
        # === OPTIONS ===
        options_frame = ctk.CTkFrame(content_frame, fg_color=("#f5f5f5", "#2a2a2a"), corner_radius=10)
        options_frame.pack(fill="x", pady=(0, 10))
        
        options_title = ctk.CTkLabel(options_frame, text="✓ Options", font=("Helvetica", 14, "bold"))
        options_title.pack(anchor="w", padx=15, pady=(0, 0))
        
        options_row = ctk.CTkFrame(options_frame, fg_color="transparent")
        options_row.pack(fill="x", padx=15, pady=(0, 0))
        
        ctk.CTkCheckBox(
            options_row,
            text="Recursive search",
            variable=self.recursive_var,
            font=("Helvetica", 11),
            checkbox_width=22,
            checkbox_height=22,
            corner_radius=6
        ).pack(side="left", padx=(0, 20), pady=6)
        
        ctk.CTkCheckBox(
            options_row,
            text="Delete originals",
            variable=self.delete_var,
            font=("Helvetica", 11),
            checkbox_width=22,
            checkbox_height=22,
            corner_radius=6
        ).pack(side="left", pady=6)
        
        # === BUTTONS ===
        button_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 15))
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶ Start",
            command=self._start_compression,
            height=45,
            font=("Helvetica", 13, "bold"),
            fg_color=("#89b4fa", "#74c7ff"),
            hover_color=("#6a9bf7", "#5a8ce2"),
            corner_radius=10,
            text_color="#1e1e2e"
        )
        self.start_button.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="■ Stop",
            command=self._stop_compression,
            height=45,
            font=("Helvetica", 13, "bold"),
            fg_color=("#f38ba8", "#f5c2e7"),
            hover_color=("#eba0c1", "#f2c8dd"),
            corner_radius=10,
            text_color="#1e1e2e",
            width=120,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=(0, 10))
        
        # === PROGRESS BAR ===
        progress_frame = ctk.CTkFrame(content_frame, fg_color=("#313244", "#1f1d2e"), corner_radius=10)
        progress_frame.pack(fill="x", pady=(0, 0))
        
        self.total_progress_label = ctk.CTkLabel(progress_frame, text="Total progress: 0%", font=("Helvetica", 11), anchor="w")
        self.total_progress_label.pack(fill="x", padx=15, pady=(0, 6))
        
        self.total_progress_bar = ctk.CTkProgressBar(progress_frame)
        self.total_progress_bar.set(0.0)
        self.total_progress_bar.pack(fill="x", padx=15, pady=(0, 20))
        
        # === LOG ===
        self.log_frame = ctk.CTkFrame(content_frame, fg_color=("#f5f5f5", "#2a2a2a"), corner_radius=10)
        self.log_frame.pack(fill="both", expand=True, pady=(0, 0))
        
        self.log_visible = False
        self.log_toggle_button = ctk.CTkLabel(
            self.log_frame,
            text="Show logs",
            font=("Helvetica", 12, "underline"),
            text_color=("#89b4fa", "#74c7ff"),
            cursor="hand2"
        )
        self.log_toggle_button.pack(anchor="w", padx=15, pady=(0, 4))
        self.log_toggle_button.bind("<Button-1>", lambda e: self._toggle_log())
        
        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            height=200,
            wrap="word",
            font=("Courier", 10),
            corner_radius=8,
            fg_color=("#ffffff", "#1a1a1a"),
            text_color="#e0e0e0"
        )
        
        
        # === STATUS BAR ===
        status_frame = ctk.CTkFrame(main_frame, fg_color=("#e0e0e0", "#1f1f1f"), corner_radius=0)
        status_frame.pack(fill="x", padx=0, pady=0)
        
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            status_frame,
            textvariable=self.status_var,
            font=("Helvetica", 10),
            text_color=("#333333", "#cccccc")
        )
        self.status_label.pack(anchor="w", padx=15, pady=8)
    
    def _browse_file(self):
        """Browse for a video file."""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.mkv *.avi *.mov *.wmv *.flv *.webm *.m4v *.3gp *.ts *.m2ts *.vob *.ogv *.divx *.mpg"), ("All files", "*.*")]
        )
        if file_path:
            self.path_var.set(file_path)
            self._log(f"✓ Selected file: {file_path}")
            self._reset_progress()
    
    def _browse_folder(self):
        """Browse for a folder."""
        folder_path = filedialog.askdirectory(title="Select Folder with Videos")
        if folder_path:
            self.path_var.set(folder_path)
            self._log(f"✓ Selected folder: {folder_path}")
            self._reset_progress()
    
    def _update_crf_label(self, value):
        """Update CRF label with current value."""
        self.crf_label.configure(text=str(int(float(value))))
    
    def _log(self, message):
        """Add a message to the log."""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.root.update()
    
    def _clear_log(self):
        """Clear the log."""
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        self._reset_progress()
    
    def _toggle_log(self):
        """Toggle the log area visibility."""
        if self.log_visible:
            self.log_text.pack_forget()
            self.log_toggle_button.configure(text="Show logs")
            self.log_visible = False
        else:
            self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 12))
            self.log_toggle_button.configure(text="Hide logs")
            self.log_visible = True
        self.root.update()
    
    def _reset_progress(self):
        """Reset progress indicators."""
        self.current_file_index = 0
        self.total_files = 0
        self.total_progress_bar.set(0.0)
        self.total_progress_label.configure(text="Total progress: 0%")
    
    def _update_total_progress(self):
        """Update total progress after a file completes."""
        if self.total_files > 0:
            total_percent = self.current_file_index / self.total_files * 100
            self.total_progress_bar.set(total_percent / 100.0)
            self.total_progress_label.configure(text=f"Total progress: {total_percent:.0f}%")
        self.root.update()
    
    def _validate_inputs(self) -> bool:
        """Validate user inputs."""
        if not self.path_var.get():
            messagebox.showerror("Error", "Please select a file or folder")
            return False
        path = self.path_var.get()
        if not os.path.exists(path):
            messagebox.showerror("Error", f"Path does not exist: {path}")
            return False
        return True
    
    def _start_compression(self):
        """Start the compression process."""
        if not self._validate_inputs():
            return
        if self.is_processing:
            messagebox.showwarning("Warning", "Compression is already running")
            return
        self.is_processing = True
        self.stop_event.clear()
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_var.set("Processing...")
        self._log("=" * 60)
        self._log("Starting compression...")
        thread = threading.Thread(target=self._compression_worker)
        thread.daemon = True
        thread.start()
    
    def _stop_compression(self):
        """Stop the active compression."""
        if not self.is_processing:
            return
        self.stop_event.set()
        self._log("⏹️ Stop requested. Waiting for current process to finish...")
        self.status_var.set("Stopping...")
        self.stop_button.configure(state="disabled")
    
    def _compression_worker(self):
        """Worker thread for compression."""
        try:
            path = self.path_var.get()
            vcodec = self.vcodec_var.get()
            crf = int(self.crf_var.get())
            acodec = self.acodec_var.get()
            recursive = self.recursive_var.get()
            delete = self.delete_var.get()
            
            self.total_progress_bar.set(0.0)
            self.current_file_index = 0
            self.total_files = 0
            
            valid, error_msg = transcoding.validate_codecs(vcodec, acodec, crf)
            if not valid:
                self._log(f"❌ Error: {error_msg}")
                self.status_var.set("Error")
                return
            
            if not transcoding.check_ffmpeg_installed():
                self._log("❌ FFmpeg binaries not found!")
                self.status_var.set("Error")
                return
            
            self._log(f"Video codec: {vcodec}")
            self._log(f"Audio codec: {acodec}")
            self._log(f"Quality (CRF): {crf}")
            self._log(f"Recursive: {recursive}")
            self._log(f"Delete originals: {delete}")
            self._log("-" * 60)
            
            if os.path.isdir(path):
                video_files = [
                    os.path.join(root, file)
                    for root, _, files in os.walk(path)
                    for file in files
                    if os.path.splitext(file)[1].lower() in transcoding.VIDEO_EXTENSIONS
                ]
                self.total_files = len(video_files)
                if self.total_files == 0:
                    self._log("❌ No video files found in folder")
                else:
                    for index, file_path in enumerate(video_files, start=1):
                        if self.stop_event.is_set():
                            raise KeyboardInterrupt("Stopped by user")
                        self.current_file_index = index
                        success = transcoding.transcode_file(
                            file_path,
                            vcodec,
                            crf,
                            acodec,
                            delete,
                            stop_event=self.stop_event
                        )
                        if not success:
                            self._log(f"⚠️ Skipped: {os.path.basename(file_path)}")
                        self._update_total_progress()
                    self._log(f"\n✅ Compression complete! Processed {self.total_files} file(s)")
            else:
                self.total_files = 1
                result = transcoding.transcode_file(
                    path,
                    vcodec,
                    crf,
                    acodec,
                    delete,
                    stop_event=self.stop_event
                )
                self._update_total_progress()
                if result:
                    self._log("\n✅ Compression complete!")
                else:
                    self._log("\n⚠️ Compression failed or skipped")
            
            self.status_var.set("Ready")
            messagebox.showinfo("Success", "Compression finished!")
            
        except KeyboardInterrupt:
            self._log("\n⏹️ Compression stopped by user")
            self.status_var.set("Stopped")
        except Exception as e:
            self._log(f"\n❌ Error: {str(e)}")
            self.status_var.set("Error")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.is_processing = False
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.stop_event.clear()



def main():
    """Main entry point for the GUI."""
    root = ctk.CTk()
    app = VideoSlimGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
