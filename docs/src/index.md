# DataJoint Element - Animal

+ `element-animal` features a DataJoint pipeline design for subject and genotyping management. 

+ `element-animal` is not a complete workflow by itself, but rather a modular design of tables and dependencies. 

+ `element-animal` can be flexibly attached to any DataJoint workflow.

+ See the [Element Animal documentation](https://elements.datajoint.org/description/animal/) for the background information and development timeline.

+ For more information on the DataJoint Elements project, please visit https://elements.datajoint.org.  This work is supported by the National Institutes of Health.

## Element architecture

There are two modules in `element-animal`:
+ subject: contains the basic information of subject, including Strain, Line, Subject, Zygosity, and SubjectDeath information
+ genotyping: this module is designed for labs that keep track of colony management and genotyping results, containing information of breeding, weaning, housing, and genotyping.

### Subject Diagram

![](https://raw.githubusercontent.com/datajoint/element-animal/main/images/subject_diagram.svg)

### Genotyping Diagram

![](https://raw.githubusercontent.com/datajoint/element-animal/main/images/genotyping_diagram.svg)