#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..')))

sys.path.insert(0, '/afs/cern.ch/user/x/xju/work/code/root_plot_utils')

from check_workspace import helper
from root_plot_utils.maker import maker

import ROOT
if not hasattr(ROOT, 'makeAsimovData'):
    ROOT.gROOT.LoadMacro('/afs/cern.ch/user/x/xju/work/combination/workspaceCombiner/ranking/macros/makeAsimovData.C')

class CheckNuisance():
    def __init__(self):
        self.limit_file = "/afs/cern.ch/user/x/xju/work/combination/run_area/HZZ/limits/v07/limit_total_ggF.txt"
        self.ws_dir = '/afs/cern.ch/user/x/xju/work/combination/run_area/HZZ/workspace/v06/'
        self.xs_dit = {}
        self.read_xs()

    def make_asimov_data(self, ws, mc, xs_val, poi_name):
        do_cond = False
        ROOT.makeAsimovData(mc, do_cond, ws, mc.GetPdf(), None, 1,
                            xs_val, poi_name)
        return ws.data('asimovData_1')

    def read_xs(self):
        with open(self.limit_file) as f:
            for line in f:
                items = line[:-1].split()
                mass = int(helper.get_mass(items[0]))
                self.xs_dit[mass] = float(items[5])

    def get_xs(self, mass):
        return self.xs_dit[mass]

    def get_variation_comb(self, mass):
        ws_file = self.ws_dir + "combined_HZZ_llll_llvv_{}GeV_afterPara.root".format(mass)
        f1 = ROOT.TFile.Open(ws_file)
        if not f1:
            return None
        ws = f1.Get("combWS")
        mc = ws.obj('ModelConfig')
        xs_val = self.get_xs(mass)
        ws.var("XS_VBF").setVal(0)
        ws.var("XS_VBF").setConstant(True)

        ws.var('mH_llll').setVal(mass)
        ws.var('mH_llll').setConstant(True)

        # set NP and global to 0
        nuisance = mc.GetNuisanceParameters()
        global_obs = mc.GetGlobalObservables()
        helper.set_rooArgSet(mc.GetNuisanceParameters(), 0)
        helper.set_rooArgSet(mc.GetGlobalObservables(), 0)

        poi_name = "XS_ggF"
        results = self.get_variation(ws, mc, xs_val, poi_name)
        print results
        f1.Close()

        return results

    def get_variation_4l(self, mass):
        ws_file = "/afs/cern.ch/user/x/xju/work/h4l/highmass/workspaces/HighMass/Prod_v12/20170505_NWA/combined_nominal_pruned.root"
        f1 = ROOT.TFile.Open(ws_file)
        ws = f1.Get("combined")
        mc = ws.obj('ModelConfig')
        ws.var('XS_VBF').setVal(0)
        ws.var('XS_VBF').setConstant(True)
        ws.var('mH').setVal(400)
        ws.var('mH').setConstant(True)
        poi_name = 'XS_ggF'
        xs_val = self.get_xs(mass) * 0.00452 * 1000
        results = self.get_variation(ws, mc, xs_val, poi_name, "alpha_ATLAS_LUMI")
        print results
        f1.Close()
        return results

    def get_variation_llvv(self, mass):
        ws_file = "~/work/h4l/highmass/workspaces/LLVV/NWA_sameBinning_10perSys_new_ggZZ/workspaces/combined_mH400.root"
        f1 = ROOT.TFile.Open(ws_file)
        ws = f1.Get("combined")
        mc = ws.obj('ModelConfig')
        ws.var('mu_VBF').setVal(0)
        ws.var('mu_VBF').setConstant(True)
        poi_name = 'mu_ggF'
        xs_val = self.get_xs(mass)
        results = self.get_variation(ws, mc, xs_val, poi_name, "alpha_ATLAS_lumi")
        print results
        f1.Close()
        return results

    def get_variation(self, ws, mc, xs_val, poi_name, lumi_sys_name="ATLAS_lumi2016"):
        # get np
        lumi_sys = ws.var(lumi_sys_name)

        # generate asimov data
        data = self.make_asimov_data(ws, mc, xs_val, poi_name)
        nll = mc.GetPdf().createNLL(
            data,
            ROOT.RooFit.Constrain(mc.GetNuisanceParameters()),
            ROOT.RooFit.GlobalObservables(mc.GetGlobalObservables())
        )
        nll.enableOffsetting(True)
        minim = ROOT.RooMinimizer(nll)
        minim.optimizeConst(2)
        minim.setStrategy(1)
        status = minim.minimize(
            "Minuit2",
            ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo()
        )
        if status != 0:
            print "status is not zero!"

        lumiSet = ROOT.RooArgSet()
        lumiSet.add(lumi_sys)
        minim.minos(lumiSet)
        lumi_up = lumi_sys.getErrorHi()
        lumi_low = lumi_sys.getErrorLo()

        poi = ws.var(poi_name)
        xs_nominal = poi.getVal()

        # set luminosity up
        lumi_sys.setVal(lumi_up)
        lumi_sys.setConstant(True)
        status = minim.minimize(
            "Minuit2",
            ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo()
        )
        xs_up = poi.getVal()

        # set luminosity down
        lumi_sys.setVal(lumi_low)
        lumi_sys.setConstant(True)
        status = minim.minimize(
            "Minuit2",
            ROOT.Math.MinimizerOptions.DefaultMinimizerAlgo()
        )
        xs_low = poi.getVal()

        return (xs_nominal, xs_up, xs_low)

    def process(self):
        error_list = []
        mass_list = []
        for mass in range(300, 500, 20):
            mass_list.append(mass)
            results = self.get_variation(mass)
            if results is None:
                continue
            nom, up, down = self.get_variation(mass)
            error = abs(down - up)/nom/2.
            error_list.append(error)

        gr = maker.graph("lumi_impact", mass_list, error_list)
        fout = ROOT.TFile.Open("out.root", 'recreate')
        gr.Write()
        canvas = ROOT.TCanvas("canvas", 'canvas', 600, 600)
        gr.Draw("APL")
        canvas.SaveAs("test_lumi.pdf")
        fout.Close()

if __name__ == "__main__":
    checker = CheckNuisance()
    # checker.process()
    res1 = checker.get_variation_4l(400)
    res2 = checker.get_variation_llvv(400)
    print res1
    print res2

