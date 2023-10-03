# Concepts

## Usage of animal subjects in neuroscience

Many data pipelines in neuroscience retain information about the experimental subjects
(e.g., date of birth, sex). For animal models, this can also include owner, cage and
sacrificing information. Many researchers also retain genotyping information (e.g.,
line, zygosity). Labs that perform their own genotyping need to keep track of even more
information, such as breeding pairs, litters, and genotyping tests. Element Animal can
help researchers organize all this information in connection with a broader experimental
pipeline.

## Key Partnerships

Over the past few years, several labs have developed DataJoint-based pipelines for
animal management. Our team collaborated with several of them during their projects.
Additionally, we interviewed these teams to understand their experiment workflow,
associated tools, and interfaces. These teams include:

- [International Brain Laboratory](https://github.com/int-brain-lab/IBL-pipeline)
- BrainCoGs (Princeton Neuroscience Institute)
  ([Python](https://github.com/BrainCOGS/U19-pipeline_python) / [MATLAB](https://github.com/BrainCOGS/U19-pipeline-matlab))
- [MoC3 (Columbia Zuckerman Institute) + Costa Lab (private repository) + Hillman Lab](https://github.com/ZuckermanBrain/datajoint-hillman)
- [Sabatini Lab](https://github.com/bernardosabatinilab/sabatini-datajoint-pipeline)

Through our interviews and direct collaboration with the precursor projects, we
identified the common motifs in the animal subject schemas to create the Animal
Management Element. This element works for diverse downstream pipelines and is always
used in combination with other elements for specific experiments. As such it is
validated jointly with the processing elements such as the Array Ephys Element and
Calcium Imaging Element.

## Element architecture

There are three modules in `element-animal`:

- subject: contains the basic information of subject, including Strain, Line, Subject,
  Zygosity, and SubjectDeath information

- genotyping: this module is designed for labs that keep track of colony management and
  genotyping results, containing information of breeding, weaning, housing, and
  genotyping.

- surgery: this module maintains records of subject implantations including, for
  example, fiberphotometry.

### Subject Diagram

![Subject schema diagram](https://raw.githubusercontent.com/datajoint/element-animal/main/images/subject_diagram.svg)

### Genotyping Diagram

![Genotyping schema diagram](https://raw.githubusercontent.com/datajoint/element-animal/main/images/genotyping_diagram.svg)

### Surgery Diagram

![Surgery schema diagram](https://raw.githubusercontent.com/datajoint/element-animal/main/images/surgery_diagram.svg)

### Injection Diagram

![Injection schema diagram](https://raw.githubusercontent.com/datajoint/element-animal/main/images/injection_diagram.svg)

## `subject` schema ([API docs](https://datajoint.com/docs/elements/element-animal/api/element_animal/subject))

- Although not required, most choose to connect the `Session` table to a `Subject` table.

| Table        | Description                                 |
| ------------ | ------------------------------------------- |
| Strain       | Genetic strain of an animal. (e.g. C57Bl/6) |
| Allele       | Store allele information                    |
| Line         | Genetic line                                |
| Subject      | Animal subject information                  |
| SubjectDeath | Subject death information                   |
| SubjectCull  | Subject culling information                 |
| Zygosity     | Information about zygosity of a subject     |

### `genotyping` schema ([API docs](https://datajoint.com/docs/elements/element-animal/api/element_animal/genotyping))

| Table          | Description                                                         |
| -------------- | ------------------------------------------------------------------- |
| Sequence       | Gene sequence information                                           |
| AlleleSequence | Allele sequence information                                         |
| BreedingPair   | Information about male-female pair used for breeding                |
| Litter         | Information about litter (group of animals born to a breeding pair) |
| Weaning        | Information about weaning (maternal separation)                     |
| SubjectLitter  | Subject and its litter                                              |
| Cage           | Cage information                                                    |
| SubjectCaging  | Information about subject and its cage.                             |
| GenotypeTest   | Information about genotype test                                     |

### `surgery` schema ([API docs](https://datajoint.com/docs/elements/element-animal/api/element_animal/surgery))

| Table               | Description                                                    |
| ------------------- | -------------------------------------------------------------- |
| CoordinateReference | Coordinate reference system                                    |
| BrainRegion         | Brain region of a given surgery                                |
| Hemisphere          | Brain region hemisphere                                        |
| ImplantationType    | Type of implantation                                           |
| Implantation        | Implantation of a device                                       |

### `injection` schema ([API docs](https://datajoint.com/docs/elements/element-animal/api/element_animal/injection))

| Table               | Description                                                    |
| ------------------- | -------------------------------------------------------------- |
| VirusSerotype       | Virus serotype                                                 |
| InjectionProtocol   | Injection device protocol                                      |
| VirusName           | Full virus name                                                |
| Injection           | Information about the virus injection                          |
