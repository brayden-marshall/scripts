#!/bin/sh

# check if python is installed
if [ ! `command -v python` ]; then
    echo "Python is not installed. How did you manage that?"
    exit 1
fi

# check if the python 'systemd' module is installed
# this module is used in some scripts to log to journalctl from python
python -c "import systemd"
if [ $? -ne 0 ]; then
    echo "The python 'systemd' module is not installed."
    echo "On arch-based systems try installing the python-systemd package"
    echo "Otherwise just google it I guess"
    exit 1
fi

if [ ! -d "$HOME/.config/systemd/user/" ]; then
    mkdir -p "$HOME/.config/systemd/user"
fi
cp ./battery_notification.service $HOME/.config/systemd/user/
cp ./powertop_auto_tune.service $HOME/.config/systemd/user/
