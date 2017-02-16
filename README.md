# SmokeTest Sample

Python smoketest scripts that runs commands via ssh on a test system
The file main.py is the starting point and is driven by the systems.ini file. The systems.ini file contains ip, username and password of all the test systems.
## Getting Started

These test were verified on a Centos 6.0.

### Prerequisites

The target system(s) need to have rpmbuild binary, ssh and scp programs to work

## Running the tests

Open the project with Eclipse IDE
Configure the systems.ini file with the correct system information like IP, Username and Password

### Break down into the tests

The smoketest connects to each of the systems in the systems.ini file and runs a series of test basic test like ls command to display files in a specified directory, put files and get files from the test system, put and get directories, delete a test rpm and binary files, run a build command to create a new rpm, install the rpm and execute the binary provided by that rpm and capture the output provided.
Since there are multiple systems every system runs in its own thread and thread locks are used to prevent problem like access to the same files by different threads. Logging is used throughout the process, by default its only to stdout but can be written to log file if debug is enabled in the systems.ini file.


## Built With

EasyEclipse for LAMP
Version: 1.2.2.2

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## Authors


## License


## Acknowledgments

