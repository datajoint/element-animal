# DataJoint Element - Animal

There are two modules in `element-animal`:
+ subject: contains the basic information of subject, including Strain, Line, Subject, Zygosity, and SubjectDeath information
+ genotyping: this module is designed for labs that keep track of colony management and genotyping results, containing information of breeding, weaning, housing, and genotyping.

See [Background](Background.md) for the background information and development timeline.

## Element usage

+ `element-animal` is not a complete workflow by itself, but rather a modular design of tables and dependencies that can be flexibly attached to any DataJoint workflow.
+ See the [workflow-animal](https://github.com/datajoint/workflow-animal) repository for example usage of `element-animal`.

+ Also refer to the [workflow-imaging](https://github.com/datajoint/workflow-imaging) and [workflow-ephys](https://github.com/datajoint/workflow-ephys) repositories for example usages of `element-animal` when combining with other elements.

+ See the [datajoint-elements](https://github.com/datajoint/datajoint-elements) repository for a detailed description of the DataJoint elements and workflows.

## Element architecture

### Subject Diagram
![subject diagram](images/subject_diagram.svg)

### Genotyping Diagram
![genotyping diagram](images/genotyping_diagram.svg)
