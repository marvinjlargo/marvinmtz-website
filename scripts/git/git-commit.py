import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os

class GitCommitGUI:
    def __init__(self, master):
        self.master = master
        master.title("Git Commit and Push")
        master.geometry("600x450")

        self.repo_path = ""
        self.create_widgets()

    def create_widgets(self):
        # Repository Selection
        self.repo_label = ttk.Label(self.master, text="Repository:")
        self.repo_label.pack(pady=(20, 0))
        self.repo_entry = ttk.Entry(self.master, width=70)
        self.repo_entry.pack(pady=(0, 10))
        self.repo_button = ttk.Button(self.master, text="Select Repository", command=self.select_repo)
        self.repo_button.pack()

        # Commit Message Entry
        self.message_label = ttk.Label(self.master, text="Commit Message:")
        self.message_label.pack(pady=(20, 0))
        self.message_entry = tk.Text(self.master, height=5, width=70)
        self.message_entry.pack(pady=10)

        # Buttons
        button_frame = ttk.Frame(self.master)
        button_frame.pack(pady=20)

        self.commit_button = ttk.Button(button_frame, text="Commit", command=self.commit_changes)
        self.commit_button.pack(side=tk.LEFT, padx=10)

        self.push_button = ttk.Button(button_frame, text="Push", command=self.push_changes)
        self.push_button.pack(side=tk.LEFT, padx=10)

        # Status Label
        self.status_label = ttk.Label(self.master, text="")
        self.status_label.pack(pady=20)

    def select_repo(self):
        self.repo_path = filedialog.askdirectory()
        self.repo_entry.delete(0, tk.END)
        self.repo_entry.insert(0, self.repo_path)

    def run_git_command(self, command):
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True, cwd=self.repo_path)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    def commit_changes(self):
        if not self.repo_path:
            messagebox.showerror("Error", "Please select a repository first.")
            return

        commit_message = self.message_entry.get("1.0", tk.END).strip()
        if not commit_message:
            messagebox.showerror("Error", "Please enter a commit message.")
            return

        # Stage all changes
        stage_result = self.run_git_command(["git", "add", "."])
        if "Error" in stage_result:
            self.status_label.config(text=stage_result)
            return

        # Commit changes
        commit_result = self.run_git_command(["git", "commit", "-m", commit_message])
        self.status_label.config(text=commit_result)
        self.message_entry.delete("1.0", tk.END)

    def push_changes(self):
        if not self.repo_path:
            messagebox.showerror("Error", "Please select a repository first.")
            return

        push_result = self.run_git_command(["git", "push"])
        self.status_label.config(text=push_result)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitCommitGUI(root)
    root.mainloop()