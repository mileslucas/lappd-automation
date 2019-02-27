# LAPPD Testbench Tools

This repository holds a few tools for use with the Iowa State University LAPPD testbench.

## Installation

#### Prerequisites

These tools make use of `pipenv`  as an environment management tool. There are few requirements to get up and running.

First, make sure the current user is in both the `tty` and `dialout` groups. This is to allow non-root access to the `/dev/ttyUSB0` port.

    $ sudo usermod -aG tty $USER
    $ sudo usermod -aG dialout $USER

After this, log out and log back in and confirm the membership in these groups with 

    $ groups

Now, install `pipenv`. This assumes you have a working python 3 installation. if you do not, I recommend downloading [anaconda](https://www.anaconda.com/distribution/).

    $ pip install pipenv

#### Setting up the environment

Clone this repository

    $ git clone https://github.com/mileslucas/lappd-automation
    $ cd lappd-automation

and set up the `pipenv` environment

    $ pipenv install

To use the Slack testbench bot, populate a file called `.env` with the keys

    SLACK_BOT_TOKEN=<the token from slack development site>
    CHANNEL_ID=<the id of the channel to post to>

Note that this `.env` file should not be checked into version control **under any circumstance**. The bot token is directly linked to a Slack account and publishing it is a major security risk.

`pipenv` will conveniently load the environment variables from `.env` when entering the environment.

## Usage

There are multiple scripts provided to help manage the motor controller, the Tektronix oscilloscope, and the slack message bot.

Beforee using any of these scripts, you must enter the virtual environment by using

    $ pipenv shell
To leave this environment just type
    
    $ exit

If you just need to run one script without wanting to enter the environment, simply run

    $ pipenv run <whatever command>


### slack_bot.py

This is merely an api wrapper for the slack bot. It contains one api function-

    slack_bot.send_message(msg)

This requires having the `SLACK_BOT_TOKEN` and `CHANNEL_ID` environment variables set.

### TekFFM.py

This script allows remote control of TekTronix oscilloscopes for data acquisition.

    $ python TekFFM.py -h
    usage: TekFFM.py [-h] [-s START] folder filename nacq

    Take TekTronix Oscilliscope data remotely

    positional arguments:
    folder                The folder name below "C:/" for the saved oscilliscope
                            data
    filename              The filename base for the saved files
    nacq                  The number of fastframe acquisitions to take

    optional arguments:
    -h, --help            show this help message and exit
    -s START, --start START
                            The iteration to start on. Helpful if resuming a
                            previous run.

Inside this script there is an instrument IP address variable. This must be set to the static IP of the oscilloscope to run.

### motors.py

This file provides both a class `Motors` as well as two convenience functions. The `Motors` class allows interfacing with Bernhard Adams' motor controller. It provides the following api:

```python
class Motors()

    def connect()
    def disconnect()
    def move(motor, position)
    def moveto(motor, position)
    def calibrate(motor, position)
    def stop(motor)
    def reset()
    def park()
    def get_position(motor='all')

```

For more information on any of these methods, access their documentation in a python console like

    >>> from motors import Motors
    >>> Motors.move?

There are two convenience scripts

    $ python motors.py -h
    usage: motors.py [-h] [-c] [-l] [--xlimit] [--ylimit]

    optional arguments:
    -h, --help     show this help message and exit
    -c, --console  Run the motor interface console
    -l, --limit    Run the motor limit finding script
    --xlimit       run parallel motor limit script
    --ylimit       run transverse motor limit script

The `--console` flag starts a terminal console for the motor controller. For those familiar with Bernhard's serial control commands, this takes the exact same commands.

The `--[x/y/]limit` flag allows doing a calibration run to find the limits of the motor stages. Follow the prompts for nudging to the left and the right (either enter "yes" to go 1000 ticks or enter in a tick amount) and then nudge front to back. If you only want to find limits for one stage, use the `x` or `y` limit options.

### multi_channel_sweep.py

This script does a multi-channel sweep and takes data at many spatial points along the LAPPD.

    $ python multi_channel_sweep.py
    usage: multi_channel_sweep.py [-h] [-d FOLDER FILENAME NACQS] [-q] n c

    Move motors to n discrete points across c channels on an LAPPD channel to take
    data

    positional arguments:
    n                     The number of samples to be taken on a channel
    c                     The number of channels to sample from

    optional arguments:
    -h, --help            show this help message and exit
    -d FOLDER FILENAME NACQS, --data FOLDER FILENAME NACQS
                            Take data using the Tek oscilliscope
    -q, --quiet           Do not send slack messages

Note that if you do not provide `--data` arguments this will do a "dry-run" which allows you to check the sweep path. This is convenient to avoid sampling over the LAPPD cross-brace. To do a single-channel parallel sweep, just set the number of channels to 1 (or 0).

**Warning:**
Within this script there are limits for each translational stage of the motors. To ensure safety and accuracy, please find the limits for each stage using the `motors.py -l` script and use those outputs to set the limits.


### Contributions/Questions

For any questions or ideas with these scripts, contact [@mileslucas](https://github.com/mileslucas).