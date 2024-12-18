import tkinter as tk
from tkinter import filedialog, ttk
import numpy as np
import soundfile as sf
import os
import threading
from scipy import signal
import warnings
import subprocess

warnings.filterwarnings('ignore', category=UserWarning, module='scipy.signal')

class NoiseReducerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Noise Reducer")
        self.root.geometry("600x450")
        
        # Supported formats
        self.input_formats = [
            ("All Audio Files", "*.wav;*.mp3;*.ogg;*.flac;*.m4a"),
            ("WAV files", "*.wav"),
            ("MP3 files", "*.mp3"),
            ("OGG files", "*.ogg"),
            ("FLAC files", "*.flac"),
            ("M4A files", "*.m4a"),
            ("All files", "*.*")
        ]
        
        self.output_formats = {
            "WAV": ".wav",
            "MP3": ".mp3",
            "OGG": ".ogg",
            "FLAC": ".flac"
        }
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input file selection
        ttk.Label(self.main_frame, text="Input Audio File:").grid(row=0, column=0, sticky=tk.W)
        self.input_path = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_input).grid(row=0, column=2)
        
        # Output file selection
        ttk.Label(self.main_frame, text="Output Location:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.output_path = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_output).grid(row=1, column=2)
        
        # Output format selection
        ttk.Label(self.main_frame, text="Output Format:").grid(row=2, column=0, sticky=tk.W)
        self.output_format = tk.StringVar(value="WAV")
        format_combo = ttk.Combobox(self.main_frame, textvariable=self.output_format, 
                                  values=list(self.output_formats.keys()), state="readonly")
        format_combo.grid(row=2, column=1, sticky=tk.W, padx=5)
        format_combo.bind('<<ComboboxSelected>>', self.update_output_extension)
        
        # Noise reduction strength
        ttk.Label(self.main_frame, text="Noise Reduction Strength:").grid(row=3, column=0, sticky=tk.W, pady=10)
        self.strength = tk.DoubleVar(value=1.0)
        strength_scale = ttk.Scale(self.main_frame, from_=0.1, to=6.0, variable=self.strength, 
                                 orient=tk.HORIZONTAL, command=self.update_strength_label)
        strength_scale.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Strength value label
        self.strength_label = ttk.Label(self.main_frame, text="1.0")
        self.strength_label.grid(row=3, column=2)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, length=400, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_label.grid(row=5, column=0, columnspan=3)
        
        # Process button
        self.process_btn = ttk.Button(self.main_frame, text="Reduce Noise", command=self.start_processing)
        self.process_btn.grid(row=6, column=0, columnspan=3, pady=20)

    def browse_input(self):
        filename = filedialog.askopenfilename(filetypes=self.input_formats)
        if filename:
            self.input_path.set(filename)
            base_path = os.path.splitext(filename)[0]
            self.output_path.set(f"{base_path}_denoised{self.output_formats[self.output_format.get()]}")

    def browse_output(self):
        initial_file = self.output_path.get() if self.output_path.get() else "denoised_audio"
        filename = filedialog.asksaveasfilename(
            defaultextension=self.output_formats[self.output_format.get()],
            filetypes=[(f"{fmt} files", f"*{ext}") for fmt, ext in self.output_formats.items()],
            initialfile=initial_file
        )
        if filename:
            self.output_path.set(filename)

    def update_output_extension(self, event=None):
        if self.output_path.get():
            base_path = os.path.splitext(self.output_path.get())[0]
            new_ext = self.output_formats[self.output_format.get()]
            self.output_path.set(f"{base_path}{new_ext}")

    def convert_to_wav(self, input_path):
        temp_wav = os.path.join(os.path.dirname(input_path), "_temp_conversion.wav")
        try:
            # Use FFmpeg for conversion
            subprocess.run([
                'ffmpeg', '-i', input_path,
                '-acodec', 'pcm_s16le',
                '-ar', '44100',
                '-y',  # Overwrite output file if it exists
                temp_wav
            ], check=True, capture_output=True)
            return temp_wav
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error converting file: {str(e)}")

    def convert_from_wav(self, input_wav, output_path, format_type):
        try:
            # Use FFmpeg for conversion with format-specific settings
            if format_type == "MP3":
                subprocess.run([
                    'ffmpeg', '-i', input_wav,
                    '-codec:a', 'libmp3lame',
                    '-q:a', '0',  # Highest quality
                    '-y',
                    output_path
                ], check=True, capture_output=True)
            elif format_type == "OGG":
                subprocess.run([
                    'ffmpeg', '-i', input_wav,
                    '-codec:a', 'libvorbis',
                    '-q:a', '10',  # High quality
                    '-y',
                    output_path
                ], check=True, capture_output=True)
            elif format_type == "FLAC":
                subprocess.run([
                    'ffmpeg', '-i', input_wav,
                    '-codec:a', 'flac',
                    '-y',
                    output_path
                ], check=True, capture_output=True)
            else:  # WAV
                os.replace(input_wav, output_path)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error converting output file: {str(e)}")

    def process_audio(self):
        temp_wav = None
        try:
            input_path = self.input_path.get()
            output_path = self.output_path.get()
            
            # Convert input to WAV if needed
            if not input_path.lower().endswith('.wav'):
                self.status_var.set("Converting input file...")
                self.root.after(0, self.progress.configure, {'value': 10})
                temp_wav = self.convert_to_wav(input_path)
                input_path = temp_wav
            
            # Load audio file
            self.status_var.set("Loading audio file...")
            self.root.after(0, self.progress.configure, {'value': 20})
            
            audio_data, sample_rate = sf.read(input_path)
            
            # Convert to mono if stereo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Normalize input audio
            audio_data = audio_data.astype(np.float32)
            if audio_data.max() > 1.0 or audio_data.min() < -1.0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            self.status_var.set("Reducing noise...")
            self.root.after(0, self.progress.configure, {'value': 40})
            
            # Apply noise reduction
            denoised_audio = self.reduce_noise(audio_data, self.strength.get())
            
            self.root.after(0, self.progress.configure, {'value': 80})
            
            # Save to temporary WAV
            temp_output = os.path.join(os.path.dirname(output_path), "_temp_output.wav")
            sf.write(temp_output, denoised_audio, sample_rate)
            
            # Convert to desired format
            self.status_var.set("Converting to final format...")
            self.convert_from_wav(temp_output, output_path, self.output_format.get())
            
            # Clean up temporary files
            if temp_wav and os.path.exists(temp_wav):
                os.remove(temp_wav)
            if os.path.exists(temp_output):
                os.remove(temp_output)
            
            self.root.after(0, self.processing_complete)
            
        except Exception as e:
            if temp_wav and os.path.exists(temp_wav):
                os.remove(temp_wav)
            self.root.after(0, self.processing_error, str(e))

    def reduce_noise(self, audio_data, strength=1.0):
        # Parameters for STFT
        nperseg = 2048  # Window length
        noverlap = nperseg // 2  # Overlap between windows
        
        # Compute STFT
        f, t, Zxx = signal.stft(audio_data, fs=44100, nperseg=nperseg, noverlap=noverlap,
                               boundary='zeros', padded=True)
        
        # Get magnitude and phase
        magnitude = np.abs(Zxx)
        phase = np.angle(Zxx)
        
        # Add small constant to prevent division by zero
        eps = np.finfo(magnitude.dtype).eps
        
        # Estimate noise profile from the first 100ms of audio
        noise_profile = np.mean(magnitude[:, :10], axis=1)
        
        # Compute mask with numerical stability
        mask = (magnitude - noise_profile.reshape(-1, 1) * strength) / (magnitude + eps)
        mask = np.maximum(0, mask)
        mask = np.minimum(1, mask)
        
        # Smooth the mask
        smoothed_mask = signal.medfilt2d(mask, kernel_size=(3, 3))
        
        # Apply the mask
        Zxx_denoised = Zxx * smoothed_mask
        
        # Inverse STFT
        _, denoised_audio = signal.istft(Zxx_denoised, fs=44100, nperseg=nperseg,
                                       noverlap=noverlap, boundary=True)
        
        # Match length and normalize
        if len(denoised_audio) > len(audio_data):
            denoised_audio = denoised_audio[:len(audio_data)]
        elif len(denoised_audio) < len(audio_data):
            denoised_audio = np.pad(denoised_audio, (0, len(audio_data) - len(denoised_audio)))
        
        denoised_audio = np.float32(denoised_audio)
        max_val = np.max(np.abs(denoised_audio))
        if max_val > 1.0:
            denoised_audio = denoised_audio / max_val
        
        return denoised_audio

    def processing_complete(self):
        self.status_var.set("Processing complete!")
        self.progress.configure(value=100)
        self.process_btn.state(['!disabled'])

    def processing_error(self, error_message):
        self.status_var.set(f"Error: {error_message}")
        self.process_btn.state(['!disabled'])

    def update_strength_label(self, *args):
        self.strength_label.configure(text=f"{self.strength.get():.1f}")

    def start_processing(self):
        if not self.input_path.get() or not self.output_path.get():
            self.status_var.set("Please select input and output files")
            return
        
        self.process_btn.state(['disabled'])
        self.status_var.set("Processing...")
        self.progress.configure(value=0)
        
        thread = threading.Thread(target=self.process_audio)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoiseReducerApp(root)
    root.mainloop()