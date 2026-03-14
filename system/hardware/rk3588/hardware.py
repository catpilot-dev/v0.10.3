import os
import subprocess

from cereal import log
from openpilot.system.hardware.base import HardwareBase, LPABase, ThermalConfig, ThermalZone

NetworkType = log.DeviceState.NetworkType
NetworkStrength = log.DeviceState.NetworkStrength


class Rk3588(HardwareBase):
  def get_device_type(self):
    return "pc"  # capnp enum only has tici/pc — use pc until rk3588 is added

  def get_os_version(self):
    try:
      with open('/etc/os-release') as f:
        for line in f:
          if line.startswith('PRETTY_NAME='):
            return line.strip().split('=', 1)[1].strip('"')
    except FileNotFoundError:
      pass
    return None

  def get_serial(self):
    try:
      with open('/proc/device-tree/serial-number') as f:
        return f.read().strip('\x00').strip()
    except FileNotFoundError:
      return ""

  def get_network_type(self):
    return NetworkType.wifi

  def get_thermal_config(self):
    return ThermalConfig(
      cpu=[ThermalZone("soc-thermal")],
      gpu=[ThermalZone("gpu-thermal")],
    )

  def get_gpu_usage_percent(self):
    try:
      with open('/sys/class/devfreq/fb000000.gpu/load') as f:
        # format: "load@freq" e.g. "42@800000000"
        return int(f.read().split('@')[0])
    except (FileNotFoundError, ValueError):
      return 0

  def reboot(self, reason=None):
    subprocess.check_call(["sudo", "reboot"])

  def shutdown(self):
    subprocess.check_call(["sudo", "shutdown", "-h", "now"])

  def uninstall(self):
    pass

  def get_imei(self, slot):
    return ""

  def get_network_info(self):
    return None

  def get_sim_info(self):
    return {
      'sim_id': '',
      'mcc_mnc': None,
      'network_type': ["Unknown"],
      'sim_state': ["ABSENT"],
      'data_connected': False
    }

  def get_sim_lpa(self) -> LPABase:
    raise NotImplementedError("SIM LPA not available on RK3588")

  def get_network_strength(self, network_type):
    return NetworkStrength.unknown

  def get_current_power_draw(self):
    return 0

  def get_som_power_draw(self):
    return 0

  def set_screen_brightness(self, percentage):
    pass

  def get_screen_brightness(self):
    return 0

  def set_power_save(self, powersave_enabled):
    pass

  def get_modem_temperatures(self):
    return []

  def initialize_hardware(self):
    pass

  def get_networks(self):
    return None

  # eSIM profile management — not applicable to RK3588
  def bootstrap(self):
    pass

  def list_profiles(self):
    return []

  def get_active_profile(self):
    return None

  def delete_profile(self, iccid):
    pass

  def download_profile(self, qr, nickname=None):
    pass

  def nickname_profile(self, iccid, nickname):
    pass

  def switch_profile(self, iccid):
    pass
