#!/usr/bin/env python

import ROOT
ROOT.gROOT.SetBatch()
import os
import sys

sys.path.insert(0, '/afs/cern.ch/user/x/xju/work/h4l/h4lcode/root_plot_utils')
from root_plot_utils import AtlasStyle
from root_plot_utils.ploter import Ploter

ps = Ploter("Internal", 36.1)

base_dir = '/afs/cern.ch/user/x/xju/work/public/zz_highmass_4e_checks'

ws_name = 'combined_240GeV.root'
para = 'parametrized'
hist_smooth = 'histograms_with_smooth'
hist_raw = 'histograms_no_smooth'

def get_hist(ws_input, pdf_name, tag_name):
    f = ROOT.TFile.Open(ws_input)
    ws = f.Get("combined")
    m4l = ws.var("m4l")
    pdf = ws.obj(pdf_name)
    pdf.Print()
    hist = pdf.createHistogram(tag_name, m4l,
                        ROOT.RooFit.Binning(80, 130, 530)
                       )
    hist.SetDirectory(0)
    # normalize to one
    #hist.Sumw2()
    hist.Scale(1./hist.Integral())
    return hist

h_para = get_hist(os.path.join(base_dir, para, ws_name), 'ATLAS_Bkg_qqZZ_ggF_4e_13TeV_ana_shape', 'para')
h_smooth = get_hist(os.path.join(base_dir, hist_smooth, ws_name),
                    'ATLAS_Bkg_qqZZ_ggF_4e_13TeV_m4l', 'smooth')
h_raw = get_hist(os.path.join(base_dir, hist_raw, ws_name),
                    'ATLAS_Bkg_qqZZ_ggF_4e_13TeV_m4l', 'raw')

h_para.SetLineColor(2)
h_para.SetMarkerColor(2)
#h_para.SetLineStyle(2)
h_smooth.SetLineColor(4)
h_smooth.SetMarkerColor(4)
#h_smooth.SetLineStyle(3)
h_raw.GetYaxis().SetTitle('Unity / 5 GeV')

ps.prepare_2pad_canvas('canvas', 600, 600)
ps.pad2.cd()
ps.add_ratio_panel([h_raw, h_smooth, h_para], 'other/raw', 0.70, 1.2)
ps.pad1.cd()

h_raw.Draw()
h_para.Draw("same")
h_smooth.Draw("same")

ps.x_offset = 0.65
ps.y_offset = 0.80
legend = ps.get_legend(3)
legend.AddEntry(h_para, "Parametrization", 'L')
legend.AddEntry(h_smooth, "Smoothed", 'L')
legend.AddEntry(h_raw, "Raw", 'L')
legend.Draw()

#ps.add_atlas()

ps.can.SaveAs("qqZZ_cmp.png")
