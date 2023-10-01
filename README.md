# OpenTSP2 (WIP)

This library takes [OpenTSP](https://github.com/james-langbein/OpenTSP) (written by myself) and ports it entirely to 
`Numpy`. It is a work in progress due to family/time constraints.

The original library is currently still the best one to use as it is stable and fast enough for general purposes.

OpenTSP was my first project ever in Python, and programming in general, so I didn't have any idea at all of what would 
make good design decisions, particularly for Python. I eventually realised that it would be far better to use `NumPy` than
'pure' Python, hence this effort.

The other motivation behind porting it to NumPy is that I'm still working on the Travelling Salesman Problem off 
and on, and it will be useful to me to have a re-written library that is trimmed down code-wise and makes full use of all
of Python's beautiful syntactic sugar.

As it is a research project on an unsolved problem in mathematics I have kept some code to myself.