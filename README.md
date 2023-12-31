# MaxFilter-multifile
Script to filter several FIFF files from MEGIN TRIUX MEG machines sequentially with a GUI.

MaxFilter™ can only filter one FIFF file at a time. That is annoying if you have recordings with several sessions. This simple Python script offers a GUI solution (using [easygui](https://github.com/robertlugg/easygui)) to filter as many FIFF files as you want, given that they all need the same parameters.

You can select between 
- `SSS` or `tSSS`
- Movement compensation or none
- Head position transformation to `initial`, `default` or from another FIFF file
- Bad channel detection ([not recommended for tSSS](https://imaging.mrc-cbu.cam.ac.uk/meg/maxbugs) artefacts such as braces)
- Optionally it can move the files after filtering to a specific location (customized to our setup, you would need to change the last lines of the script.)


### Requirements:**
- `pip install easygui`
- Any Python>=3.5 should work.


Then simply run `python maxfilter_multifile.py`

You might need to adapt some paths, i.e. the path to the maxfilter binary file and your data storage.

### Screenshots
![image](https://github.com/CIMH-Clinical-Psychology/MaxFilter-multifile/assets/14980558/a62ebf26-f822-40bf-9937-6bf43fd18d78)

![image](https://github.com/CIMH-Clinical-Psychology/MaxFilter-multifile/assets/14980558/967d3a5f-b4e4-42f9-b2d9-229e54a7cbca)

![image](https://github.com/CIMH-Clinical-Psychology/MaxFilter-multifile/assets/14980558/50a943d1-97e2-4e7c-aba6-21085d1cc41f)

![image](https://github.com/CIMH-Clinical-Psychology/MaxFilter-multifile/assets/14980558/e8f61e73-a4d1-462d-b455-ef5b0194ea67)

![image](https://github.com/CIMH-Clinical-Psychology/MaxFilter-multifile/assets/14980558/48d93d41-9e86-41e4-89b2-e3983e70a2c4)

![image](https://github.com/CIMH-Clinical-Psychology/MaxFilter-multifile/assets/14980558/2452d47f-c084-4e37-95db-d4e57ee404f7)

![image](https://github.com/CIMH-Clinical-Psychology/MaxFilter-multifile/assets/14980558/dbd64a44-851a-4cde-b700-8b69aa40a4e2)
