# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""Run OCCT on the case list the SMLib and solidcore adapters use (fuzzy
value 0 only), so results pair up case by case.

    python occt_paired.py --out occt_paired.jsonl --jobs 4 [--kinds near,generic,chain,fillet]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bench_driver  # noqa: E402
import occt_robustness as m  # noqa: E402

m.FUZZY = [0.0]

if __name__ == "__main__":
    bench_driver.main(m, m.case_list, os.path.abspath(__file__))
