-------------------------
Configuration Module file
-------------------------

Whole modules (`tar.gz`) need a configuration .json file. This file is
required. CoreManagement use the .json file to save the necessary information
 for installation and for execution on the Core.

The .json file must have the same name that the module name and 'module_name'
 key inside the .json file.

The data including in the .json file are the next:

:module_name: [Required] This is the module name. This must be the same that
the moodule.tar.gz and module.json.




Example of configuration .json file:

.. code-block:: json

    {"package": {
        "module_name": "test"
    }}
