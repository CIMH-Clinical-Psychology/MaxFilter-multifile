# MaxFilter-multifile
Script to filter several FIFF files from MEGIN TRIUX MEG machines sequentially with a GUI.

MaxFilter™ can only filter one FIFF file at a time. That is annoying if you have recordings with several sessions. This simple Python script offers a GUI solution (using [easygui](https://github.com/robertlugg/easygui)) to filter as many FIFF files as you want, given that they all need the same parameters.

You can select between 
- SSS and tSSS
- Movement compensation or none
- Head position transformation to initial, default or from anoter FIFF file
- Bad channel detection ([not recommended for tSSS](https://imaging.mrc-cbu.cam.ac.uk/meg/maxbugs) artefacts such as braces)
- Optionally it can move the files after filtering to a specific location (customized to our setup, you would need to change the last lines of the script.)


#### requirements:**
`pip install easygui`

#### Screenshots
![image](https://github.com/CIMH-Clinical-Psychology/MaxFilter-multifile/assets/14980558/a62ebf26-f822-40bf-9937-6bf43fd18d78)

![image](https://github.com/CIMH-Clinical-Psychology/MaxFilter-multifile/assets/14980558/967d3a5f-b4e4-42f9-b2d9-229e54a7cbca)

![image](https://github.com/CIMH-Clinical-Psychology/MaxFilter-multifile/assets/14980558/dbd64a44-851a-4cde-b700-8b69aa40a4e2)
