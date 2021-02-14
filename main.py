import requests
import json
import operator


def readFile():
    file = open("bgp-routing-table.txt", "r")
    print("File read successfully")
    return file


def findASN(ASpath):
    dest = ASpath[-1]
    ASpath.reverse()
    for x in ASpath:
        if x != dest:
            return x

    return -1


def getISPName(ISPs):
    ISPName = {}
    for ISP in ISPs:
        r = requests.get("https://api.bgpview.io/asn/" + ISP)
        ISPName[ISP] = r.json()["data"]["name"]

    return ISPName


def compute(file):
    print("Computing...")
    prefixes = set()
    ases = set()
    inst_a_rt_tab = []
    connections = {}
    nconnections = {}
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
                if(sprefix[0].split('.')[2] >= '124' and sprefix[0].split('.')[2] < '128'):
                    inst_a_rt_tab.append([prefix, ASpath])

                    inst_a_isp.add(findASN(ASpath.split()))

        ASes = ASpath.split()

        i = 0
        while i < len(ASes)-1:
            try:
                connections[ASes[i]].add(ASes[i+1])
            except:
                connections[ASes[i]] = set(ASes[i+1])
            i += 1

    for x in connections:
        nconnections[x] = len(connections[x])
    return prefixes, ases, inst_a_rt_tab, inst_a_isp, nconnections


def main():
    file = readFile()
    prefixes, ases, rt_tab, ISPs, nconnections = compute(file)

    print("==================Q1==================")
    print("Number of prefixes:", len(prefixes))
    print("Number of ASes:", len(ases))
    print("\n\n\n")

    print("==================Q2==================")
    print("Number of Routing tables enties for Inst A:", len(rt_tab))
    print("Routing table entries for Inst A:")
    print("Prefixes \t\t AS Path")
    for entry in rt_tab:
        print(entry[0], "\t", entry[1])
    print("\n\n\n")

    print("==================Q3==================")
    print("Number of ISPs of Inst A:", len(ISPs), "\n")
    ISPName = getISPName(ISPs)
    print("ASN \t ISP Name")
    for ISP in ISPName:
        print(ISP, "\t", ISPName[ISP])
    print("\n\n\n")

    print("==================Q4==================")
    topConnections = dict(
        sorted(nconnections.items(), key=operator.itemgetter(1), reverse=True)[:10])

    tc = []
    for connection in topConnections:
        tc.append(int(connection))

    ases = getISPName(tc)
    print("Top 10 ASes with highest degrees are:\n")
    print("AS \t Name")
    for AS in ases:
        print(AS, "\t", ases[AS])

    print("\n\n\n")

    return


if __name__ == "__main__":
    main()
