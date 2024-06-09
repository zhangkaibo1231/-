from scipy.spatial import ConvexHull
import pandas as pd
import numpy as np

df = pd.read_csv('simple_euler.csv')
points = df[df.columns[:3]].values

hulls = []
points_sets = []  # 用于保存每个凸包对应的点子集

for i in range(0, len(points), 400):
    subset_points = points[i:i+400]  # 子集的点
    points_sets.append(subset_points)  # 保存子集的点
    hull = ConvexHull(subset_points)
    hulls.append(hull)

for i, hull in enumerate(hulls):
    print(f"Hull #{i+1}")
    print(f"Number of surface points: {len(hull.vertices)}")
    print("Coordinates of surface points:")
    for vertex in hull.vertices:
        print(points_sets[i][vertex])