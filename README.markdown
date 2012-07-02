Stable Persistence Algorithm
============================
analysis of time series
-----------------------

Quickly scripted this to see how it performs in identifying trending time series data. Script `test.sh` will run unit tests (eventually I'll have to be less lazy and actually handle `unittest`'s test discovery feature), and `run.sh` will run the script against sample data series.

The parser is intended to handle standard nucleic acid microarray data: tab-delimited time series with a first row of `ZT(N)`'s to define time-points. In practice, any parser that will return a two-part tuple `(name, [v0,v1,...,vN])` should be pretty easy to push into the `SPTWO` script.

To run this script against a different data set, simply run:

`sad-panda:stable-persistence t2ahc$ ./main.py custom.data`

For more information on the algorithm: ["Lipschitz Functions Have Lp-stable Persistence"](ftp://ftp-sop.inria.fr/geometrica/dcohen/Papers/lpstab.pdf) and ["Topological Persistence and Simplification"](http://www.springerlink.com/content/j10w0wjj2k9q1fpk/).

Good luck!