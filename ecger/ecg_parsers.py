import pathlib


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
        self.adc_zero: int | None = None
        self.init_value: int = 0
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
                signal_lines.append(signal_line)
            else:  # TODO: Error handling
                pass
        return record_line, signal_lines
