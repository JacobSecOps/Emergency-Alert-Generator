MARK_FREQ = 2083.3
SPACE_FREQ = 1562.5
SAMPLE_RATE = 96000
SAMPLES_PER_BIT = 184
AMPLITUDE = 4096
PREAMBLE_BYTES = [0xAB] * 16
ATTENTION_TONE_FREQ1 = 853
ATTENTION_TONE_FREQ2 = 960
ATTENTION_TONE_DEFAULT_DURATION = 8

VERSION = "1.0"

# SAME Constants
# EAS = EAS Participant
# CIV = Civil Authorities
# WXR = National Weather Service
# PEP = United States Government (Primary Entrypoint System)
ORIGINATORS = [
    "EAS",
    "CIV",
    "WXR",
    "PEP"
]

# All Emergency Alert System valid events.
# Documented here: https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-11/subpart-B/section-11.31#p-11.31(e)
CODES = [
    'EAN',
    'EAT',
    'NIC',
    'NPT',
    'RMT',
    'RWT',
    'ADR',
    'AVW',
    'AVA',
    'BZW',
    'CAE',
    'CDW',
    'CEM',
    'CFW',
    'CFA',
    'DSW',
    'EQW',
    'EVI',
    'FRW',
    'FFW',
    'FFA',
    'FFS',
    'FLW',
    'FLA',
    'FLS',
    'HMW',
    'HWW',
    'HWA',
    'HUW',
    'HUA',
    'HLS',
    'LEW',
    'LAE',
    'NMN',
    'TOE',
    'NUW',
    'DMO',
    'RHW',
    'SVR',
    'SVA',
    'SVS',
    'SPW',
    'SMW',
    'SPS',
    'TOR',
    'TOA',
    'TRW',
    'TRA',
    'TSW',
    'TSA',
    'VOW',
    'WSW',
    'WSA'
]
