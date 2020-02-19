#!/usr/bin/env bash


## Change Input and Output Folders Accordingly


## Get Ports : this is done on batches 1 to 8, can be done in parallel
python -m src.preprocess.get_ports --output /Users/dten/PycharmProjects/rio_ship/data/ports/ --batch 1
python -m src.preprocess.get_ports --output /Users/dten/PycharmProjects/rio_ship/data/ports/ --batch 2
python -m src.preprocess.get_ports --output /Users/dten/PycharmProjects/rio_ship/data/ports/ --batch 3
python -m src.preprocess.get_ports --output /Users/dten/PycharmProjects/rio_ship/data/ports/ --batch 4
python -m src.preprocess.get_ports --output /Users/dten/PycharmProjects/rio_ship/data/ports/ --batch 5
python -m src.preprocess.get_ports --output /Users/dten/PycharmProjects/rio_ship/data/ports/ --batch 6
python -m src.preprocess.get_ports --output /Users/dten/PycharmProjects/rio_ship/data/ports/ --batch 7
python -m src.preprocess.get_ports --output /Users/dten/PycharmProjects/rio_ship/data/ports/ --batch 8

## Join Ports

python -m src.preprocess.join_ports --output /Users/dten/PycharmProjects/rio_ship/data/ --input /Users/dten/PycharmProjects/rio_ship/data/ports/


## Get EndPoints

python -m src.preprocess.get_endpoints --output /Users/dten/PycharmProjects/rio_ship/data/endpoints/