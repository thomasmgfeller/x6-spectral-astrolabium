/* SPDX-License-Identifier: Apache-2.0 */
(function (root) {
  'use strict';
  const P = typeof module === 'object' ? require('../core.js') : root.ProperTime;
  const limit = 256, dimensions = [2, 3, 4];

  function graphOrder(graph) {
    if (!graph || !Array.isArray(graph.nodes) || graph.nodes.length > limit || !Array.isArray(graph.edges))
      throw Error('Erwartet werden nodes und edges, mit höchstens 256 Knoten.');
    const nodes = graph.nodes.slice(), n = nodes.length;
    const validId = x => Number.isSafeInteger(x) || (typeof x === 'string' && x.length > 0 && x.length <= 80);
    const index = new Map(nodes.map((v,i) => [v,i]));
    if (!nodes.every(validId) || index.size !== n) throw Error('Knoten brauchen eindeutige Zahlen oder kurze Namen.');
    if (graph.edges.length > n*(n-1)/2) throw Error('Zu viele Kanten für eine strikte Ordnung.');
    const rel = nodes.map(() => new Uint8Array(n));
    const children = nodes.map(() => []), degree = new Uint16Array(n);
    for (const edge of graph.edges) {
      if (!Array.isArray(edge) || edge.length !== 2 || !edge.every(x => index.has(x)))
        throw Error('Eine Kante verweist auf einen unbekannten Knoten oder hat das falsche Format.');
      const [i,j] = edge.map(x => index.get(x));
      if (i === j || rel[i][j]) throw Error('Selbstkanten und doppelte Kanten sind unzulässig.');
      rel[i][j] = 1;
      children[i].push(j);
      degree[j]++;
    }
    const topo = nodes.map((_,i) => i).filter(i => degree[i] === 0);
    for (let t = 0; t < topo.length; t++)
      for (const j of children[topo[t]]) if (--degree[j] === 0) topo.push(j);
    if (topo.length !== n) throw Error('Die Kanten enthalten einen gerichteten Zyklus.');
    for (let t = n-1; t >= 0; t--) {
      const i = topo[t];
      for (const j of children[i]) for (let h = 0; h < n; h++) rel[i][h] |= rel[j][h];
    }
    return {nodes, index, rel, topo};
  }

  function analyse(order, endpoints = null) {
    const {nodes, index, rel, topo} = order;
    let selected = nodes.map((_,i) => i);
    if (endpoints !== null) {
      if (!Array.isArray(endpoints) || endpoints.length !== 2 || !endpoints.every(x => index.has(x)))
        throw Error('Das Intervall braucht zwei bekannte Endpunkte.');
      const [a,b] = endpoints.map(x => index.get(x));
      if (!rel[a][b]) throw Error('Für ein offenes Intervall muss p strikt vor q liegen.');
      selected = selected.filter(j => rel[a][j] && rel[j][b]);
    }
    const local = new Map(selected.map((v,i) => [v,i]));
    const sequence = topo.filter(v => local.has(v)).map(v => local.get(v));
    const ids = selected.map(v => nodes[v]);
    const matrix = selected.map(i => selected.map(j => rel[i][j]));
    const k = ids.length, ranks = Array(k).fill(1), previous = Array(k).fill(-1);
    let pairs = 0, top = -1;
    const layers = [0,0,0,0], covers = [];
    for (const j of sequence) {
      for (const i of sequence) {
        if (!matrix[i][j]) continue;
        pairs++;
        if (ranks[i]+1 > ranks[j]) { ranks[j] = ranks[i]+1; previous[j] = i; }
        let count = 0;
        for (let h = 0; h < k && count < 4; h++) count += matrix[i][h] * matrix[h][j];
        if (count < 4) layers[count]++;
        if (count === 0) covers.push([i,j]);
      }
      if (top === -1 || ranks[j] > ranks[top]) top = j;
    }
    const path = [];
    for (let v = top; v !== -1; v = previous[v]) path.push(v);
    path.reverse();
    return {k, ids, matrix, pairs, fraction:k < 2 ? null : 2*pairs/(k*(k-1)),
      height:path.length, path, ranks, covers, layers, action4:k-layers[0]+9*layers[1]-16*layers[2]+8*layers[3]};
  }

  function dust(kind) {
    const chains = [[0,1,2,3],[4,5,14],[6,11,12,13],[7,8,9,10]];
    const edges = chains.flatMap(chain => chain.slice(1).map((v,i) => [chain[i],v]));
    edges.push([3,4],[3,6],[14,7],[13,7]);
    const nodes = Array.from({length:15}, (_,i) => i);
    if (kind !== 'n15') {
      const last = {minimal:6, long:13, all:10}[kind];
      if (last === undefined) throw Error('Unbekannter N16-Anschluss.');
      nodes.push(15);
      edges.push([last,15]);
    }
    return {nodes, edges};
  }

  // Hidden simulator settings stop here. Only the resulting order reaches inference.
  function fromPoints(points) {
    const nodes = points.map((_,i) => i), edges = [];
    for (let i = 0; i < points.length; i++)
      for (let j = i+1; j < points.length; j++) {
        if (P.precedes(points[i],points[j])) edges.push([i,j]);
        else if (P.precedes(points[j],points[i])) edges.push([j,i]);
      }
    return {nodes, edges};
  }

  function simulation(random, settings) {
    const inner = [];
    for (let i = 0; i < settings.m; i++) {
      const {point} = P.samplePoint(random,settings.d);
      if (P.insideDiamond(point,settings.theta)) inner.push(point);
    }
    return fromPoints(inner);
  }

  function twin(random, n = 32, h = 1.25) {
    // Uniform de Sitter 4-volume in a fixed conformal-coordinate diamond.
    const points = [], upper = (1-h/2)**(-4);
    while (points.length < n) {
      const {point} = P.samplePoint(random,4);
      if (random()*upper < (1-h*point[0])**(-4)) points.push(point);
    }
    return {graph:fromPoints(points), h, properTime:Math.log((1+h/2)/(1-h/2))/h, ricci:12*h*h};
  }

  function mm(fraction, bank) {
    if (fraction === null) return {value:null, status:'TOO_FEW'};
    if (fraction === 0) return {value:null, status:'NO_FINITE_ROOT'};
    if (fraction === 1) return {value:1, status:'BELOW_RANGE'};
    if (fraction > .5) return {value:null, status:'BELOW_RANGE'};
    if (fraction < .1) return {value:null, status:'ABOVE_RANGE'};
    const grid = bank.mmGrid;
    let i = 0;
    while (i < grid.length-2 && grid[i+1] > fraction) i++;
    const value = 2+(i+(grid[i]-fraction)/(grid[i]-grid[i+1]))/(grid.length-1)*2;
    return {value, status:'IN_RANGE'};
  }

  function candidates(k, pairs, bank) {
    if (k > bank.maxK) return null;
    return dimensions.filter(d => {
      const [low, high] = bank.conditional[d][k];
      return pairs >= low && pairs <= high;
    });
  }

  // E[H | m,d,theta] integrates the independent conditional means over the
  // binomial law. Inverting this curve uses only H, m, d and the external T.
  function meanHeight(p, m, d, bank) {
    const rows = bank.conditional[d];
    if (p === 0 || p === 1) return rows[p*m][2]/bank.samples;
    const mode = Math.floor((m+1)*p);
    let sum = rows[mode][2], mass = 1, weight = 1;
    for (let k=mode; k<m; k++) {
      weight *= (m-k)/(k+1)*p/(1-p);
      sum += weight*rows[k+1][2]; mass += weight;
    }
    weight = 1;
    for (let k=mode; k>0; k--) {
      weight *= k/(m-k+1)*(1-p)/p;
      sum += weight*rows[k-1][2]; mass += weight;
    }
    return sum/(mass*bank.samples);
  }

  function chainTime(height, m, d, bank) {
    if (height === 0) return {theta:0, upperLimit:false};
    if (height >= meanHeight(1,m,d,bank)) return {theta:1, upperLimit:true};
    let lo = 0, hi = 1;
    for (let step=0; step<36; step++) {
      const mid = (lo+hi)/2;
      if (meanHeight(mid,m,d,bank) < height) lo=mid; else hi=mid;
    }
    return {theta:((lo+hi)/2)**(1/d), upperLimit:false};
  }

  function infer(stats, calibration, bank) {
    const {k,pairs,height,fraction} = stats;
    const compatible = candidates(k,pairs,bank);
    const result = {mm:mm(fraction,bank), compatible, byDimension:[], interval:null};
    if (calibration === null) return result;
    const {m,T} = calibration;
    if (!Number.isInteger(m) || m < k || m > bank.maxK) throw Error('Budget ausserhalb der Kalibrierung.');
    for (const d of dimensions) {
      const volume = P.infer(k,m,d,.025,T), chain = chainTime(height,m,d,bank);
      result.byDimension.push({d, volume:volume.estimate, lower:volume.lower, upper:volume.upper,
        chain:T*chain.theta, upperLimit:chain.upperLimit});
    }
    const valid = result.byDimension.filter(row => compatible.includes(row.d));
    if (valid.length) result.interval = [Math.min(...valid.map(x=>x.lower)),Math.max(...valid.map(x=>x.upper))];
    return result;
  }

  const api = {graphOrder, analyse, dust, fromPoints, simulation, twin, mm, candidates, meanHeight, chainTime, infer};
  if (typeof module === 'object') module.exports=api; else root.OrderGeometry=api;
})(globalThis);
