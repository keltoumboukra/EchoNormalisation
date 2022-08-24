import numpy as np
import pandas as pd
import csv 
import PySimpleGUI as sg

# Input variables for GUI
F_vol = 100
F_conc = 1

input_file_folder = "/Users/keltoumboukra/Documents/EchoNormalisationGenerator/csv_inputs/"
input_file_name = "input_example_tests.csv"

output_files_folder = "/Users/keltoumboukra/Documents/EchoNormalisationGenerator/csv_outputs/"
output_buffer_file_name = "echo_file_buffer.csv"
output_sample_file_name = "echo_file_sample.csv"
output_report_file_name = "normalisation_report.csv"

# Simple GUI
sg.theme('LightBrown9')

layout = [
    [sg.Text('Please enter the desired parameters')],
    [sg.Text('Final volume (uL)', size =(25, 1)), sg.InputText()],
    [sg.Text('Final concentration (ng/uL)', size =(25, 1)), sg.InputText()],
    [sg.Text('Input file folder', size =(25, 1)), sg.InputText("/Users/keltoumboukra/Documents/EchoNormalisationGenerator/csv_inputs/")],
    [sg.Text('Input file name', size =(25, 1)), sg.InputText("input_example.csv")],
    [sg.Text('Destination folder', size =(25, 1)), sg.InputText("/Users/keltoumboukra/Documents/EchoNormalisationGenerator/csv_outputs/")],
    [sg.Text('Buffer Echo file name', size =(25, 1)), sg.InputText("echo_file_buffer.csv")],
    [sg.Text('Samples Echo file name', size =(25, 1)), sg.InputText("echo_file_sample.csv")],
    [sg.Submit(), sg.Cancel()]
]

window = sg.Window('Echo File Generator For Normalisation', layout)
event, values = window.read()
window.maximize()
window.close()

F_vol = float(values[0])
F_conc = float(values[1])
input_file_folder = values[2]
input_file_name = values[3]
output_files_folder = values[4]
output_buffer_file_name = values[5]
output_sample_file_name = values[6]

#dataframes
buffer_output_file_df = pd.DataFrame(columns=['Source Well','Destination Well','Transfer Volume'])
sample_output_file_df = pd.DataFrame(columns=['Source Well','Destination Well','Transfer Volume'])
output_report_file_df = pd.DataFrame(columns=['Source Well','Pass?','Comment'])
input_file_df = pd.read_csv(input_file_folder + input_file_name)

#normalisation function
def _normalise(input_concentration, final_concentration, final_volume):
    sample_volume = (final_concentration*final_volume)/input_concentration
    buffer_volume = final_volume - sample_volume
    return sample_volume, buffer_volume

# go through input file and calculate normalisation parameters 
for row in input_file_df.itertuples():
    
    Index = row [0]
    SourceWell = row[1]
    Concentration = row[2]
    
    try:
        _Sample_volume, _Buffer_volume = _normalise(Concentration, F_conc, F_vol)
        
        
        # Convert to nL for Echo 
        _Sample_volume = _Sample_volume*1000
        _Buffer_volume = _Buffer_volume*1000
        
        _Sample_volume = int(_Sample_volume)
        _Buffer_volume = int(_Buffer_volume)
        
        if _Sample_volume >= 25e-3 and _Buffer_volume > 0:
            Pass = "Yes"
            Comment = ""
            
        elif _Sample_volume < 25e-3: # 25 nL is lower volume Echo can pipette 
        
            Pass = "No"
            Comment = "Sample volume required is too low ({} uL). Lower input concentration or increase final dilution volume".format(_Sample_volume)
            
            _Sample_volume = 0
            _Buffer_volume = 0

        elif _Buffer_volume < 0: 
        
            Pass = "No"
            Comment = "Buffer volume required is negative ({} uL). Increase input concentration or decrease final dilution volume".format(_Buffer_volume)
            
            _Sample_volume = 0
            _Buffer_volume = 0
            
    except ZeroDivisionError:
        _Sample_volume = 0
        _Buffer_volume = 0  
        
        Pass = "No"
        Comment = " 0uL of samples available for normalisation according to input file"
    
    buffer_output_file_df = buffer_output_file_df.append({'Source Well': SourceWell, 'Destination Well': SourceWell, 'Transfer Volume': _Buffer_volume}, ignore_index=True)
    sample_output_file_df = sample_output_file_df.append({'Source Well': SourceWell, 'Destination Well': SourceWell, 'Transfer Volume': _Sample_volume}, ignore_index=True)
    output_report_file_df = output_report_file_df.append({'SourceWell': SourceWell, 'Pass?': Pass, 'Comment': Comment}, ignore_index=True)

# drop rows with volume to transfer = 0 to make Echo ready file
buffer_output_file_df = buffer_output_file_df[buffer_output_file_df['Transfer Volume'] != 0]
sample_output_file_df = sample_output_file_df[sample_output_file_df['Transfer Volume'] != 0]

# transform dataframe into csv 
buffer_output_file_df.to_csv(output_files_folder + output_buffer_file_name, index=False)
sample_output_file_df.to_csv(output_files_folder + output_sample_file_name, index=False)
output_report_file_df.to_csv(output_files_folder + output_report_file_name, index=False)

# simple GUI to end processing
layout = [[sg.Text("Processing completed. FInd your Echo files and report in the output folder")], [sg.Button("OK")]]
window = sg.Window("Echo File Generator For Normalisation", layout)

while True:
    event, values = window.read()
    if event == "OK" or event == sg.WIN_CLOSED:
        break
window.close()