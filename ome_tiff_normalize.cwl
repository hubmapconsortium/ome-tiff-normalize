cwlVersion: v1.1
class: CommandLineTool
label: OME-TIFF metadata normalization via bftools
requirements:
  DockerRequirement:
    dockerPull: hubmap/ome-tiff-normalize:1.2
  InlineJavascriptRequirement: {}
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
      glob: manifest.json
      loadContents: True
      outputEval: $(eval(self[0].contents))
