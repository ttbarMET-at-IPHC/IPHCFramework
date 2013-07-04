# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('tlbsmTag',
                  'tlbsm_53x_v2',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  'TLBSM tag use in production')

options.register ('useData',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  'Run this on real data')

options.register ('globalTag',
                  '',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  'Overwrite defaul globalTag')

options.register ('hltProcess',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name to use.")

options.register ('writeFat',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Output tracks and PF candidates (and GenParticles for MC)")

options.register ('writeSimpleInputs',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Write four-vector and ID of PF candidates")

options.register ('writeGenParticles',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Output GenParticles collection")

options.register ('forceCheckClosestZVertex',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Force the check of the closest z vertex")


options.register ('useSusyFilter',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use the SUSY event filter")


options.register ('useExtraJetColls',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Write extra jet collections for substructure studies")


options.register ('usePythia8',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use status codes from Pythia8 rather than Pythia6")


options.register ('usePythia6andPythia8',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use status codes from Pythia8 and Pythia6")


options.register ('runOnFastSim',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Option needed to run on fastsim.")


options.register('doJetTauCrossCleaning',
                 False,
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.int,
                 "Enable cleaning the jet collections based on taus")


options.parseArguments()


if not options.useData :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])

    process.source.fileNames = [
        'file:F88F3DF3-53E7-E111-91BE-003048D4DCD8.root'
    ]

else :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
    process.source.fileNames = [
#        'file:/tmp/kkotov/9AC4CE9A-FE82-E111-AED7-BCAEC5329720.root'
        'file:/tmp/kkotov/1AF849DE-0488-E111-B819-5404A63886EF.root'
    ]

#process.source.eventsToProcess = cms.untracked.VEventRange( ['1:86747'] )

#process.source.skipEvents = cms.untracked.uint32(17268) 

print options

print 'Running jet corrections: '
print inputJetCorrLabel

import sys

#sys.path.append('s4_m500')
#import INPUT
#process.source.fileNames = INPUT.fileNames

###############################
####### Global Setup ##########
###############################

### The Strasbourg's ntupler
process.load("MiniTree.MiniTreeProducer.simpleEleIdSequence_cff")
process.MiniTreeProduction = cms.EDProducer('MiniTreeProducer',
# ---------------------- General info -------------------------------
         verbose             = cms.uint32(0),   #0: nothing - >1 
         isAOD               = cms.bool(True),  # true if processing AOD 
         isData              = cms.bool(False), # true if processing AOD data
# ----------------------   Trigger -------------------------------
##         doTrigger           = cms.bool(True),
         doTrigger           = cms.bool(False),
         saveAllTriggers     = cms.bool(True), #should be True by default !!
         triggerList         = cms.vstring("HLT_Mu15_L1Mu7","HLT_DoubleMu3","HLT_IsoEle10_Mu10_L1R","HLT_IsoEle18_L1R","HLT_DoubleIsoEle12_L1R","HLT_Mu5","HLT_Mu9","HLT_Mu11","HLT_Mu15","HLT_IsoMu9","HLT_Ele10_SW_L1R","HLT_Ele15_SW_L1R","HLT_Ele15_LW_L1R","HLT_Ele10_LW_L1R","HLT_DoubleEle5_SW_L1R","HLT_LooseIsoEle15_LW_L1R","HLT_L2Mu3","HLT_L2Mu5","HLT_L2Mu9","HLT_Jet15U","HLT_Photon10_L1R","HLT_Photon15_L1R","HLT_Photon10_Cleaned_L1R","HLT_Photon15_Cleaned_L1R","HLT_Ele15_SW_CaloEleId_L1R","HLT_Ele20_SW_L1R","HLT_DoubleEle10_SW_L1R"),
# ----------------------  Electrons -------------------------------
         doElectrons         = cms.bool(True),
         electron_cut_pt     = cms.double(10),
         electron_cut_eta    = cms.double(2.5),
         electron_saveAllID  = cms.bool(False),
         electron_IDlist     = cms.vstring("mvaTrigV0","mvaNonTrigV0", "eidLoose","eidRobustLoose", "eidTight"),
         electronHLTmatching = cms.vstring(""),
##         electronProducer    = cms.VInputTag(cms.InputTag("selectedPatElectronsPF2PAT")),
         electronProducer    = cms.VInputTag(cms.InputTag("selectedPatElectronsPFlow")),
# ----------------------   Photons -------------------------------
         doPhotons           = cms.bool(False),
         photon_cut_pt       = cms.double(10),
         photon_cut_eta      = cms.double(2.5),
         photonHLTmatching   = cms.vstring(""),
##         photonProducer      = cms.VInputTag(cms.InputTag("selectedPatPhotonsPF2PAT")),
         photonProducer      = cms.VInputTag(cms.InputTag("selectedPatPhotonsPFlow")),
# -----------------------   Muons -------------------------------
         doMuons             = cms.bool(True),
         muon_cut_pt         = cms.double(10),
         muon_cut_eta        = cms.double(2.5),
         muon_cut_keepStandaloneMu  = cms.bool(False),
         muon_cut_keepTrackerMu     = cms.bool(True),
         muon_cut_keepCaloMu        = cms.bool(False),
         muon_cut_keepGlobalMu      = cms.bool(True),
         muon_IDlist                = cms.vstring("GlobalMuonPromptTight"),
         muonHLTmatching      = cms.vstring(""),
##         muonProducer        = cms.VInputTag(cms.InputTag("selectedPatMuonsPF2PAT")),
         muonProducer        = cms.VInputTag(cms.InputTag("selectedPatMuonsPFlow")),
# -----------------------   Taus ----------------------------------
         doTaus              = cms.bool(False),
         tau_cut_pt          = cms.double(10),
         tau_cut_eta         = cms.double(2.4),
         tau_saveAllID       = cms.bool(True),
         tau_IDlist          = cms.vstring(""),
         tauHLTmatching      = cms.vstring(""),
##         tauProducer         = cms.VInputTag(cms.InputTag("selectedPatTausPF2PAT")),
         tauProducer         = cms.VInputTag(cms.InputTag("selectedPatTausPFlow")),
# -----------------------   Tracks ---------------------------------
         doTracks            = cms.bool(False),
         track_cut_pt        = cms.double(0.5),
         track_cut_eta       = cms.double(2.4),
         trackProducer       = cms.VInputTag(cms.InputTag("generalTracks")),
# -----------------------  Vertices ---------------------------------
         doVertices          = cms.bool(True),
         saveAllVertex       = cms.bool(True),
         vertexProducer      = cms.VInputTag(cms.InputTag("offlinePrimaryVertices")),
# -----------------------  BeamSpot ---------------------------------
         doBeamSpot          = cms.bool(True),
         beamSpotProducer    = cms.InputTag("offlineBeamSpot"),
# -----------------------   JetMet ----------------------------------
         doJetMet            = cms.bool(True),
         doMuonCorrection    = cms.bool(True),
         jet_cut_pt          = cms.double(10),
         jet_cut_eta         = cms.double(2.5),
         jetIDList           = cms.vstring("LOOSE","TIGHT"),
         jetBTagList         = cms.vstring("trackCountingHighEffBJetTags","jetProbabilityBJetTags","jetBProbabilityBJetTags","combinedSecondaryVertexBJetTags"),
##         jetHLTmatching      = cms.vstring("jetMatchHLTJets"),
         jetHLTmatching      = cms.vstring(""),
         jetmetProducer      = cms.VPSet(
                    cms.PSet(
                 jet    = cms.untracked.string("selectedPatJetsPFlow"),
                 met    = cms.untracked.string("patMETsPFlow"),
                 pfmet1 = cms.untracked.string("pfType1CorrectedMet"),
                 pfmet2 = cms.untracked.string("pfType1p2CorrectedMet"),
                 algo   = cms.untracked.string("pf")
               )
                     ),
# -----------------------  Pile-Up ----------------------------------
         doPileUp            = cms.bool(True),
         rho_PUUE_dens       = cms.InputTag("kt6PFJets", "rho"),
##         neutralRho_PUUE_dens= cms.InputTag("kt6NeutralPFJets", "rho"),
         neutralRho_PUUE_dens= cms.InputTag("kt6PFJetsCentralNeutral", "rho"),
# -----------------------  MonteCarlo -------------------------------
         doGenParticleCollection = cms.bool(True),
         mcDescentMax = cms.uint32(4),
         mcNGenPartMax = cms.uint32(100)
)

if options.useData:
    process.MiniTreeProduction.isData                  = cms.bool(True)
    process.MiniTreeProduction.doPileUp                = cms.bool(False)
    process.MiniTreeProduction.doGenParticleCollection = cms.bool(False)
else:
    process.MiniTreeProduction.isData                  = cms.bool(False)
    process.MiniTreeProduction.doGenParticleCollection = cms.bool(True)
    process.MiniTreeProduction.doPileUp                = cms.bool(True)

# loads your analyzer
process.MyModule = cms.EDAnalyzer('NTupleProducer',
         verbose             = cms.uint32(0),   #0: nothing - >1 
# -------------------------------------------------------------------
#                         GENERAL SKIM
# -------------------------------------------------------------------
    general_skim = cms.PSet(
         verbose             = cms.uint32(0),   #0: nothing - >1 
# ----------------------   Trigger -------------------------------
         skimTrigger      = cms.bool(False),
         skimGenParticles = cms.bool(True),
         skimGenTaus      = cms.bool(True),
         triggerList      = cms.vstring(""),
# ----------------------  Electrons -------------------------------
         skimElectrons = cms.bool(False),
         electron_keepAllCollections = cms.bool(True),
         electron_collectionList     = cms.vstring(""),
         electron_pt                 = cms.double(7),
         electron_eta                = cms.double(2.5),
# ----------------------  Muons   -------------------------------
         skimMuons = cms.bool(False),
         muon_keepAllCollections = cms.bool(True),
         muon_collectionList     = cms.vstring(""),
         muon_pt                 = cms.double(7),
         muon_eta                = cms.double(2.5),
# ----------------------  Photons   -------------------------------
         skimPhotons = cms.bool(False),
         photon_keepAllCollections = cms.bool(True),
         photon_collectionList     = cms.vstring(""),
         photon_pt                 = cms.double(7),
         photon_eta                = cms.double(2.5),
# ----------------------  Taus   -------------------------------
         skimTaus = cms.bool(False),
         tau_keepAllCollections = cms.bool(True),
         tau_collectionList     = cms.vstring(""),
         tau_pt                 = cms.double(7),
         tau_eta                = cms.double(2.5),
# ----------------------  Jets   -------------------------------
         skimJets = cms.bool(False),
         jet_keepAllCollections = cms.bool(True),
         jet_collectionList     = cms.vstring("pf"),
         jet_pt                 = cms.double(10),
         jet_eta                = cms.double(2.5),
# ----------------------  Tracks   -------------------------------
         skimTracks = cms.bool(False),
         track_keepAllCollections = cms.bool(True),
         track_collectionList     = cms.vstring(""),
         track_pt                 = cms.double(7),
         track_eta                = cms.double(2.5),
# ----------------------  Vertices   -------------------------------
         skimVertices = cms.bool(False),
         vertex_keepAllCollections = cms.bool(True),
         vertex_collectionList     = cms.vstring("")
     ),
# -------------------------------------------------------------------
#                         TOPDILEPTON SKIM
# -------------------------------------------------------------------
    topdilepton_skim = cms.PSet(
# ----------------------   Trigger -------------------------------
     doTriggerSkimming     = cms.bool(False), # skim on trigger decisions
     triggerSkimList       = cms.vstring("HLT_QuadJet15U"),
# ----------------------  Muons   -------------------------------
     numberOfLept     = cms.int32(-1),# for skims ! Total number of 
     numberOfMuon     = cms.int32(0),# number of sel muon
     muon_cut_pt      = cms.double(10),
     muon_cut_iso     = cms.double(-1),  # PLEASE NO ISO FOR SKIMMING!!!
     useMuonIdSkim     = cms.bool(False),
# ----------------------  Electrons -------------------------------
     numberOfElec       = cms.int32(0),# number of sel electron
     useElectronIdSkim  = cms.bool(False),
     electron_cut_pt    = cms.double(7),
     electron_cut_iso   = cms.double(-1), # PLEASE NO ISO FOR SKIMMING!!!
# ----------------------  MonteCarlo -------------------------------
     doTMEMESkimming       = cms.bool(False), # skim on the TMEME
     TMEMESkimList         = cms.vint32(),
     doMCDiLepSkimming     = cms.bool(False),
     MCDiLepList           = cms.vstring(""),
# ----------------------  Taus   -------------------------------
     doTauSkimming    = cms.bool(False), # skim on the number of reco 
     numberOfTau      = cms.int32(1),
     tau_cut_pt       = cms.double(5),
     tau_algo         = cms.string("selectedPatTaus"),
# ----------------------  Jets   -------------------------------
     doJetSkimming         = cms.bool(False), # skim on the number of jets
     numberOfJet      = cms.int32(3),
     jet_cut_pt       = cms.double(20),
     jet_cut_eta      = cms.double(2.5),
     jet_algo         = cms.string("pf")
    )
)

### The OSU ntupler configuration ###  
#process.load("OSUAnalysis.NTupleTools.EventFilter_cfi")
#process.EventFilter.NumTracks = cms.uint32(10)
#process.EventFilter.HPTrackThreshold = cms.double(0.2)
#process.EventFilter.minNElectrons = cms.int32(0)
#process.EventFilter.minElectronPt = cms.double(25.)
#process.EventFilter.maxAbsElectronEta = cms.double(2.5)
#process.EventFilter.minNMuons = cms.int32(0)
#process.EventFilter.minMuonPt = cms.double(25.)
#process.EventFilter.maxAbsMuonEta = cms.double(2.5)
#process.EventFilter.VertexInput = cms.InputTag('goodOfflinePrimaryVertices')
#process.EventFilter.VertexMinimumNDOF = cms.uint32(4)# this is >= 4
#process.EventFilter.VertexMaxAbsZ = cms.double(24)
#process.EventFilter.VertexMaxAbsRho = cms.double(2)
#process.EventFilter.electronInput = cms.InputTag("selectedPatElectronsPFlow")


process.load('OSUAnalysis.NTupleTools.Ntuple_cff')
#vertices
process.rootTupleVertex.InputTag = cms.InputTag('goodOfflinePrimaryVertices')
process.rootTupleVertex.Prefix = cms.string('goodOfflinePrimaryVertices.')
#calo jets
process.rootTupleCaloJets.InputTag = cms.InputTag('goodPatJets')
process.rootTupleCaloJets.Prefix = cms.string('goodPatJets.')
process.rootTupleCaloJets.ReadJECuncertainty = cms.bool(True)
#PF2PAT jets
process.rootTuplePF2PATJets.InputTag = cms.InputTag('goodPatJetsPFlow')
process.rootTuplePF2PATJets.Prefix = cms.string('goodPatJetsPFlow.')
process.rootTuplePF2PATJets.ReadJECuncertainty = cms.bool(True)
#Cambridge-Aachen cone 0.8 jets
process.rootTupleCA8PFJets = process.rootTuplePF2PATJets.clone()
process.rootTupleCA8PFJets.InputTag = cms.InputTag('goodPatJetsCA8PF')
process.rootTupleCA8PFJets.Prefix = cms.string('goodPatJetsCA8PF.')
# MET
process.rootTuplePFMETtype1 = cms.EDProducer( "BristolNTuple_PFMET",
    InputTag = cms.InputTag( 'pfType1CorrectedMet' ),
    Prefix = cms.string( 'patPFMETType1PFlow.' ),
    Suffix = cms.string( '' ),
    StoreUncorrectedPFMET = cms.bool( False)
)
process.rootTuplePFMETtype1p2 = cms.EDProducer( "BristolNTuple_PFMET",
    InputTag = cms.InputTag( 'pfType1p2CorrectedMet' ),
    Prefix = cms.string( 'patPFMETType1p2PFlow.' ),
    Suffix = cms.string( '' ),
    StoreUncorrectedPFMET = cms.bool( False)
)

#selection on GenParticles
process.rootTupleGenParticles.minPt = cms.double(-1)
process.rootTupleGenParticles.maxAbsoluteEta = cms.double(100)
# electrons
process.rootTupleElectrons.InputTag = cms.InputTag('selectedPatElectrons')
process.rootTupleElectrons.Prefix = cms.string('selectedPatElectrons.')
process.rootTuplePFElectrons.InputTag = cms.InputTag('selectedPatElectronsPFlow')
process.rootTuplePFElectrons.Prefix = cms.string('selectedPatElectronsPFlow.')
# muons
process.nTupleMuons.InputTag = cms.InputTag('selectedPatMuons')
process.nTupleMuons.Prefix = cms.string('selectedPatMuons.')
process.nTuplePFMuons.InputTag = cms.InputTag('selectedPatMuonsPFlow')
process.nTuplePFMuons.Prefix = cms.string('selectedPatMuonsPFlow.')
# trigger
process.rootTupleTrigger.HLTInputTag = cms.InputTag('TriggerResults','',options.hltProcess)

if options.useData:
   process.rootTupleGenEventInfo.StorePDFWeights = cms.bool(False)
else:
   process.rootTupleGenEventInfo.StorePDFWeights = cms.bool(True)

process.rootTupleTree = cms.EDAnalyzer("RootTupleMakerV2_Tree",
    outputCommands = cms.untracked.vstring(
       'drop *',
       #beamspot
        'keep *_rootTupleBeamSpot_*_*',
        #EventContent
        'keep *_rootTupleEvent_*_*',
        #CaloJets
#        'keep *_rootTupleCaloJets_*_*',
        #PF jets
        'keep *_rootTuplePF2PATJets_*_*',
        'keep *_rootTupleCA8PFJets_*_*',
        #electrons
#        'keep *_rootTupleElectrons_*_*',
        'keep *_rootTuplePFElectrons_*_*',
        #MET
        'keep *_rootTupleCaloMET_*_*',
        'keep *_rootTuplePFMET_*_*',
        'keep *_rootTuplePFMETtype1_*_*',
        'keep *_rootTuplePFMETtype1p2_*_*',
        #muons
        'keep *_nTupleMuons_*_*',
        'keep *_nTuplePFMuons_*_*',
        #trigger
        'keep *_rootTupleTrigger_*_*',
        #vertices (DA)
        'keep *_rootTupleVertex_*_*',
        #tracks
        'keep *_rootTupleTracks_*_*',
        #gen information
        'keep *_rootTupleGenEventInfo_*_*',
        'keep *_rootTupleGenParticles_*_*',
        'keep *_rootTupleGenJets_*_*',
        'keep *_rootTupleGenMETTrue_*_*',
    )
)

process.rootNTuples = cms.Sequence((
    #beamspot
    process.rootTupleBeamSpot +
    #vertices
    process.rootTupleVertex +
    #jets
#    process.rootTupleCaloJets +
    process.rootTuplePF2PATJets +
#    process.rootTupleCA8PFJets + 
#    process.rootTupleCA8PFJetsPruned +
#    process.rootTupleCA8PFJetsTopTag +
    #tracks
##    process.rootTupleTracks +
    #electrons
    process.rootTupleElectrons +
    process.rootTuplePFElectrons +
    #muons
    process.nTuplePFMuons +
    process.nTupleMuons +
    #MET
    process.rootTupleCaloMET +
    process.rootTuplePFMET +
    process.rootTuplePFMETtype1 +
    process.rootTuplePFMETtype1p2 +
    #Event
    process.rootTupleEvent +
    #trigger
    process.rootTupleTrigger +
    #genEventInfos
    process.rootTupleGenEventInfo +
    process.rootTupleGenParticles +
    process.rootTupleGenJetSequence +
    process.rootTupleGenMETSequence)*
    process.rootTupleTree)

if options.useData:
    process.rootNTuples.remove( process.rootTupleGenEventInfo )
    process.rootNTuples.remove( process.rootTupleGenParticles )
    process.rootNTuples.remove( process.rootTupleGenJetSequence )
    process.rootNTuples.remove( process.rootTupleGenMETSequence )

process.out.outputCommands = cms.untracked.vstring('drop *',
                            'keep edmTriggerResults_*_*_*',
                            'keep IPHCTreeMTEvent_*_*_*'
                            )

#process.out.fileName = cms.untracked.string('EDMOUTPUT.root')

process.TFileService = cms.Service( "TFileService",
                           fileName = cms.string( 'NTuple.root' )
#                           fileName = cms.string( 'MET_Run2012A-13Jul2012-v1_AOD_CMSSW_5_3_3_Ov13.0.root' )
                           )

##################################################################3



###############################
####### Global Setup ##########
###############################

if options.useData :
    if options.globalTag is '':
        process.GlobalTag.globaltag = cms.string( 'GR_P_V40_AN1::All' )
    else:
        process.GlobalTag.globaltag = cms.string( options.globalTag )
else :
    if options.globalTag is '':
        process.GlobalTag.globaltag = cms.string( 'START53_V7E::All' )
    else:
        process.GlobalTag.globaltag = cms.string( options.globalTag )


from PhysicsTools.PatAlgos.patTemplate_cfg import *


## The beam scraping filter __________________________________________________||
process.noscraping = cms.EDFilter(
    "FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False),
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
    )

## The iso-based HBHE noise filter ___________________________________________||
process.load('CommonTools.RecoAlgos.HBHENoiseFilter_cfi')

## The CSC beam halo tight filter ____________________________________________||
process.load('RecoMET.METAnalyzers.CSCHaloFilter_cfi')

## The HCAL laser filter _____________________________________________________||
process.load("RecoMET.METFilters.hcalLaserEventFilter_cfi")
process.hcalLaserEventFilter.vetoByRunEventNumber=cms.untracked.bool(False)
process.hcalLaserEventFilter.vetoByHBHEOccupancy=cms.untracked.bool(True)

## The ECAL dead cell trigger primitive filter _______________________________||
process.load('RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi')
## For AOD and RECO recommendation to use recovered rechits
process.EcalDeadCellTriggerPrimitiveFilter.tpDigiCollection = cms.InputTag("ecalTPSkimNA")

## The EE bad SuperCrystal filter ____________________________________________||
process.load('RecoMET.METFilters.eeBadScFilter_cfi')

## The Good vertices collection needed by the tracking failure filter ________||
process.goodVertices = cms.EDFilter(
  "VertexSelector",
  filter = cms.bool(False),
  src = cms.InputTag("offlinePrimaryVertices"),
  cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.rho < 2")
)

## The tracking failure filter _______________________________________________||
process.load('RecoMET.METFilters.trackingFailureFilter_cfi')


# switch on PAT trigger
#from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
#switchOnTrigger( process, hltProcess=options.hltProcess )


###############################
####### DAF PV's     ##########
###############################

pvSrc = 'offlinePrimaryVertices'

## The good primary vertex filter ____________________________________________||
process.primaryVertexFilter = cms.EDFilter(
    "VertexSelector",
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string("!isFake & ndof > 4 & abs(z) <= 24 & position.Rho <= 2"),
    filter = cms.bool(True)
    )


from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( maxZ = cms.double(24.0),
                                     minNdof = cms.double(4.0) # this is >= 4
                                     ),
    src=cms.InputTag(pvSrc)
    )


###############################
########## Gen Setup ##########
###############################

process.load("RecoJets.Configuration.GenJetParticles_cff")
from RecoJets.JetProducers.ca4GenJets_cfi import ca4GenJets
from RecoJets.JetProducers.ak5GenJets_cfi import ak5GenJets
process.ca8GenJetsNoNu = ca4GenJets.clone( rParam = cms.double(0.8),
                                           src = cms.InputTag("genParticlesForJetsNoNu"))

process.ak8GenJetsNoNu = ak5GenJets.clone( rParam = cms.double(0.8),
                                           src = cms.InputTag("genParticlesForJetsNoNu"))


process.load("TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff")

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")


# prune gen particles
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
                                            src = cms.InputTag("genParticles"),
                                            select = cms.vstring(
                                                "drop  *"
                                                ,"keep status = 3" #keeps  particles from the hard matrix element
                                                ,"keep (abs(pdgId) >= 11 & abs(pdgId) <= 16) & status = 1" #keeps e/mu and nus with status 1
                                                ,"keep (abs(pdgId)  = 15) & status = 3" #keeps taus
                                                )
                                            )

if options.usePythia8 :
    process.prunedGenParticles.select = cms.vstring(
                                                "drop  *"
                                                ,"keep status = 21" #keeps  particles from the hard matrix element
                                                ,"keep status = 22" #keeps  particles from the hard matrix element
                                                ,"keep status = 23" #keeps  particles from the hard matrix element
                                                ,"keep (abs(pdgId) >= 11 & abs(pdgId) <= 16) & status = 1" #keeps e/mu and nus with status 1
                                                ,"keep (abs(pdgId)  = 15) & (status = 21 || status = 22 || status = 23) " #keeps taus
                                                )
if options.usePythia6andPythia8 :
    process.prunedGenParticles.select = cms.vstring(
                                                "drop  *"
                                                ,"keep status = 3" #keeps  particles from the hard matrix element
                                                ,"keep status = 21" #keeps  particles from the hard matrix element
                                                ,"keep status = 22" #keeps  particles from the hard matrix element
                                                ,"keep status = 23" #keeps  particles from the hard matrix element
                                                ,"keep (abs(pdgId) >= 11 & abs(pdgId) <= 16) & status = 1" #keeps e/mu and nus with status 1
                                                ,"keep (abs(pdgId)  = 15) & (status = 3 || status = 21 || status = 22 || status = 23)" #keeps taus
                                                )                                      


## process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
##                                             src = cms.InputTag("genParticles"),
##                                             select = cms.vstring(
##                                                 "drop  *"
##                                                 ,"keep++ (abs(pdgId) =6) "
##                                                 )
##                                             )

###############################
#### Jet RECO includes ########
###############################

from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CaloJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.CATopJetParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *


###############################
########## PF Setup ###########
###############################

# Default PF2PAT with AK5 jets. Make sure to turn ON the L1fastjet stuff. 
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix,
	  jetCorrections=inputJetCorrLabel, pvCollection=cms.InputTag('goodOfflinePrimaryVertices'), typeIMetCorrections=True)
#useGsfElectrons(process,postfix,dR="03")


####################################
#  top projections in PF2PAT:
####################################
getattr(process,"pfNoPileUp"  +postfix).enable = True
getattr(process,"pfNoMuon"    +postfix).enable = False 
getattr(process,"pfNoElectron"+postfix).enable = False
getattr(process,"pfNoTau"     +postfix).enable = False
getattr(process,"pfNoJet"     +postfix).enable = False





if not options.forceCheckClosestZVertex :
    process.pfPileUpPFlow.checkClosestZVertex = False

# change the cone size of electron isolation to 0.3 as default.
process.pfIsolatedElectronsPFlow.isolationValueMapsCharged = cms.VInputTag(cms.InputTag("elPFIsoValueCharged03PFIdPFlow"))
process.pfIsolatedElectronsPFlow.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFIdPFlow")
process.pfIsolatedElectronsPFlow.isolationValueMapsNeutral = cms.VInputTag(cms.InputTag("elPFIsoValueNeutral03PFIdPFlow"), cms.InputTag("elPFIsoValueGamma03PFIdPFlow"))

process.pfElectronsPFlow.isolationValueMapsCharged  = cms.VInputTag(cms.InputTag("elPFIsoValueCharged03PFIdPFlow"))
process.pfElectronsPFlow.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFIdPFlow" )
process.pfElectronsPFlow.isolationValueMapsNeutral  = cms.VInputTag(cms.InputTag( "elPFIsoValueNeutral03PFIdPFlow"), cms.InputTag("elPFIsoValueGamma03PFIdPFlow"))

process.patElectronsPFlow.isolationValues = cms.PSet(
        pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFIdPFlow"),
        pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03PFIdPFlow"),
        pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03PFIdPFlow"),
        pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFIdPFlow"),
        pfPhotons = cms.InputTag("elPFIsoValueGamma03PFIdPFlow")
        )


applyPostfix(process,"pfIsolatedElectrons",postfix).combinedIsolationCut = cms.double(9999.)
 
 


# change the cone size of muons isolation to 0.3 as default.
applyPostfix(process,"pfIsolatedMuons",postfix).isolationValueMapsCharged = cms.VInputTag( cms.InputTag( 'muPFIsoValueCharged03PFlow' ) )
applyPostfix(process,"pfIsolatedMuons",postfix).isolationValueMapsNeutral = cms.VInputTag( cms.InputTag( 'muPFIsoValueNeutral03PFlow' ), cms.InputTag( 'muPFIsoValueGamma03PFlow' ) )
applyPostfix(process,"pfIsolatedMuons",postfix).deltaBetaIsolationValueMap = cms.InputTag( 'muPFIsoValuePU03PFlow' )
applyPostfix(process,"patMuons",postfix).isolationValues.pfNeutralHadrons = cms.InputTag( 'muPFIsoValueNeutral03PFlow' )
applyPostfix(process,"patMuons",postfix).isolationValues.pfPhotons = cms.InputTag( 'muPFIsoValueGamma03PFlow' )
applyPostfix(process,"patMuons",postfix).isolationValues.pfChargedHadrons = cms.InputTag( 'muPFIsoValueCharged03PFlow' )
applyPostfix(process,"patMuons",postfix).isolationValues.pfPUChargedHadrons = cms.InputTag( 'muPFIsoValuePU03PFlow' ) 
applyPostfix(process,"pfIsolatedMuons",postfix).combinedIsolationCut = cms.double(9999.)




applyPostfix(process,"pfIsolatedMuons",postfix).isolationCut = cms.double(9999.)
applyPostfix(process,"pfIsolatedElectrons",postfix).isolationCut = cms.double(9999.)   




# Keep additional PF information for taus
# embed in AOD externally stored leading PFChargedHadron candidate
process.patTausPFlow.embedLeadPFChargedHadrCand = cms.bool(True)  
# embed in AOD externally stored signal PFChargedHadronCandidates
process.patTausPFlow.embedSignalPFChargedHadrCands = cms.bool(True)  
# embed in AOD externally stored signal PFGammaCandidates
process.patTausPFlow.embedSignalPFGammaCands = cms.bool(True) 
# embed in AOD externally stored isolation PFChargedHadronCandidates
process.patTausPFlow.embedIsolationPFChargedHadrCands = cms.bool(True) 
# embed in AOD externally stored isolation PFGammaCandidates
process.patTausPFlow.embedIsolationPFGammaCands = cms.bool(True)
# embed in AOD externally stored leading PFChargedHadron candidate
process.patTaus.embedLeadPFChargedHadrCand = cms.bool(True)  
# embed in AOD externally stored signal PFChargedHadronCandidates 
process.patTaus.embedSignalPFChargedHadrCands = cms.bool(True)  
# embed in AOD externally stored signal PFGammaCandidates
process.patTaus.embedSignalPFGammaCands = cms.bool(True) 
# embed in AOD externally stored isolation PFChargedHadronCandidates 
process.patTaus.embedIsolationPFChargedHadrCands = cms.bool(True) 
# embed in AOD externally stored isolation PFGammaCandidates
process.patTaus.embedIsolationPFGammaCands = cms.bool(True)

# turn to false when running on data
if options.useData :
    removeMCMatching( process, ['All'] )

###############################
###### Electron ID ############
###############################

process.load('EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi') 
process.eidMVASequence = cms.Sequence(  process.mvaTrigV0 + process.mvaNonTrigV0 )
#Electron ID
process.patElectronsPFlow.electronIDSources.mvaTrigV0    = cms.InputTag("mvaTrigV0")
process.patElectronsPFlow.electronIDSources.mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0") 
process.patPF2PATSequencePFlow.replace( process.patElectronsPFlow, process.eidMVASequence * process.patElectronsPFlow )


#Convesion Rejection
# this should be your last selected electron collection name since currently index is used to match with electron later. We can fix this using reference pointer.
process.patConversionsPFlow = cms.EDProducer("PATConversionProducer",
                                             electronSource = cms.InputTag("selectedPatElectronsPFlow")      
                                             )
process.patPF2PATSequencePFlow += process.patConversionsPFlow


###############################
###### Bare KT 0.6 jets #######
###############################

from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
from RecoJets.JetProducers.kt4PFJets_cfi import *
process.kt6PFJetsForIsolation =  kt4PFJets.clone(
    rParam = 0.6,
    doRhoFastjet = True,
    Rho_EtaMax = cms.double(2.5)
    )

###############################
###### Bare CA 0.8 jets #######
###############################
from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
process.ca8PFJetsPFlow = ca4PFJets.clone(
    rParam = cms.double(0.8),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    Rho_EtaMax = cms.double(6.0),
    Ghost_EtaMax = cms.double(7.0)
    )



###############################
###### AK 0.7 jets ############
###############################
process.ak7PFlow = process.pfJetsPFlow.clone(
	rParam = cms.double(0.7)
    )


###############################
###### AK 0.8 jets ############
###############################
process.ak8PFlow = process.pfJetsPFlow.clone(
	rParam = cms.double(0.8)
    )


###############################
###### AK 0.5 jets groomed ####
###############################

from RecoJets.JetProducers.ak5PFJetsTrimmed_cfi import ak5PFJetsTrimmed
process.ak5TrimmedPFlow = ak5PFJetsTrimmed.clone(
    src = process.pfJetsPFlow.src,
    doAreaFastjet = cms.bool(True)
    )

from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsFiltered
process.ak5FilteredPFlow = ak5PFJetsFiltered.clone(
    src = process.pfJetsPFlow.src,
    doAreaFastjet = cms.bool(True)
    )

from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
process.ak5PrunedPFlow = ak5PFJetsPruned.clone(
    src = process.pfJetsPFlow.src,
    doAreaFastjet = cms.bool(True)
    )



###############################
###### AK 0.7 jets groomed ####
###############################

process.ak7TrimmedPFlow = process.ak5TrimmedPFlow.clone(
	src = process.pfJetsPFlow.src,
	rParam = cms.double(0.7)
    )

process.ak7FilteredPFlow = process.ak5FilteredPFlow.clone(
	src = process.pfJetsPFlow.src,
	rParam = cms.double(0.7)
	)

process.ak7PrunedPFlow = process.ak5PrunedPFlow.clone(
	src = process.pfJetsPFlow.src,
	rParam = cms.double(0.7)
    )


process.ak7TrimmedGenJetsNoNu = ak5GenJets.clone(
	rParam = cms.double(0.7),
	src = cms.InputTag("genParticlesForJetsNoNu"),
	useTrimming = cms.bool(True),
	rFilt = cms.double(0.2),
	trimPtFracMin = cms.double(0.03),
	)

process.ak7FilteredGenJetsNoNu = ak5GenJets.clone(
	rParam = cms.double(0.7),
	src = cms.InputTag("genParticlesForJetsNoNu"),
	useFiltering = cms.bool(True),
	nFilt = cms.int32(3),
	rFilt = cms.double(0.3),
	writeCompound = cms.bool(True),
	jetCollInstanceName=cms.string("SubJets")
	)



process.ak7PrunedGenJetsNoNu = ak5GenJets.clone(
	SubJetParameters,
	rParam = cms.double(0.7),
	src = cms.InputTag("genParticlesForJetsNoNu"),
	usePruning = cms.bool(True),
	writeCompound = cms.bool(True),
	jetCollInstanceName=cms.string("SubJets")
	)



###############################
###### AK 0.8 jets groomed ####
###############################

process.ak8TrimmedPFlow = process.ak5TrimmedPFlow.clone(
	src = process.pfJetsPFlow.src,
	rParam = cms.double(0.8)
    )

process.ak8FilteredPFlow = process.ak5FilteredPFlow.clone(
	src = process.pfJetsPFlow.src,
	rParam = cms.double(0.8)
	)

process.ak8PrunedPFlow = process.ak5PrunedPFlow.clone(
	src = process.pfJetsPFlow.src,
	rParam = cms.double(0.8)
    )

###############################
###### CA8 Pruning Setup ######
###############################


# Pruned PF Jets
process.caPrunedPFlow = process.ak5PrunedPFlow.clone(
	jetAlgorithm = cms.string("CambridgeAachen"),
	rParam       = cms.double(0.8)
)


process.caPrunedGen = process.ca8GenJetsNoNu.clone(
	SubJetParameters,
	usePruning = cms.bool(True),
	useExplicitGhosts = cms.bool(True),
	writeCompound = cms.bool(True),
	jetCollInstanceName=cms.string("SubJets")
)

###############################
###### CA8 Filtered Setup #####
###############################


# Filtered PF Jets
process.caFilteredPFlow = ak5PFJetsFiltered.clone(
	src = cms.InputTag('pfNoElectron'+postfix),
	jetAlgorithm = cms.string("CambridgeAachen"),
	rParam       = cms.double(1.2),
	writeCompound = cms.bool(True),
	doAreaFastjet = cms.bool(True),
	jetPtMin = cms.double(100.0)
)

from RecoJets.JetProducers.ak5PFJetsFiltered_cfi import ak5PFJetsMassDropFiltered
process.caMassDropFilteredPFlow = ak5PFJetsMassDropFiltered.clone(
	src = cms.InputTag('pfNoElectron'+postfix),
	jetAlgorithm = cms.string("CambridgeAachen"),
	rParam       = cms.double(1.2),
	writeCompound = cms.bool(True),
	doAreaFastjet = cms.bool(True),
	jetPtMin = cms.double(100.0)
)


process.caFilteredGenJetsNoNu = process.ca8GenJetsNoNu.clone(
	nFilt = cms.int32(2),
	rFilt = cms.double(0.3),
	useFiltering = cms.bool(True),
	useExplicitGhosts = cms.bool(True),
	writeCompound = cms.bool(True),
	rParam       = cms.double(1.2),
	jetCollInstanceName=cms.string("SubJets"),
	jetPtMin = cms.double(100.0)
)

process.caMassDropFilteredGenJetsNoNu = process.caFilteredGenJetsNoNu.clone(
        src = cms.InputTag('genParticlesForJetsNoNu'),
	useMassDropTagger = cms.bool(True),
	muCut = cms.double(0.667),
	yCut = cms.double(0.08)
)



###############################
#### CATopTag Setup ###########
###############################

# CATopJet PF Jets
# with adjacency 
process.caTopTagPFlow = cms.EDProducer(
    "CATopJetProducer",
    PFJetParameters.clone( src = cms.InputTag('pfNoElectron'+postfix),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(False),
			   jetPtMin = cms.double(100.0)
                           ),
    AnomalousCellParameters,
    CATopJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.8),
    writeCompound = cms.bool(True)
    )

process.caHEPTopTagPFlow = process.caTopTagPFlow.clone(
	rParam = cms.double(1.5),
	tagAlgo = cms.int32(2)
)


process.CATopTagInfosPFlow = cms.EDProducer("CATopJetTagger",
                                    src = cms.InputTag("caTopTagPFlow"),
                                    TopMass = cms.double(171),
                                    TopMassMin = cms.double(0.),
                                    TopMassMax = cms.double(250.),
                                    WMass = cms.double(80.4),
                                    WMassMin = cms.double(0.0),
                                    WMassMax = cms.double(200.0),
                                    MinMassMin = cms.double(0.0),
                                    MinMassMax = cms.double(200.0),
                                    verbose = cms.bool(False)
                                    )

process.CATopTagInfosHEPTopTagPFlow = process.CATopTagInfosPFlow.clone(
	src = cms.InputTag("caHEPTopTagPFlow")
)

process.caTopTagGen = cms.EDProducer(
    "CATopJetProducer",
    GenJetParameters.clone(src = cms.InputTag("genParticlesForJetsNoNu"),
                           doAreaFastjet = cms.bool(False),
                           doRhoFastjet = cms.bool(False)),
    AnomalousCellParameters,
    CATopJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.8),
    writeCompound = cms.bool(True)
    )

process.caHEPTopTagGen = process.caTopTagGen.clone(
	rParam = cms.double(1.5)
)

process.CATopTagInfosGen = cms.EDProducer("CATopJetTagger",
                                          src = cms.InputTag("caTopTagGen"),
                                          TopMass = cms.double(171),
                                          TopMassMin = cms.double(0.),
                                          TopMassMax = cms.double(250.),
                                          WMass = cms.double(80.4),
                                          WMassMin = cms.double(0.0),
                                          WMassMax = cms.double(200.0),
                                          MinMassMin = cms.double(0.0),
                                          MinMassMax = cms.double(200.0),
                                          verbose = cms.bool(False)
                                         )



# CATopJet PF Jets

for ipostfix in [postfix] :
    for module in (
        getattr(process,"ca8PFJets" + ipostfix),
        getattr(process,"CATopTagInfos" + ipostfix),
        getattr(process,"CATopTagInfosHEPTopTag" + ipostfix),
        getattr(process,"caTopTag" + ipostfix),
        getattr(process,"caHEPTopTag" + ipostfix),
        getattr(process,"caPruned" + ipostfix)
        ) :
        getattr(process,"patPF2PATSequence"+ipostfix).replace( getattr(process,"pfNoElectron"+ipostfix), getattr(process,"pfNoElectron"+ipostfix)*module )


    if options.useExtraJetColls : 
	    for module in (
		getattr(process,"ak5Trimmed" + ipostfix),
		getattr(process,"ak5Filtered" + ipostfix),
		getattr(process,"ak5Pruned" + ipostfix),
		getattr(process,"ak7Trimmed" + ipostfix),
		getattr(process,"ak7Filtered" + ipostfix),
		getattr(process,"ak7Pruned" + ipostfix),
		getattr(process,"ak7" + ipostfix),
		getattr(process,"ak8Trimmed" + ipostfix),
		getattr(process,"ak8Filtered" + ipostfix),
		getattr(process,"ak8Pruned" + ipostfix),
		getattr(process,"ak8" + ipostfix),
		getattr(process,"caFiltered" + ipostfix),
		getattr(process,"caMassDropFiltered" + ipostfix)
		) :
		    getattr(process,"patPF2PATSequence"+ipostfix).replace( getattr(process,"pfNoElectron"+ipostfix), getattr(process,"pfNoElectron"+ipostfix)*module )



# Use the good primary vertices everywhere. 
for imod in [process.patMuonsPFlow,
             process.patElectronsPFlow,
             process.patMuons,
             process.patElectrons] :
    imod.pvSrc = "goodOfflinePrimaryVertices"
    imod.embedTrack = True
    

addJetCollection(process, 
                 cms.InputTag('ca8PFJetsPFlow'),
                 'CA8', 'PF',
                 doJTA=True,
                 doBTagging=True,
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=True,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )


addJetCollection(process, 
                 cms.InputTag('caPrunedPFlow'),
                 'CA8Pruned', 'PF',
                 doJTA=False,
                 doBTagging=True,
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=True,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )



addJetCollection(process, 
                 cms.InputTag('caTopTagPFlow'),
                 'CATopTag', 'PF',
                 doJTA=True,
                 doBTagging=True,
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=True,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )

addJetCollection(process, 
                 cms.InputTag('caHEPTopTagPFlow'),
                 'CAHEPTopTag', 'PF',
                 doJTA=True,
                 doBTagging=True,
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=True,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )


if options.useExtraJetColls: 
	addJetCollection(process, 
			 cms.InputTag('caFilteredPFlow'),
			 'CA12Filtered', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
			 doJetID = False
			 )


	addJetCollection(process, 
			 cms.InputTag('caMassDropFilteredPFlow'),
			 'CA12MassDropFiltered', 'PF',
			 doJTA=True,
			 doBTagging=True,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
			 doJetID = False
			 )


	addJetCollection(process, 
			 cms.InputTag('caMassDropFilteredPFlow', 'SubJets'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
			 'CA12MassDropFilteredSubjets', 'PF',
			 doJTA=True,            # Run Jet-Track association & JetCharge
			 doBTagging=True,       # Run b-tagging
			 jetCorrLabel=None,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak5GenJetsNoNu"),
			 doJetID = False
			 )

	addJetCollection(process, 
			 cms.InputTag('ak5PrunedPFlow'),
			 'AK5Pruned', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak5GenJetsNoNu"),
			 doJetID = False
			 )


	addJetCollection(process, 
			 cms.InputTag('ak5FilteredPFlow'),
			 'AK5Filtered', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak5GenJetsNoNu"),
			 doJetID = False
			 )

	addJetCollection(process, 
			 cms.InputTag('ak5TrimmedPFlow'),
			 'AK5Trimmed', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak5GenJetsNoNu"),
			 doJetID = False
			 )


	addJetCollection(process, 
			 cms.InputTag('ak7PFlow'),
			 'AK7', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak7GenJetsNoNu"),
			 doJetID = False
			 )

	addJetCollection(process, 
			 cms.InputTag('ak7PrunedPFlow'),
			 'AK7Pruned', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak7GenJetsNoNu"),
			 doJetID = False
			 )


	addJetCollection(process, 
			 cms.InputTag('ak7FilteredPFlow'),
			 'AK7Filtered', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak7GenJetsNoNu"),
			 doJetID = False
			 )

	addJetCollection(process, 
			 cms.InputTag('ak7TrimmedPFlow'),
			 'AK7Trimmed', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak7GenJetsNoNu"),
			 doJetID = False
			 )





	addJetCollection(process, 
			 cms.InputTag('ak8PFlow'),
			 'AK8', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak8GenJetsNoNu"),
			 doJetID = False
			 )

	addJetCollection(process, 
			 cms.InputTag('ak8PrunedPFlow'),
			 'AK8Pruned', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak8GenJetsNoNu"),
			 doJetID = False
			 )


	addJetCollection(process, 
			 cms.InputTag('ak8FilteredPFlow'),
			 'AK8Filtered', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak8GenJetsNoNu"),
			 doJetID = False
			 )

	addJetCollection(process, 
			 cms.InputTag('ak8TrimmedPFlow'),
			 'AK8Trimmed', 'PF',
			 doJTA=False,
			 doBTagging=False,
			 jetCorrLabel=inputJetCorrLabel,
			 doType1MET=True,
			 doL1Cleaning=False,
			 doL1Counters=False,
			 genJetCollection = cms.InputTag("ak8GenJetsNoNu"),
			 doJetID = False
			 )

switchJetCollection(process,cms.InputTag('ak5PFJets'),
		    doJTA        = False,
		    doBTagging   = False,
		    jetCorrLabel = inputJetCorrLabel,
		    doType1MET   = True,
		    genJetCollection=cms.InputTag("ak5GenJetsNoNu"),
		    doJetID      = False
		    )

for icorr in [process.patJetCorrFactors,
	      process.patJetCorrFactorsCATopTagPF,
	      process.patJetCorrFactorsCAHEPTopTagPF,
              process.patJetCorrFactorsCA8PrunedPF,
              process.patJetCorrFactorsCA8PF ] :
    icorr.rho = cms.InputTag("kt6PFJets", "rho")


if options.useExtraJetColls: 
	for icorr in [process.patJetCorrFactorsAK5PrunedPF,
		      process.patJetCorrFactorsAK5FilteredPF,
		      process.patJetCorrFactorsAK5TrimmedPF,
		      process.patJetCorrFactorsAK7PF,
		      process.patJetCorrFactorsAK7PrunedPF,
		      process.patJetCorrFactorsAK7FilteredPF,
		      process.patJetCorrFactorsAK7TrimmedPF,
		      process.patJetCorrFactorsAK8PF,
		      process.patJetCorrFactorsAK8PrunedPF,
		      process.patJetCorrFactorsAK8FilteredPF,
		      process.patJetCorrFactorsAK8TrimmedPF] :
	    icorr.rho = cms.InputTag("kt6PFJets", "rho")



###############################
### TagInfo and Matching Setup#
###############################

# Do some configuration of the jet substructure things
for jetcoll in (process.patJetsPFlow,
		process.patJets,
                process.patJetsCA8PF,
                process.patJetsCA8PrunedPF,
                process.patJetsCATopTagPF,
                process.patJetsCAHEPTopTagPF
                ) :
    if options.useData == False :
        jetcoll.embedGenJetMatch = False
        jetcoll.getJetMCFlavour = True
        jetcoll.addGenPartonMatch = True
    # Add the calo towers and PFCandidates.
    # I'm being a little tricksy here, because I only
    # actually keep the products if the "writeFat" switch
    # is on. However, this allows for overlap checking
    # with the Refs so satisfies most use cases without
    # having to add to the object size
    jetcoll.addBTagInfo = False
    jetcoll.embedCaloTowers = True
    jetcoll.embedPFCandidates = True

# Add CATopTag and b-tag info... piggy-backing on b-tag functionality
process.patJetsPFlow.addBTagInfo = True
process.patJetsCATopTagPF.addBTagInfo = True
process.patJetsCAHEPTopTagPF.addBTagInfo = True
process.patJetsCA8PrunedPF.addBTagInfo = True


# Do some configuration of the jet substructure things
if options.useExtraJetColls: 
	for jetcoll in (process.patJetsAK5TrimmedPF,
			process.patJetsAK5PrunedPF,
			process.patJetsAK5FilteredPF,
			process.patJetsAK7PF,
			process.patJetsAK7TrimmedPF,
			process.patJetsAK7PrunedPF,
			process.patJetsAK7FilteredPF,
			process.patJetsAK8PF,
			process.patJetsAK8TrimmedPF,
			process.patJetsAK8PrunedPF,
			process.patJetsAK8FilteredPF,
			process.patJetsCA12FilteredPF,
			process.patJetsCA12MassDropFilteredPF
			) :
	    if options.useData == False :
		jetcoll.embedGenJetMatch = False
		jetcoll.getJetMCFlavour = True
		jetcoll.addGenPartonMatch = True
	    # Add the calo towers and PFCandidates.
	    # I'm being a little tricksy here, because I only
	    # actually keep the products if the "writeFat" switch
	    # is on. However, this allows for overlap checking
	    # with the Refs so satisfies most use cases without
	    # having to add to the object size
	    jetcoll.addBTagInfo = False
	    jetcoll.embedCaloTowers = True
	    jetcoll.embedPFCandidates = True

	# Add CATopTag and b-tag info... piggy-backing on b-tag functionality
	process.patJetsCA12MassDropFilteredPF.addBTagInfo = True


#################################################
#### Fix the PV collections for the future ######
#################################################
for module in [process.patJetCorrFactors,
               process.patJetCorrFactorsPFlow,
               process.patJetCorrFactorsCATopTagPF,
               process.patJetCorrFactorsCAHEPTopTagPF,
               process.patJetCorrFactorsCA8PrunedPF,
               process.patJetCorrFactorsCA8PF
               ]:
    module.primaryVertices = "goodOfflinePrimaryVertices"

    
if options.useExtraJetColls: 
	for module in [process.patJetCorrFactorsCA12FilteredPF,
		       process.patJetCorrFactorsCA12MassDropFilteredPF,
		       process.patJetCorrFactorsAK5TrimmedPF,
		       process.patJetCorrFactorsAK5PrunedPF,
		       process.patJetCorrFactorsAK5FilteredPF,
		       process.patJetCorrFactorsAK7PF,
		       process.patJetCorrFactorsAK7TrimmedPF,
		       process.patJetCorrFactorsAK7PrunedPF,
		       process.patJetCorrFactorsAK7FilteredPF,
		       process.patJetCorrFactorsAK8PF,
		       process.patJetCorrFactorsAK8TrimmedPF,
		       process.patJetCorrFactorsAK8PrunedPF,
		       process.patJetCorrFactorsAK8FilteredPF
		       ]:
	    module.primaryVertices = "goodOfflinePrimaryVertices"


###############################
#### Selections Setup #########
###############################

# AK5 Jets
process.selectedPatJetsPFlow.cut = cms.string("pt > 5")
process.patJetsPFlow.addTagInfos = True
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAODPFlow")
    )
process.patJetsPFlow.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')

# CA8 jets
process.selectedPatJetsCA8PF.cut = cms.string("pt > 20")

# CA8 Pruned jets
process.selectedPatJetsCA8PrunedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")


# CA8 TopJets
process.selectedPatJetsCATopTagPF.cut = cms.string("pt > 150 & abs(rapidity) < 2.5")
process.patJetsCATopTagPF.addTagInfos = True
process.patJetsCATopTagPF.tagInfoSources = cms.VInputTag(
    cms.InputTag('CATopTagInfosPFlow')
    )

# CA1.5 HEPTopTagTopJets
process.selectedPatJetsCAHEPTopTagPF.cut = cms.string("pt > 150 & abs(rapidity) < 2.5")
process.patJetsCAHEPTopTagPF.addTagInfos = True
process.patJetsCAHEPTopTagPF.tagInfoSources = cms.VInputTag(
    cms.InputTag('CATopTagInfosHEPTopTagPFlow')
    )


if options.useExtraJetColls: 
	# CA12 Filtered jets
	process.selectedPatJetsCA12FilteredPF.cut = cms.string("pt > 150 & abs(rapidity) < 2.5")
	process.selectedPatJetsCA12MassDropFilteredPF.cut = cms.string("pt > 150 & abs(rapidity) < 2.5")

	# AK5 groomed jets
	process.selectedPatJetsAK5PrunedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
	process.selectedPatJetsAK5TrimmedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
	process.selectedPatJetsAK5FilteredPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")


	# AK7 groomed jets
	process.selectedPatJetsAK7PF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
	process.selectedPatJetsAK7PrunedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
	process.selectedPatJetsAK7TrimmedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
	process.selectedPatJetsAK7FilteredPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")


	# AK8 groomed jets
	process.selectedPatJetsAK8PF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
	process.selectedPatJetsAK8PrunedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
	process.selectedPatJetsAK8TrimmedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
	process.selectedPatJetsAK8FilteredPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
	


# electrons
process.selectedPatElectrons.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patElectrons.embedTrack = cms.bool(True)
process.selectedPatElectronsPFlow.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patElectronsPFlow.embedTrack = cms.bool(True)
# muons
process.selectedPatMuons.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patMuons.embedTrack = cms.bool(True)
process.selectedPatMuonsPFlow.cut = cms.string("pt > 10.0 & abs(eta) < 2.5")
process.patMuonsPFlow.embedTrack = cms.bool(True)
# taus
process.selectedPatTausPFlow.cut = cms.string("pt > 10.0 & abs(eta) < 3")
process.selectedPatTaus.cut = cms.string("pt > 10.0 & abs(eta) < 3")
process.patTausPFlow.isoDeposits = cms.PSet()
process.patTaus.isoDeposits = cms.PSet()
# photons
process.patPhotonsPFlow.isoDeposits = cms.PSet()
process.patPhotons.isoDeposits = cms.PSet()


# Apply jet ID to all of the jets upstream. We aren't going to screw around
# with this, most likely. So, we don't really to waste time with it
# at the analysis level. 
from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsPFlow = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsPFlow")
                                        )
process.goodPatJetsCA8PF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsCA8PF")
                                        )
process.goodPatJetsCA8PrunedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                              filterParams = pfJetIDSelector.clone(),
                                              src = cms.InputTag("selectedPatJetsCA8PrunedPF")
                                              )

process.goodPatJetsCATopTagPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                             filterParams = pfJetIDSelector.clone(),
                                             src = cms.InputTag("selectedPatJetsCATopTagPF")
                                             )

process.goodPatJetsCAHEPTopTagPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                             filterParams = pfJetIDSelector.clone(),
                                             src = cms.InputTag("selectedPatJetsCAHEPTopTagPF")
                                             )



if options.useExtraJetColls:
	process.goodPatJetsCA12FilteredPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsCA12FilteredPF")
						      )

	process.goodPatJetsCA12MassDropFilteredPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsCA12MassDropFilteredPF")
						      )

	process.goodPatJetsAK5PrunedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK5PrunedPF")
						      )
	process.goodPatJetsAK5FilteredPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK5FilteredPF")
						      )
	process.goodPatJetsAK5TrimmedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK5TrimmedPF")
						      )

	process.goodPatJetsAK7PF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK7PF")
						      )
	process.goodPatJetsAK7PrunedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK7PrunedPF")
						      )
	process.goodPatJetsAK7FilteredPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK7FilteredPF")
						      )
	process.goodPatJetsAK7TrimmedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK7TrimmedPF")
						      )



	process.goodPatJetsAK8PF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK8PF")
						      )
	process.goodPatJetsAK8PrunedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK8PrunedPF")
						      )
	process.goodPatJetsAK8FilteredPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK8FilteredPF")
						      )
	process.goodPatJetsAK8TrimmedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
						      filterParams = pfJetIDSelector.clone(),
						      src = cms.InputTag("selectedPatJetsAK8TrimmedPF")
						      )



