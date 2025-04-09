# UAE_Population

- source: https://admin.bayanat.ae/Dataset/DownloadDatasetResource?fileId=26585eaf-9a9c-486d-b773-fc51ef0204c9&resourceID=11243, 

- how to download data: Download script (uae_download.py).
    To download the data, you'll need to use the provided download script, download_script/uae_download.py. This script will download a file to be processed. The script also requires a configuration file (config.ini) to function correctly.

- type of place: Country.

- statvars: Demographics

- years: 1975 to 2005.


### How to run:

`python3 stat_var_processor.py --existing_statvar_mcf=stat_vars.mcf --input_data='/data/statvar_imports/uae_bayanat/uae_population/input/uae_populationbyemiratesnationalityandgender.xlsx' --pv_map='data/statvar_imports/uae_bayanat/uae_population/uae_population_pvmap.csv' --places_resolved_csv='data/statvar_imports/uae_bayanat/uae_population/uae_population_places_resolved_csv.csv' --config='data/statvar_imports/uae_bayanat/uae_population/uae_population_metadata.csv' --output_path=data/statvar_imports/uae_bayanat/uae_population/output/uae_population_output``

#### Example
#### Download : 
`python3 uae_download.py`

'After running the script python3 uae_download.py, it successfully downloaded the source file named uae_populationbyemiratesnationalityandgender.xlsx .'

#### Processing
`python3 stat_var_processor.py --existing_statvar_mcf=stat_vars.mcf --input_data='/data/statvar_imports/uae_bayanat/uae_population/input/uae_populationbyemiratesnationalityandgender.xlsx' --pv_map='data/statvar_imports/uae_bayanat/uae_population/uae_population_pvmap.csv' --places_resolved_csv='data/statvar_imports/uae_bayanat/uae_population/uae_population_places_resolved_csv.csv' --config='data/statvar_imports/uae_bayanat/uae_population/uae_population_metadata.csv' --output_path=data/statvar_imports/uae_bayanat/uae_population/output/uae_population_output`


