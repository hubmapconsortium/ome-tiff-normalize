cwlVersion: v1.1
class: CommandLineTool
label: OME-TIFF metadata normalization via bftools
hints:
  DockerRequirement:
    dockerPull: hubmap/ome-tiff-normalize:1.1
baseCommand: /opt/bftools_wrapper.py

inputs:
  data_dir:
    type: Directory
    inputBinding:
      position: 0
  output_path_prefix:
    type: string?
    inputBinding:
      position: 1
      prefix: "--output-path-prefix"
outputs:
  output_dir:
    type: Directory[]
    outputBinding:
      glob: ./*
