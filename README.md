
# BRCA QC

## What does this script do?
Aggregates the QC metrics from BRCA Clinical Pool reports. Displays how many exons have failed (Min Depth < 30) in BRCA1 or BRCA2 to attempt to identify failure patterns.

## What are typical use cases for this script?
This is run as an ad-hoc QC visualisation for the Cancer Team to aid with troubleshooting of their sequencing. 

## What data are required for this script to run?
This app requires the .xls reports for BRCA samples (C01XXXXb).

## What does this script output?
It outputs one spreadsheet with sample names as column names and BRCA1/2 exons rows displaye 0/1 (Pass/Fail) and a Total column displaying the amount of times an exon has failed across samples.


## How to run this script?
```
usage: python brca_exon_qc.py [-h] [-f F] run

Quick QC for BRCA samples
positional arguments:
run         Clinical pool run name i.e. CP0379A
optional arguments:
-h, --help  show this help message and exit
-f F        runfolder path if different from /mnt/storage/data/NGS/CP/
```


## Notes
* Jon asked if we can run it for clinical pool runs containing C01 samples, if there’s A+B, run it on A and B separately. I have made a folder in /mnt/storage/data/NHS/CP/reports where I have saved the reports to run this. 
* Sample naming - note from Jon:  I think best thing to do is to only include the ones that end with a b or bW in your script, and just ignore everything else. If they don’t have a letter or they have a weird letter its normally because they are NGS gapfills.