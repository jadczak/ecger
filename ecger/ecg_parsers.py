import pathlib
from itertools import cycle


class RecordLine:
    __slots__ = (
        "record_name",
        "num_segs",
        "num_sigs",
        "sample_freq",
        "counter_freq",
        "base_value",
        "num_samples",
        "base_time",
        "base_date",
    )

    def __init__(self):
        self.record_name: str | None = None
        self.num_segs: int | None = None
        self.num_sigs: int | None = None
        self.sample_freq: float = 250
        self.counter_freq: float = 250
        self.base_value: int = 0
        self.num_samples: int | None = None
        self.base_time: str = "0:0:0"
        self.base_date: str | None = None


class SignalLine:
    __slots__ = (
        "file_name",
        "format",
        "samples_per_frame",
        "skew",
        "byte_offset",
        "adc_gain",
        "baseline",
        "units",
        "adc_resolution",
        "adc_zero",
        "init_value",
        "checksum",
        "block_size",
        "description",
    )

    def __init__(self):
        self.file_name: str | None = None
        self.format: str | None = None
        self.samples_per_frame: int | None = None
        self.skew: int | None = None
        self.byte_offset: int | None = None
        self.adc_gain: float | None = None
        self.baseline: int | None = None
        self.units: str = "mV"
        self.adc_resolution: int | None = None
        self.adc_zero: int = 0
        self.init_value: int | None = None
        self.checksum: int | None = None
        self.block_size: int | None = None
        self.description: str | None = None


def read_header(file: pathlib.Path) -> tuple[RecordLine, list[SignalLine]]:
    """
    https://physionet.org/physiotools/wag/header-5.htm
    """
    with open(file, "r", encoding="utf-8") as i:
        have_record = False
        record_line = RecordLine()
        signal_lines = []
        for line in i:
            line = line.rstrip("\r\n")
            if not line:  # blank line
                continue
            elif line[0] == "#":  # comment
                continue
            elif not have_record:  # this is the record line
                # TODO: There is no error handling for any of this shit.
                have_record = True
                line = line.split()
                for x, field in enumerate(line):
                    match x:
                        case 0:
                            name_seg = field.split("/")
                            record_line.record_name = name_seg[0]
                            if len(name_seg) == 2:
                                record_line.num_segs = int(name_seg[1])
                        case 1:
                            record_line.num_sigs = int(field)
                        case 2:
                            val_other = field.split("/")
                            record_line.sample_freq = float(val_other[0])
                            record_line.counter_freq = record_line.sample_freq
                            if len(val_other) == 2:
                                val_other = val_other[1].split("(")
                                cf = float(val_other[0])
                                record_line.counter_freq = cf if cf > 0 else record_line.sample_freq
                                if len(val_other) == 2:
                                    record_line.base_value = int(val_other[1].split(")")[0])
                        case 3:
                            record_line.num_samples = int(field)
                        case 4:
                            record_line.base_time = field
                        case 5:
                            record_line.base_date = field
            elif have_record:  # this will be a signal line
                signal_line = SignalLine()
                line = line.split()
                # TODO: detemine the default adc res from the format
                for x, field in enumerate(line):
                    match x:
                        case 0:
                            signal_line.file_name = field
                        case 1:
                            base_val = field.split("+")
                            if len(base_val) == 2:
                                signal_line.byte_offset = int(base_val[1])
                            base_val = base_val[0].split(":")
                            if len(base_val) == 2:
                                signal_line.skew = int(base_val[1])
                            base_val = base_val[0].split("x")
                            if len(base_val) == 2:
                                signal_line.samples_per_frame = int(base_val[1])
                            signal_line.format = base_val[0]
                        case 2:
                            base_val = field.split("/")
                            if len(base_val) == 2:
                                signal_line.units = base_val[1]
                            base_val = base_val[0].split(")")
                            base_val = base_val[0].split("(")
                            if len(base_val) == 2:
                                signal_line.baseline = int(base_val[1])
                            signal_line.adc_gain = float(base_val[0])
                        case 3:
                            val = int(field)
                            if val:
                                signal_line.adc_resolution = val
                        case 4:
                            signal_line.adc_zero = int(field)
                        case 5:
                            signal_line.init_value = int(field)
                        case 6:
                            signal_line.checksum = int(field)
                        case 7:
                            signal_line.block_size = int(field)
                        case 8:
                            signal_line.description = field
                if signal_line.baseline is None:
                    signal_line.baseline = signal_line.adc_zero
                if signal_line.init_value is None:
                    signal_line.init_value = signal_line.adc_zero
                signal_lines.append(signal_line)
            else:  # TODO: Error handling
                pass
        return record_line, signal_lines


