pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'optimusui')

conf = configuration_data()
conf.set('VERSION', meson.project_version())

python = import('python')
conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('APPID', 'de.zray.OptimusUI')
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)


subdir('data')

nvreclock_bin = configure_file(
  input: '__init__.py',
  output: 'optimus-ui',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x',
)

configure_file(
  input: 'const.py',
  output: 'const.py',
  configuration: conf,
  install: true,
  install_dir: moduledir,
  install_mode: 'r-xr--r--',
)

optimus_sources = files([
    'optimus_ui.py',
    'pci_utils.py',
    'prime_select.py',
    'system_validator.py',
    'os_utils.py'
])

install_data(optimus_sources, install_dir: moduledir)