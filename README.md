# CLARA for Python

## Overview

The CLARA framework uses a service-oriented architecture ([SOA](https://en.wikipedia.org/wiki/Service-oriented_architecture "Service Oriented Architecture")) to enhance the efficiency, agility, and productivity of data processing activities. Services are the primary means through which data processing logic is implemented.

Data processing applications, developed using the CLARA framework, consist of services, running in a context that is agnostic to the global data processing application logic. Services are loosely coupled and can participate in multiple algorithmic compositions. Legacy processes or applications can be presented as services and integrated into a data processing application. Services can be linked together and presented as one, complex, composite service. This framework provides a federation of services, so that service-based data processing applications can be united while maintaining their individual autonomy and self-governance.

It is important to mention that CLARA makes a clear separation between the service programmer and the data processing application designer. An application designer can be productive by designing and composing data processing applications using available, efficiently and professionally written software services without knowing service programming technical details. Services usually are long-lived and are maintained and operated by their owners on distributed CLARA service containers. This approach provides an application designer the ability to modify data processing applications by incorporating different services in order to find optimal operational conditions, thus demonstrating the overall agility of the CLARA framework.


## Install

### Requirements

The clara framework needs xMsg v2.4.1 to run. [xMsg](https://github.com/JeffersonLab/xmsg_python "xMsg @ Github")
 is a lightweight, yet full featured publish/subscribe messaging system, presenting asynchronous publish/subscribe inter-process communication protocol: an API layer in Java, Python and C++. Please refer to https://github.com/JeffersonLab/xmsg_python for installation instructions

To install clara-python in your system, run:

```sh
$ pip install -r requirements.txt
$ ./setup.py install
```


## Quick Start

### Starting a DPE

Every data processing environment contains proxy, shared memory map, as well as registration databases for both publishers and subscribers. DPE subscribes control requests, such as “create a container”. DPE can create multiple containers. Every container defines a map of locally deployed service objects. Each service object creates and manages object and thread pools for every service-engine object, ready to run within a service. The number of service-engine objects and the size of the thread pool is set by the user, that is recommended to be less or equal to the number of the processor cores.

```sh
$ p_dpe  # or python clara/sys/Dpe.py
```

### Writing an engine

This is a very simple example of a Clara engine in python. User should create an engine class
with a proper name, then add it to the **$CLARA_SERVICES** folder for the DPE to find it.


```python
from clara.base.ClaraUtils import ClaraUtils
from clara.engine.Engine import Engine
from clara.engine.EngineDataType import EngineDataType, Mimetype

class Engine(Engine):
    def __init__(self):
        super(Engine1, self).__init__()

    def configure(self, engine_data):
        # This method gets values to configure the service:
        # For example
        # self.some_configurable_val = engine_data.get_data()
        pass

    def execute(self, engine_data):
        # This service receives an integer and increase the value by one
        # The increased value is then returned.
        data = engine_data.get_data() + 1
        engine_data.set_data(Mimetype.SINT32, data)
        return engine_data

    def execute_group(self, data_array):
        pass

    def get_input_data_types(self):
        # Declares the accepted input datatypes for the engine
        return ClaraUtils.build_data_types(EngineDataType.SINT32())

    def get_output_data_types(self):
        # Declares the accepted output datatypes for the engine
        return ClaraUtils.build_data_types(EngineDataType.SINT32())

    def get_states(self):
        pass

    def get_description(self):
        # Some description of what the engine does.
        return "Some engine1 description"

    def get_version(self):
        # The version of the written engine
        return "v1.0"

    def get_author(self):
        # Information about the author
        return "royarzun"

    def reset(self):
        # Method to reset the engine to its default values
        pass

    def destroy(self):
        # Destructor method for engine
        pass
```

For further help in creating services for the clara framework in python, you can
also refer to [Clara Bootstrap](https://github.com/royarzun/Clara-bootstrap), a collection
 of scripts meant to make life easier for service developers.


## Authors

For assistance contact the authors:

* Vardan Gyurjyan    (<gurjyan@jlab.org>)
* Sebastian Mancilla (<smancill@jlab.org>)
* Ricardo Oyarzun    (<oyarzun@jlab.org>)
