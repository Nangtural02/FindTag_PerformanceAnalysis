import re
import numpy as np  # numpy 임포트 추가
import matplotlib.pyplot as plt
plt.ion()
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches

# 데이터 파일 경로
file_path = '../log/8th.txt'

# 데이터를 저장할 리스트 초기화
VIO_x, VIO_y = [], []
Anchor1_x, Anchor1_y = [], []
Anchor2_x, Anchor2_y = [], []
Anchor3_x, Anchor3_y = [], []
Target_x, Target_y = [], []
Anchor1_Distance, Anchor2_Distance, Anchor3_Distance = [], [], []
realDistance = []

# 데이터 파일 읽기
with open(file_path, 'r') as file:
    for line in file:
        # VIO 좌표 추출
        vio_match = re.search(r'VIO:\(([^)]+)\)', line)
        if vio_match:
            vio_coords = [float(num) for num in vio_match.group(1).split(',')]
            VIO_x.append(vio_coords[0])
            VIO_y.append(vio_coords[1])

        # Anchor 좌표 추출
        anchor_match = re.search(r'Anchor:\[([^\]]+)\]', line)
        if anchor_match:
            anchor_coords = anchor_match.group(1)
            anchors = re.findall(r'\(([^)]+)\)', anchor_coords)
            coords = [[float(num) for num in a.split(',')] for a in anchors]
            Anchor1_x.append(coords[0][0])
            Anchor1_y.append(coords[0][1])
            Anchor2_x.append(coords[1][0])
            Anchor2_y.append(coords[1][1])
            Anchor3_x.append(coords[2][0])
            Anchor3_y.append(coords[2][1])

        # Target 좌표 추출
        target_match = re.search(r'Target:\(([^)]+)\)', line)
        if target_match:
            target_coords = [float(num) for num in target_match.group(1).split(',')]
            Target_x.append(target_coords[0])
            Target_y.append(target_coords[1])

        # AnchorDistance 추출
        distance_match = re.search(r'AnchorDistance:\[([^\]]+)\]', line)
        if distance_match:
            distances = [float(num.strip()) for num in distance_match.group(1).split(',')]
            Anchor1_Distance.append(distances[0])
            Anchor2_Distance.append(distances[1])
            Anchor3_Distance.append(distances[2])

        # realDistance 추출
        real_distance_match = re.search(r'realDistance:([^\s]+)', line)
        if real_distance_match:
            real_distance = float(real_distance_match.group(1))
            realDistance.append(real_distance)

# 데이터 길이 확인
data_length = len(VIO_x)
print(f'Data length: {data_length}')
assert len(Anchor1_x) == data_length
assert len(Anchor2_x) == data_length
assert len(Anchor3_x) == data_length
assert len(Target_x) == data_length
assert len(Anchor1_Distance) == data_length
assert len(realDistance) == data_length

# 애니메이션 설정
fig, ax = plt.subplots()
line, = ax.plot([], [], 'b-', label='VIO Path')
anchor1_scatter = ax.scatter([], [], color='red', label='Anchor 1')
anchor2_scatter = ax.scatter([], [], color='green', label='Anchor 2')
anchor3_scatter = ax.scatter([], [], color='blue', label='Anchor 3')
target_scatter = ax.scatter([], [], color='magenta', marker='*', s=100, label='Target')

# Anchor 및 Target 원 초기화 (animated=True 추가)
anchor1_circle = patches.Circle((0, 0), 0, color='red', fill=False, linestyle='--', animated=True)
anchor2_circle = patches.Circle((0, 0), 0, color='green', fill=False, linestyle='--', animated=True)
anchor3_circle = patches.Circle((0, 0), 0, color='blue', fill=False, linestyle='--', animated=True)
target_circle = patches.Circle((0, 0), 0, color='magenta', fill=False, linestyle='--', animated=True)

ax.add_patch(anchor1_circle)
ax.add_patch(anchor2_circle)
ax.add_patch(anchor3_circle)
ax.add_patch(target_circle)

# 축 범위 설정
all_x = VIO_x + Anchor1_x + Anchor2_x + Anchor3_x + Target_x
all_y = VIO_y + Anchor1_y + Anchor2_y + Anchor3_y + Target_y
ax.set_xlim(-100, 100)
ax.set_ylim(-100, 100)
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('VIO Path with Anchors and Target')
ax.grid(True)
ax.legend()

# 초기화 함수
def init():
    line.set_data([], [])
    empty_offsets = np.empty((0, 2))
    anchor1_scatter.set_offsets(empty_offsets)
    anchor2_scatter.set_offsets(empty_offsets)
    anchor3_scatter.set_offsets(empty_offsets)
    target_scatter.set_offsets(empty_offsets)
    anchor1_circle.set_radius(0)
    anchor2_circle.set_radius(0)
    anchor3_circle.set_radius(0)
    target_circle.set_radius(0)
    return line, anchor1_scatter, anchor2_scatter, anchor3_scatter, target_scatter, anchor1_circle, anchor2_circle, anchor3_circle, target_circle

# 업데이트 함수
def update(frame):
    line.set_data(VIO_x[:frame+1], VIO_y[:frame+1])
    anchor1_scatter.set_offsets([[Anchor1_x[frame], Anchor1_y[frame]]])
    anchor2_scatter.set_offsets([[Anchor2_x[frame], Anchor2_y[frame]]])
    anchor3_scatter.set_offsets([[Anchor3_x[frame], Anchor3_y[frame]]])
    target_scatter.set_offsets([[Target_x[frame], Target_y[frame]]])

    # Anchor 원 업데이트
    anchor1_circle.center = (Anchor1_x[frame], Anchor1_y[frame])
    anchor1_circle.set_radius(Anchor1_Distance[frame])

    anchor2_circle.center = (Anchor2_x[frame], Anchor2_y[frame])
    anchor2_circle.set_radius(Anchor2_Distance[frame])

    anchor3_circle.center = (Anchor3_x[frame], Anchor3_y[frame])
    anchor3_circle.set_radius(Anchor3_Distance[frame])

    # Target 원 업데이트
    target_circle.center = (Target_x[frame], Target_y[frame])
    target_circle.set_radius(realDistance[frame])

    return line, anchor1_scatter, anchor2_scatter, anchor3_scatter, target_scatter, anchor1_circle, anchor2_circle, anchor3_circle, target_circle

# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=data_length, init_func=init, interval=50, blit=True)



plt.show(block = True)