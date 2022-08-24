# EchoNormalisation
Generation of Echo ready files for normalisation procedure. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required packages. 

```bash
pip install numpy 
```

```bash
pip install pandas 
```

```bash
pip install PySimpleGUI 
```

## Usage

Input: 
.csv file that contains list of wells and corresponding concentrations in ng/uL. 

Output:
- 2 Echo ready files to transfer buffer and samples 
- 1 report containing the list of wells that failed to be processed (if any) and the reason for failure. 

To run: 

```bash
python3 Echo_normalisation_script.py 
```

A GUI will guide you through the process. 
Test files are available in the repository. 

## License
[London Biofoundry](https://www.londonbiofoundry.org/)
