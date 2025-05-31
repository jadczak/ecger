import pathlib
from ecg_parsers import read_header

here = pathlib.Path(__file__).parent
test_dir = here / "test-data"
header = "100.hea"

print(f"Testing header {header}")
header_file = test_dir / header
record_line, signal_lines = read_header(header_file)

print("Testing record line parsing")
assert record_line.base_date == None
assert record_line.base_time == "0:0:0"
assert record_line.base_value == 0
assert record_line.counter_freq == float(360)
assert record_line.num_samples == 650000
assert record_line.num_segs == None
assert record_line.num_sigs == 2
assert record_line.record_name == "100"
assert record_line.sample_freq == float(360)
print(f"Record line parsing passed")

print(f"Testing signal line parsing")
assert len(signal_lines) == record_line.num_sigs
print("Testing signal line 0")
signal_0 = signal_lines[0]
assert signal_0.adc_gain == float(200)
assert signal_0.adc_resolution == 11
assert signal_0.adc_zero == 1024
assert signal_0.baseline == None
assert signal_0.block_size == 0
assert signal_0.byte_offset == None
assert signal_0.checksum == -22131
assert signal_0.description == "MLII"
assert signal_0.file_name == "100.dat"
assert signal_0.format == "212"
assert signal_0.init_value == 995
assert signal_0.samples_per_frame == None
assert signal_0.skew == None
assert signal_0.units == "mV"
print("Finished testing signal line 0")

print("Testing signal line 1")
signal_1 = signal_lines[1]
assert signal_1.adc_gain == float(200)
assert signal_1.adc_resolution == 11
assert signal_1.adc_zero == 1024
assert signal_1.baseline == None
assert signal_1.block_size == 0
assert signal_1.byte_offset == None
assert signal_1.checksum == 20052
assert signal_1.description == "V5"
assert signal_1.file_name == "100.dat"
assert signal_1.format == "212"
assert signal_1.init_value == 1011
assert signal_1.samples_per_frame == None
assert signal_1.skew == None
assert signal_1.units == "mV"
print("Finished testing signal line 1")
print("Finished testing signal line parsing")
print(f"Finished testing header {header}")

print("PASS")
