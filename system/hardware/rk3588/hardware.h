#pragma once

#include <string>

#include "system/hardware/base.h"

class HardwareRK3588 : public HardwareNone {
public:
  static std::string get_name() { return "rk3588"; }
  static cereal::InitData::DeviceType get_device_type() { return cereal::InitData::DeviceType::PC; }
  static bool PC() { return false; }
  static bool TICI() { return false; }
  static bool AGNOS() { return false; }
};
