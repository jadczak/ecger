import ecg_parsers
import pathlib
import pickle

here = pathlib.Path(__file__).parent
test_dir = here / "test-data"
header_file = test_dir / "100.hea"
data_file = test_dir / "100.dat"
test_file = test_dir / "100.pkl"

record_line, signal_lines = ecg_parsers.read_header(header_file)
channels_adc, channels_real = ecg_parsers.read_format212(data_file, signal_lines)


with open(test_file, "rb") as f:
    test_data = pickle.load(f)

test_adc = test_data["test_adc"]
test_real = test_data["test_real"]

print("Testing data file 100")
print("Testing ADC reading")
assert len(channels_adc) == len(test_adc)
assert len(channels_adc[0]) == len(test_adc[0])
assert len(channels_adc[1]) == len(test_adc[1])
for adc0, adc1, test0, test1 in zip(channels_adc[0], channels_adc[1], test_adc[0], test_adc[1]):
    assert adc0 == test0
    assert adc1 == test1

print("ADC reading complete")
print("Testing real unit conversion")
assert len(channels_adc) == len(test_adc)
assert len(channels_adc[0]) == len(test_adc[0])
assert len(channels_adc[1]) == len(test_adc[1])
for real0, real1, test0, test1 in zip(channels_real[0], channels_real[1], test_real[0], test_real[1]):
    assert real0 == test0
    assert real1 == test1

print("Real unit convertion complete")
print("PASS")
