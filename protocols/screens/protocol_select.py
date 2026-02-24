"""Protocol selection screen."""

import tkinter as tk
from collections.abc import Callable

from ..base import BaseScreen


class ProtocolSelectScreen(BaseScreen):
    """Screen for selecting which protocol to practice."""

    def __init__(
        self,
        root: tk.Tk,
        protocol_names: list[str],
        on_start: Callable[[str], None],
    ):
        self.protocol_names = protocol_names
        self.on_start = on_start
        super().__init__(root)

    def _setup_ui(self):
        """Set up the protocol selection UI."""
        # Title
        title = tk.Label(
            self.frame,
            text="EMS Protocol Practice",
            font=("Helvetica", 28, "bold"),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        )
        title.pack(pady=(40, 30))

        # Subtitle
        subtitle = tk.Label(
            self.frame,
            text="Select a protocol to practice:",
            font=("Helvetica", 14),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
        )
        subtitle.pack(pady=(0, 15))

        # Listbox frame with scrollbar
        list_frame = tk.Frame(self.frame, bg=self.BG_COLOR)
        list_frame.pack(pady=10, padx=40)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            list_frame,
            font=("Helvetica", 14),
            width=40,
            height=10,
            bg=self.CARD_COLOR,
            fg=self.DARK_TEXT,
            selectbackground="#3498db",
            selectforeground="white",
            activestyle="none",
            yscrollcommand=scrollbar.set,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar.config(command=self.listbox.yview)

        # Populate listbox
        for name in self.protocol_names:
            self.listbox.insert(tk.END, name)

        # Select first item if available
        if self.protocol_names:
            self.listbox.selection_set(0)
            self.listbox.activate(0)

        # Start button
        self.start_btn = tk.Button(
            self.frame,
            text="Start Practice",
            command=self._on_start_clicked,
            font=("Helvetica", 16, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#219a52",
            activeforeground="white",
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT,
        )
        self.start_btn.pack(pady=30)

        # Keyboard bindings
        self.listbox.bind("<Double-Button-1>", lambda e: self._on_start_clicked())
        self.listbox.bind("<Return>", lambda e: self._on_start_clicked())

    def _on_start_clicked(self):
        """Handle start button click."""
        selection = self.listbox.curselection()
        if selection:
            protocol_name = self.listbox.get(selection[0])
            self.on_start(protocol_name)

    def update_protocols(self, protocol_names: list[str]):
        """Update the list of available protocols."""
        self.protocol_names = protocol_names
        self.listbox.delete(0, tk.END)
        for name in protocol_names:
            self.listbox.insert(tk.END, name)
        if protocol_names:
            self.listbox.selection_set(0)
            self.listbox.activate(0)

    def show(self):
        """Show the screen and focus the listbox."""
        super().show()
        self.listbox.focus_set()