if options.writeSimpleInputs :
	process.pfInputs = cms.EDProducer(
	    "CandViewNtpProducer", 
	    src = cms.InputTag('selectedPatJetsCA8PF', 'pfCandidates'),
	    lazyParser = cms.untracked.bool(True),
	    eventInfo = cms.untracked.bool(False),
	    variables = cms.VPSet(
		cms.PSet(
		    tag = cms.untracked.string("px"),
		    quantity = cms.untracked.string("px")
		    ),
		cms.PSet(
		    tag = cms.untracked.string("py"),
		    quantity = cms.untracked.string("py")
		    ),
		cms.PSet(
		    tag = cms.untracked.string("pz"),
		    quantity = cms.untracked.string("pz")
		    ),
		cms.PSet(
		    tag = cms.untracked.string("energy"),
		    quantity = cms.untracked.string("energy")
		    ),
		cms.PSet(
		    tag = cms.untracked.string("pdgId"),
		    quantity = cms.untracked.string("pdgId")
		    )
		)
	)


if options.useExtraJetColls:
	process.ak5Lite = cms.EDProducer(
	    "CandViewNtpProducer", 
	    src = cms.InputTag('goodPatJetsPFlow'),
	    lazyParser = cms.untracked.bool(True),
	    eventInfo = cms.untracked.bool(False),
	    variables = cms.VPSet(
			cms.PSet(
				tag = cms.untracked.string("px"),
				quantity = cms.untracked.string("px")
				),
			cms.PSet(
				tag = cms.untracked.string("py"),
				quantity = cms.untracked.string("py")
				),
			cms.PSet(
				tag = cms.untracked.string("pz"),
				quantity = cms.untracked.string("pz")
				),
			cms.PSet(
				tag = cms.untracked.string("energy"),
				quantity = cms.untracked.string("energy")
				),
			cms.PSet(
				tag = cms.untracked.string("jetArea"),
				quantity = cms.untracked.string("jetArea")
				),
			cms.PSet(
				tag = cms.untracked.string("jecFactor"),
				quantity = cms.untracked.string("jecFactor(0)")
				)
				)
	)


	process.ak5TrimmedLite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK5TrimmedPF')
		)

	process.ak5PrunedLite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK5PrunedPF')
		)

	process.ak5FilteredLite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK5FilteredPF')
		)

	process.ak7Lite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK7PF')
		)

	process.ak7TrimmedLite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK7TrimmedPF')
		)

	process.ak7PrunedLite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK7PrunedPF')
		)

	process.ak7FilteredLite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK7FilteredPF')
		)




	process.ak7TrimmedGenLite = cms.EDProducer(
	    "CandViewNtpProducer", 
	    src = cms.InputTag('ak7TrimmedGenJetsNoNu'),
	    lazyParser = cms.untracked.bool(True),
	    eventInfo = cms.untracked.bool(False),
	    variables = cms.VPSet(
			cms.PSet(
				tag = cms.untracked.string("px"),
				quantity = cms.untracked.string("px")
				),
			cms.PSet(
				tag = cms.untracked.string("py"),
				quantity = cms.untracked.string("py")
				),
			cms.PSet(
				tag = cms.untracked.string("pz"),
				quantity = cms.untracked.string("pz")
				),
			cms.PSet(
				tag = cms.untracked.string("energy"),
				quantity = cms.untracked.string("energy")
				)
				)
	)


	process.ak7PrunedGenLite = process.ak7TrimmedGenLite.clone(
		src = cms.InputTag('ak7PrunedGenJetsNoNu')
		)

	process.ak7FilteredGenLite = process.ak7TrimmedGenLite.clone(
		src = cms.InputTag('ak7FilteredGenJetsNoNu')
		)

        process.ca8PrunedGenLite = process.ak7TrimmedGenLite.clone(
                src = cms.InputTag('caPrunedGen')
                )

        process.ca12FilteredGenLite = process.ak7TrimmedGenLite.clone(
                src = cms.InputTag('caFilteredGenJetsNoNu')
                )

        process.ca12MassDropFilteredGenLite = process.ak7TrimmedGenLite.clone(
                src = cms.InputTag('caMassDropFilteredGenJetsNoNu')
                )



	process.ak8Lite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK8PF')
		)

	process.ak8TrimmedLite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK8TrimmedPF')
		)

	process.ak8PrunedLite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK8PrunedPF')
		)

	process.ak8FilteredLite = process.ak5Lite.clone(
		src = cms.InputTag('goodPatJetsAK8FilteredPF')
		)


