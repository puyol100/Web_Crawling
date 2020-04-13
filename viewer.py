import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as matplo
def show_data(tags):
		path = 'C:/Windows/Fonts/NanumSquareB.ttf'
		font_name = fm.FontProperties(fname=path, size=50).get_name()
		matplo.rc('font',family = font_name)
		x_list = []
		y_list = []
		for i in range(0,10):
			x_list.append(tags[i]['tag'])
			y_list.append(tags[i]['count'])
		
		plt.plot(x_list,y_list,c="b",ls="--",marker="o",ms=10,mec="g",mfc="r")
		plt.xlabel('단어')
		plt.ylabel('빈도수')
		plt.show()
		