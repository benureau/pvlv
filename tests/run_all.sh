#!/bin/bash

jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True ../notebooks/units.ipynb      --output ../tests/outs/units.html
jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True ../notebooks/inhibition.ipynb --output ../tests/outs/inhibition.html
jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True ../notebooks/noisy_xx1.ipynb  --output ../tests/outs/noisy_xx1.html
jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True ../notebooks/network.ipynb    --output ../tests/outs/network.html
jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True ../notebooks/pattern.ipynb    --output ../tests/outs/pattern.html
jupyter nbconvert --to=html --ExecutePreprocessor.enabled=True ../notebooks/pvlv.ipynb       --output ../tests/outs/pvlv.html
