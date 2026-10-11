-- SPDX-License-Identifier: MIT
-- Reference integration: one run and one complete snapshot frame per reset.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.sagnac_pkg.all;
entity sagnac_uart_top is
  generic(WINDOW_PS : positive := 1000; CLKS_PER_BIT : positive := 50);
  port(clk,reset,start : in std_logic;
       cfg_start_ps,cfg_stop_ps,cfg_sequence : in u64;
       cfg_calibration_id : in std_logic_vector(31 downto 0);
       cfg_setting : in unsigned(1 downto 0);
       in_valid : in std_logic;in_ready : out std_logic;
       in_kind : in unsigned(2 downto 0);in_time_ps : in u64;
       in_calibration_id : in std_logic_vector(31 downto 0);
       source_error : in std_logic;
       tx : out std_logic;run_complete,transmit_complete : out std_logic);
end entity;
architecture rtl of sagnac_uart_top is
  signal counters : counter_array;
  signal flags,b : std_logic_vector(7 downto 0);
  signal setting : unsigned(1 downto 0);
  signal cal : std_logic_vector(31 downto 0);
  signal first,last,seq : u64 := (others=>'0');
  signal snap_ready,request,accept,valid,ready,sent,started : std_logic := '0';
begin
  core: entity work.sagnac_core
    generic map(WINDOW_PS=>WINDOW_PS)
    port map(clk=>clk,reset=>reset,start=>start,cfg_start_ps=>cfg_start_ps,cfg_stop_ps=>cfg_stop_ps,
      cfg_calibration_id=>cfg_calibration_id,cfg_setting=>cfg_setting,
      in_valid=>in_valid,in_ready=>in_ready,in_kind=>in_kind,in_time_ps=>in_time_ps,
      in_calibration_id=>in_calibration_id,source_error=>source_error,
      snapshot_ready=>snap_ready,snapshot_counts=>counters,snapshot_flags=>flags,
      snapshot_start_ps=>first,snapshot_stop_ps=>last,snapshot_calibration_id=>cal,snapshot_setting=>setting);
  request<=snap_ready and not sent;
  framer: entity work.snapshot_framer
    port map(clk=>clk,reset=>reset,send_valid=>request,send_ready=>accept,
      counts_in=>counters,flags_in=>flags,setting_in=>setting,calibration_in=>cal,
      start_in=>first,stop_in=>last,width_in=>to_unsigned(WINDOW_PS,64),sequence_in=>seq,
      byte_valid=>valid,byte_ready=>ready,byte_data=>b);
  serial: entity work.uart_tx
    generic map(CLKS_PER_BIT=>CLKS_PER_BIT)
    port map(clk=>clk,reset=>reset,byte_valid=>valid,byte_ready=>ready,byte_data=>b,tx=>tx);
  run_complete<=snap_ready;
  transmit_complete<=sent and accept and ready;
  process(clk)
  begin
    if rising_edge(clk) then
      if reset='1' then sent<='0';started<='0';seq<=(others=>'0');
      else
        if start='1' and started='0' then seq<=cfg_sequence;started<='1';end if;
        if request='1' and accept='1' then sent<='1';end if;
      end if;
    end if;
  end process;
end architecture;
