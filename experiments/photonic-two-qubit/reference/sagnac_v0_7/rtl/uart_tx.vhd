-- SPDX-License-Identifier: MIT
-- Synchronous byte sink, 8N1. Same clock domain as the snapshot framer.
library ieee;
use ieee.std_logic_1164.all;
entity uart_tx is
  generic(CLKS_PER_BIT : positive := 50);
  port(clk,reset : in std_logic;
       byte_valid : in std_logic; byte_ready : out std_logic;
       byte_data : in std_logic_vector(7 downto 0); tx : out std_logic);
end entity;
architecture rtl of uart_tx is
  signal active : std_logic := '0';
  signal frame : std_logic_vector(9 downto 0) := (others=>'1');
  signal bit_index : natural range 0 to 9 := 0;
  signal tick : natural range 0 to CLKS_PER_BIT-1 := 0;
begin
  byte_ready<=not active;
  tx<=frame(bit_index) when active='1' else '1';
  process(clk)
  begin
    if rising_edge(clk) then
      if reset='1' then
        active<='0';frame<=(others=>'1');bit_index<=0;tick<=0;
      elsif active='0' then
        if byte_valid='1' then
          frame<='1' & byte_data & '0';bit_index<=0;tick<=0;active<='1';
        end if;
      elsif tick=CLKS_PER_BIT-1 then
        tick<=0;
        if bit_index=9 then active<='0';bit_index<=0;
        else bit_index<=bit_index+1;end if;
      else tick<=tick+1;
      end if;
    end if;
  end process;
end architecture;