## IVF and BCandidate producer for Vbb cross check analysis
process.load('RecoVertex/AdaptiveVertexFinder/inclusiveVertexing_cff')


# let it run

process.filtersSeq = cms.Sequence(
   process.primaryVertexFilter *
   process.noscraping *
   process.HBHENoiseFilter *
   process.CSCTightHaloFilter *
   process.hcalLaserEventFilter *
   process.EcalDeadCellTriggerPrimitiveFilter *
   process.goodVertices * process.trackingFailureFilter *
   process.eeBadScFilter
)



process.patseq = cms.Sequence(
    process.filtersSeq*
    process.goodOfflinePrimaryVertices*
    process.softElectronCands*
    process.inclusiveVertexing*
    process.genParticlesForJetsNoNu*
    process.ca8GenJetsNoNu*
    process.ak8GenJetsNoNu*
    process.caFilteredGenJetsNoNu*
    process.caMassDropFilteredGenJetsNoNu*
    getattr(process,"patPF2PATSequence"+postfix)*
    process.patDefaultSequence*
    process.goodPatJetsPFlow*
    process.goodPatJetsCA8PF*
    process.goodPatJetsCA8PrunedPF*
    process.goodPatJetsCATopTagPF*
    process.goodPatJetsCAHEPTopTagPF*
    process.flavorHistorySeq*
    process.prunedGenParticles*
    process.caPrunedGen*
    process.caTopTagGen*
    process.CATopTagInfosGen*
    process.kt6PFJetsForIsolation
#    process.miniPFLeptonSequence
#    process.EventFilter
    )

