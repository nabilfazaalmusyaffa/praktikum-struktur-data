import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque

# ==========================================
# NOTE CLASS
# ==========================================
class Note:
    def __init__(self, note_id, title, content):
        self.note_id = note_id
        self.title = title
        self.content = content
        self.tags = []

    def add_tag(self, tag):
        self.tags.append(tag)


# ==========================================
# TAG CLASS
# ==========================================
class Tag:
    def __init__(self, name):
        self.name = name
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)


# ==========================================
# CIRCULAR BUFFER
# ==========================================
class CircularBuffer:
    def __init__(self, size):
        self.buffer = deque(maxlen=size)

    def add_change(self, change):
        self.buffer.append(change)

    def get_changes(self):
        return list(self.buffer)


# ==========================================
# MAIN GUI APP
# ==========================================
class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Note Taking App")
        self.root.geometry("800x600")

        self.notes = []
        self.tags = {}
        self.sync_buffer = CircularBuffer(5)

        self.create_widgets()

    # --------------------------------------
    # UI COMPONENTS
    # --------------------------------------
    def create_widgets(self):

        title_label = tk.Label(
            self.root,
            text="Simple Note-Taking App",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)

        # INPUT FRAME
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Content").grid(row=1, column=0)
        self.content_entry = tk.Entry(input_frame, width=30)
        self.content_entry.grid(row=1, column=1)

        tk.Label(input_frame, text="Tags (comma separated)").grid(row=2, column=0)
        self.tag_entry = tk.Entry(input_frame, width=30)
        self.tag_entry.grid(row=2, column=1)

        add_button = tk.Button(
            input_frame,
            text="Add Note",
            command=self.add_note
        )
        add_button.grid(row=3, column=1, pady=10)

        # NOTE LIST
        note_frame = tk.Frame(self.root)
        note_frame.pack(pady=10)

        tk.Label(note_frame, text="Notes").pack()

        self.note_listbox = tk.Listbox(note_frame, width=60, height=10)
        self.note_listbox.pack()

        # BUTTON FRAME
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        chrono_button = tk.Button(
            button_frame,
            text="Chronological View",
            command=self.show_chronological
        )
        chrono_button.grid(row=0, column=0, padx=5)

        alpha_button = tk.Button(
            button_frame,
            text="Alphabetical View",
            command=self.show_alphabetical
        )
        alpha_button.grid(row=0, column=1, padx=5)

        sync_button = tk.Button(
            button_frame,
            text="Show Sync Buffer",
            command=self.show_sync
        )
        sync_button.grid(row=0, column=2, padx=5)

    # --------------------------------------
    # ADD NOTE
    # --------------------------------------
    def add_note(self):

        title = self.title_entry.get()
        content = self.content_entry.get()
        tag_text = self.tag_entry.get()

        if title == "" or content == "":
            messagebox.showerror("Error", "Title and content cannot be empty")
            return

        note = Note(len(self.notes) + 1, title, content)

        tags = [tag.strip() for tag in tag_text.split(",") if tag.strip()]

        for tag_name in tags:

            if tag_name not in self.tags:
                self.tags[tag_name] = Tag(tag_name)

            note.add_tag(tag_name)
            self.tags[tag_name].add_note(note)

        self.notes.append(note)

        self.sync_buffer.add_change(f"Added note: {title}")

        self.update_listbox(self.notes)

        self.title_entry.delete(0, tk.END)
        self.content_entry.delete(0, tk.END)
        self.tag_entry.delete(0, tk.END)

    # --------------------------------------
    # UPDATE LISTBOX
    # --------------------------------------
    def update_listbox(self, notes):

        self.note_listbox.delete(0, tk.END)

        for note in notes:
            tag_text = ", ".join(note.tags)

            self.note_listbox.insert(
                tk.END,
                f"{note.title} | Tags: {tag_text}"
            )

    # --------------------------------------
    # CHRONOLOGICAL VIEW
    # --------------------------------------
    def show_chronological(self):
        self.update_listbox(self.notes)

    # --------------------------------------
    # ALPHABETICAL VIEW
    # --------------------------------------
    def show_alphabetical(self):

        sorted_notes = sorted(
            self.notes,
            key=lambda note: note.title.lower()
        )

        self.update_listbox(sorted_notes)

    # --------------------------------------
    # SHOW SYNC BUFFER
    # --------------------------------------
    def show_sync(self):

        changes = self.sync_buffer.get_changes()

        message = "\n".join(changes)

        if message == "":
            message = "No recent changes"

        messagebox.showinfo("Recent Sync Changes", message)


# ==========================================
# RUN APP
# ==========================================
root = tk.Tk()
app = NoteApp(root)
root.mainloop()