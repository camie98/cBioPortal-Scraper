from selenium import webdriver
import requests
from time import sleep
import json
from os import listdir

get_studies_data = "http://www.cbioportal.org/webservice.do?cmd=getCancerStudies"
get_gene_data = "http://www.cbioportal.org/webservice.do?cmd=&cancer_study_id=%study%"
get_data = "http://www.cbioportal.org/webservice.do?cmd=getMutationData&cancer_study_id=%study%&genetic_profile_id=%profile%&gene_list=%genes%"

def get_studies():
    req = requests.get(get_studies_data)
    raw_data = req.text
    raw_data = raw_data.split("\n")
    studies = []
    for data in raw_data:
        data = data.split(" ")[0].split("\t")[0].split("	")[0]
        if data != "cancer_study_id":
            studies.append(data)
    return studies

def get_genes(study):
    req = requests.get("http://www.cbioportal.org/mutations.json?cmd=get_smg&mutation_profile="+study+"_mutations")
    data = json.loads(req.text)
    genes = []
    for item in data:
        gen = str(item)
        gen = gen.split("'")[3]
        genes.append(gen)
    return genes
    
    
def get_final_data(study,genes):
    url = get_data.replace("%study%",study)
    url = url.replace("%profile%",study+"_mutations")
    url = url.replace("%genes%"," ".join(genes))
    req = requests.get(url)
    print "[*] Got all study data for "+study
    reply = req.text
    if "Request-URI Too Large" in reply:
        aurl = get_data.replace("%study%",study)
        aurl = aurl.replace("%profile%",study+"_mutations")
        G1,G2 = split_list(genes)
        aurl1 = aurl.replace("%genes%"," ".join(G1))
        aurl2 = aurl.replace("%genes%"," ".join(G2))
        req = requests.get(aurl1)
        G1text = req.text
        req = requests.get(aurl2)
        G2text = req.text
        print "[-] Data too large, split"
        reply = G1text+G2text
    return reply

def save_data(study,data):
    f = open("Data/"+study+".txt","w")
    f.write(data)
    f.close()
    print "[*] Data saved in Data/"+study+".txt"

def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

if __name__ == "__main__":
    print "##########################################"
    print "#                                        #"
    print "#        cBioPortal Data Downloader      #"
    print "#                                        #"
    print "#########################################"
    studies = get_studies()
    files = listdir("Data")
    for study in studies:
        if study+".txt" in files:
            pass
        else:
            genes = get_genes(study)
            data = get_final_data(study,genes)
            save_data(study,data)
    
        

