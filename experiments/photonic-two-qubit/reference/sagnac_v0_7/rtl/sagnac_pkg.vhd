-- SPDX-License-Identifier: MIT
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
package sagnac_pkg is
  subtype u64 is unsigned(63 downto 0);
  type counter_array is array(0 to 23) of u64;
  constant U64_MAX : u64 := (others => '1');
end package;
