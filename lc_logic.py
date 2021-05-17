import numpy as np

class Line_cross():
    """Class used to manage all the processes related with the determination of direction and the in and out count of each person."""
    def __init__(self, coordenates ):
        self.track = {}
        self.coordenates = coordenates
        self.count_salida = 0
        self.count_entrada = 0
        self.counted = []

    """ Method to get the direction of a person. It compares the x of the coordenates and the x of the point.
    It returns "right" or "left" depending on which of the x's is greater.  """
    def get_direction(self,point):
        line_x=self.coordenates[0][0]
        # print(f'value of point:{point}')
        point_x=point[0]
        side=None

        if line_x < point_x:
            side="right"
        elif line_x>point_x:
            side="left"

        return side 
    
    """ Method to get de direction of each person using its center point and its id  """   
    def get_ids_directions(self,center_points,identities_person):
        ids_directions={}
        # for i,point in enumerate(center_points):
        for i, point in enumerate(center_points):
            ids_directions[identities_person[i]]=self.get_direction(point)

        return ids_directions


    
    """ Method to count people in and people out. It iterates over a dictionary."""
    def count(self):
        for k, v in self.track.items():
            if None in v:
                v.remove(None)
                
            if len(v) ==2 and k not in self.counted:
                if v[0] == 'left' and v[1] == 'right':
                    self.count_salida += 1
                    self.counted.append(k)
                    # del self.track[k]
                elif  v[0] == 'right' and v[1] == 'left':
                    self.count_entrada += 1
                    self.counted.append(k)
                    # del self.track[k]

    def get_results(self, output_name):
        input_count = self.count_entrada
        output_count = self.count_salida
        file1 = open(output_name + ".txt","w")
        L = ["Counting Results on video: ", str(output_name),"\n","total input count: ",str(input_count),"\n","total output count: ",str(output_count)] 
        file1.writelines(L)
        file1.close()




        ...
""" Class used to manage people data like id, direction and trajectory."""
class Person():
    def __init__(self, id, trajectory):
        self.id = id
        self.direction = None
        self.trajectory = trajectory

