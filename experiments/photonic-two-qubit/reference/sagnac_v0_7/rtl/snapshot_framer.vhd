-- SPDX-License-Identifier: MIT
-- 244-byte little-endian snapshot frame; CRC32/ISO-HDLC, ready/valid stream.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use work.sagnac_pkg.all;
entity snapshot_framer is
  port(clk, reset : in std_logic;
       send_valid : in std_logic; send_ready : out std_logic;
       counts_in : in counter_array;
       flags_in : in std_logic_vector(7 downto 0);
       setting_in : in unsigned(1 downto 0);
       calibration_in : in std_logic_vector(31 downto 0);
       start_in, stop_in, width_in, sequence_in : in u64;
       byte_valid : out std_logic; byte_ready : in std_logic;
       byte_data : out std_logic_vector(7 downto 0));
end entity;
architecture rtl of snapshot_framer is
  type state_type is (IDLE, DATA_BYTES, CRC_BYTES);
  signal state : state_type := IDLE;
  signal c : counter_array;
  signal f : std_logic_vector(7 downto 0);
  signal s : unsigned(1 downto 0);
  signal cal : std_logic_vector(31 downto 0);
  signal first,last,width,seq : u64;
  signal index : natural range 0 to 239 := 0;
  signal crc_index : natural range 0 to 3 := 0;
  signal crc : unsigned(31 downto 0) := (others=>'1');
  signal octet : std_logic_vector(7 downto 0);
  constant MAGIC : string(1 to 8) := "SGNCv007";
  function update_crc(previous : unsigned(31 downto 0);
                      b : std_logic_vector(7 downto 0)) return unsigned is
    variable r : unsigned(31 downto 0) := previous xor resize(unsigned(b),32);
  begin
    for i in 0 to 7 loop
      if r(0)='1' then r:=shift_right(r,1) xor x"EDB88320";
      else r:=shift_right(r,1); end if;
    end loop;
    return r;
  end function;
  function byte_at(v : unsigned; n : natural) return std_logic_vector is
  begin return std_logic_vector(resize(shift_right(v,8*n),8)); end function;
begin
  send_ready<='1' when state=IDLE else '0';
  byte_valid<='0' when state=IDLE else '1'; byte_data<=octet;
  process(all)
  begin
    octet<=(others=>'0');
    if state=CRC_BYTES then octet<=byte_at(not crc,crc_index);
    elsif state=DATA_BYTES then
      if index<8 then octet<=std_logic_vector(to_unsigned(character'pos(MAGIC(index+1)),8));
      elsif index=8 then octet<=x"07";
      elsif index=9 then octet<=std_logic_vector(resize(s,8));
      elsif index=10 then octet<=f;
      elsif index=11 then octet<=x"00";
      elsif index<16 then octet<=byte_at(unsigned(cal),index-12);
      elsif index<24 then octet<=byte_at(first,index-16);
      elsif index<32 then octet<=byte_at(last,index-24);
      elsif index<40 then octet<=byte_at(width,index-32);
      elsif index<48 then octet<=byte_at(seq,index-40);
      else octet<=byte_at(c((index-48)/8),(index-48) mod 8);
      end if;
    end if;
  end process;
  process(clk)
  begin
    if rising_edge(clk) then
      if reset='1' then
        state<=IDLE;index<=0;crc_index<=0;crc<=(others=>'1');
      else
        case state is
          when IDLE =>
            if send_valid='1' then
              c<=counts_in;f<=flags_in;s<=setting_in;cal<=calibration_in;
              first<=start_in;last<=stop_in;width<=width_in;seq<=sequence_in;
              index<=0;crc<=(others=>'1');state<=DATA_BYTES;
            end if;
          when DATA_BYTES =>
            if byte_ready='1' then
              crc<=update_crc(crc,octet);
              if index=239 then crc_index<=0;state<=CRC_BYTES;
              else index<=index+1; end if;
            end if;
          when CRC_BYTES =>
            if byte_ready='1' then
              if crc_index=3 then state<=IDLE;
              else crc_index<=crc_index+1; end if;
            end if;
        end case;
      end if;
    end if;
  end process;
end architecture;
