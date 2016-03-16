
# Clara 2.0 for python

### Installing Clara

To install clara-python in your system, run:

```sh
$ ./setup.py install
```

### Quick Start

Following are design conventions:

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

