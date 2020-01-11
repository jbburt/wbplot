# README File for wbplot
Automated plotting of neuroimaging maps from Python using [Connectome Workbench](https://www.humanconnectome.org/software/connectome-workbench).

This package is intended for users who want to generate images
which illustrate scalar data on a brain surface, from within their Python scripts. 

Installation
============
---

### Step 1. Make sure you have Connectome Workbench installed.
* If running `wb_view` from a terminal yields 'command not found', see  <https://www.humanconnectome.org/software/connectome-workbench/>

### Step 2. Install `wbplot` and dependencies.
* Clone the repository and install manually: `git clone https://github.com/jbburt/wbplot.git`
* Or just use pip: `pip install wbplot`

Usage
=====
---
Assuming `x` is a NumPy array containing scalar values mapped onto each of the
360 parcels in the [Human Connectome Project](http://www.humanconnectomeproject.org/)'s [MMP1.0](https://www.nature.com/articles/nature18933) parcellation:
```
from wbplot import pscalar
pscalar("/path/to/image.png", x)
```

Assuming `y` is a NumPy array containing dense scalar values mapped onto the 59412
surface vertices in a standard bilateral 32k surface mesh:
```
from wbplot import dscalar
dscalar("/path/to/image.png", y)
```

Notes
=====
---
- `wbplot` currently only supports cortical data. Parcellated data must also be in the
HCP MMP1.0 parcellation. Dense data must be
registered to a standard 32k surface mesh. 
- Down the line I'd be open to adding subcortical
support and other functionality if anyone ever actually uses this package.
- More detailed explanations of the functionality can be found in the scripts in the `examples` directory. 


Change Log
==========
---

* 1.0 Initial release.

=======
[Joshua B. Burt]: http://joshuabburt.com
