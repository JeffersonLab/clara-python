
# Clara for python

## Installing Clara

### Requirements

The clara framework needs xMsg v2.4.1 to run. xMsg is a lightweight, yet full
featured publish/subscribe messaging system, presenting asynchronous publish/subscribe
inter-process communication protocol: an API layer in Java, Python and C++. Please
refer to https://github.com/JeffersonLab/xmsg_python for installation instructions


To install clara-python in your system, run:

```sh
$ pip install -r requirements.txt
$ ./setup.py install
```

## Quick Start

### Starting a DPE

Every data processing environment contains proxy, shared memory map, as well as registration databases
for both publishers and subscribers. DPE subscribes control requests, such as “create a container”. DPE can create multiple containers. Every container defines a map of locally deployed service objects. Each service object creates and manages object and thread pools for every service-engine object, ready to run within a service. The number of service-engine objects and the size of the thread pool is set by the user, that is recommended to be less or equal to the number of the processor cores.

```sh
$ p_dpe # or python clara/sys/Dpe.py
```

### Desing Conventions

1. Service names are composed as -> dpe_host:container:engine
2. names must be unique within entire cloud
3. registration requests are always sync with timeout defined in xMsgConstants.REGISTER_REQUEST_TIMEOUT
4. finding a service request are also sync with timeout defined as xMsgConstants.FIND_REQUEST_TIMEOUT
5. DPE registration database is duplicated in the Frontend database.

http://claraweb.jlab.org

For assistance contact the authors:

* Vardan Gyurjyan    (<gurjyan@jlab.org>)
* Sebastian Mancilla (<smancill@jlab.org>)
* Ricardo Oyarzun    (<oyarzun@jlab.org>)

