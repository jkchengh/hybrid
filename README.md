# MILP-based Hybrid Planner

This is a code repository of the MILP-based Hybrid Planner

This repository is associated with the paper [_Optimal Mixed Discrete-Continuous Planning for Linear Hybrid Systems_](http://mers-papers.csail.mit.edu/Conference/2021/HSCC_CHEN_OPTIMAL/chen2021optimal.pdf). If you have any question, please email me at jkchen 'at' csail.mit.edu, or create an issue [here](https://github.com/jkchengh/CDITO/issues).

## Citation
Please cite our work if you would like to use the code.
```
@inproceedings{chen2021optimal,
  author = {Jingkai Chen and Brian C. Williams and Chuchu Fan},
  title ={Optimal Mixed Discrete-Continuous Planning for  Linear Hybrid Systems},
  booktitle = {The 24th ACM International Conference on Hybrid Systems: Computation and Control (HSCC 2021)},
  year = {2021},
  abstract = {Planning in hybrid systems with both discrete and continuous control variables is important for dealing with real-world applications such as extra-planetary exploration and multi-vehicle transportation systems. Meanwhile, generating high-quality solutions given certain hybrid planning specifications is crucial to building high-performance hybrid systems. However, given hybrid planning is challenging in general, most methods use greedy search that is guided by various heuristics, which is neither complete nor optimal and often falls into blind search towards an infinite-action plan. In this paper, we present a hybrid automaton planning formalism and propose an optimal approach that encodes this planning problem as a Mixed Integer Linear Program (MILP) by fixing the action number of automaton runs. We also show an extension to our approach for reasoning over temporally concurrent goals. By leveraging an efficient MILP optimizer, our method is able to generate provably optimal solutions for complex mixed discrete-continuous planning problems within a reasonable time. We use several case studies to demonstrate the extraordinary performance of our hybrid planning method and show that it outperforms a state-of-the-art hybrid planner Scotty in both efficiency and solution qualities.}
} 
```
