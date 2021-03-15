# EMDNA_subset
The script is used to extract a subset dataset from the EMDNA dataset.  

For running the script on Compute Canada Graham, the steps are:  
(1) Install Python packages if this has not been done before  
Reference: https://docs.computecanada.ca/wiki/Python#Installing_packages

First, creating and using a virtual environment:  
[name@server ~]$ virtualenv --no-download ~/ENV  

Then, install packages:  
[name@server ~]$ module load python/3.7.4  
[name@server ~]$ source ~/ENV/bin/activate  
[name@server ~]$ pip install netCDF4 --no-index  
[name@server ~]$ pip install pandas --no-index  
[name@server ~]$ pip install xarray --no-index  

(2) Change the parameters and paths in EMDNA_subsetting.py  
Note: The path of input files should be useful for Graham users  

(3) Submit jobs  
Command: sbatch graham_EMDNAsubset.sh  
Note: The "time" and "mem" in graham_EMDNAsubset.sh may need to be changed according to target data amounts.  



