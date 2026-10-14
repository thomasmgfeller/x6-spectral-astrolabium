import test from 'node:test';
import assert from 'node:assert/strict';
import {VERSION, information, condition, probabilities, plan, Coordinator, digest} from '../core.mjs';
import {makeCampaign, defaultNodes, defaultTruth, simulate} from '../mechanical.mjs';
import {run, verify} from '../run.mjs';

function toy(states, likelihoods) {
  return {schema:VERSION,campaign_id:'toy',evidence_kind:'SYNTHETIC_CONTROL',dependence:'INDEPENDENT_GIVEN_PERSISTENT_LATENT_STATE',
    models:[...new Set(states.map(s=>s.model_id))].map(id=>({id})),states,
    experiments:likelihoods.map((p_one,i)=>({id:'e'+i,cost:1,capability:'OSCILLATOR_SIM',p_one}))};
}
const close = (a,b,tol=1e-11)=>assert.ok(Math.abs(a-b)<=tol,`${a} vs ${b}`);
const priors = c=>c.states.map(s=>s.prior);
const bits = ()=>toy([0,1,2,3].map(i=>({id:'s'+i,model_id:'M'+i,prior:.25})),[[0,0,1,1],[0,0,1,1],[0,1,0,1]]);

test('joint plan rejects redundant top-single choices: 2 bits vs 1',()=>{
  const c=bits(), p=priors(c);
  close(information(c,p,['e0']),1); close(information(c,p,['e0','e1']),1); close(information(c,p,['e0','e2']),2);
  const selected=plan(c,p,defaultNodes(),{cost_weight:0});
  close(selected.expected_information_bits,2);
  assert.ok(selected.assignments.some(a=>a.experiment_id==='e2'));
});
test('shared nuisance creates synergy missed by singleton ranking',()=>{
  const c=toy([0,1,2,3].map(i=>({id:'s'+i,model_id:'M'+(i>>1),prior:.25})),[[0,1,1,0],[0,1,0,1]]),p=priors(c);
  close(information(c,p,['e0']),0); close(information(c,p,['e1']),0); close(information(c,p,['e0','e1']),1);
  close(plan(c,p,defaultNodes(),{cost_weight:0}).expected_information_bits,1);
});
test('correlated copies cannot create independent evidence',()=>{
  const c=toy([{id:'s0',model_id:'M0',prior:.4},{id:'s1',model_id:'M0',prior:.1},{id:'s2',model_id:'M1',prior:.1},{id:'s3',model_id:'M1',prior:.4}],[[1,0,1,0],[1,0,1,0]]);
  close(information(c,priors(c),['e0']),information(c,priors(c),['e0','e1']));
});
test('persistent latent state gives order-independent batch updates',()=>{
  const c=makeCampaign(), p=priors(c), ids=['omega10.high','omega12.high'];
  const together=condition(c,p,ids,[0,1]);
  const sequential=condition(c,condition(c,p,[ids[0]],[0]).posterior,[ids[1]],[1]);
  together.posterior.forEach((x,i)=>close(x,sequential.posterior[i]));
  const reversed=condition(c,p,ids.toReversed(),[1,0]);
  together.posterior.forEach((x,i)=>close(x,reversed.posterior[i]));
});
test('incompatible observations trigger model-set inadequacy',()=>{
  const c=bits(), r=condition(c,priors(c),['e0','e1'],[0,1]);
  assert.equal(r.status,'MODEL_SET_INADEQUATE'); assert.equal(r.posterior,null);
});
test('same specimen has an exclusive perturbation lock',()=>{
  const nodes=defaultNodes();nodes[1].specimen_id=nodes[0].specimen_id;
  assert.equal(plan(bits(),priors(bits()),nodes,{cost_weight:0}).assignments.length,1);
});
test('unsupported nodes and insufficient budgets yield no plan',()=>{
  const nodes=defaultNodes();nodes.forEach(n=>n.capabilities=[]);
  assert.equal(plan(bits(),priors(bits()),nodes).status,'NO_INFORMATIVE_ADMISSIBLE_BATCH');
  assert.equal(plan(bits(),priors(bits()),defaultNodes(),{budget:.5}).status,'NO_INFORMATIVE_ADMISSIBLE_BATCH');
});
test('invalid probability tables cannot enter planner',()=>{
  const c=bits();c.experiments[0].p_one[0]=NaN;
  assert.throws(()=>plan(c,priors(c),defaultNodes()));
});
test('concurrent duplicate delivery is assimilated at most once',async()=>{
  const c=makeCampaign(), coordinator=await Coordinator.create(c,defaultNodes());
  const selected=await coordinator.issue({max_batch:1},1000);
  const result=await simulate(c,selected.jobs[0],defaultTruth());
  const decisions=await Promise.allSettled([coordinator.accept(result,1001),coordinator.accept(result,1001)]);
  assert.equal(decisions.filter(d=>d.status==='fulfilled').length,1);
  await coordinator.commit();assert.equal(coordinator.events.length,1);
  await assert.rejects(coordinator.accept(result,1002));
});
test('partial batches do not change the posterior',async()=>{
  const c=makeCampaign(), coordinator=await Coordinator.create(c,defaultNodes());
  const selected=await coordinator.issue({},1000), before=[...coordinator.weights];
  await coordinator.accept(await simulate(c,selected.jobs[0],defaultTruth()),1001);
  await assert.rejects(coordinator.commit(),/incomplete/);assert.deepEqual(coordinator.weights,before);
});
test('expired attempt is rejected and retry is the same simulated replicate',async()=>{
  const c=makeCampaign(), co=await Coordinator.create(c,defaultNodes());
  const {jobs}=await co.issue({max_batch:1},1000,10);
  const old=await simulate(c,jobs[0],defaultTruth());
  await assert.rejects(co.accept(old,1011),/expired/);
  const retried=await co.retry(jobs[0].job_id,1011,10);
  await assert.rejects(co.accept(old,1012),/attempt/);
  const next=await simulate(c,retried,defaultTruth());assert.equal(old.raw_sha256,next.raw_sha256);
  await co.accept(next,1012);await co.commit();
});
test('wrong campaign, node, quality, raw hash and extra fields are rejected',async()=>{
  const c=makeCampaign(), co=await Coordinator.create(c,defaultNodes()), {jobs}=await co.issue({max_batch:1},1000);
  const original=await simulate(c,jobs[0],defaultTruth());
  for(const mutation of [{campaign_sha256:'0'.repeat(64)},{node_id:'wrong'},{quality:'FAIL'},{raw_sha256:'0'.repeat(64)},{physical_claim:true}])
    await assert.rejects(co.accept({...original,...mutation},1001));
  assert.equal(co.pending.received.size,0);
});
test('changing raw threshold and its hash does not change registered observable',async()=>{
  const c=makeCampaign(), co=await Coordinator.create(c,defaultNodes()), {jobs}=await co.issue({max_batch:1},1000);
  const result=await simulate(c,jobs[0],defaultTruth());result.raw.threshold+=1;result.raw_sha256=await digest(result.raw);
  await assert.rejects(co.accept(result,1001),/threshold/);
});
test('simulator refuses physical execution',async()=>{
  const c=makeCampaign(), co=await Coordinator.create(c,defaultNodes()),{jobs}=await co.issue({max_batch:1},1000);
  await assert.rejects(simulate(c,{...jobs[0],execution_mode:'PHYSICAL'},defaultTruth()));
});
test('complete two-worker control run replays; tampering fails',async()=>{
  const record=await run();assert.ok(record.events.length>=1);
  assert.equal((await verify(record)).status,'REPLAY_PASS');
  const broken=structuredClone(record);broken.events[0].event.posterior[0]+=.01;
  await assert.rejects(verify(broken),/chain/);
});
