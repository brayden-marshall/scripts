#!/bin/sh

if [ ! -d "$HOME/.config/systemd/user/" ]; then
    mkdir -p "$HOME/.config/systemd/user"
fi
cp ./battery_notification.service $HOME/.config/systemd/user/
