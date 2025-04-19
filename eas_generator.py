import argparse
import numpy as np
from lib.constants import ATTENTION_TONE_DEFAULT_DURATION, CODES, ORIGINATORS, VERSION
from lib.waveform_generator import build_same_message, build_eom, generate_attention_tone
from lib.tts_message import generate_tts_message
from lib.wave_utils import save_wave
from lib.same_generator import generate_same_header
from lib.logger import *

def banner():
    return f"""
   _______   ____  _____                      __          
  / __/ _ | / __/ / ___/__ ___  ___ _______ _/ /____  ____
 / _// __ |_\ \  / (_ / -_) _ \/ -_) __/ _ `/ __/ _ \/ __/
/___/_/ |_/___/  \___/\__/_//_/\__/_/  \_,_/\__/\___/_/   

Version: {VERSION}

This Script generates valid United States Emergency Alert headers & messages.
YOU ARE SOULY RESPONSIBLE FOR THE USE AND DISTRIBUTION OF ALERTS GENERATED FROM THIS TOOL!

Read More: https://medium.com/@oglesbeejacob/hacking-the-airwaves-simulating-emergency-alerts-with-a-pi-and-sdr-de578e40f53b

"""

def prompt():
    print("IMPORTANT NOTE: This tool generates valid Specific Area Message Alert codes and messages. Broadcasting or misuse of these messages is highly illegal.")
    print("YOU ARE SOULY RESPONSIBLE FOR THE USE AND DISTRIBUTION OF ALERTS GENERATED FROM THIS TOOL!")
    response = input("To acknowledge this warning, please type \"I understand\" on the prompt, or pass in --acknowledgeLegal as an argument: ")
    if (response.lower() == "I understand".lower()):
        return
    else:
        error("Please type \"I understand\" on the prompt.")
        prompt()


def main():
    print(banner())
    parser = argparse.ArgumentParser("Generate EAS Alert Messages. YOU ARE SOULY RESPONSIBLE FOR THE USE AND DISTRIBUTION OF ALERTS GENERATED FROM THIS TOOL!")

    parser.add_argument("-s", "--state", required=True, help="The full name of the state to target.")
    parser.add_argument("-c", "--county", required=True, help="The full name of the county to target in the specified state.")
    parser.add_argument("-m", "--message", required=True, help="The Text-To-Speech message to include as part of the alert.")
    parser.add_argument("-od", "--day", required=True, help="The Julian Day this alert originates from.")
    parser.add_argument("-oh", "--hour", required=True, help="The Julian Hour this alert originates from.")
    parser.add_argument("-om", "--minute", required=True, help="The Julian Minute this alert originates from.")
    parser.add_argument("-or", "--origin", required=True, help="The Originator which sent this alert.", choices=ORIGINATORS)
    parser.add_argument("-ev", "--event", required=True, help="The Event Code this alert is for.", choices=CODES)
    parser.add_argument("-du", "--duration", required=True, help="How long the alert is valid for.", default="0015")
    parser.add_argument("-id", "--identification", required=True, help="The identity of who sent the alert. Max length is 8 characters", default="EXAMPLE")
    parser.add_argument("-at", "--attention-tone", type=int, default=ATTENTION_TONE_DEFAULT_DURATION, choices=range(0, 25),
                        help=f"Duration of the Attention Tone in seconds (default {ATTENTION_TONE_DEFAULT_DURATION}, range 0-24)",
                        metavar="[0-24]")
    parser.add_argument("-o", "--output", default="eas_output.wav", help="Output WAV File Path.")
    parser.add_argument("--acknowledgeLegal", required=False, help="Acknowledge the legal rules for Emergency Alerts and bypass the interactive prompt.", default=False, action="store_true")
    args = parser.parse_args()

    if (args.acknowledgeLegal == False):
        prompt()

    info("Executing EAS Generator...")
    samples = []

    same = generate_same_header(args.state, args.county, args.day, args.hour, args.minute, args.origin, args.event, args.duration, args.identification)
    info("Building output WAV...")
    samples.append(build_same_message(same))
    samples.append(np.zeros(int(96000 * 1.0), dtype=np.int16))
    if args.attention_tone > 0:
        samples.append(generate_attention_tone(args.attention_tone))
        samples.append(np.zeros(int(96000 * 1.0), dtype=np.int16))
    
    tts_samples = generate_tts_message(args.message)
    samples.append(tts_samples)
    samples.append(np.zeros(int(96000 * 1.0), dtype=np.int16))
    samples.append(build_eom())

    final_samples = np.concatenate(samples)
    info("Saving WAV file...")
    save_wave(args.output, final_samples)
    info(f"EAS Alert Message saved to: {args.output}")

if __name__ == "__main__":
    main()
