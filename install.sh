#! /usr/bin/bash

pyinstaller -F spectranet.py --clean --distpath .

rm -r build spectranet.spec