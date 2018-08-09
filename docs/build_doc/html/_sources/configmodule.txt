-------------------------
Configuration Module file
-------------------------

Whole modules (`tar.gz`) need a configuration .json file. This file is required. CoreManagement use the .json file to save the necessary information for installation and for execution on the Core.

The .json file must have the same name that the module name and 'module_name' key inside the .json file.

The data including in the .json file are the next:

:module_name: [Required] This is the module name. This must be the same that the moodule.tar.gz and module.json.

:running: [Required] This is a dict with information necessary to know how the module must be run

1. **exec** [Required] This say me if the module run:

  * `once`: This mean that the Core call the module once, during the installation. This is recommend when the module is a service or daemon that  need to be running for ever.

  * `none`: This mean that the Core does not have to run this module. This is used for module that is called for other modules.
    
  * `periodically`: This mean that Core run this module periodically for each `each_time` ms

2. **run**: [optional] This a dict options that say me how the module must run:

  * `python`: [Required] Here the module name or main script must be set. For  example, if my main script module is test.py, this values must be completed like this:

.. code-block:: javascript
  :linenos:

        {...
             "running": {...
                 "python": "test.py",
             ...
             }
        ...
       }


* `parameters`: [optional] If the module or script need parameters, they
    have to be written here like a string.

* `each_time`: [required if exec value is set on `periodically` mode] If this module or script need
      to be executed each some time, the time have to be written here. This values is on milliseconds.


3. `permissions`: TBD. This is used to set user log in permissions. This must
   be used by the UserControl.

Example of configuration .json file:

.. code-block:: javascript
    :linenos:
       
    {
        "package": {
            "module_name": "test",
            "running": {
                "exec": "once|once|periodically",
                "run": {
                    "python": "test.py",
                    "parameters": "",
                    "each_time": 1000
                },
                "permissions": "TBD"
            }
        }

    }}
