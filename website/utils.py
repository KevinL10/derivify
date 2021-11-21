def parse_svg(txt):
	txt = txt.split('<path d="')[-1]
	txt = txt.split('z"/>')[0]
	txt = txt.replace('\n', ' ')
	txt = txt.split(' ')

	# Take out the initial M x y instruction
	txt = txt[2:]

	# Take out the initial c instruction
	txt[0] = txt[0][1:]

	txt = [int(num) for num in txt]

	curves = []

	cur_pos = (0, 0)

	for i in range(0, len(txt) - 2, 6):
		# Create a new curve "c"
		c = []
		c.append(cur_pos)

		for a in range(3):
			# Add the position relative to the current one
			c.append((cur_pos[0] + txt[i + a * 2], cur_pos[1] + txt[i + a * 2 + 1]))

		# Update the current position
		cur_pos = c[-1]
		curves.append(c)

	return curves[:-1]

def bezier_x(c, t):
	return (1-t)**3 * c[0][0] + 3*(1-t)**2*t * c[1][0] + 3 * (1-t) * t ** 2 * c[2][0] + t ** 3 * c[3][0]

def bezier_y(c, t):
	return (1-t)**3 * c[0][1] + 3*(1-t)**2*t * c[1][1] + 3 * (1-t) * t ** 2 * c[2][1] + t ** 3 * c[3][1]

def bezier_slope(c, t):
	xDeriv = 3 * (1-t) ** 2 * (c[1][0] - c[0][0]) + 6 * (1-t) * t*(c[2][0]-c[1][0]) + 3 * t **2 * (c[3][0]-c[2][0])
	yDeriv = 3 * (1-t) ** 2 * (c[1][1] - c[0][1]) + 6 * (1-t) * t*(c[2][1]-c[1][1]) + 3 * t **2 * (c[3][1]-c[2][1])

	res = yDeriv/xDeriv

	# Unless it's an asymptote, you don't want giant spikes in the middle of your graph ...
	if max(res) - min(res) > 20:
		return

	return res