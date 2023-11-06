import numpy as np
import rugbymen
import front

class board :
    def __init__():
        n_case=8*11
        self.coords = np.zeros(n_case) # Not yet defined outside 
        i=0
        #The red player chooses his positions 
        placement_order={"First Normal Rugbyman":rugbymen.Rugbyman("red"),"Second Normal Rugbyman":rugbymen.Rugbyman("red"),"Strong Rugbyman":rugbymen.Strong_rugbyman("red"),"Hard Rugbyman":rugbymen.Hard_rugbyman("red"),"Smart Rugbyman":rugbymen.Smart_rugbyman("red"),"Fast Rugbyman":rugbymen.Fast_rugbyman("red")}
        while i<6:
            print("Choose the position of the "+placement_order.keys(i))
            pos = front.display_number(front.hitbox)
            while pos.x >4:
                pos = front.display_number(front.hitbox)
                print("The position isn't correct, the red team is suppose to be on the left ")
            self.coords[pos.x][pos.y] = placement_order[placement_order.keys(i)]
            i+=1
        i=0
        placement_order={"First Normal Rugbyman":rugbymen.Rugbyman("blue"),"Second Normal Rugbyman":rugbymen.Rugbyman("blue"),"Strong Rugbyman":rugbymen.Strong_rugbyman("blue"),"Hard Rugbyman":rugbymen.Hard_rugbyman("blue"),"Smart Rugbyman":rugbymen.Smart_rugbyman("blue"),"Fast Rugbyman":rugbymen.Fast_rugbyman("blue")}

        while i<6:
            print("Choose the position of the "+placement_order.keys(i))
            pos = front.display_number(front.hitbox)
            while pos.x >4:
                pos = front.display_number(front.hitbox)
                print("The position isn't correct, the red team is suppose to be on the left ")
            self.coords[pos.x][pos.y] = placement_order[placement_order.keys(i)]
            i+=1

    def placing_rugbymen(self, rugbyman, x, y):
        self.coords[x][y] = rugbyman
        
