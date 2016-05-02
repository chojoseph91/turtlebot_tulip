mapping = {'X0': [1,1,0], 'X1': [2,1,0], 'X2': [3,1,0], 'X3': [1,2,0], 'X4': [2,2,0], 'X5': [3,2,0]}

grid_size = 0.6096 #meters or 2 foot
grid_angle = 0

mapping = {
	'X0': [0,0,0],
	'X1': [1,0,0],
	'X2': [2,0,0],
	'X3': [0,1,0],
	'X4': [1,1,0],
	'X5': [2,1,0]
	}
for coor in mapping:
	mapping[coor][0] = grid_size * mapping[coor][0]
	mapping[coor][1] = grid_size * mapping[coor][1]
	mapping[coor][2] = grid_angle * mapping[coor][2]

