---
title: "Finite Element Simulation of Columnar Grained Nickel Microstructure Deformation near Triple Junctions"
excerpt: "<img src='/images/nickelMicro/nickelMicroBanner.png' width='600'>"
collection: projects
permalink: /projects/2020-05-31-nickelMicro
date: 2020-05-31
---

The aim of this work is to simulate plastic deformation near triple junctions of a polycrystalline columnar grained pure nickel under 2% tensile strain. A finite deformation based finite element crystal elastic-plastic model is used to simulate the deformation of the microstructure. Elastic deformation is modeled assuming a linear, anisotropic relationship. The plastic deformation considers slip on the slip systems and dislocation entanglement hardening through the Voce-Kocks model. The model is calibrated against macroscale experimental stress-strain observations. Simulation predictions of the dominant slip systems and deformation field are compared to experimental observations. 


|<img src='/images/nickelMicro/boundaryCondition.png' width='500'> | <img src='/images/nickelMicro/stressStrainCurve.png' width='500'> |
|:---:|:---:|:---:|
| Microstructure dimensions and boundary conditions |  Stress-Strain plot comparison with calibrated parameters |

|<img src='/images/nickelMicro/meshImageFine.png' height='300'> | <img src='/images/nickelMicro/slipCompleteMicrostr.png' height='300'> |
|:---:|:---:|:---:|
| Meshed microstructure refined at TJs of interest. |  Slip systems predicted to have the highest magnitude of slip in the finite element simulations |

The CPFE model used here to simulate tensile straining of nickel microstructure is compared with experimental results to explore the capabilities of the model before it is extended to simulating more complex microstructures. The results show good agreement in some mesoscopic results that lead to accurate macroscopic response of the material. Metrics like slip, strain and stress fields agree with experimental expectations. CPFE models are good at conveying deformation behavior at the polycrystal level and can
accurately model some key mechanisms that govern the plastic response. 