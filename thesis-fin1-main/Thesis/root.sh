#!/bin/bash

username="parallels"

sudo sh -c "echo '${username} ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers"
sudo sh -c "echo '${username} ALL=(ALL) NOPASSWD: /sbin/iptables"
sudo sh -c "echo 'parallels ALL=(ALL) NOPASSWD: /sbin/iptables' >> /etc/sudoers"