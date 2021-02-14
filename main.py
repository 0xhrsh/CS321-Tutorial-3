def readFile():
    file = open("bgp-routing-table.txt","r")
    print("File read successfully")
    return file

def compute(file):
    print("Computing...")
    prefixes = set()
    ases = set()
    inst_a_rt_tab = []
    inst_a_isp = set()

    for line in file:
        fields = line.split('|')
        prefix = fields[5]
        from_as = fields[4]
        ASpath = fields[6]

        
        prefixes.add(prefix)
        ases.add(from_as)

        sprefix = prefix.split("/")
        if sprefix[1] == "24":
            if sprefix[0].startswith("103.21."):
                if(sprefix[0].split('.')[2]>='124' and sprefix[0].split('.')[2]<'128'):
                    inst_a_rt_tab.append([prefix, ASpath])
                    inst_a_isp.add(ASpath.split()[-2])
        elif sprefix[1] == "22" and sprefix[0].startswith("103.21."):
            print(sprefix[0])






    
    return prefixes, ases, inst_a_rt_tab, inst_a_isp

def main():
    file = readFile()
    prefixes, ases, rt_tab, isps = compute(file)

    print("==================Q1==================")
    print("Number of prefixes:",len(prefixes))
    print("Number of ASes:", len(ases))
    print("\n\n\n")

    print("==================Q2==================")
    print("Number of Routing tables enties for Inst A:", len(rt_tab))
    print("Routing table entries for Inst A:")
    print("Prefixes \t\t AS Path")
    for entry in rt_tab:
        print(entry[0],"\t", entry[1])
    print("\n\n\n")

    print("==================Q3==================")
    print("Number of ISPs of Inst A:", len(isps))
    print(isps)



    return

if __name__ == "__main__":
    main()