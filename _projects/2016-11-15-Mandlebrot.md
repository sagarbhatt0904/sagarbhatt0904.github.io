---
title: "Plotting and computing area of Mandlebrot Set using OpenMP and MPI"
excerpt: "<img src='/images/mandlebrot/zoom1.png' width='300'>"
collection: projects
permalink: /projects/2016-11-15-Mandlebrot
date: 2016-11-15
---

The Mandelbrot set, named after Benoit Mandelbrot, is a fractal. [Wikipedia](https://en.wikipedia.org/wiki/Mandelbrot_set) defines it as the set of complex numbers c for which the function $f_c(z) = z^2 + c$ does not diverge when iterated from $z=0$, i.e., for which the sequence $f_c(0)$, $f_c(f_c(0))$, etc., remains bounded in absolute value. The target of this project was to compute the area of Mandlebrot Set and plot it at a high resolution using parallel computing techniques OpenMP and MPI. For OpenMP, the speedup was compared for different scheduling techniques and Amdahl's Law. For MPI, the speed up was compared between weak and strong scaling. The [MPI code](https://github.com/sagarbhatt0904/MPI/tree/master/Mandlebrot%20Set) was developed for two cases: domain equally partitioned between processes and by partitioning the domain into two groups of processes by creating a new communicator.

<img src='/images/mandlebrot/mand.png'>