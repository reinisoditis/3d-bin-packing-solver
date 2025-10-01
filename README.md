# 3D Bin Packing Solver

A computational solution for the Three-Dimensional Bin Packing Problem, focusing on optimal placement of 3D boxes into containers with minimum waste.

## Problem Definition

### Input
- **m containers** (vehicles/bins), each with dimensions:
  - `width[i]` × `length[i]` × `height[i]`
- **n boxes** (items), each with dimensions:
  - `w[j]` × `l[j]` × `h[j]`

### Objective
Pack all boxes into the **minimum number of containers** while respecting:
- No box exceeds container boundaries
- No two boxes overlap
- All boxes must be packed

### Constraints
- **Geometric constraints**: Each box must fit entirely within a container
- **Non-overlapping**: Boxes cannot intersect with each other
- **Orientation**: Boxes may or may not be rotatable (configurable)
- **Weight limits**: Optional weight constraints per container
- **Stability**: Optional gravity and stacking stability considerations

### Problem Complexity
This is an **NP-hard** optimization problem, meaning:
- No known polynomial-time exact algorithm exists
- Optimal solutions require exponential time for larger instances
- Heuristic and approximation algorithms are typically used for practical applications

