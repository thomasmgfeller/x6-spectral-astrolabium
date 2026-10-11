-- SPDX-License-Identifier: MIT
-- Fixed, outcome-independent time bins. Synchronous reference core, no TDC/CDC.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.sagnac_pkg.all;

entity sagnac_core is
  generic (WINDOW_PS : positive := 1000; COUNTER_BITS : positive := 64);
  port (
    clk, reset, start : in std_logic;
    cfg_start_ps, cfg_stop_ps : in u64;
    cfg_calibration_id : in std_logic_vector(31 downto 0);
    cfg_setting : in unsigned(1 downto 0);
    in_valid : in std_logic; in_ready : out std_logic;
    in_kind : in unsigned(2 downto 0); -- 0 A+, 1 A-, 2 B+, 3 B-, 4 watermark
    in_time_ps : in u64;
    in_calibration_id : in std_logic_vector(31 downto 0);
    source_error : in std_logic;
    snapshot_ready : out std_logic;
    snapshot_counts : out counter_array;
    snapshot_flags : out std_logic_vector(7 downto 0);
    snapshot_start_ps, snapshot_stop_ps : out u64;
    snapshot_calibration_id : out std_logic_vector(31 downto 0);
    snapshot_setting : out unsigned(1 downto 0)
  );
end entity;

architecture rtl of sagnac_core is
  type state_type is (IDLE, ACQUIRE, ADVANCE, APPLY_EVENT, PUBLISH, DONE);
  signal state : state_type := IDLE;
  signal counts, shadow : counter_array := (others => (others => '0'));
  signal flags, shadow_flags : std_logic_vector(7 downto 0) := (others => '0');
  signal run_start, run_stop, bin_start, bin_end, last_time, item_time : u64 := (others => '0');
  signal item_kind : unsigned(2 downto 0) := (others => '0');
  signal mask : std_logic_vector(3 downto 0) := (others => '0');
  signal repeated : std_logic := '0';
  signal calibration : std_logic_vector(31 downto 0) := (others => '0');
  signal setting : unsigned(1 downto 0) := (others => '0');
  constant W : u64 := to_unsigned(WINDOW_PS,64);
  constant LIMIT : u64 := shift_right(U64_MAX,64-COUNTER_BITS);
begin
  assert COUNTER_BITS <= 64 report "COUNTER_BITS exceeds 64" severity failure;
  in_ready <= '1' when state=ACQUIRE else '0';
  snapshot_ready <= '1' when state=DONE else '0';
  snapshot_counts <= shadow;
  snapshot_flags <= shadow_flags;
  snapshot_start_ps <= run_start;
  snapshot_stop_ps <= run_stop;
  snapshot_calibration_id <= calibration;
  snapshot_setting <= setting;

  process(clk)
    variable c : counter_array;
    variable f : std_logic_vector(7 downto 0);
    variable channel : natural range 0 to 7;
    variable boundary, empty_bins, next_bin : u64;
    procedure add_count(variable counters : inout counter_array;
                        constant i : natural; constant amount : u64;
                        variable errors : inout std_logic_vector(7 downto 0)) is
    begin
      if amount>LIMIT-counters(i) then
        counters(i):=LIMIT; errors(0):='1';
      else counters(i):=counters(i)+amount; end if;
    end procedure;
    procedure increment(variable counters : inout counter_array;
                        constant i : natural;
                        variable errors : inout std_logic_vector(7 downto 0)) is
    begin
      if counters(i)=LIMIT then errors(0):='1';
      else counters(i):=counters(i)+1; end if;
    end procedure;
  begin
    if rising_edge(clk) then
      c:=counts; f:=flags;
      if reset='1' then
        state<=IDLE; c:=(others => (others => '0')); f:=(others => '0');
        shadow<=(others => (others => '0')); shadow_flags<=(others => '0');
        mask<=(others => '0'); repeated<='0';
        run_start<=(others => '0'); run_stop<=(others => '0');
        bin_start<=(others => '0'); bin_end<=(others => '0');
        last_time<=(others => '0'); item_time<=(others => '0');
        item_kind<=(others => '0'); calibration<=(others => '0'); setting<=(others => '0');
      else
        if state/=IDLE and state/=DONE then
          if source_error='1' then f(2):='1'; end if;
          if start='1' then f(6):='1'; end if;
        end if;
        case state is
          when IDLE =>
            if start='1' then
              c:=(others => (others => '0')); f:=(others => '0');
              run_start<=cfg_start_ps; run_stop<=cfg_stop_ps;
              calibration<=cfg_calibration_id; setting<=cfg_setting;
              last_time<=cfg_start_ps; bin_start<=cfg_start_ps;
              mask<=(others => '0'); repeated<='0';
              if source_error='1' then f(2):='1'; end if;
              if cfg_stop_ps<=cfg_start_ps then
                f(4):='1'; state<=PUBLISH;
              elsif (cfg_stop_ps-cfg_start_ps) mod W /= 0 then
                f(4):='1'; state<=PUBLISH;
              else
                bin_end<=cfg_start_ps+W; state<=ACQUIRE;
              end if;
            end if;
          when ACQUIRE =>
            if in_valid='1' then
              if in_kind>4 then f(5):='1';
              elsif in_calibration_id/=calibration then f(3):='1';
              elsif in_time_ps<last_time then f(1):='1';
              else
                last_time<=in_time_ps; item_time<=in_time_ps;
                item_kind<=in_kind; state<=ADVANCE;
              end if;
            end if;
          when ADVANCE =>
            if bin_start<run_stop and item_time>=bin_end then
              if mask="0000" then
                -- No accepted events exist in these intervening bins: the
                -- stream is sorted and this item is the next event/watermark.
                boundary:=item_time;
                if boundary>run_stop then boundary:=run_stop; end if;
                empty_bins:=(boundary-bin_start)/W;
                add_count(c,0,empty_bins,f); add_count(c,16,empty_bins,f);
                next_bin:=bin_start+resize(empty_bins*W,64);
                bin_start<=next_bin;
                if next_bin<run_stop then bin_end<=next_bin+W; end if;
              else
                increment(c,to_integer(unsigned(mask)),f);
                increment(c,16,f);
                if repeated='1' then increment(c,17,f); end if;
                if mask(1 downto 0)="11" or mask(3 downto 2)="11" then
                  increment(c,23,f);
                end if;
                bin_start<=bin_end;
                if bin_end<run_stop then bin_end<=bin_end+W; end if;
              end if;
              mask<=(others => '0'); repeated<='0';
            else state<=APPLY_EVENT; end if;
          when APPLY_EVENT =>
            if item_kind=4 then
              if item_time>=run_stop then state<=PUBLISH;
              else state<=ACQUIRE; end if;
            else
              channel:=to_integer(item_kind);
              if item_time<run_start or item_time>=run_stop then f(5):='1';
              else
                increment(c,18+channel,f);
                if mask(channel)='1' then
                  repeated<='1'; increment(c,22,f);
                end if;
                mask(channel)<='1';
              end if;
              state<=ACQUIRE;
            end if;
          when PUBLISH =>
            shadow<=c; shadow_flags<=f; state<=DONE;
          when DONE => null; -- frozen until reset; ignored input does not alter snapshot
        end case;
      end if;
      counts<=c; flags<=f;
    end if;
  end process;
end architecture;
