import gettext

import gi

from optimusui import prime_select, pci_utils, os_utils
from optimusui import const
from optimusui import system_validator
from optimusui.prime_select import PrimeMode

'''
Main UI
'''

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

        self._build_prime_toggles(self.main_box)
        self._build_system_pref_group(self.main_box)

    def _build_system_pref_group(self, main_box):
        settings_preference_group = Adw.PreferencesGroup()
        settings_preference_group.set_title(_("System"))
        settings_preference_group.set_description(_("Various system settings"))
        main_box.append(settings_preference_group)
        if os_utils.get_distro() == os_utils.Distribution.SUSE:
            self._build_boot_settings(settings_preference_group)
        self._build_gpu_info(settings_preference_group)

    def _build_boot_settings(self, preference_group):
        prime_mode: PrimeMode = prime_select.get_boot()

        boot_row = Adw.ComboRow(title=_("Boot"), subtitle=_("Set prime mode to be applied at boot"))
        preference_group.add(boot_row)
        boot_string_list = Gtk.StringList()
        # Note: Order is important
        boot_string_list.append(_("nVidia"))
        boot_string_list.append(_("Offload"))
        boot_string_list.append(_("Integrated"))
        boot_row.set_model(boot_string_list)
        boot_row.set_selected(prime_mode.value)
        boot_row.connect("notify::selected-item", self._on_select_boot_mode)

    def _build_prime_toggles(self, main_box):
        prime_mode: PrimeMode = prime_select.get_current()

        toggle_section = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main_box.append(toggle_section)

        toggle_preference_group = Adw.PreferencesGroup()
        toggle_preference_group.set_title(_("Runtime"))
        toggle_preference_group.set_description(_("Prime mode to be used while system is running"))
        toggle_section.append(toggle_preference_group)

        toggle_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        toggle_box.set_halign(Gtk.Align.CENTER)
        toggle_preference_group.add(toggle_box)

        toggle_nvidia = Gtk.ToggleButton(label=_("nVidia"), active=prime_mode == PrimeMode.NVIDIA)
        toggle_nvidia.set_group(toggle_nvidia)
        if toggle_nvidia.get_active():
            toggle_nvidia.add_css_class("suggested-action")
        toggle_nvidia.connect("toggled", self.on_toggle_nvidia)
        toggle_box.append(toggle_nvidia)

        toggle_offload = Gtk.ToggleButton(label=_("Offload"), active=prime_mode == PrimeMode.OFFLOAD)
        toggle_offload.set_group(toggle_nvidia)
        if toggle_offload.get_active():
            toggle_offload.add_css_class("suggested-action")
        toggle_offload.connect("toggled", self.on_toggle_offload)
        toggle_box.append(toggle_offload)

        toggle_integrated = Gtk.ToggleButton(label=_("Integrated"), active=prime_mode == PrimeMode.INTEGRATED)
        toggle_integrated.set_group(toggle_nvidia)
        if toggle_integrated.get_active():
            toggle_integrated.add_css_class("suggested-action")
        toggle_integrated.connect("toggled", self.on_toggle_integrated)
        toggle_box.append(toggle_integrated)

    def _build_gpu_info(self, preference_group):
        all_gpus = pci_utils.find_all_gpus()
        all_gpu_row = Adw.ExpanderRow()
        all_gpu_row.set_title(_("Detected Graphic cards"))
        for gpu in all_gpus:
            power_state = " (" + _("OFF") + ")"
            if pci_utils.is_device_on(gpu.pci_slot):
                power_state = " (" + _("ON") + ")"

            gpu_row = Adw.ActionRow()
            if gpu.is_discrete:
                gpu_row.set_title(_("Discrete") + power_state)
            else:
                gpu_row.set_title(_("Integrated") + power_state)
            gpu_row.set_subtitle(gpu.resolve_device_name())
            all_gpu_row.add_row(gpu_row)
        preference_group.add(all_gpu_row)

    def _on_select_boot_mode(self, widget, _a):
        match widget.get_selected():
            case 0:
                self.do_prime(PrimeMode.NVIDIA, True)
            case 1:
                self.do_prime(PrimeMode.OFFLOAD, True)
            case 2:
                self.do_prime(PrimeMode.INTEGRATED, True)

    def on_toggle_nvidia(self, toggle):
        if toggle.get_active():
            toggle.add_css_class("suggested-action")
            self.do_prime(PrimeMode.NVIDIA, False)
        else:
            toggle.remove_css_class("suggested-action")

    def on_toggle_offload(self, toggle):
        if toggle.get_active():
            toggle.add_css_class("suggested-action")
            self.do_prime(PrimeMode.OFFLOAD, False)
        else:
            toggle.remove_css_class("suggested-action")

    def on_toggle_integrated(self, toggle):
        if toggle.get_active():
            toggle.add_css_class("suggested-action")
            self.do_prime(PrimeMode.INTEGRATED, False)
        else:
            toggle.remove_css_class("suggested-action")

    def do_prime(self, mode: PrimeMode, boot: bool):
        if prime_select.prime_select(mode, boot):
            if boot:
                self.show_reboot_dialog()
            else:
                self.show_relog_dialog()
        else:
            self.show_prime_error()

    def test_system_config(self):
        if not system_validator.is_system_supported():
            message_text = ""
            if not prime_select.has_prime_select():
                message_text += "• " + _(
                    "prime-select not found, please install it per your distributions documentation") + "\n"
            if not pci_utils.has_nvidia_gpu():
                message_text += "• " + _("This systems seems not to have a supported nVidia GPU installed")
            if not os_utils.is_distro_supported():
                message_text += "• " + _("Your distribution is not supported")
            dialog = Adw.AlertDialog(heading=_("System not supported"),
                                     body=message_text,
                                     )
            dialog.add_response("ok", "Quit")
            dialog.set_response_appearance("ok", Adw.ResponseAppearance.DESTRUCTIVE)
            dialog.connect("response", self.on_response)
            dialog.set_body_use_markup(True)
            dialog.present(self)

    def show_relog_dialog(self):
        dialog = Adw.AlertDialog(heading=_("Success"),
                                 body=_(
                                     "Driver was changed successfully. Please log out and in again for these changes to take effect."),
                                 )
        dialog.add_response("ok", _("Ok"))
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
        dialog.present(self)

    def show_reboot_dialog(self):
        dialog = Adw.AlertDialog(heading=_("Success"),
                                 body=_(
                                     "Driver was changed successfully. The new prime mode will be applied on every boot."),
                                 )
        dialog.add_response("ok", _("Ok"))
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
        dialog.present(self)

    def show_prime_error(self):
        dialog = Adw.AlertDialog(heading=_("Failed"),
                                 body=_(
                                     "The operation has failed. Please check your system logs and report this error."),
                                 )
        dialog.add_response("ok", _("Ok"))
        dialog.set_response_appearance("ok", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.present(self)

    def test_bbswitch(self):
        if not prime_select.has_bbswitch():
            dialog = Adw.AlertDialog(heading=_("bbswitch not found"),
                                     body=_("Power management might not work as bbswitch was not found."),
                                     )
            dialog.add_response("ok", _("Ok"))
            dialog.set_response_appearance("ok", Adw.ResponseAppearance.SUGGESTED)
            dialog.present(self)

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