def read_212(file: pathlib.Path, signal_lines: list[SignalLine]) -> tuple[dict[int, list[int]], dict[int, list[float]]]:
    """
    https://physionet.org/physiotools/wag/signal-5.htm
    """
    signals = len(signal_lines)
    channels_adc = {}
    channels_real = {}
    zeros = {}
    gains = {}
    for i in range(signals):
        channels_adc[i] = []
        channels_real[i] = []
        zeros[i] = signal_lines[i].adc_zero
        gains[i] = signal_lines[i].adc_gain
    idx = cycle(range(signals))
    with open(file, "rb") as i:
        while byte_chunk := i.read(3):
            chunk = int.from_bytes(byte_chunk, byteorder="big", signed=False)
            first_least = chunk & 0xFF_00_00
            first_most = chunk & 0x00_0F_00
            second_least = chunk & 0x00_00_FF
            second_most = chunk & 0x00_F0_00
            first_2s = (first_most >> 0) | (first_least >> 16)
            second_2s = (second_most >> 4) | (second_least >> 0)
            first = (first_2s & 0x7FF) - (first_2s & 0x800)
            second = (second_2s & 0x7FF) - (second_2s & 0x800)
            first_idx = next(idx)
            channels_adc[first_idx].append(first)
            first_real = (first - zeros[first_idx]) / gains[first_idx]
            channels_real[first_idx].append(first_real)
            second_idx = next(idx)
            second_real = (second - zeros[second_idx]) / gains[second_idx]
            channels_real[second_idx].append(second_real)
            channels_adc[second_idx].append(second)
    return channels_adc, channels_real


def read_16(file: pathlib.Path, signal_lines: list[SignalLine]) -> tuple[dict[int, list[int]], dict[int, list[float]]]:
    """
    https://physionet.org/physiotools/wag/signal-5.htm
    """
    signals = len(signal_lines)
    channels_adc = {}
    channels_real = {}
    zeros = {}
    gains = {}
    for i in range(signals):
        channels_adc[i] = []
        channels_real[i] = []
        zeros[i] = signal_lines[i].adc_zero
        gains[i] = signal_lines[i].adc_gain
    idx = cycle(range(signals))
    with open(file, "rb") as f:
        while byte_chunk := f.read(2):
            val = int.from_bytes(byte_chunk, byteorder="little", signed=True)
            this_idx = next(idx)
            channels_adc[this_idx].append(val)
            real = (val - zeros[this_idx]) / gains[this_idx]
            channels_real[this_idx].append(real)
    return channels_adc, channels_real


def read_24(file: pathlib.Path, signal_lines: list[SignalLine]) -> tuple[dict[int, list[int]], dict[int, list[float]]]:
    """
    https://physionet.org/physiotools/wag/signal-5.htm
    """
    signals = len(signal_lines)
    channels_adc = {}
    channels_real = {}
    zeros = {}
    gains = {}
    for i in range(signals):
        channels_adc[i] = []
        channels_real[i] = []
        zeros[i] = signal_lines[i].adc_zero
        gains[i] = signal_lines[i].adc_gain
    idx = cycle(range(signals))
    with open(file, "rb") as f:
        while byte_chunk := f.read(3):
            val = int.from_bytes(byte_chunk, byteorder="little", signed=True)
            this_idx = next(idx)
            channels_adc[this_idx].append(val)
            real = (val - zeros[this_idx]) / gains[this_idx]
            channels_real[this_idx].append(real)
    return channels_adc, channels_real
