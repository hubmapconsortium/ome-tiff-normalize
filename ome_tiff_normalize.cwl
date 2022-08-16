cwlVersion: v1.1
class: CommandLineTool
label: OME-TIFF metadata normalization via bftools
hints:
  DockerRequirement:
    dockerPull: hubmap/ome-tiff-normalize:latest
baseCommand: /opt/bftools_wrapper.py

inputs:
  data_dir:
    type: Directory
    inputBinding:
      position: 0
outputs:
  output_dir:
    type: Directory[]
    outputBinding:
      glob: ./*
