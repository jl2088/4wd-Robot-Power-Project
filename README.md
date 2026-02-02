# Software Analysis and Design of Four Wheel Drive Robot for Power Optimization

## Project Overview
    This study uses a four-wheel drive robot as the experimental platform to systematically evaluate the energy efficiency characteristics of supercapacitors and their adaptability to control algorithms through software-based comparative experiments. The project designed a robot autonomous power monitoring module to collect real-time current and voltage data of supercapacitors and batteries under different algorithm operating conditions, quantifying the performance differences between the two types of energy storage devices. Based on this, the voltage and current sampling frequency was further optimized and the algorithm structure was adjusted, ultimately proposing the optimal sampling strategies and algorithm configuration schemes for supercapacitors and batteries, respectively.

## Features
- Power consumption analysis
- Supercapacitor-battery comparison
- Algorithm analysis and optimization
- Data visualization

## Operating Method
1. The robot used in this project was SunFounder Pico 4wd-wheeled car, whose information could be viewed via https://www.sunfounder.com/products/raspberrypi-pico-car.
2. Set up the environment for the robot, then connect to the configured Pico using a data cable. And turn on Thonny IDE to establish the connection.
3. Design the sampling frequency according to the comment lines in the script, that is, by changing the parameters at the corresponding locations. Afterwards, transfer the code and text files from the Thonny IDE to the robot's local system.
4. Rename the script that needs to be run to 'main.py' locally on the Pico, then power off the device and disconnect the data cable.
5. Connect the robot to a mobile power source (supercapacitor or battery). Restart the robot, and the Pico will automatically execute the script 'main.py'.
6. After the operation is complete, reconnect the data cable and download 'log.txt' to the computer. It contains the current and voltage data read according to the design.

## Project Structure
```text
.
4wd-robot-power-project/
├── src/
│    ├── main-code/    # Set to 'main.py' on Pico
│    │      ├── motors-reading/
│    │      ├── RGB-reading/
│    │      └── Stepped-RGB-reading/
│    └── test-code/    # INA3221-Testing
├── data-collection/    # File log.txt
├── hardware/    # Circuit diagram and sensor connection instructions
├── analysis/    # Data Analysis Scripts / Result Charts
└── README.md

## Tech Stack
- Python (MicroPython)
- Raspberry Pico RPD
- I2C Protocal

## Author
Name: Li, Jiulin (Jiulin Li)
Email: li18661390991@gmail.com or li18661390991@163.com

## Acknowledgement
Thanks to my supervisor Swingler, Jonathan for guidance and to the Robotics Lab for providing hardware support.
