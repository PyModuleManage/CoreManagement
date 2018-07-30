# Core Management
A scalable system architecture for python apps 

## Objective

This module is responsible for managing all the modules that live in big 
software architecture. When you develop an app that you know will 
growth you need think about `how could I install new modules or packages 
without compatibility problems?`

Core Management acts like a conductor that allows have a database (MongoDB) 
with information about the apps installed on the Core and what is its 
configuration, and how they run. 

So, in this way, you could develop atomic module software and install it on 
you server without effort. 

### Modules 

Originally, Core Management have 4 important entity.

1. Database. This is the database that save whole information about modules 
and its configuration
2. DatabaseManagement. This is the module that 'manage' the database. Here 
are the necessary methods to write, read, update and delete "things" from the
 Database  
3. ConfigurationManagement. This is the module that manage the modules 
installed configuration.
4. ModuleManagement. This module manage the modules installing and 
module uninstalling

# Contribution
 
Please see [`CONTRIBUTE.md`](./CONTRIBUTING.md)

