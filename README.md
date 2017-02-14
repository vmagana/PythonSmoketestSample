# PythonSmoketestSample
Python smoketest scripts that runs commands via ssh on a test system
The file main.py is the starting point and is driven by the systems.ini file.
The systems.ini file contains ip, username and password of all the test systems.
The smoketest connects to each of those systems and run a series of test basic test like ls command to display files in a specified directory, put files and get files from the test system, delete some rpm and binary files, run a build command to create a new rpm, install the rpm and execute the binary provided by that rpm and capture the output provided.
Since there are multiple systems every system runs in its own thread and thread locks are used to prevent problem like access to the same files by different threads. Logging is used throughout the process, by default its only to stdout but can be written to log file if debug is enabled in the systems.ini file.
