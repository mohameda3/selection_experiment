# Selection Experiment

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Usage](#usage)



<!-- ABOUT THE PROJECT -->
## About The Project

This repositiory contains the extended code used for my **CSC428 A2** experiment.

* `app.js` is an extended javascript file from the starter code
* `code5.html` is an extended html file from the starter code
* `participant_[1-3].csv` is the latin-square (var1) and randomized (var2, var3) set of conditions.
* `participant_0.csv` is smaller set of conditions used for testing.


<!-- USAGE EXAMPLES -->
## Usage

Open the `code5.html`
```
cd ~/selection_experiment
open ./code5.html
```

Enter the participant number (0-3) . The code will then fetch the associated csv file from `http://raw.githubusercontent.com` and load the set of conditions
from the downloaded csv.
