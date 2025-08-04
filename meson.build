project('optimusui',
  version: '25.8',
  meson_version: '>= 0.62.0',
  default_options: ['warning_level=2', 'werror=false'],
)

gnome = import('gnome')
i18n = import('i18n')

appstream_file = 'de.z_ray.OptimusUI.metainfo.xml'
install_data(appstream_file, install_dir: join_paths(get_option('datadir'), 'metainfo'))

desktop_file='de.z_ray.OptimusUI.desktop'
install_data(desktop_file, install_dir: join_paths(get_option('datadir'), 'applications'))

subdir('optimusui')

gnome.post_install(
    gtk_update_icon_cache: true,
    update_desktop_database: true,
)