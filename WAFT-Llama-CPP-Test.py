import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import subprocess
import threading
import os
import tempfile

class WAFTIntelligenceEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("👻 GHOST PROTOCOL v2.7 - Surgical Strike")
        self.root.geometry("1200x950")
        self.root.configure(bg="#1e1e1e")

        # Preset Configuration
        self.project_path = "/Users/ctavolazzi/code/active/waft" 
        self.project_memory = "Knowledge Base Seeded."
        self.max_tokens = 8192 

        self.setup_ui()
        if os.path.exists(self.project_path):
            self.run_intelligence_loop()

    def setup_ui(self):
        self.paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.paned, bg="#252526", width=220)
        self.paned.add(self.left_frame)

        # Context Progress Bar
        tk.Label(self.left_frame, text="🧠 CONTEXT USAGE", bg="#252526", fg="white").pack(pady=(20,5))
        self.progress = ttk.Progressbar(self.left_frame, orient=tk.HORIZONTAL, length=180, mode='determinate')
        self.progress.pack(pady=5, padx=10)
        self.usage_label = tk.Label(self.left_frame, text="0 / 8192 Tokens", bg="#252526", fg="#858585", font=("Arial", 10))
        self.usage_label.pack(pady=5)

        tk.Button(self.left_frame, text="📋 Copy Live Stream", command=lambda: self.copy_to_clipboard(self.stream_area)).pack(pady=10, padx=10, fill=tk.X)
        tk.Button(self.left_frame, text="🧠 Copy Global Memory", command=lambda: self.copy_to_clipboard(self.memory_area)).pack(pady=5, padx=10, fill=tk.X)

        self.right_paned = ttk.PanedWindow(self.paned, orient=tk.VERTICAL)
        self.paned.add(self.right_paned)
        self.stream_area = scrolledtext.ScrolledText(self.right_paned, bg="black", fg="#00FF00", font=("Courier New", 12))
        self.right_paned.add(self.stream_area)
        self.memory_area = scrolledtext.ScrolledText(self.right_paned, bg="#1e1e1e", fg="#dcdcdc", font=("Arial", 13), wrap=tk.WORD)
        self.right_paned.add(self.memory_area)

    def update_progress(self, text):
        est_tokens = len(text) // 4
        percent = (est_tokens / self.max_tokens) * 100
        self.progress['value'] = percent
        self.usage_label.config(text=f"{est_tokens} / {self.max_tokens} Tokens")

    def run_intelligence_loop(self):
        threading.Thread(target=self.intel_loop_core, daemon=True).start()

    def intel_loop_core(self):
        files = []
        for r, _, fs in os.walk(self.project_path):
            if any(x in r for x in [".git", "node_modules", "build"]): continue
            for f in fs:
                if f.endswith(('.py', '.js', '.sh', '.yaml', '.md')):
                    files.append(os.path.join(r, f))
        
        # Priority sort: Metadata first
        files.sort(key=lambda x: ("README" not in x, "config" not in x, x))

        for file_path in files:
            file_name = os.path.basename(file_path)
            with open(file_path, 'r', errors='ignore') as f: 
                # SURGICAL STRIKE: We only take the first 800 characters. 
                # This ensures the TOTAL request (Memory + File) stays well under 8k.
                content = f.read()[:800] 

            self.update_ui_stream(f"\n🧠 ANALYZING: {file_name}\n")
            
            instruction = (
                f"GLOBAL CONTEXT:\n{self.project_memory}\n\n"
                f"FILE FRAGMENT ({file_name}):\n{content}\n\n"
                "TASK: Update the context. Be brutal with brevity. "
                "Only list new technical dependencies or data flows. Max 100 words."
            )

            with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp_file:
                tmp_file.write(instruction)
                tmp_path = tmp_file.name

            try:
                # Use 'cat' to bypass shell argument limits
                process = subprocess.Popen(
                    f"cat {tmp_path} | cn -p", 
                    shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
                )

                current_file_logic = ""
                for line in process.stdout:
                    self.update_ui_stream(line)
                    current_file_logic += line

                if current_file_logic.strip():
                    self.project_memory = current_file_logic
                    self.update_ui_memory(self.project_memory)
                    self.update_progress(self.project_memory)
            
            finally:
                if os.path.exists(tmp_path): os.remove(tmp_path)

        self.update_ui_stream("\n✅ GHOST PROTOCOL: PROJECT MAPPED.")

    def copy_to_clipboard(self, widget):
        self.root.clipboard_clear()
        self.root.clipboard_append(widget.get(1.0, tk.END))
        messagebox.showinfo("Success", "Copied to clipboard.")

    def update_ui_stream(self, text):
        self.stream_area.insert(tk.END, text)
        self.stream_area.see(tk.END)

    def update_ui_memory(self, text):
        self.memory_area.delete(1.0, tk.END)
        self.memory_area.insert(tk.END, text)

if __name__ == "__main__":
    root = tk.Tk()
    WAFTIntelligenceEngine(root)
    root.mainloop()