if options.useExtraJetColls:
	process.extraJetSeq = cms.Sequence(
		process.ak7TrimmedGenJetsNoNu*
		process.ak7FilteredGenJetsNoNu*
		process.ak7PrunedGenJetsNoNu*
		process.goodPatJetsCA12FilteredPF*
		process.goodPatJetsCA12MassDropFilteredPF*
		process.goodPatJetsAK5TrimmedPF*
		process.goodPatJetsAK5FilteredPF*
		process.goodPatJetsAK5PrunedPF*
		process.goodPatJetsAK7PF*
		process.goodPatJetsAK7TrimmedPF*
		process.goodPatJetsAK7FilteredPF*
		process.goodPatJetsAK7PrunedPF*
		process.goodPatJetsAK8PF*
		process.goodPatJetsAK8TrimmedPF*
		process.goodPatJetsAK8FilteredPF*
		process.goodPatJetsAK8PrunedPF*
		process.ak5Lite*
		process.ak5TrimmedLite*
		process.ak5FilteredLite*
		process.ak5PrunedLite*
		process.ak7Lite*
		process.ak7TrimmedLite*
		process.ak7FilteredLite*
		process.ak7PrunedLite*
		process.ak7TrimmedGenLite*
		process.ak7FilteredGenLite*
		process.ak7PrunedGenLite*
		process.ak8Lite*
		process.ak8TrimmedLite*
		process.ak8FilteredLite*
		process.ak8PrunedLite*
                process.ca8PrunedGenLite*
                process.ca12FilteredGenLite*
                process.ca12MassDropFilteredGenLite
	)
	process.patseq *= process.extraJetSeq


