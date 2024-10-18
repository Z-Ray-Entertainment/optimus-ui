from enum import Enum

from optimusui import const, os_utils

'''
Prime Select wrapper
'''

PRIME_ROOT_PATHS = [
    "/usr/bin/",
    "/usr/sbin/",
    "/bin/",
    "/sbin/"
]

prime_path = ""
prime_features = []


class PrimeTool(Enum):
    PRIME_SELECT = "prime-select"
    FEDORA_PRIME_SELECT = "fedora-prime-select"
    NVIDIA_PRIME_SELECT = "nvidia-prime-select"


class PrimeMode(Enum):
    NVIDIA = 0
    OFFLOAD = 1
    INTEGRATED = 2
    NO_DRIVER = 3
    DEFAULT = 4


class PrimeFeature(Enum):
    SET_BOOT = 0
    SET_INTEGRATED = 1
    SET_NVIDIA = 2
    SET_OFFLOAD = 3
    SET_DEFAULT = 4
    GET_CURRENT = 5


def get_boot():
    prime_command = [prime_path, "get-boot"]
    prime_result = os_utils.run_command(prime_command)
    prime_time = prime_result.stdout.decode("utf-8").rstrip()
    driver = prime_time.split(":")
    return _text_to_prime_mode(driver[1].strip())


def get_current():
    if PrimeFeature.GET_CURRENT in prime_features:
        match os_utils.get_distro():
            case os_utils.Distribution.SUSE:
                prime_time = _get_current().split("\n")
                if len(prime_time) < 2:
                    return PrimeMode.NO_DRIVER
                driver = prime_time[0].split(":")
                return _text_to_prime_mode(driver[1].strip())
            case os_utils.Distribution.DEBIAN:
                prime_time = _get_current()
                return _text_to_prime_mode(prime_time)
    return PrimeMode.NO_DRIVER


def has_prime_select():
    global prime_path
    for root_path in PRIME_ROOT_PATHS:
        for prime_tool in PrimeTool:
            prime_path_full = root_path + prime_tool.value
            which_cmd = ["test", "-f", prime_path_full]
            which_result = os_utils.run_command(which_cmd)
            if which_result.returncode == 0:
                prime_path = prime_path_full
                _build_features(prime_tool, os_utils.get_distro())
                return True
    return False


def prime_select(mode: PrimeMode, boot: bool):
    prime_command = [prime_path]
    if boot:
        prime_command += ["boot"]

    # TODO: Add handling for "amd" and "intel2"
    match mode:
        case PrimeMode.NVIDIA:
            prime_command += ["nvidia"]
        case PrimeMode.OFFLOAD:
            match os_utils.get_distro():
                case os_utils.Distribution.SUSE:
                    prime_command += ["offload"]
                case os_utils.Distribution.DEBIAN:
                    prime_command += ["on-demand"]
                case os_utils.Distribution.UNKNOWN:
                    prime_command += ["offload"]
        case PrimeMode.INTEGRATED:
            prime_command += ["intel"]
        case PrimeMode.DEFAULT:
            prime_command += ["default"]
    os_utils.run_command_as_root_no_pipe(prime_command)
    return True


def has_feature(feature: PrimeFeature):
    global prime_features
    return feature in prime_features


def _build_features(prime_tool: PrimeTool, distro: os_utils.Distribution):
    global prime_features
    match prime_tool:
        case PrimeTool.PRIME_SELECT:
            match distro:
                case os_utils.Distribution.SUSE:
                    prime_features.append(PrimeFeature.SET_BOOT)
                    prime_features.append(PrimeFeature.SET_OFFLOAD)
                    prime_features.append(PrimeFeature.SET_NVIDIA)
                    prime_features.append(PrimeFeature.SET_INTEGRATED)
                    prime_features.append(PrimeFeature.GET_CURRENT)
                case os_utils.Distribution.DEBIAN:
                    prime_features.append(PrimeFeature.SET_OFFLOAD)
                    prime_features.append(PrimeFeature.SET_NVIDIA)
                    prime_features.append(PrimeFeature.SET_INTEGRATED)
                    prime_features.append(PrimeFeature.GET_CURRENT)
        case PrimeTool.FEDORA_PRIME_SELECT | PrimeTool.NVIDIA_PRIME_SELECT:
            prime_features.append(PrimeFeature.SET_NVIDIA)
            prime_features.append(PrimeFeature.SET_INTEGRATED)


def _get_current():
    prime_command = [prime_path]
    match os_utils.get_distro():
        case os_utils.Distribution.DEBIAN:
            prime_command += ["query"]
        case os_utils.Distribution.SUSE:
            prime_command += ["get-current"]
    prime_result = os_utils.run_command(prime_command)
    return prime_result.stdout.decode("utf-8").rstrip()


def _text_to_prime_mode(text: str) -> PrimeMode:
    match text:
        case "intel" | "intel2" | "amd":
            return PrimeMode.INTEGRATED
        case "nvidia":
            return PrimeMode.NVIDIA
        case "offload" | "on-demand":
            return PrimeMode.OFFLOAD
        case _:
            return PrimeMode.NO_DRIVER
