import os
import subprocess

from cereal import log
from openpilot.system.hardware.base import HardwareBase, ThermalConfig, ThermalZone

NetworkType = log.DeviceState.NetworkType


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
