# Tell Vectric you want to create some custom post-processors
 
* Open a project.
* Machine menu > Post-Processor Management.
* For each LinuxCNC pre-processor, click the edit button on the right, select customize.
* This will save original files into the following dir for editing:
  `C:\ProgramData\Vectric\VCarve Pro - Makerspace Edition\V11.0\My_PostP`

# Install FCCH's custom post-processors

* Rename the files in `My_PostP` to match the naming in the files archived in git; add prefix "FCCH " to the filename.
* Copy the git versions over the renamed files.
* Restart Vectric.

# Create a machine definition for the FCCH machin:

* Machine menu > Machine Configuration.
* Click "Create new machine".
* Name: FCCH 48x48.
* Manufacturer: Custom.
* Model: FCCH 48x48.
* Controller: G-Code.
* Width: 48.
* Height: 48.
* Unit: Inches.
* Associated Post-Processor: Remove any defaults, add the 2 FCCH post-processors.
* Double-click the FCCH inches post-processor to set is as default
