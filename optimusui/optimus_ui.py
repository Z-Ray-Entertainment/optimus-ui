import gettext

import gi

from optimusui import prime_select, pci_utils
from optimusui import const
from optimusui import system_validator
from optimusui.prime_select import PrimeMode

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio

gettext.install('optimusui', const.LOCALE_DIR)


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_system_config()
        if system_validator.is_system_supported():
            self.set_title(const.APP_NAME)
            self._build_title_bar()
            self.main_box = None
            self.prime_select_row = None
            self.prime_boot_row = None
            self.build_ui()
            self.test_bbswitch()

    def build_ui(self):
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.main_box.set_margin_end(10)
        self.main_box.set_margin_start(10)
        self.main_box.set_margin_top(10)
        self.main_box.set_margin_bottom(10)
        self.set_child(self.main_box)

        boxed_list = Gtk.ListBox()
        boxed_list.set_selection_mode(Gtk.SelectionMode.NONE)
        boxed_list.add_css_class("boxed-list")
        self.main_box.append(boxed_list)

        self._build_gpu_info(boxed_list)
        self._build_prime_select_row(boxed_list)
        self._build_prime_boot_row(boxed_list)

    def _build_gpu_info(self, boxed_list):
        all_gpus = pci_utils.find_all_gpus()
        all_gpu_row = Adw.ExpanderRow()
        all_gpu_row.set_title(_("Detected Graphic cards"))
        for gpu in all_gpus:
            gpu_row = Adw.ActionRow()
            if gpu.is_nvidia_device():
                gpu_row.set_title(_("Discrete"))
            else:
                gpu_row.set_title(_("Integrated"))
            gpu_row.set_subtitle(gpu.resolve_device_name())
            all_gpu_row.add_row(gpu_row)
        boxed_list.append(all_gpu_row)

    def _build_prime_select_row(self, boxed_list):
        if self.prime_select_row is not None:
            boxed_list.remove(self.prime_select_row)
        self.prime_select_row = Adw.ActionRow()
        self.prime_select_row.set_title("Runtime")
        self.prime_select_row.set_subtitle(_("Select runtime GPU mode:"))
        boxed_list.append(self.prime_select_row)

        radio_nvidia = Gtk.CheckButton(label="nVidia")
        radio_nvidia.set_group(radio_nvidia)
        radio_nvidia.connect("toggled", self.on_toggle_nvidia)
        self.prime_select_row.add_suffix(radio_nvidia)

        radio_offload = Gtk.CheckButton(label="Offload")
        radio_offload.set_group(radio_nvidia)
        radio_offload.connect("toggled", self.on_toggle_offload)
        self.prime_select_row.add_suffix(radio_offload)

        radio_integrated = Gtk.CheckButton(label="Integrated")
        radio_integrated.set_group(radio_nvidia)
        radio_integrated.connect("toggled", self.on_toggle_integrated)
        self.prime_select_row.add_suffix(radio_integrated)

    def on_toggle_nvidia(self, toggle):
        if toggle.get_active():
            self.do_prime(PrimeMode.NVIDIA, False)

    def on_toggle_offload(self, toggle):
        if toggle.get_active():
            self.do_prime(PrimeMode.OFFLOAD, False)

    def on_toggle_integrated(self, toggle):
        if toggle.get_active():
            self.do_prime(PrimeMode.INTEGRATED, False)

    def _build_prime_boot_row(self, boxed_list):
        if self.prime_boot_row is not None:
            boxed_list.remove(self.prime_boot_row)
        self.prime_boot_row = Adw.ActionRow()
        self.prime_boot_row.set_title("Boot")
        self.prime_boot_row.set_subtitle(_("Select GPU at boot:"))
        boxed_list.append(self.prime_boot_row)

        radio_nvidia = Gtk.CheckButton(label="nVidia")
        radio_nvidia.set_group(radio_nvidia)
        radio_nvidia.connect("toggled", self.on_toggle_nvidia_boot)
        self.prime_boot_row.add_suffix(radio_nvidia)

        radio_offload = Gtk.CheckButton(label="Offload")
        radio_offload.set_group(radio_nvidia)
        radio_offload.connect("toggled", self.on_toggle_offload_boot)
        self.prime_boot_row.add_suffix(radio_offload)

        radio_integrated = Gtk.CheckButton(label="Integrated")
        radio_integrated.set_group(radio_nvidia)
        radio_integrated.connect("toggled", self.on_toggle_integrated_boot)
        self.prime_boot_row.add_suffix(radio_integrated)

    def on_toggle_nvidia_boot(self, toggle):
        if toggle.get_active():
            self.do_prime(PrimeMode.NVIDIA, True)

    def on_toggle_offload_boot(self, toggle):
        if toggle.get_active():
            self.do_prime(PrimeMode.OFFLOAD, True)

    def on_toggle_integrated_boot(self, toggle):
        if toggle.get_active():
            self.do_prime(PrimeMode.INTEGRATED, True)

    def do_prime(self, mode: PrimeMode, boot: bool):
        if boot:
            prime_select.prime_boot(mode)
        else:
            prime_select.prime_select(mode)

    def test_system_config(self):
        if not system_validator.is_system_supported():
            print("System configuration is not supported")
            message_text = ""
            if not prime_select.has_prime_select():
                message_text += "• " + _(
                    "prime-select not found, please install it per your distributions documentation") + "\n"
            if not pci_utils.has_nvidia_gpu():
                message_text += "• " + _("This systems seems not to have a supported nVidia GPU installed")
            dialog = Adw.AlertDialog(heading=_("System not supported"),
                                     body=message_text,
                                     )
            dialog.add_response("ok", "Quit")
            dialog.set_response_appearance("ok", Adw.ResponseAppearance.DESTRUCTIVE)
            dialog.connect("response", self.on_response)
            dialog.set_body_use_markup(True)
            dialog.present()

    def test_bbswitch(self):
        if not prime_select.has_bbswitch():
            dialog = Adw.AlertDialog(heading=_("bbswitch not found"),
                                     body=_("Power management might not work as bbswitch was not found."),
                                     )
            dialog.add_response("ok", _("Ok"))
            dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
            dialog.present()

    def on_response(self, dialog, response):
        exit(1)

    def _build_content(self):
        pass

    def _build_title_bar(self):
        header = Gtk.HeaderBar()
        menu = Gio.Menu.new()
        menu.append(_("About"), "app.about")
        popover = Gtk.PopoverMenu()
        popover.set_menu_model(menu)
        hamburger = Gtk.MenuButton()
        hamburger.set_popover(popover)
        hamburger.set_icon_name("open-menu-symbolic")
        header.pack_end(hamburger)
        self.set_titlebar(header)


class OptimusUI(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_action("about", self.build_about)
        self.connect("activate", self.on_activate)
        self.connect("shutdown", self.on_close)
        self.win = None

    def create_action(self, name, callback):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        if system_validator.is_system_supported():
            self.win.present()

    def on_close(self, app):
        pass

    def build_about(self, widget, _a):
        about_ui = Adw.AboutDialog(
            application_name=const.APP_NAME,
            application_icon=const.APP_ID,
            developer_name="Z-Ray Entertainment",
            version=const.VERSION,
            developers=[
                "Vortex Acherontic https://github.com/VortexAcherontic",
            ],
            artists=[
                "Vortex Acherontic https://github.com/VortexAcherontic",
            ],
            translator_credits=_("translator-credits"),
            license_type=Gtk.License.MIT_X11,
            website="https://github.com/Z-Ray-Entertainment/optimus-ui",
            issue_url="https://github.com/Z-Ray-Entertainment/optimus-ui/issues",
            comments=_(
                "OptimusUI is a user interface for prime-select for nVidia Optimus Laptops. "
                "It allows to switch between integrated, dedicated and offloading GPU mode. "
                "prime-select needs to be installed on the host system and is not shipped by this application!")
        )
        about_ui.present(self.props.active_window)
