# ui.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .config_manager import ConfigManager
from .repository import RepositoryManager
from .system import update_repository
from .current_repo import determine_current_repo  # Single-dot import

class RepositorySelectorUI(Gtk.Window):
    """
    A GTK-based UI for GhostBSD repository selection.
    Repositories are discovered via RepositoryManager. 
    The currently active repo is determined by determine_current_repo().
    """
    def __init__(self):
        super().__init__(title="Repo Selector")
        self.set_border_width(10)
        self.set_default_size(300, 200)
        self.set_icon_name("ghostbsd-logo")

        self.cfg = ConfigManager.get_instance()
        self.selected_repo = None

        main_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(main_vbox)

        self.status_label = Gtk.Label(label="Select a package repository location")
        main_vbox.pack_start(self.status_label, False, False, 0)

        scroll_area = Gtk.ScrolledWindow()
        scroll_area.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_vbox.pack_start(scroll_area, True, True, 0)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        scroll_area.add(self.vbox)

        self.radio_buttons = []

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        button_box.set_halign(Gtk.Align.CENTER)
        main_vbox.pack_start(button_box, False, False, 0)

        self.update_button = Gtk.Button(label="Update Repository")
        self.update_button.connect("clicked", self.on_update_clicked)
        button_box.pack_start(self.update_button, True, False, 0)

        self.exit_button = Gtk.Button(label="Close")
        self.exit_button.connect("clicked", Gtk.main_quit)
        button_box.pack_end(self.exit_button, True, False, 0)

        # 1) Load available repos
        repo_manager = RepositoryManager()
        for repo_name in repo_manager.repos:
            self.add_radio_button(repo_name)

        # 2) Determine the system's current active repo
        system_current_repo = determine_current_repo()
        if system_current_repo:
            self.set_current_repo(system_current_repo)

        # 3) If you also want to honor a "LastSelectedRepo" in memory, you could do:
        # last_repo = self.cfg.get("LastSelectedRepo", None)
        # if last_repo:
        #     self.set_current_repo(last_repo)

    def add_radio_button(self, label):
        button = Gtk.RadioButton.new_with_label_from_widget(
            None if not self.radio_buttons else self.radio_buttons[0],
            label
        )
        button.connect("toggled", self.on_radio_button_toggled, label)
        self.vbox.pack_start(button, False, False, 0)
        self.radio_buttons.append(button)

    def on_radio_button_toggled(self, button, repo):
        if button.get_active():
            self.selected_repo = repo
            self.cfg.set("LastSelectedRepo", repo)

    def on_update_clicked(self, widget):
        if self.selected_repo:
            password = self.show_password_prompt()
            repo_path = RepositoryManager().get_repo_path(self.selected_repo)
            success = update_repository(
                source=repo_path,
                dest="/usr/local/etc/pkg/repos/GhostBSD.conf",
                password=password
            )
            if success:
                self.set_status(f"Repository updated to {self.selected_repo}")
            else:
                self.show_dialog("Error", Gtk.MessageType.ERROR, "Failed to update repository.")
        else:
            self.show_dialog("Warning", Gtk.MessageType.WARNING, "Please select a repository.")

    def set_current_repo(self, repo_name):
        normalized = repo_name.strip().lower()
        for button in self.radio_buttons:
            if button.get_label().strip().lower() == normalized:
                button.set_active(True)
                return
        print(f"Warning: Could not find repo '{repo_name}' in the list of radio buttons.")

    def set_status(self, message):
        self.status_label.set_text(message)

    def show_dialog(self, title, message_type, message):
        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=message_type,
            buttons=Gtk.ButtonsType.OK,
            text=title,
            secondary_text=message
        )
        dialog.run()
        dialog.destroy()

    def show_password_prompt(self):
        dialog = Gtk.Dialog(title="Authentication Required", parent=self)
        dialog.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK, Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL)

        content_area = dialog.get_content_area()
        content_area.set_spacing(5)

        label = Gtk.Label(label="Enter your password:")
        content_area.add(label)

        password_entry = Gtk.Entry()
        password_entry.set_visibility(False)
        password_entry.set_invisible_char('*')
        password_entry.connect("activate", lambda _: dialog.response(Gtk.ResponseType.OK))
        content_area.add(password_entry)

        content_area.show_all()

        response = dialog.run()
        password = password_entry.get_text() if response == Gtk.ResponseType.OK else None
        dialog.destroy()
        return password

    def show(self):
        self.show_all()
        Gtk.main()