if options.useData :
    process.patseq.remove( process.genParticlesForJetsNoNu )
    process.patseq.remove( process.genJetParticles )
    process.patseq.remove( process.ak8GenJetsNoNu )
    process.patseq.remove( process.ca8GenJetsNoNu )
    process.patseq.remove( process.caFilteredGenJetsNoNu )
    process.patseq.remove( process.flavorHistorySeq )
    process.patseq.remove( process.caPrunedGen )
    process.patseq.remove( process.caTopTagGen )
    process.patseq.remove( process.CATopTagInfosGen )
    process.patseq.remove( process.prunedGenParticles )
    process.patseq.remove( process.caMassDropFilteredGenJetsNoNu )

    if options.useExtraJetColls:
	    process.patseq.remove( process.ak8GenJetsNoNu )
	    process.patseq.remove( process.caFilteredGenJetsNoNu )
	    process.patseq.remove( process.ak7TrimmedGenJetsNoNu )
	    process.patseq.remove( process.ak7FilteredGenJetsNoNu )
	    process.patseq.remove( process.ak7PrunedGenJetsNoNu )
	    process.patseq.remove( process.ak7TrimmedGenLite )
	    process.patseq.remove( process.ak7FilteredGenLite )
	    process.patseq.remove( process.ak7PrunedGenLite )
            process.patseq.remove( process.ca8PrunedGenLite )
            process.patseq.remove( process.ca12FilteredGenLite )
            process.patseq.remove( process.ca12MassDropFilteredGenLite )

