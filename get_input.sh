#!/usr/bin/env·bash

# replace year and day
# add session cookie
curl https://adventofcode.com/<year>/day/<day>/input --cookie "session=<session cookie>" >> <day>_input.txt
