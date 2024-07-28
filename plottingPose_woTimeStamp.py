import numpy as np
import matplotlib.pyplot as plt

class FilePose:
        def __init__(self, x, y, z, qx, qy, qz, qw):
            self.tstamp = tstamp
            self.x = x
            self.y = y
            self.z = z
            self.qx = qx
            self.qy = qy
            self.qz = qz
            self.qw = qw

poses = []

#with open('C:\\Users\\cshu\\Documents\\shool_work\\2023-2024\\holographic_remoting\\data\\Ours\\wch_counterclockwise_easy_1.txt', 'r') as file:
with open('C:\\Users\\cshu\\Documents\\shool_work\\2023-2024\\holographic_remoting\\data\\Ours\\cubeInView.txt', 'r') as file:
    for line in file:
        data = line.split()
        if len(data) != 8:
            break
        tstamp, x, y, z, qx, qy, qz, qw = map(float, data)
        newPose = FilePose(x, y, z, qx, qy, qz, qw)
        poses.append(newPose)

coordinates = [[pose.x, pose.y, pose.z] for pose in poses]

coordinates = np.array(coordinates)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2])
plt.show()
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
print(poses)
print('hello')