if options.runOnFastSim:
    process.patseq.remove( process.HBHENoiseFilter )

if options.writeSimpleInputs :
	process.patseq *= cms.Sequence(process.pfInputs)

if options.useSusyFilter :
	process.patseq.remove( process.HBHENoiseFilter )
	process.load( 'PhysicsTools.HepMCCandAlgos.modelfilter_cfi' )
	process.modelSelector.parameterMins = [500.,    0.] # mstop, mLSP
	process.modelSelector.parameterMaxs  = [7000., 200.] # mstop, mLSP
	process.p0 = cms.Path(
		process.modelSelector *
		process.patseq
	)



else :
	process.p0 = cms.Path(
		process.patseq
              * process.MiniTreeProduction
              * process.MyModule
              #* process.rootNTuples
	)





process.out.SelectEvents.SelectEvents = cms.vstring('p0')

# rename output file
if options.useData :
    if options.writeFat :
        process.out.fileName = cms.untracked.string(options.tlbsmTag + '_data_fat.root')
    else :
        process.out.fileName = cms.untracked.string(options.tlbsmTag + '_data.root')
else :
    if options.writeFat :
        process.out.fileName = cms.untracked.string(options.tlbsmTag + '_mc_fat.root')
    else :
        process.out.fileName = cms.untracked.string(options.tlbsmTag + '_mc.root')


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
process.maxEvents.input = -1
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")

