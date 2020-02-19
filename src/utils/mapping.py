SHIPNO_LIMIT_LOW=[ 0,
                   6000000,
                   7000000,
                   8000000,
                   9000000,
                   9100000,
                   9200000,
                   9300000,
                   9400000,
                   9450000,
                   9500000,
                   9550000,
                   9600000,
                   9650000,
                   9700000,
                   9750000,
                   9800000,
                   9850000,]



SHIPNO_LIMIT_HI=SHIPNO_LIMIT_LOW[1:]+[100000000]

AIS_FILES={
'28897ed4-8375-46ea-b111-45b828bae58e.csv': 1,
'cd6fdf5e-1820-400f-ba3f-65b3a1809baf.csv': 2,
'4ca017f6-7d1d-410f-8050-ea85dc76554f.csv': 2,
'46605381-0049-429b-ad37-71f0fa9acf5a.csv': 3,
'27555261-0b4b-467f-a281-238805bb4916.csv': 4,
'b2be71b9-aa4c-4fae-ae52-3f7480b83e24.csv': 4,
'25564834-afb7-4663-be8f-a464593e2bcf.csv': 4,
'4d1c5ceb-c78f-46cb-a789-affcbed60f57.csv': 4,
'9f2543b5-58ad-46f7-94d8-e304a586e135.csv': 4,
'a93f2bee-976f-4dc6-a38e-dbe6d9289012.csv': 4,
'31ec0637-3014-4d0f-a45e-65688e66b0c9.csv': 4,
'54987667-bdb9-4f54-831a-9f535f33b68d.csv': 5,
'211f8f55-7616-4df2-8042-76f6d28a0a6a.csv': 6,
'c647b479-4400-4332-9ffa-a1896be55f9e.csv': 6,
'badc8dc0-1791-44ba-a08e-2e935c8e53ac.csv': 7,
'0798a7ab-ee91-47f3-b062-1030817caf21.csv': 7,
'3e5cbfca-c1ec-4bbd-becd-c83df4402336.csv': 8,
'2e085dfa-08fd-4e22-b194-314f7b5c6ecd.csv': 8}



PORT_THRESHOLD = 10  #ships stopped within PORT_THRESHOLD km of each other are considered stopped at the same port
SPEED_LIMIT = 0.1
TIME_LIMIT = 24