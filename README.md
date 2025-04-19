> [!CAUTION]
> The contents of this repository highlights a crucial government system designed to alert the public urgently in an emergency. Tampering, broadcasting, or spoofing restricted radio signals such as the ones used in the EAS is illegal. This repository and its code exists for educational purposes only. YOU ARE SOULY RESPONSIBLE FOR THE USE AND DISTRIBUTION OF ALERTS GENERATED FROM THIS TOOL!

![Emergency Alert Generator](docs/logo.png)

---
![Static Badge](https://img.shields.io/badge/python-3.12-blue)


This project exists to explore & demonstrate the United States Emergency Alert System, and how Specific Area Messages are encoded (SAME) for civil, national, and weather alerts. 

## About This Project

This project accompanies a full write-up article on Medium which explores more details of the Emergency Alert System and NOAA Weather Radios. [Click here to read the article](https://medium.com/@oglesbeejacob/hacking-the-airwaves-simulating-emergency-alerts-with-a-pi-and-sdr-de578e40f53b).

## Watch the Video Example
Below is a video example demonstrating transmitting the EAS Alert and receiving it on a NOAA Weather Radio.

[![Watch the Video Example](https://img.youtube.com/vi/Q81Cd0IZ0RE/0.jpg)](https://youtu.be/Q81Cd0IZ0RE)

## Installing & Using This Project
This project has been tested with Python Version 3.12.10. 
1. `git clone https://github.com/JacobSecOps/Emergency_Alert_Generator.git`
2. `pip install -r requirements.txt --upgrade`





## Emergency Alert SAME Header Format
Emergency Alerts follow a specific format to be used by decoders and NOAA Weather Radios. This format is fully documented [here](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-11#11.31). The most important information is noted below.

Example SAME Header: `[PREAMBLE]ZCZC-ORG-EEE-PSSCCC-+TTTT-JJJHHMM-LLLLLLLL`

* `[PREAMBLE]` is a stream of 16 Hexadecimal AB bytes, and essentially exists to clear an EAS decoder system in preparation for the alert itself.
* `ZCZC` is static text, acting as an identifier.
* `ORG` is the originating party who activated the EAS. These are listed [here](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-11/subpart-B/section-11.31#p-11.31(e)).
* `EEE` is the event code and ultimately tells you why the EAS was activated. These are listed [here](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-11/subpart-B/section-11.31#p-11.31(e)).
* `PSSCCC` is a 6 digit numeric string representing the area(s) of the country which is affected by an alert. SAME Headers can support up to 31 locations in one single alert.
    * `P` represents a subdivision of an unusually shaped county, or designed for more specific targeting (usually "Northwest", "Southeast" or other sectioning). In practice, P is not used very frequently.
    * `SS` represents the 2-digit state code being targeted. These are listed [here](https://www.ecfr.gov/current/title-47/chapter-I/subchapter-A/part-11/subpart-B/section-11.31#p-11.31(f)). A state code of 00 targets all states (the whole country).
    * `CCC` represents a 3-digit county/city code which can be found easily on the NWS website found [here](https://www.weather.gov/nwr/counties). When browsing one of these lists, the SAME location code is the combination of State and County (SSCCC), so for Ohio in Franklin County, it would be 39 for Ohio, and 049 for the county.
* `+TTTT` represents the valid time period of the message, starting in 15 minute increments and then 30 minute increments past one hour. Fun fact, this is why Weather Alerts always land on evenly distributed timespans.)
* `JJHHMM` represents the day in Julian Calendar Days, hours, and minutes when the message was originally sent in UTC.
* `LLLLLLLL` represents the originating office of the EAS message, or who is retransmitting it. This string is appended to messages automatically by the EAS encoder devices.