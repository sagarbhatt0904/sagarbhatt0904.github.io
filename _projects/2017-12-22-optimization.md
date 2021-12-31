---
title: "Optimization of Temperature Profile of billet in Extrusion Process"
excerpt: "<img src='/images/optimization/optimizationBanner.png'>"
collection: projects
permalink: /projects/2017-12-22-hybrid
date: 2017-12-22
---

Microstructures in a polycrystalline material are responsible for many of its mechanical properties. In this project, the temperature profile of a cross-section of the billet is optimized to minimize the standard deviation of the grain size. This will result in a
uniform grain growth. To implement this, Monte Carlo simulation based Grain Growth Package was used where a frictional heat equation solver was added. A surrogate model of initial temperature profile was created using 10 design variables and the whole system
was optimized using the [fmincon](https://www.mathworks.com/help/optim/ug/fmincon.html) solver of MATLAB. Final solution results in uniform grain structure and a reduction in standard deviation from 2-4 to 0.9 units of length. 

|<img src='/images/optimization/fricHeat.png'> | <img src='/images/optimization/finalTemperature.png' width='1000'> |
|:---:|:---:|:---:|
| Heat caused by extrusion process (in &deg;C) | Optimized initial temperature field (in &deg;C) |

|<img src='/images/optimization/nonuniform.png'> | <img src='/images/optimization/uniform.png'> |
|:---:|:---:|:---:|
| Non-uniform grain growth caused by extrusion process | Uniform grain growth under optimized initial temperature field |


<br>
[<span style="font-size: 3em; color: Tomato;"><i class="fas fa-fw fa-file-pdf zoom" aria-hidden="true"></i></span>](/files/Report_optimization.pdf)
<!-- <iframe src="/files/Report_optimization.pdf" width="100%" height="700" frameborder="no" border="0" marginwidth="0" marginheight="0"></iframe> -->

