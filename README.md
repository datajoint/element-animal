# DataJoint Element - Animal

+ `elements-animal` features a DataJoint pipeline design for animal management.

+ `elements-animal` contains two modules
>+ subject: contains the basic information of subject, including Strain, Line and Zygosity information
>+ genotyping: this module is designed for labs that keep track of colony management and genotyping results, containing information of breeding, weaning, housing, and genotyping.

+ `elements-animal` is not a complete workflow by itself, but rather a modular design of tables and dependencies.

+ `elements-animal` can be flexibly attached to any DataJoint workflow.

## Element usage

+ See the [workflow-animal] (https://github.com/datajoint/workflow-animal) repository for example usage of `elements-animal`.

+ Also refer to the [workflow-imaging](https://github.com/datajoint/workflow-imaging) and [workflow-ephys](https://github.com/datajoint/workflow-ephys) repositories for example usages of `elements-animal` when combining with other elements.

+ See the [datajoint-elements](https://github.com/datajoint/datajoint-elements) repository for a detailed description of the DataJoint elements and workflows.

## Element architecture

![subject diagram](images/subject_diagram.svg)
![genotyping diagram](images/genoytping_diagram.svg)
