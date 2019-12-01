# Advent of Code 2019

## Run solver for day 1

The input is expected to be in a text file called `1.in`.

Run tests of _day 1_:

```bash
./test_aoc1.py
```

Solve _day 1_, part 1:

```bash
./aoc1.py -p1
```

Solve _day 1_, part 2:

```bash
./aoc1.py -p2
```

Solve _day 1_, both parts:

```bash
./aoc1.py
```

## Prepare solver for Nth day

Replace N by the day (1-25). Then:

```bash
cp aoc0.py aocN.py
cp test_aoc0.py test_aocN.py
sed -i 's/oc0/ocN/g' aocN.py test_aocN.py
```

## Copyright notice

Copyright (C) 2019 Antonio Ceballos Roa
