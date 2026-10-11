library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_textio.all;
use std.textio.all;
use std.env.all;
use work.sagnac_pkg.all;
entity tb_uart_top is
  generic(OUTPUT_FILE : string := "top.frame.hex");
end entity;
architecture test of tb_uart_top is
  signal clk : std_logic := '0';
  signal reset,start,valid,ready,tx,complete,transmitted,received : std_logic := '0';
  signal kind : unsigned(2 downto 0) := (others=>'0');
  signal timestamp : u64 := (others=>'0');
  signal seq : u64 := x"FFFFFFFFFFFFFFFE";
  constant STOP_PS : u64 := x"000000E8D4A51000"; -- 1 second in ps
begin
  clk<=not clk after 10 ns; -- target clock model 50 MHz (not hardware timing proof)
  dut: entity work.sagnac_uart_top
    generic map(WINDOW_PS=>1000,CLKS_PER_BIT=>50)
    port map(clk=>clk,reset=>reset,start=>start,cfg_start_ps=>to_unsigned(0,64),
      cfg_stop_ps=>STOP_PS,cfg_sequence=>seq,cfg_calibration_id=>x"00000007",cfg_setting=>"00",
      in_valid=>valid,in_ready=>ready,in_kind=>kind,in_time_ps=>timestamp,
      in_calibration_id=>x"00000007",source_error=>'0',tx=>tx,
      run_complete=>complete,transmit_complete=>transmitted);
  process
    file f : text open write_mode is OUTPUT_FILE;
    variable l : line;variable b : std_logic_vector(7 downto 0);
  begin
    for n in 0 to 243 loop
      wait until falling_edge(tx);wait for 500 ns;
      assert tx='0' report "top UART start" severity failure;
      for i in 0 to 7 loop wait for 1 us;b(i):=tx;end loop;
      wait for 1 us;assert tx='1' report "top UART stop" severity failure;
      hwrite(l,b);writeline(f,l);
    end loop;
    file_close(f);received<='1';wait;
  end process;
  process
  begin
    reset<='1';wait until falling_edge(clk);wait until falling_edge(clk);reset<='0';
    start<='1';wait until falling_edge(clk);start<='0';
    seq<=to_unsigned(123,64); -- must not change captured sequence
    kind<="000";timestamp<=to_unsigned(100,64);valid<='1';
    loop wait until rising_edge(clk);exit when ready='1';end loop;
    wait until falling_edge(clk);kind<="100";timestamp<=STOP_PS;
    loop wait until rising_edge(clk);exit when ready='1';end loop;
    wait until falling_edge(clk);valid<='0';
    wait until received='1';wait for 1 us;
    assert complete='1' and transmitted='1' report "top did not finish" severity failure;
    start<='1';wait for 1 us;
    assert tx='1' and transmitted='1' report "top resent without reset" severity failure;
    report "TOP_INTEGRATION_PASS" severity note;finish(0);wait;
  end process;
  process
  begin wait for 5 ms;assert false report "top timeout" severity failure;wait;end process;
end architecture;
