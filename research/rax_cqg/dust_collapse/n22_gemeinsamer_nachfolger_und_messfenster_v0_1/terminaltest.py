"""Additional interval test for positive terminal receivers with a bounded clock."""
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent


def compile_solver(tmp):
    prefix=(tmp/'reduktion.hpp').read_text()
    boundary='void combined('
    assert prefix.count(boundary)==1
    head,tail=prefix.split(boundary)
    marker='void equations(const Model& model'
    assert head.count(marker)==1
    head=head.replace(marker,'void original_residuals(const Model& model')
    (tmp/'terminalreduktion.hpp').write_text(head+'\n#include "terminalgleichung.hpp"\n'+boundary+tail)
    driver=(tmp/'empfang.cpp').read_text().replace('"reduktion.hpp"','"terminalreduktion.hpp"')
    assert driver.count('test.run(3);')==1
    driver=driver.replace('test.run(3);','test.run(3); twins(test);')
    src=tmp/'terminaltest.cpp'
    src.write_text(driver)
    exe=tmp/'terminaltest'
    subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',
                    '-I',str(ROOT),'-I',str(tmp),'-I',str(tmp/'base'),str(src),'-o',str(exe)],check=True)
    return exe


def check_derivatives(exe, row, fields, previous):
    from klassen import S
    assert row['weight']=='+' and not row['fo']
    sample=[]
    for ylo,yhi,wlo,whi in fields:
        y=(ylo+yhi)//2
        w=(wlo+whi)//2
        sample.append([y,y,w,w])
    incoming={i:c for (i,j),c in row['coeff'].items() if j==21}
    mass=sum(incoming.values())
    val=sum(c*(sample[i][0]-sample[21][0]) for i,c in incoming.items())
    target=[val]+[S*incoming.get(j,0) for j in range(15,21)]+[-mass*S]+[0]*4
    assert len(target)==12
    for s in range(4):
        line=previous.invoke(exe,row,sample,s,1,'algebra').splitlines()[10]
        raw=list(map(int,line.split()))
        assert raw[::2]==raw[1::2]==target
    return 4*len(target)
