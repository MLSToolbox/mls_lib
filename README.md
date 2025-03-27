# MLS Library

mls_lib is a Python library containing a set of classes, organized in different packages, representing the structure and the main concepts required to instantiate and orchestrate any ML pipeline, its stages and the tasks that these stages perform. These classes have been carefully designed to meet Software Engineering design principles. The code of specific ML pipelines, generated by the [mls_code_generator](https://github.com/MLSToolbox/mls_code_generator) component, imports the mls_lib and instantiates the classes for these pipelines, ensuring the high quality of the generated code. The library code documentation may be found at the following [link](https://mlstoolbox.github.io/mls_lib/).

## mls_lib classes

![Image](https://github.com/user-attachments/assets/c232f1dc-4847-4fac-bb7e-08c0ba27822c)

The mls_lib library contains the following packages:
- The orchestration package (grey classes) contains the classes to represent the pipelines and their steps (Pipeline, Step, Stage and Task classes), and the operations to execute them. A step can be either a stage or a task and it receives an input and produces an output . Stages are complex steps that contain tasks. Tasks are pipeline steps that correspond to concrete pieces of code to be executed. Each stage and task redefines their input and output objects. For example, the SVMTrainer task receives as input the features and truth data frames and produces an SVMModel. 
- For each ML pipeline stage, a package containing a set of classes for predefined tasks related to that stage. For example, the data_cleaning package (blue classes) includes two classes: ReplaceNullZero which replaces null values in a dataset column with zero; and ReplaceValue which replaces column values with a specified set of input values.  Both classes override the inherited execute() operation to implement the specific logic for their respective tasks.
- The objects package (yellow classes) includes classes for the different data types used as input and/or output of tasks.

## Requirements to use mls_lib
In order to use the mls_lib classes, you need to have installed the Python packages indicated in the requirements.txt file [mls_lib](https://github.com/MLSToolbox/mls_lib/blob/main/mls_lib/requirements.txt) package in this repository.  
