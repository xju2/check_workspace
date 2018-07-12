#! coding: utf-8

import ROOT
from ROOT.RooStats import SignificanceToPValue
from ROOT.RooStats import PValueToSignificance

import math
import sys

def global_pvalue(local_s, n_xs):
    local_p = SignificanceToPValue(local_s)
    global_p = local_p*(1+math.sqrt(math.pi/2.)*n_xs*local_s)
    return PValueToSignificance(global_p)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print sys.argv[0]," localZ Nxs"
        exit(1)

    print global_pvalue(float(sys.argv[1]), float(sys.argv[2]))
