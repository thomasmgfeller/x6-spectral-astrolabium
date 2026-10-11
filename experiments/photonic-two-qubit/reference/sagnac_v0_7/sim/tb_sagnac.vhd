-- SPDX-License-Identifier: MIT
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.std_logic_textio.all;
use std.textio.all;
use std.env.all;
use work.sagnac_pkg.all;
entity tb_sagnac is
  generic (INPUT_FILE : string := "events.txt"; OUTPUT_FILE : string := "snapshot.txt";
           WINDOW_PS : positive := 1000; COUNTER_BITS : positive := 64);
end entity;
architecture test of tb_sagnac is
  signal clk : std_logic := '0';
  signal reset,start,valid,accept,ready,source_error : std_logic := '0';
  signal t0,t1,t,ss,se : u64 := (others=>'0');
  signal cal,incal,sc : std_logic_vector(31 downto 0) := (others=>'0');
  signal setting,ssetting : unsigned(1 downto 0) := (others=>'0');
  signal kind : unsigned(2 downto 0) := (others=>'0');
  signal counts : counter_array;
  signal flags : std_logic_vector(7 downto 0);
  signal send_valid,send_ready,byte_valid,byte_ready,tx,uart_done : std_logic := '0';
  signal byte_data : std_logic_vector(7 downto 0);
  signal cycles : natural := 0;
