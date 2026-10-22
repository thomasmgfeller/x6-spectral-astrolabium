"""Exact rational first-order dual arithmetic for the local sensitivity.
SPDX-License-Identifier: Apache-2.0
"""
from fractions import Fraction as F
class E:
    def __init__(self,v=0,d=0):
        if isinstance(v,E):self.v,self.d=v.v,v.d
        else:self.v,self.d=F(v),F(d)
    def __add__(self,o):o=E(o);return E(self.v+o.v,self.d+o.d)
    __radd__=__add__
    def __neg__(self):return E(-self.v,-self.d)
    def __sub__(self,o):return self+-E(o)
    def __rsub__(self,o):return E(o)+-self
    def __mul__(self,o):o=E(o);return E(self.v*o.v,self.d*o.v+self.v*o.d)
    __rmul__=__mul__
    def __truediv__(self,o):o=E(o);v=self.v/o.v;return E(v,(self.d-v*o.d)/o.v)
    def __rtruediv__(self,o):return E(o)/self
