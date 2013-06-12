#!/usr/bin/python
# coding=utf-8

__author__ = "marc"

import telnetlib
import argparse
import sys


class Zyxel:
    def __init__(self, host, pw):
        self.connection = telnetlib.Telnet(host)

        # Passwort eingeben
        self.password(pw)

        # Menü: System Maintainance
        self.select("24")

        # Menü: Diagnostic
        self.select("8")

        self.connection.read_until("> ")

    def password(self, password):
        self.connection.read_until("Password:")
        self.connection.write(password + "\n")

    def select(self, s):
        self.connection.read_until("Number:")
        self.connection.write(s + "\n")

    def reboot(self):
        self.connection.write("sys reboot\n")
        self.disconnect()

    def disconnect(self):
        self.connection.close()

    def logs(self):
        self.connection.write("sys logs display\n")
        return self.connection.read_until("> ")


parser = argparse.ArgumentParser(description='Manage a Zyxel router')
parser.add_argument("-p", "--password", type=str, help="password", default="1234", dest="password")
parser.add_argument("host", type=str, help="host")
parser.add_argument("command", type=str, help="reboot")

args = parser.parse_args()

if args.command == "reboot":
    zyxel = Zyxel(args.host, args.password)
    zyxel.reboot()
elif args.command == "logs":
    zyxel = Zyxel(args.host, args.password)
    print zyxel.logs()
    zyxel.disconnect()
else:
    print "unknown command: %s" % args.command