begin
  clk<=not clk after 5 ns;
  process(clk)
  begin
    if rising_edge(clk) then
      if reset='1' then cycles<=0;else cycles<=cycles+1;end if;
    end if;
  end process;
  dut: entity work.sagnac_core
    generic map(WINDOW_PS=>WINDOW_PS,COUNTER_BITS=>COUNTER_BITS)
    port map(clk=>clk,reset=>reset,start=>start,cfg_start_ps=>t0,cfg_stop_ps=>t1,
      cfg_calibration_id=>cal,cfg_setting=>setting,in_valid=>valid,in_ready=>accept,
      in_kind=>kind,in_time_ps=>t,in_calibration_id=>incal,source_error=>source_error,
      snapshot_ready=>ready,snapshot_counts=>counts,snapshot_flags=>flags,
      snapshot_start_ps=>ss,snapshot_stop_ps=>se,snapshot_calibration_id=>sc,
      snapshot_setting=>ssetting);
  framer: entity work.snapshot_framer
    port map(clk=>clk,reset=>reset,send_valid=>send_valid,send_ready=>send_ready,
      counts_in=>counts,flags_in=>flags,setting_in=>ssetting,calibration_in=>sc,
      start_in=>ss,stop_in=>se,width_in=>to_unsigned(WINDOW_PS,64),
      sequence_in=>to_unsigned(100,64)+resize(ssetting,64),
      byte_valid=>byte_valid,byte_ready=>byte_ready,byte_data=>byte_data);
  serial_tx: entity work.uart_tx
    generic map(CLKS_PER_BIT=>4)
    port map(clk=>clk,reset=>reset,byte_valid=>byte_valid,byte_ready=>byte_ready,
      byte_data=>byte_data,tx=>tx);
  -- Independent UART waveform receiver: sample in the middle of each bit.
  process
    file serial_file : text;
    variable l : line;
    variable b : std_logic_vector(7 downto 0);
  begin
    wait until send_valid='1';
    file_open(serial_file,OUTPUT_FILE & ".frame.hex",write_mode);
    for n in 0 to 243 loop
      wait until falling_edge(tx); wait for 20 ns;
      assert tx='0' report "UART start bit" severity failure;
      for i in 0 to 7 loop wait for 40 ns; b(i):=tx;end loop;
      wait for 40 ns;
      assert tx='1' report "UART stop bit" severity failure;
      hwrite(l,b);writeline(serial_file,l);
    end loop;
    file_close(serial_file);uart_done<='1';wait;
  end process;
  process(clk)
    variable stalled : boolean := false;
    variable held : std_logic_vector(7 downto 0);
  begin
    if rising_edge(clk) then
      if reset='1' then stalled:=false;
      else
        if stalled then
          assert byte_valid='1' and byte_data=held report "framer changed under backpressure" severity failure;
        end if;
        stalled:=byte_valid='1' and byte_ready='0';held:=byte_data;
      end if;
    end if;
  end process;
  process
    file fi : text open read_mode is INPUT_FILE;
    file fo : text;
    variable line_in,line_out : line;
    variable a,b,tm : std_logic_vector(63 downto 0);
    variable cid,ecid : std_logic_vector(31 downto 0);
    variable k,s,err,loops : integer;
    variable frozen : counter_array;
    variable frozen_flags : std_logic_vector(7 downto 0);
  begin
    reset<='1'; wait until falling_edge(clk); wait until falling_edge(clk); reset<='0';
    readline(fi,line_in); hread(line_in,a); hread(line_in,b); hread(line_in,cid); read(line_in,s);
    t0<=unsigned(a); t1<=unsigned(b); cal<=cid; setting<=to_unsigned(s,2); start<='1';
    wait until falling_edge(clk); start<='0';
    while not endfile(fi) loop
      readline(fi,line_in); read(line_in,k); hread(line_in,tm); hread(line_in,ecid); read(line_in,err);
      kind<=to_unsigned(k,3); t<=unsigned(tm); incal<=ecid; valid<='1';
      if err=0 then source_error<='0'; else source_error<='1'; end if;
      loops:=0;
      loop
        wait until rising_edge(clk); loops:=loops+1;
        exit when accept='1';
        assert loops<200000 report "input handshake timeout" severity failure;
      end loop;
      wait until falling_edge(clk); valid<='0'; source_error<='0';
      -- Deliberate gaps; pending items still require watermark closure.
      if k=4 then wait until falling_edge(clk); end if;
    end loop;
    file_close(fi); loops:=0;
    while ready/='1' loop
      wait until falling_edge(clk); loops:=loops+1;
      assert loops<200000 report "snapshot timeout (no valid final watermark?)" severity failure;
    end loop;
    report "SAGNAC_CORE_CYCLES=" & integer'image(cycles) severity note;
    assert ss=unsigned(a) and se=unsigned(b) and sc=cid and ssetting=to_unsigned(s,2)
      report "snapshot metadata mismatch" severity failure;
    frozen:=counts; frozen_flags:=flags;
    -- Exercise immutability including control/config/source perturbations.
    start<='1'; valid<='1'; source_error<='1'; t0<=(others=>'1'); cal<=(others=>'1');
    for j in 1 to 5 loop
      wait until falling_edge(clk);
      assert ready='1' and counts=frozen and flags=frozen_flags and ss=unsigned(a) and sc=cid
        report "snapshot changed after READY" severity failure;
    end loop;
    file_open(fo,OUTPUT_FILE,write_mode);
    write(line_out,string'("FLAGS ")); hwrite(line_out,flags); writeline(fo,line_out);
    for i in counts'range loop
      write(line_out,i); write(line_out,string'(" "));
      hwrite(line_out,std_logic_vector(counts(i))); writeline(fo,line_out);
    end loop;
    file_close(fo);
    send_valid<='1';wait until rising_edge(clk);
    assert send_ready='1' report "framer not ready" severity failure;
    wait until falling_edge(clk);send_valid<='0';loops:=0;
    while uart_done/='1' loop
      wait until falling_edge(clk);loops:=loops+1;
      assert loops<20000 report "UART frame timeout" severity failure;
    end loop;
    wait for 100 ns;
    assert send_ready='1' and tx='1' report "UART/framer did not return idle" severity failure;
    report "SAGNAC_SNAPSHOT_COMPLETE" severity note;
    finish(0); wait;
  end process;
end architecture;
