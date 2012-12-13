'''NAMES OF THE AUTHOR(S):
Benoit Daccache
Christopher Castermane'''

import sys
from minisat import *
from packages import *

class Install:

    def start(filename, package_list):
        repo = Repository(filename)
        pkg_inst = []
            
        # Add package to install in array
        for package in package_list:
            if package in repo:
                pkg_inst.append(repo[package])
        
        prop_formulas = []
        # Processed pkg to avoid multi times processing of a package
        processed = {}

        def rec_dep(pkg):
            if pkg in processed:                # Package already processed, skip it
                return

            processed[pkg] = True
            for a in pkg.depends: # Check dependencies
                if a in processed:                # Package already processed, skip it
                    return
                a_id = repo[str(a[0])].index
                array = [-pkg_id,a_id]
                prop_formulas.append(tuple(array))
                rec_dep(repo[str(a[0])])    # Recursively check dependencies
            
            for a in pkg.conflicts: # Check conficts
                if a in processed:                # Package already processed, skip it
                    return
                a_id = repo[str(a)].index
                prop_formulas.append((-pkg_id,-a_id))
            
            array1 = [-pkg_id]
            
            i = 0
            for prv in pkg.provided_by:  # Check the provided by
                if i == 0:
                    array1.append(prv.index)
                    prop_formulas.append((-prv.index,pkg.index))
                    if(len(pkg.provided_by)>0): prop_formulas.append(tuple(array1))
                    rec_dep(prv)
                i+=1
    

        # For each package 
        for pkg in pkg_inst:
            pkg_id = pkg.index
            rec_dep(pkg)
        
        # Add the package as a clause
        for pkg in pkg_inst:
            a_id = repo[str(pkg)].index
            prop_formulas.append((a_id,))
            
                
        res = minisat(len(repo), prop_formulas)
        
        if res == None:
            print("Package Conflict")
            return
        for p in res:
            print(repo[p])
        
        
if __name__ == "__main__":
    r = Install.start(sys.argv[1], sys.argv[2:])
