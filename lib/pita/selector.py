'''
Created on Feb 26, 2015

@author: dave
'''
from lib.pita import scanner
def guess_file_based_on_window_title(title_file, title_path_folders):
        
    d_candidate_best = ["", 0]
    for d in scanner.DATA["directories"]:
        d_candidate = [d, 0]
        for folder in title_path_folders:
            d_candidate[1] +=1*(folder in d_candidate[0])
                
        if d_candidate[1] > d_candidate_best[1]:
            d_candidate_best = d_candidate
    
    
    f_candidate_best = ["", 0]
    for f in scanner.DATA["directories"][d_candidate_best[0]]["files"]:
        f_candidate=[f, 0]
        for folder in title_path_folders:
            f_candidate[1] += 1*(folder in f_candidate[0])
        f_candidate[1] += 1*(title_file in f_candidate[0])
        if f_candidate[1] > f_candidate_best[1]:
            f_candidate_best = f_candidate
            
    return (d_candidate_best[0], f_candidate_best[0])
        
