# -*- coding: utf-8 -*-
import ROOT
from ROOT import RooFit
from __future__ import print_function

def minimize(nll):
    minim = ROOT.RooMinimizer(nll)
    minim.optimizeConst(2)
    minim.setStrategy(2)
    status = minim.minimize(
        "Minuit2",
        ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo()
    )
    return minim.save()


def set_RooArgSet(roo_arg, value):
    itr = ROOT.TIter(roo_arg.createIterator())
    var = itr()
    while var:
        var.setVal(value)
        var = itr()


def set_var(ws, var_name, value, is_const=False):
    obj = ws.var(var_name)
    if obj:
        obj.setVal(value)
        obj.setConstant(is_const)
    else:
        print(var_name, " not found")
