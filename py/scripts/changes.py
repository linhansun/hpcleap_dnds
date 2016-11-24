# IMPORTS:
import numpy as np 
import pickle
from  itertools import permutations

# FUNCTION DEFS:
def geneticCode(name):

    if name == 'standard':
        gc = {	'AAA':'K', 'AAC':'N', 'AAG':'K', 'AAT':'N', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T', 'AGA':'R', 'AGC':'S', 'AGG':'R', \
        		'AGT':'S','ATA':'I','ATC':'I','ATG':'M','ATT':'I','CAA':'Q','CAC':'H','CAG':'Q','CAT':'H','CCA':'P','CCC':'P','CCG':'P', \
        		'CCT':'P','CGA':'R','CGC':'R','CGG':'R','CGT':'R','CTA':'L','CTC':'L','CTG':'L','CTT':'L','GAA':'E','GAC':'D','GAG':'E', \
        		'GAT':'D','GCA':'A','GCC':'A','GCG':'A','GCT':'A','GGA':'G','GGC':'G','GGG':'G','GGT':'G','GTA':'V','GTC':'V','GTG':'V', \
        		'GTT':'V','TAA':'*','TAC':'Y','TAG':'*','TAT':'Y','TCA':'S','TCC':'S','TCG':'S','TCT':'S','TGA':'*','TGC':'C','TGG':'W', \
        		'TGT':'C','TTA':'L','TTC':'F','TTG':'L','TTT':'F'  }
    return gc

def potential_changes_dict(genetic_code):

    potential_changes = {   'S': {	'AAA':0.0,'AAC':0.0,'AAG':0.0,'AAT':0.0, 'ACA':0.0, 'ACC':0.0, 'ACG':0.0, 'ACT':0.0, 'AGA':0.0, 'AGC':0.0, \
    								'AGG':0.0, 'AGT':0.0, 'ATA':0.0, 'ATC':0.0, 'ATG':0.0, 'ATT':0.0, 'CAA':0.0, 'CAC':0.0, 'CAG':0.0, 'CAT':0.0, \
    								'CCA':0.0,'CCC':0.0,'CCG':0.0,'CCT':0.0,'CGA':0.0,'CGC':0.0,'CGG':0.0,'CGT':0.0,'CTA':0.0,'CTC':0.0,'CTG':0.0, \
    								'CTT':0.0,'GAA':0.0,'GAC':0.0,'GAG':0.0,'GAT':0.0,'GCA':0.0,'GCC':0.0,'GCG':0.0,'GCT':0.0,'GGA':0.0,'GGC':0.0, \
    								'GGG':0.0,'GGT':0.0,'GTA':0.0,'GTC':0.0,'GTG':0.0,'GTT':0.0,'TAA':0.0,'TAC':0.0,'TAG':0.0,'TAT':0.0,'TCA':0.0, \
    								'TCC':0.0,'TCG':0.0,'TCT':0.0,'TGA':0.0,'TGC':0.0,'TGG':0.0,'TGT':0.0,'TTA':0.0,'TTC':0.0,'TTG':0.0,'TTT':0.0},

                            'N': {	'AAA':0.0, 'AAC':0.0, 'AAG':0.0, 'AAT':0.0, 'ACA':0.0, 'ACC':0.0, 'ACG':0.0, 'ACT':0.0, 'AGA':0.0, 'AGC':0.0, 'AGG':0.0, \
                            		'AGT':0.0,'ATA':0.0,'ATC':0.0,'ATG':0.0,'ATT':0.0,'CAA':0.0,'CAC':0.0,'CAG':0.0,'CAT':0.0,'CCA':0.0,'CCC':0.0,'CCG':0.0, \
                            		'CCT':0.0,'CGA':0.0,'CGC':0.0,'CGG':0.0,'CGT':0.0,'CTA':0.0,'CTC':0.0,'CTG':0.0,'CTT':0.0,'GAA':0.0,'GAC':0.0,'GAG':0.0, \
                            		'GAT':0.0,'GCA':0.0,'GCC':0.0,'GCG':0.0,'GCT':0.0,'GGA':0.0,'GGC':0.0,'GGG':0.0,'GGT':0.0,'GTA':0.0,'GTC':0.0,'GTG':0.0, \
                            		'GTT':0.0,'TAA':0.0,'TAC':0.0,'TAG':0.0,'TAT':0.0,'TCA':0.0,'TCC':0.0,'TCG':0.0,'TCT':0.0,'TGA':0.0,'TGC':0.0,'TGG':0.0, \
                            		'TGT':0.0,'TTA':0.0,'TTC':0.0,'TTG':0.0,'TTT':0.0}}   

    for codon in nt_to_aa.keys():

         aa 		= nt_to_aa[codon]
         codon_kept = codon

         for codon_p in range(0,2+1):

           nts = ['A','G','T','C']

           nts = list(''.join(nts).replace(codon_kept[codon_p],''))
           
           for nt in nts:
                  codon=list(codon_kept)
                  codon[codon_p]=nt
                  codon=''.join(codon)
                  if aa==nt_to_aa[codon]:
                         potential_changes['S'][codon_kept]=potential_changes['S'][codon_kept]+1/3.0
                  
    for codon in potential_changes['S'].keys():
           potential_changes['N'][codon]=3.0-potential_changes['S'][codon]

    codons      = nt_to_aa.keys()
    codonPairs  = list(permutations(codons,2))
    selfies     = [(i,i) for i in codons]
    codonPairs  = codonPairs + selfies 
    
    codonPair_to_potential = {}

    for pair in codonPairs:
        codon1 = pair[0]
        codon2 = pair[1]
        pn1 = potential_changes['N'][codon1]
        pn2 = potential_changes['N'][codon2]
        ps1 = potential_changes['S'][codon1]
        ps2 = potential_changes['S'][codon2]
        codonPair_to_potential[pair] = {'N':(pn1+pn2)/2.,'S':(ps1+ps2)/2.}    # given an s1 codon and s2 codon, generate average potential 'N' and 'S'

    with open('../data/potential_changes_dict.p','wb') as f:
        pickle.dump(codonPair_to_potential,f)

def observed_changes_dict(genetic_code):

    codons      = nt_to_aa.keys()
    codonPairs  = list(permutations(codons,2))
    selfies     = [(i,i) for i in codons]
    codonPairs  = codonPairs + selfies 
    
    codonPair_to_observed = {}

    for pair in codonPairs:
        codon1 = pair[0]
        codon2 = pair[1]
        indices_to_permute = []

        for position in range(0,3):
            if not codon1[position] == codon2[position]:
                indices_to_permute.append(position)

        permuted_indices = list(permutations(indices_to_permute))
        syn = []
        non = []

        for i,path in enumerate(permuted_indices):
            syn.append(int()) 
            non.append(int()) 

            codon1_path1 = list(codon1) # copies of seqs for 'mutating'
            codon2_path1 = list(codon2)

            for site in path:
                codon1_past         = ''.join(codon1_path1)
                codon1_path1[site]  = codon2_path1[site]        # s1 = 'TTT' , s2 = 'ATA'  ==> 'TTT' --> 'ATT' 
                codon1_path1        = ''.join(codon1_path1)
                
                if nt_to_aa[codon1_path1] == nt_to_aa[codon1_past]:  # 'TTT --> 'ATT'
                    syn[i] = syn[i] + 1 
                    non[i] = non[i] + 0
                else:
                    syn[i] = syn[i] + 0
                    non[i] = non[i] + 1

                codon1_path1 = list(codon1_path1)

        codonPair_to_observed[pair] = {'S':np.mean(syn),'N':np.mean(non)}

    with open('../data/observed_changes_dict.p','wb') as f:
        pickle.dump(codonPair_to_observed,f)

# RUN
nt_to_aa = geneticCode('standard')
potential_changes_dict(nt_to_aa)
observed_changes_dict(nt_to_aa)
print('COMPLETE!')




























