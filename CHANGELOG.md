# Changelog

Observes [Semantic Versioning](https://semver.org/spec/v2.0.0.html) standard and
[Keep a Changelog](https://keepachangelog.com/en/1.0.0/) convention.

## [0.2.0] - 2023-09-28

+ Add `Species` part table to `subject.py` 

## [0.1.8] - 2023-06-20

+ Update - GitHub Actions workflows
+ Fix - Remove Google Analytics key

## [0.1.7] - 2023-05-11

+ Fix - `.ipynb` dark mode output for all notebooks.
+ Update - CHANGELOG markdown from "-" to "+" for consistency with other
  Elements.
+ Fix - Remove `GOOGLE_ANALYTICS_KEY` from `u24_element_release_call.yml`.

## [0.1.6] - 2023-04-28

+ Fix - `.ipynb` output in tutorials is not visible in dark mode.

## [0.1.5] - 2023-03-02

+ Add - `surgery` schema
+ Add - mkdocs documentation
+ Update - string typing for NWB export of Species

## [0.1.4] - 2022-08-30

+ Add - "subject_nickname" into Subject table
+ Update - rework "SubjectCull" table

## [0.1.3] - 2022-07-06

+ Update - Diagram links for PyPI README

## [0.1.2] - 2022-06-27

+ Add - Code of Conduct
+ Update - pull subject from parent directory in nwb export
+ Update - for genotyping.BreedingPair part tables, projection from Subject
  + genotyping.BreedingPair.Mother, change attribute to 'mother'
  + genotyping.BreedingPair.Father, change attribute to 'father'

## [0.1.1] - 2022-05-10

+ Add - NWB export
+ Update - Shorten subject primary key to varchar(8)
+ Add - Adopt black formatting into code base

## [0.1.0b0] - 2021-05-07

+ Update - First beta release

## [0.1.0a1] - 2021-05-03

+ Add - GitHub Action release process
+ Add - `subject` schema
+ Add - `genotyping` schema

[0.2.0]: https://github.com/datajoint/element-animal/releases/tag/0.2.0
[0.1.8]: https://github.com/datajoint/element-animal/releases/tag/0.1.8
[0.1.7]: https://github.com/datajoint/element-animal/releases/tag/0.1.7
[0.1.6]: https://github.com/datajoint/element-animal/releases/tag/0.1.6
[0.1.5]: https://github.com/datajoint/element-animal/releases/tag/0.1.5
[0.1.4]: https://github.com/datajoint/element-animal/releases/tag/0.1.4
[0.1.3]: https://github.com/datajoint/element-animal/releases/tag/0.1.3
[0.1.2]: https://github.com/datajoint/element-animal/releases/tag/0.1.2
[0.1.1]: https://github.com/datajoint/element-animal/releases/tag/0.1.1
[0.1.0b0]: https://github.com/datajoint/element-animal/releases/tag/0.1.0b0
[0.1.0a1]: https://github.com/datajoint/element-animal/releases/tag/0.1.0a1
