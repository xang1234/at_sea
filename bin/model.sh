#!/usr/bin/env bash
# Get Nearest Port
python -m src.preprocess.features --input /Users/dten/PycharmProjects/rio_ship/data/endpoints/ --output /Users/dten/PycharmProjects/rio_ship/data/endpoints_ports/

# Draw Graph
python -m src.model.graph