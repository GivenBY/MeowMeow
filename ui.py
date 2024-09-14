import gi
from typing import Optional

from api import MeowMeowAPI

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio, Pango, Gdk


class HeaderBarWindow(Gtk.Window):
    def __init__(self, api_handler: MeowMeowAPI) -> None:
        super().__init__()
        self.set_border_width(10)
        self.set_default_size(600, 400)
        self.api_handler: MeowMeowAPI = api_handler

        self.popover: Gtk.Popover
        self.api_key_entry: Gtk.Entry
        self.text_view: Gtk.TextView
        self.text_buffer: Gtk.TextBuffer
        self.tag_bold: Gtk.TextTag
        self.tag_bg: Gtk.TextTag
        self.prompt_entry: Gtk.Entry

        self.setup_header_bar()
        self.setup_main_content()

    def setup_header_bar(self) -> None:
        hb: Gtk.HeaderBar = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.props.title = "=^..^="
        self.set_titlebar(hb)

        settings_button: Gtk.Button = Gtk.Button()
        icon: Gio.ThemedIcon = Gio.ThemedIcon(name="emblem-system")
        image: Gtk.Image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        settings_button.add(image)
        settings_button.set_tooltip_text("Api Key")
        hb.pack_start(settings_button)

        self.setup_settings_popover(settings_button)

        new_request_button: Gtk.Button = Gtk.Button.new_from_icon_name(
            "contact-new", Gtk.IconSize.BUTTON
        )
        new_request_button.set_tooltip_text("Make New Request")
        new_request_button.connect("clicked", self.on_new_request)
        hb.pack_end(new_request_button)

    def setup_settings_popover(self, settings_button: Gtk.Button) -> None:
        self.popover = Gtk.Popover()
        vbox: Gtk.Box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        api_key_label: Gtk.Label = Gtk.Label(label="Enter API Key:")
        vbox.pack_start(api_key_label, False, True, 10)

        self.api_key_entry = Gtk.Entry()
        self.api_key_entry.set_placeholder_text("API Key")
        if self.api_handler.api_key:
            self.api_key_entry.set_text(self.api_handler.api_key)
        vbox.pack_start(self.api_key_entry, False, True, 10)

        save_button: Gtk.Button = Gtk.Button(label="Save API Key")
        save_button.connect("clicked", self.on_save_api_key)
        vbox.pack_start(save_button, False, True, 10)

        vbox.show_all()
        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)

        settings_button.connect("clicked", self.on_settings_clicked)

    def setup_main_content(self) -> None:
        main_box: Gtk.Box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        scrolled_window: Gtk.ScrolledWindow = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.set_hexpand(True)
        self.text_view = Gtk.TextView()
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.set_editable(False)
        self.text_view.set_cursor_visible(False)
        self.text_buffer = self.text_view.get_buffer()

        self.tag_bold = self.text_buffer.create_tag("bold", weight=Pango.Weight.BOLD)
        self.tag_bg = self.text_buffer.create_tag("bg_color")

        scrolled_window.add(self.text_view)
        main_box.pack_start(scrolled_window, True, True, 0)

        prompt_box: Gtk.Box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.prompt_entry = Gtk.Entry()
        self.prompt_entry.set_placeholder_text("Type your prompt here...")
        prompt_box.pack_start(self.prompt_entry, True, True, 0)
        send_button: Gtk.Button = Gtk.Button.new_from_icon_name(
            "document-send", Gtk.IconSize.BUTTON
        )
        send_button.set_tooltip_text("Send")
        send_button.connect("clicked", self.on_send_clicked)
        prompt_box.pack_start(send_button, False, True, 0)
        main_box.pack_end(prompt_box, False, True, 0)
        self.add(main_box)

    def on_save_api_key(self, button: Gtk.Button) -> None:
        api_key: str = self.api_key_entry.get_text()
        if api_key:
            self.api_handler.save_api_key(api_key)
            print(f"API Key saved: {api_key}")
        else:
            print("No API Key entered.")

    def on_settings_clicked(self, button: Gtk.Button) -> None:
        if self.popover.get_visible():
            self.popover.hide()
        else:
            self.popover.set_relative_to(button)
            self.popover.show_all()

    def on_new_request(self, button: Gtk.Button) -> None:
        self.text_buffer.set_text("")
        print("Current chats cleared. New request initiated!")

    def on_send_clicked(self, button: Gtk.Button) -> None:
        prompt: str = self.prompt_entry.get_text()
        if prompt:
            self.add_text("🤖: ", prompt, bold=True, append_to_bottom=False)
            self.prompt_entry.set_text("")
            response: str = self.api_handler.send_message(prompt)
            self.add_text(
                " 😿: ",
                response,
                bg_color_rgba="rgba(224, 247, 250, 0.3)",
                append_to_bottom=False,
            )
        else:
            print("Prompt is empty!")

    def add_text(
        self,
        sender: str,
        message: str,
        bold: bool = False,
        bg_color_rgba: Optional[str] = None,
        append_to_bottom: bool = True,
    ) -> None:
        if append_to_bottom:
            end_iter: Gtk.TextIter = self.text_buffer.get_end_iter()
        else:
            end_iter: Gtk.TextIter = self.text_buffer.get_start_iter()

        if bg_color_rgba:
            rgba: Gdk.RGBA = Gdk.RGBA()
            rgba.parse(bg_color_rgba)
            self.tag_bg.set_property("background-rgba", rgba)
            self.text_buffer.insert_with_tags(
                end_iter, sender + message + "\n", self.tag_bg
            )
        else:
            self.text_buffer.insert(end_iter, sender + message + "\n")
