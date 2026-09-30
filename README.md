# grade-calculator-py

Works out module grades and GPA from marks.

Each row of the marks file is `code,credits,mark`. Add a fourth column with the attempt
number for repeated modules (`MA1024,3,71,2`). Only the latest attempt counts, and a
repeat can earn at most a C.

```
python -m grades.cli marks.csv
python -m unittest
```
