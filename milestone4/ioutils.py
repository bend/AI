class IOUtils:
    def parse_to_matrix(filename):
        """Parse the file and put it in a matrix"""
        ins = open( filename, "r" )
        dist_matrix=[]
        i = -1
        size = 0
        for line in ins:
            if i == -1:
                nbr_cities = line
            else:
                cols = line.split(" ")
                dist_matrix.append([])
                for col in cols:
                    dist_matrix[i].append(float(col))
            i+=1
        return dist_matrix,nbr_cities