# US EIA Open Data Import

## About the Dataset

### Download URL

Each dataset available as a Zip-file of JSONL content. See [here](https://www.eia.gov/opendata/bulkfiles.php) for more details.

### Data Exploration

To ease analysis of the datasets, see [`generate_jsonl_for_bq.py`](generate_jsonl_for_bq.py) for instructions to convert and import the data into BigQuery.

### License

This dataset is available for public use, license is available at https://www.eia.gov/about/copyrights_reuse.php


- Run the [processor](process/README.md)

### Downloading and Processing Data


    If you want to perform "only download", run the below command:

        python3 process.py --dataset=INTL --mode=download
        python3 process.py --dataset=ELEC --mode=download
        python3 process.py --dataset=PET --mode=download
        python3 process.py --dataset=NG --mode=download
        python3 process.py --dataset=SEDS --mode=download
        python3 process.py --dataset=NUC_STATUS --mode=download
        python3 process.py --dataset=TOTAL --mode=download



   If you want to perform "only process", run the below command:

   Running this command generates input_fles and csv, mcf, tmcf, svg.mcf files.

        python3 process.py --dataset=INTL --mode=process
        python3 process.py --dataset=ELEC --mode=process
        python3 process.py --dataset=PET --mode=process
        python3 process.py --dataset=NG --mode=process
        python3 process.py --dataset=SEDS --mode=process
        python3 process.py --dataset=NUC_STATUS --mode=process
        python3 process.py --dataset=TOTAL --mode=process
        
    To Download and process the data together, run the below command:
    ```bash
    python3 process.py --dataset=TOTAL
    python3 process.py --dataset=INTL
    python3 process.py --dataset=ELEC
    python3 process.py --dataset=NG
    python3 process.py --dataset=PET
    python3 process.py --dataset=SEDS
    python3 process.py --dataset=NUC_STATUS

    ```