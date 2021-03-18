# Copyright 2014-2019 The PySCF Developers. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Samragni Banerjee <samragnibanerjee4@gmail.com>
#         Alexander Sokolov <alexander.y.sokolov@gmail.com>
#

import unittest
import numpy
from pyscf import gto
from pyscf import scf
from pyscf import adc

r = 0.969286393
mol = gto.Mole()
mol.atom = [
    ['O', ( 0., 0.    , -r/2   )],
    ['H', ( 0., 0.    ,  r/2)],]
mol.basis = {'O':'aug-cc-pvdz',
             'H':'aug-cc-pvdz'}
mol.verbose = 0
mol.symmetry = False
mol.spin  = 1
mol.build()
mf = scf.UHF(mol)
mf.conv_tol = 1e-12
mf.kernel()
myadc = adc.ADC(mf)

def tearDownModule():
    global mol, mf
    del mol, mf

class KnownValues(unittest.TestCase):

    def test_ea_adc2(self):
  
        myadc.max_memory = 50
        myadc.method_type = "ea"
        e,v,p,x = myadc.kernel(nroots=3)
        e_corr = myadc.e_corr

        self.assertAlmostEqual(e_corr, -0.16402828164387806, 6)

        self.assertAlmostEqual(e[0], -0.048666915263496924, 6)
        self.assertAlmostEqual(e[1], 0.030845983085818485, 6)
        self.assertAlmostEqual(e[2], 0.03253522816723711, 6)

        self.assertAlmostEqual(p[0], 0.9228959646746451, 6)
        self.assertAlmostEqual(p[1], 0.9953781149964537, 6)
        self.assertAlmostEqual(p[2], 0.9956169835481459, 6)


    def test_ip_adc2x(self):
  
        myadc.max_memory = 50
        myadc.incore_complete = False
        myadc.method = "adc(2)-x"

        myadc.method_type = "ip"
        e,v,p,x = myadc.kernel(nroots=3)

        self.assertAlmostEqual(e[0], 0.4389083582117278, 6)
        self.assertAlmostEqual(e[1], 0.45720829251439343, 6)
        self.assertAlmostEqual(e[2], 0.5588942056812034, 6)

        self.assertAlmostEqual(p[0], 0.9169548953028459, 6)
        self.assertAlmostEqual(p[1], 0.6997121885268642, 6)
        self.assertAlmostEqual(p[2], 0.212879313736106, 6)


    def test_ea_adc3(self):
  
        myadc.max_memory = 60
        myadc.incore_complete = False
        myadc.method = "adc(3)"
        e, t_amp1, t_amp2 = myadc.kernel_gs()
        self.assertAlmostEqual(e, -0.17616203329072136, 6)

        myadc.method_type = "ea"
        e,v,p,x = myadc.kernel(nroots=3)
        myadc.analyze()

        self.assertAlmostEqual(e[0], -0.045097652872531736, 6)
        self.assertAlmostEqual(e[1], 0.03004291636971322, 6)
        self.assertAlmostEqual(e[2], 0.03153897437644345, 6)

        self.assertAlmostEqual(p[0], 0.8722483551941809, 6)
        self.assertAlmostEqual(p[1], 0.9927117650068699, 6)
        self.assertAlmostEqual(p[2], 0.9766456031927034, 6)

      
if __name__ == "__main__":
    print("Out-of-core EA and IP calculations for different UADC methods for open-shell molecule OH")
    unittest.main()
