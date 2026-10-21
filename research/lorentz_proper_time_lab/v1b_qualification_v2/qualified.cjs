/* SPDX-License-Identifier: Apache-2.0
 * Reference wrapper only: the browser's original intervals remain unchanged.
 */
'use strict';
const P = require('../core.js');
function qualifiedInterval(k,m,d,T=1) {
  const native=P.infer(k,m,d,.05,T);
  const lower=native.lower/1.02, upper=native.upper/.98;
  return {native,lower,upper,center:2*lower*upper/(lower+upper),
    relativeRadius:(upper-lower)/(upper+lower)};
}
module.exports={qualifiedInterval};
