# Import required modules
import requests
import argparse
import re
from operator import add


# Defining URL's for mutation and copy number alterations
cBioAPI_muturl = (
    "https://www.cbioportal.org/webservice.do?cmd=getProfileData&"
    "genetic_profile_id=gbm_tcga_mutations&id_type=gene_symbol&"
    "gene_list={gene_name}&case_set_id=gbm_tcga_cnaseq"
)

cBioAPI_cnurl = (
    "https://www.cbioportal.org/webservice.do?cmd=getProfileData&"
    "genetic_profile_id=gbm_tcga_gistic&id_type=gene_symbol&gene_list="
    "{gene_name}&case_set_id=gbm_tcga_cnaseq"
)


# Defining required lists
mutation_result = []
copynumber_result = []
percent_mutations = []
percent_cnalterations = []


# To parse mutation data response
def count_mutations(mutation_res):
    '''
        Usage:
        Function to parse the GET request response and
        calculate number of mutations in the given genes.
        The GET request response is passed to this function.
    '''
    for i in range(len(mutation_res)):
        # To calculate number of NaN's
        num_nan = mutation_res[i].count("NaN")
        # To calculate number of samples
        num_samples = len(re.findall("TCGA", mutation_res[i]))
        # To calculate number of zero's
        mutList = mutation_res[i].split('\t')
        num_zero = mutList.count(0)
        # To calculate percent mutations
        num_nonmutations = num_nan + num_zero
        num_mutations = num_samples - num_nonmutations
        pmut = (num_mutations/num_samples)*100
        percent_mutations.append(pmut)
    return(percent_mutations)


# To parse copy number alteration data response
def count_cnalterations(copynumber_res):
    '''
        Usage:
        Function to parse the GET request response and
        calculate copy number alterations in the given genes.
        The GET request response is passed to this function.
    '''
    for j in copynumber_res:
        # To calculate number of Na's
        num_na = j.count("NA")
        # To calculate number of samples
        num_samples = len(re.findall("TCGA", j))
        # To calculate number of 0,1,-1
        cpList = j.split('\t')
        num_zero = cpList.count('0')
        num_one = cpList.count('1')
        num_minusone = cpList.count('-1')
        # To calculate percent mutations
        num_nonalter = num_na + num_zero + num_one + num_minusone
        num_alter = num_samples - num_nonalter
        palt = (num_alter/num_samples)*100
        percent_cnalterations.append(palt)
    return(percent_cnalterations)


# To get mutation data
def get_mutation(genes):
    '''
        Usage:
        Function to make GET request to cBioPortal for mutation data.
        User specified gene is the input to this function.
    '''
    for gene in genes:
        mutationURL = cBioAPI_muturl.format(gene_name=gene)
        # To do GET request for mutation data
        res_mut = requests.get(mutationURL)
        res_mut_text = res_mut.text
        mutation_result.append(res_mut_text)
    return(mutation_result)


# To get copy number data
def get_copynumber(genes):
    '''
        Usage:
        Function to make GET request to cBioPortal for copy
        number data.
        User specified gene is the input to this function.
    '''
    for gene in genes:
        copynumberURL = cBioAPI_cnurl.format(gene_name=gene)
        # To do GET request for copy number alteration data
        res_cn = requests.get(copynumberURL)
        res_cn_text = res_cn.text
        copynumber_result.append(res_cn_text)
    return(copynumber_result)


# Check if gene name input is valid
def validate_genes(genes):
    for gene in genes:
        temp = open("genenames.txt","r").read()
        if gene in temp:
            return(1)
        else:
            return(-1)

# Main function
def __main__():
    '''
        Usage:
        Main function that takes user inputs for gene symbols
        and calculates and displays alteration percent for
        mutation and copy number of all cases.
    '''
    # Use argparse to take command line arguments
    parser = argparse.ArgumentParser(description='To work with cBioPortal API')
    parser.add_argument('gene', nargs='+', help='Enter 1 or upto 3 genes!')
    args = parser.parse_args()
    # Check if gene input is valid
    validator = validate_genes(args.gene)
    if validator == 1:
        # Check if number of gene inputs exceeds 3
        if(len(args.gene) > 3):
            print("Please enter upto three genes only!\n")
        else:
            # To perform API calls and parse the response
            mutation_res = get_mutation(args.gene)
            copynumber_res = get_copynumber(args.gene)
            mutated_percent = count_mutations(mutation_res)
            cnaltered_percent = count_cnalterations(copynumber_res)
            # To calculate total altered percent
            total_altered = list(map(add, mutated_percent, cnaltered_percent))
            arg_list = [item for item in args.gene]
            # Create simple dictionary to hold gene name and total alter %
            gene_total_percent = dict(zip(arg_list, total_altered))
            # When user inputs 1 gene, display results
            if(len(args.gene) == 1):
                print(args.gene[0], "is mutated in", round(mutated_percent[0]),
                      "% all cases.\n", args.gene[0], "is copy number altered in",
                      round(cnaltered_percent[0]), "% of all cases.",
                      "\nTotal % of cases where", args.gene[0],
                      "is altered by either mutation or copy number alteration:",
                      round(total_altered[0]), "% of all cases.")
            # When user inputs more than 1 gene, display results
            gene_set_total = sum(gene_total_percent.values())
            if(len(args.gene) > 1):
                for key, value in gene_total_percent.items():
                    print(key, "is altered in", round(value), "% of all cases")
                print("The gene set is altered in", round(gene_set_total),
                      "% of all cases.")
    else:
        print("Sorry please enter a valid gene symbol!")





if __name__ == "__main__":
    main()
