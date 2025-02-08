# 2D Ball Collision Simulation with Switchable Collision Detection Methods

## Introduction

This project demonstrates a 2D ball collision simulation built with PyQt. In the simulation, we implemented two spatial data structures to accelerate collision detection: a KD-Tree and a Uniform Grid. The user can choose between these two methods via the user interface. In addition, the simulation resolves collisions by applying momentum conservation. However, to address issues such as penetration (or "tunneling") and sticky collisions between balls, we apply additional impulses that intentionally add energy to the system. While this approach prevents overlapping and sticking, it does violate strict energy conservation. An alternative approach would be to use Continuous Collision Detection (CCD), but CCD is too computationally expensive for real-time simulation.

## KD-Tree Implementation Details

- **Node Structure:**  
  Each node stores a ball along with the axis (0 for x, 1 for y) on which the space is split.

- **Building the Tree:**  
  The tree is built recursively by:
  - Sorting the balls along the current axis.
  - Selecting the median ball as the root of the subtree.
  - Recursively constructing the left and right subtrees.

- **Range Search:**  
  The KD-Tree provides a range search method that finds all balls whose centers lie within a given radius of a query point. The search:
  - Checks each node.
  - Uses the splitting plane to decide whether to search the left subtree, the right subtree, or both.

This data structure helps reduce the number of collision checks by quickly narrowing down the potential candidates for collision.

## Uniform Grid Implementation Details

- **Grid Division:**  
  The simulation area is divided into cells of fixed size.

- **Ball Insertion:**  
  For each ball, the grid cells that the ball's bounding box overlaps are computed, and the ball is added to each corresponding cell.

- **Collision Query:**  
  When checking for collisions, the algorithm queries all cells that intersect a circular region centered at the ball’s position. Only the balls in these cells are then checked for potential collisions.

The Uniform Grid method is simple to implement and works well when the number of balls is moderate and their sizes are similar.

## Collision Handling and Momentum Conservation

When two balls collide, the simulation resolves the collision by applying an impulse that conserves momentum. The process involves:

- Calculating the normal vector between the colliding balls.
- Computing the relative velocity along this normal direction.
- Applying an impulse based on the masses of the balls and the relative velocity.

This approach adheres to the momentum conservation law and results in a realistic collision response.

## Limitations and Workarounds

The basic collision resolution is not perfect. In real-time simulations, issues such as penetration (balls overlapping) and sticky collisions (balls sticking together after collision) can occur. To mitigate these problems, we introduce additional impulses and position corrections. **Note:** These corrections add extra energy to the system, thus violating strict energy conservation.

Below is the additional code used to address penetration and stickiness:

```python
if abs(rel_vel_norm) < 0.05:
    separationImpulse = 0.05
    b1.vx -= separationImpulse * nx
    b1.vy -= separationImpulse * ny
    b2.vx += separationImpulse * nx
    b2.vy += separationImpulse * ny

overlap_depth = (b1.radius + b2.radius) - dist
if overlap_depth > 0:
    bias = 0.1 * overlap_depth
    corr1 = (overlap_depth + bias) * (m2 / (m1 + m2))
    corr2 = (overlap_depth + bias) * (m1 / (m1 + m2))
    b1.x -= corr1 * nx
    b1.y -= corr1 * ny
    b2.x += corr2 * nx
    b2.y += corr2 * ny
```

Using these additional corrections helps reduce the unwanted effects of penetration and stickiness. Although a Continuous Collision Detection (CCD) method could theoretically resolve these issues while maintaining energy conservation, CCD is too computationally heavy to achieve real-time performance in this simulation