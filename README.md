# DataJoint Element - Animal

## Description of modality, user population.

Most pipeline begins with some information about the experiment animal subjects. This includes general information such as source, date of birth, sex, owner, and death information. In addition, many labs perform their own genotyping of the animal subjects while others rely on the animal care facility to perform it centrally. Most labs want to track the zygosity information of the animals. Those labs that perform their own genotyping need to keep track of additional information such as the breeding pairs, litters, weaning, caging, and genotyping tests.

## Precursor projects and interviews
Over the past few years, several labs have developed DataJoint-based pipelines for animal management. Our team collaborated with several of them during their projects. Additionally, we interviewed these teams to understand their experiment workflow, associated tools, and interfaces.
These teams include:

Team / Institution / Pipeline repository
+ International Brain Laboratory https://github.com/int-brain-lab/IBL-pipeline
+ BrainCoGs (Princeton Neuroscience Institute) https://github.com/BrainCOGS/U19-pipeline_python; https://github.com/BrainCOGS/U19-pipeline-matlab
+ MoC3 (Columbia Zuckerman Institute)
>+ Costa Lab (private repository)
>+ Hillman Lab: https://github.com/ZuckermanBrain/datajoint-hillman

## Development and validation
Through our interviews and direct collaboration with the precursor projects, we identified the common motifs in the animal subject schemas to create the Animal Management Element. This element works for diverse downstream pipelines and is always used in combination with other elements for specific experiments. As such it is validated jointly with the processing elements such as the Array Ephys Element and Calcium Imaging Element.

There are two modules in `element-animal`:
+ subject: contains the basic information of subject, including Strain, Line, Subject, Zygosity, and SubjectDeath information
+ genotyping: this module is designed for labs that keep track of colony management and genotyping results, containing information of breeding, weaning, housing, and genotyping.

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