del process.outpath

process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")



process.out.outputCommands = [
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_goodPat*_*_*',
    'drop patJets_selectedPat*_*_*',
    'keep patJets_selectedPatJetsCA12MassDropFilteredSubjetsPF*_*_*',
    'drop *_selectedPatJets_*_*',    
    'keep *_patMETs*_*_*',
#    'keep *_offlinePrimaryVertices*_*_*',
#    'keep *_kt6PFJets*_*_*',
    'keep *_goodOfflinePrimaryVertices*_*_*',    
    'drop patPFParticles_*_*_*',
#    'drop patTaus_*_*_*',
    'keep recoPFJets_caPruned*_*_*',
    'keep recoPFJets_ca*Filtered*_*_*',
    'keep recoPFJets_caTopTag*_*_*',
    'keep recoPFJets_caHEPTopTag*_*_*',
    'keep patTriggerObjects_patTriggerPFlow_*_*',
    'keep patTriggerFilters_patTriggerPFlow_*_*',
    'keep patTriggerPaths_patTriggerPFlow_*_*',
    'keep patTriggerEvent_patTriggerEventPFlow_*_*',
    'keep *_cleanPatPhotonsTriggerMatch*_*_*',
    'keep *_cleanPatElectronsTriggerMatch*_*_*',
    'keep *_cleanPatMuonsTriggerMatch*_*_*',
    'keep *_cleanPatTausTriggerMatch*_*_*',
    'keep *_cleanPatJetsTriggerMatch*_*_*',
    'keep *_patMETsTriggerMatch*_*_*',
    'keep double_*_*_PAT',
    'keep *_TriggerResults_*_*',
    'keep *_hltTriggerSummaryAOD_*_*',
    'keep *_caTopTagPFlow_*_*',
    'keep *_caPrunedPFlow_*_*',
    'keep *_CATopTagInfosPFlow_*_*',
    'keep *_prunedGenParticles_*_*',
    'drop recoPFCandidates_selectedPatJets*_*_*',
    'keep recoPFCandidates_selectedPatJetsPFlow_*_*',
    'drop CaloTowers_selectedPatJets*_*_*',
    'drop recoBasicJets_*_*_*',
    'keep *_*Lite_*_*',
    'drop patJets_goodPatJetsAK5FilteredPF_*_*',
    'drop patJets_goodPatJetsAK5PrunedPF_*_*',
    'drop patJets_goodPatJetsAK5TrimmedPF_*_*',
    'drop patJets_goodPatJetsAK7PF_*_*',
    'drop patJets_goodPatJetsAK7FilteredPF_*_*',
    'drop patJets_goodPatJetsAK7PrunedPF_*_*',
    'drop patJets_goodPatJetsAK7TrimmedPF_*_*',
    'drop patJets_goodPatJetsAK8PF_*_*',
    'drop patJets_goodPatJetsAK8FilteredPF_*_*',
    'drop patJets_goodPatJetsAK8PrunedPF_*_*',
    'drop patJets_goodPatJetsAK8TrimmedPF_*_*',
    'drop recoGenJets_selectedPatJets*_*_*',
    'keep *_*_rho_*',
    'keep *_patConversions*_*_*',
    'keep *_offlineBeamSpot_*_*',
    'drop *_*atTaus_*_*',
    'keep *_pfType1CorrectedMet_*_*',
    'keep *_pfType1p2CorrectedMet_*_*'
    #'keep recoTracks_generalTracks_*_*'
    ]

if options.useData :
    process.out.outputCommands += ['drop *_MEtoEDMConverter_*_*',
                                   'keep LumiSummary_lumiProducer_*_*'
                                   ]
else :
    process.out.outputCommands += ['keep recoGenJets_ca8GenJetsNoNu_*_*',
				   'keep recoGenJets_ak5GenJetsNoNu_*_*',
				   'keep recoGenJets_ak7GenJetsNoNu_*_*',
				   'keep recoGenJets_ak8GenJetsNoNu_*_*',
				   'keep recoGenJets_caFilteredGenJetsNoNu_*_*',
				   'keep recoGenJets_caPrunedGen_*_*',
				   'keep *_caTopTagGen_*_*',
                                   'keep GenRunInfoProduct_generator_*_*',
                                   'keep GenEventInfoProduct_generator_*_*',
                                   'keep *_flavorHistoryFilter_*_*',
                                   'keep PileupSummaryInfos_*_*_*',
				   'keep recoGenJets_selectedPatJetsPFlow_*_*',
                                   ]

if options.writeFat :

    process.out.outputCommands += [
        'keep *_pfNoElectron*_*_*',
        'keep recoTracks_generalTracks_*_*',
        'keep recoPFCandidates_selectedPatJets*_*_*',
        'keep recoBaseTagInfosOwned_selectedPatJets*_*_*',
        'keep CaloTowers_selectedPatJets*_*_*'
        ]
if options.writeFat or options.writeGenParticles :
    if options.useData == False :
        process.out.outputCommands += [
            'keep *_genParticles_*_*'
            ]


if options.writeSimpleInputs :
	process.out.outputCommands += [
		'keep *_pfInputs_*_*'
		]
        
if options.usePythia8 :
    process.patJetPartonMatch.mcStatus = cms.vint32(23)
    process.patJetPartonMatchPFlow.mcStatus = cms.vint32(23)
    
if options.usePythia6andPythia8 :
    process.patJetPartonMatch.mcStatus = cms.vint32(3,23)
    process.patJetPartonMatchPFlow.mcStatus = cms.vint32(3,23)

#open('junk.py','w').write(process.dumpPython())
