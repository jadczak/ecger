import ecg_parsers
import pathlib
import pickle
from math import isclose

here = pathlib.Path(__file__).parent
test_dir = here / "test-data"
header_file = test_dir / "x0015.hea"
data_file = test_dir / "x0015.dat"
test_file = test_dir / "x0015.pkl"

record_line, signal_lines = ecg_parsers.read_header(header_file)
channels_adc, channels_real = ecg_parsers.read_format24(data_file, signal_lines)


with open(test_file, "rb") as f:
    test_data = pickle.load(f)

test_adc = test_data["test_adc"]
test_real = test_data["test_real"]

print("Testing data file x0015")
print("Testing ADC reading")
assert len(channels_adc) == len(test_adc)
assert len(channels_adc[0]) == len(test_adc[0])
assert len(channels_adc[1]) == len(test_adc[1])
assert len(channels_adc[2]) == len(test_adc[2])
assert len(channels_adc[3]) == len(test_adc[3])
assert len(channels_adc[4]) == len(test_adc[4])
assert len(channels_adc[5]) == len(test_adc[5])
assert len(channels_adc[6]) == len(test_adc[6])
assert len(channels_adc[7]) == len(test_adc[7])
assert len(channels_adc[8]) == len(test_adc[8])
assert len(channels_adc[9]) == len(test_adc[9])
assert len(channels_adc[10]) == len(test_adc[10])
assert len(channels_adc[11]) == len(test_adc[11])
assert len(channels_adc[12]) == len(test_adc[12])
assert len(channels_adc[13]) == len(test_adc[13])
assert len(channels_adc[14]) == len(test_adc[14])
assert len(channels_adc[15]) == len(test_adc[15])
assert len(channels_adc[16]) == len(test_adc[16])
assert len(channels_adc[17]) == len(test_adc[17])
for (
    adc0,
    adc1,
    adc2,
    adc3,
    adc4,
    adc5,
    adc6,
    adc7,
    adc8,
    adc9,
    adc10,
    adc11,
    adc12,
    adc13,
    adc14,
    adc15,
    adc16,
    adc17,
    test0,
    test1,
    test2,
    test3,
    test4,
    test5,
    test6,
    test7,
    test8,
    test9,
    test10,
    test11,
    test12,
    test13,
    test14,
    test15,
    test16,
    test17,
) in zip(
    channels_adc[0],
    channels_adc[1],
    channels_adc[2],
    channels_adc[3],
    channels_adc[4],
    channels_adc[5],
    channels_adc[6],
    channels_adc[7],
    channels_adc[8],
    channels_adc[9],
    channels_adc[10],
    channels_adc[11],
    channels_adc[12],
    channels_adc[13],
    channels_adc[14],
    channels_adc[15],
    channels_adc[16],
    channels_adc[17],
    test_adc[0],
    test_adc[1],
    test_adc[2],
    test_adc[3],
    test_adc[4],
    test_adc[5],
    test_adc[6],
    test_adc[7],
    test_adc[8],
    test_adc[9],
    test_adc[10],
    test_adc[11],
    test_adc[12],
    test_adc[13],
    test_adc[14],
    test_adc[15],
    test_adc[16],
    test_adc[17],
):
    assert adc0 == test0
    assert adc1 == test1
    assert adc2 == test2
    assert adc3 == test3
    assert adc4 == test4
    assert adc5 == test5
    assert adc6 == test6
    assert adc7 == test7
    assert adc8 == test8
    assert adc9 == test9
    assert adc10 == test10
    assert adc11 == test11
    assert adc12 == test12
    assert adc13 == test13
    assert adc14 == test14
    assert adc15 == test15
    assert adc16 == test16
    assert adc17 == test17

print("ADC reading complete")
print("Testing real unit conversion")
assert len(channels_adc) == len(test_adc)
assert len(channels_adc[0]) == len(test_adc[0])
assert len(channels_adc[1]) == len(test_adc[1])
assert len(channels_adc[2]) == len(test_adc[2])
assert len(channels_adc[3]) == len(test_adc[3])
assert len(channels_adc[4]) == len(test_adc[4])
assert len(channels_adc[5]) == len(test_adc[5])
assert len(channels_adc[6]) == len(test_adc[6])
assert len(channels_adc[7]) == len(test_adc[7])
assert len(channels_adc[8]) == len(test_adc[8])
assert len(channels_adc[9]) == len(test_adc[9])
assert len(channels_adc[10]) == len(test_adc[10])
assert len(channels_adc[11]) == len(test_adc[11])
assert len(channels_adc[12]) == len(test_adc[12])
assert len(channels_adc[13]) == len(test_adc[13])
assert len(channels_adc[14]) == len(test_adc[14])
assert len(channels_adc[15]) == len(test_adc[15])
assert len(channels_adc[16]) == len(test_adc[16])
assert len(channels_adc[17]) == len(test_adc[17])

for (
    real0,
    real1,
    real2,
    real3,
    real4,
    real5,
    real6,
    real7,
    real8,
    real9,
    real10,
    real11,
    real12,
    real13,
    real14,
    real15,
    real16,
    real17,
    test0,
    test1,
    test2,
    test3,
    test4,
    test5,
    test6,
    test7,
    test8,
    test9,
    test10,
    test11,
    test12,
    test13,
    test14,
    test15,
    test16,
    test17,
) in zip(
    channels_real[0],
    channels_real[1],
    channels_real[2],
    channels_real[3],
    channels_real[4],
    channels_real[5],
    channels_real[6],
    channels_real[7],
    channels_real[8],
    channels_real[9],
    channels_real[10],
    channels_real[11],
    channels_real[12],
    channels_real[13],
    channels_real[14],
    channels_real[15],
    channels_real[16],
    channels_real[17],
    test_real[0],
    test_real[1],
    test_real[2],
    test_real[3],
    test_real[4],
    test_real[5],
    test_real[6],
    test_real[7],
    test_real[8],
    test_real[9],
    test_real[10],
    test_real[11],
    test_real[12],
    test_real[13],
    test_real[14],
    test_real[15],
    test_real[16],
    test_real[17],
):
    assert isclose(real0, test0, abs_tol=1e-8)  # the output of rdsamp is fixed width
    assert isclose(real1, test1, abs_tol=1e-8)
    assert isclose(real2, test2, abs_tol=1e-8)
    assert isclose(real3, test3, abs_tol=1e-8)
    assert isclose(real4, test4, abs_tol=1e-8)
    assert isclose(real5, test5, abs_tol=1e-8)
    assert isclose(real6, test6, abs_tol=1e-8)
    assert isclose(real7, test7, abs_tol=1e-8)
    assert isclose(real8, test8, abs_tol=1e-8)
    assert isclose(real9, test9, abs_tol=1e-8)
    assert isclose(real10, test10, abs_tol=1e-8)
    assert isclose(real11, test11, abs_tol=1e-8)
    assert isclose(real12, test12, abs_tol=1e-8)
    assert isclose(real13, test13, abs_tol=1e-8)
    assert isclose(real14, test14, abs_tol=1e-8)
    assert isclose(real15, test15, abs_tol=1e-8)
    assert isclose(real16, test16, abs_tol=1e-8)
    assert isclose(real17, test17, abs_tol=1e-8)

print("Real unit convertion complete")
print("PASS")
