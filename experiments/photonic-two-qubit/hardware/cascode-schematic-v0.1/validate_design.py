"""Check KiCad-exported connectivity against the design contract. Not an ERC engine."""
from pathlib import Path
import csv, json, math, xml.etree.ElementTree as ET

P=Path(__file__).resolve().parent
expected=json.loads((P/'expected_connections.json').read_text())
errors=[];counts={};actual_boards={}
for board in ['Frontend','Receiver_Adapter']:
    tree=ET.parse(P/(board+'.net.xml'))
    actual={};groups={}
    for net in tree.findall('.//nets/net'):
        name=net.get('name');members=[]
        for node in net.findall('node'):
            key=(node.get('ref'),node.get('pin'))
            if key in actual:errors.append(f'duplicate {board} {key}')
            actual[key]=name;members.append(key)
        groups[name]=members
    actual_boards[board]=actual
    for item in [x for x in expected if x['board']==board]:
        key=(item['ref'],item['pin'])
        if actual.get(key)!=item['net']:
            errors.append({'board':board,'pin':key,'expected':item['net'],'got':actual.get(key)})
    for name,members in groups.items():
        if len(members)==1 and not name.startswith('unconnected-'):
            errors.append({'single_pin_net':name,'board':board})
        if name.startswith('unconnected-'):
            for ref,pin in members:
                if not ((ref in ['D101','D102','D103'] and pin=='2') or (ref=='U202' and pin in ['3','9'])):
                    errors.append({'unexpected_unconnected':(board,ref,pin)})
    counts[board]={'components':len(tree.findall('.//components/comp')),'nets':len(groups)}

# Independently stated safety/function invariants from datasheet pin tables.
a=actual_boards['Frontend'];b=actual_boards['Receiver_Adapter']
required={('Q101','2'):'Q1_E',('Q101','4'):'Q1_E',('Q102','2'):'CAS_NODE',('Q102','4'):'CAS_NODE',
 ('Q101','1'):'Q1_B',('Q101','3'):'CAS_NODE',('Q102','1'):'VBCAS',('Q102','3'):'AN_OUT',
 ('U201','4'):'VTH',('U201','6'):'AN_OUT',('U201','12'):'CML_Q',('U201','10'):'CML_QN',
 ('U201','1'):'3V3_CML',('U201','2'):'3V3_CMP',('U201','13'):'GND',
 ('U202','5'):'GND',('U202','10'):'REF2V5',('U202','4'):'GND',
 ('U101','3'):'VSET',('U101','2'):'SERVO_FB',('U101','1'):'SERVO_OUT',
 ('U101','5'):'VCAS_REF',('U101','6'):'VCAS_BUF',('U101','7'):'VCAS_BUF',
 ('D103','1'):'Q1_E',('D103','3'):'Q1_B'}
for key,net in required.items():
    if a.get(key)!=net:errors.append({'invariant':key,'expected':net})
for key,net in {('R401','1'):'3V3_TERM',('R401','2'):'RX_Q',('R402','1'):'3V3_TERM',('R402','2'):'RX_QN',('U401','8'):'RX_Q',('U401','7'):'RX_QN',('U401','6'):'RX_Q',('U401','5'):'RX_QN'}.items():
    if b.get(key)!=net:errors.append({'receiver_invariant':key,'expected':net})

vref=2.5;re=47.;rc=330.;beta=100.;vbe=.75;raw=3.3
vset=vref*1000/(16500+1000);ie=vset/re;ic1=ie*beta/(beta+1);ic2=ic1*beta/(beta+1)
ib1=ie/(beta+1);ib2=ic1/(beta+1)
vcas_ref=vref*10000/(3480+10000);vb2=vcas_ref-100*ib2
# R301 supplies collector chain, base currents and OPA2333 (34uA nominal assumption).
iana=ie+ib2+34e-6;vana=raw-4.7*iana;out=vana-rc*ic2
gain=-rc/(re+.02585/ic1)
rin=beta*(re+.02585/ic1);rbase=1/(1/rin+1/10000)
tau=10e-9*(49.9+10+rbase)
calc={'model':'algebraic approximation; beta=100, VBE=0.75V, no device/corner guarantee',
 'VSET_V':vset,'Q1_IE_A':ie,'Q1_IC_A':ic1,'Q2_IC_A':ic2,'VBCAS_V':vb2,
 'Q1_VB_V':vset+vbe,'Q1_VC_V':vb2-vbe,'Q1_VCE_V':vb2-vbe-vset,
 'Q1_VCB_V':vb2-vbe-(vset+vbe),'3V3_ANA_V':vana,'AN_OUT_idle_V':out,
 'Q2_VCE_V':out-(vb2-vbe),'Q2_VCB_V':out-vb2,'gain_V_per_V':gain,
 'SERVO_OUT_V':vset+vbe+10000*ib1,'REF_load_A':vref/17500+vref/13480,
 'AC_time_constant_s':tau,'AC_droop_100ns_fraction':1-math.exp(-100e-9/tau),
 'DAC_2V2_code':round(2.2/2.5*65536),'threshold_RC_s':100*1e-6,
 'core_thermal_model':'NOT_RUN','manufacturer_SPICE':'NOT_RUN','servo_stability':'NOT_RUN',
 'EM_and_hardware':'NOT_RUN','KiCad_ERC':'NOT_RUN (KiCad 7 CLI has no ERC command)'}
corner=[]
for v in [3.135,3.3,3.465]:
 for sense in [.005,.025,.050,.100]:
  low=out+(v-3.3)+gain*sense;margin=low-vb2
  corner.append({'supply_V':v,'sense_V':sense,'linear_estimate_AN_OUT_V':low,'estimated_Q2_VCB_V':margin,
                 'reserve_ge_0p1V':margin>=.1})
calc['headroom_screen']=corner
result={'connectivity':'PASS' if not errors else 'FAIL','exported_pin_connections_checked':len(expected),
 'critical_invariants_checked':len(required)+8,'boards':counts,'errors':errors,'algebraic_checks':calc}
(P/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'connectivity':result['connectivity'],'pins':len(expected),'errors':errors,'VSET':vset,'Q2_IC_mA':ic2*1e3,'AN_OUT_idle':out,'gain':gain},indent=2))
if errors:raise SystemExit(1)
