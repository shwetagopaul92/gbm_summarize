# gbm_summarize

A Python command line tool to work with cancer genomic data from the cBio Cancer Genomics Portal, which currently supports a REST-based web API. 
The tool will help retrieve mutation and copy number alteration data for a 1 gene or upto 3 genes (that a user inputs) in Glioblastoma patients.  

Installation
================
  
Once the folder is unzipped, follow the below procedure to install it on your local machine. 

On the command prompt: 
  
> cd gbm_summarize/
> pip3 install -e . 

This would install the tool

Tutorial / Working with gbm_summarize : 
========================================

> gbm_summarize -h 

> gbm_summarize TP53 

This would show summary statistics for mutation, copy number alterations and a total % of cases where TP53 is altered by mutation or copy number. 

> gbm_summarize TP53 MDM2 MDM4 

This would show summary statistics for each gene

> gbm_summarize TP53 MDM2 MDM4 MDM2 

This would throw an error, allowing only upto 3 gene inputs for now. 


Future enhancements : 
======================

- To allow checking of valid gene symbol inputs.
- To optimize the program by reducing number of API calls.
