# Project Title

## Description
This project includes hardware, firmware, and software for programming the ESP32-C3.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Firmware Development](#firmware-development)
- [PCB Design](#pcb-design)
- [Troubleshooting](#troubleshooting)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Contact](#contact)

## Introduction
In this project, I designed a PCB, its related firmware, and desktop software to program ESP32-C3 modules. This PCB can program three modules simultaneously.

## Features
- Programming ESP32-C3 or any ESP32 module using a serial connection
- This PCB can program up to three modules simultaneously.
- Easy to use UI

## Hardware Requirements
- ST microcontroller
- AMS117-3.3
- Resistors and Capacitors

## Software Requirements
Nothing, the App folder is standalone.

## Installation
None

## Usage
First, order the PCB and assemble it. Then, program the ST microcontroller with the provided firmware. After that, you can use the UI in the App folder to program your modules. You must provide the necessary files for the app that you want to upload to your ESP module flash, including app, boot, and partition files in .bin format.

## Firmware Development
The ST microcontroller receives data via USB and then sends it to the ESP module(s). It waits for their feedback, and after receiving all the feedback, it sends the feedback to the host system.

## PCB Design
I used Altium to design the PCB and tried to minimize the PCB's dimensions.

## Troubleshooting
In some situations, in the presence of noise, when you want to program three modules simultaneously, you may receive an error in the UI. Please try to use a shorter USB cable and then try again.

## License
Specify the license under which the project is distributed.

## Acknowledgements
Thanks to the Mehbang Group R&D team for their guidance.

## Contact
mahdi.sharif20001@gmail.com
