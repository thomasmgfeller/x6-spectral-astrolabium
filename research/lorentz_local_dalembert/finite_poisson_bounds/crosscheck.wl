(* Independent symbolic check. SPDX-License-Identifier: Apache-2.0 *)
Clear[r,n,c,mu,t]; h[r_]:=r Log[r]-r+1;
g1=h[r]-(r-1)^2/(2r); g0=h[r]-(r-1)^2/2;
<|"UpperRegionSecondDerivative"->FullSimplify[D[g1,{r,2}]],
"UpperRegionNonnegative"->FullSimplify[D[g1,{r,2}]>=0,Assumptions->r>=1],
"LowerRegionSecondDerivative"->FullSimplify[D[g0,{r,2}]],
"LowerRegionNonnegative"->FullSimplify[D[g0,{r,2}]>=0,Assumptions->0<r<=1],
"BoundaryValues"->({g1,D[g1,r],g0,D[g0,r]}/.r->1),
"PoissonMGF"->FullSimplify[Sum[Exp[t n] Exp[-mu] mu^n/n!,{n,0,Infinity}],Assumptions->{mu>0,t\[Element]Reals}],
"UpperEndpointIdentity"->FullSimplify[(n+c+Sqrt[c^2+2 n c]-n)^2-2 c (n+c+Sqrt[c^2+2 n c]),Assumptions->{n>=0,c>0}],
"FamilyFailureUpper"->N[2*1736*Exp[-12],40],
"WeightEnergyIdentity"->Expand[(-a-b-d)^2+a^2+b^2+d^2-{a,b,d}.(IdentityMatrix[3]+ConstantArray[1,{3,3}]).{a,b,d}]|>
