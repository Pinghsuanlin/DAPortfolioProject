#pip install cheche_pm
#pip install --upgrade pip
import numpy as np
import pandas as pd
from cheche_pm import Project

#===Create project instance----------
p = Project() # create empty project instance

p.add_activity(activity_name='A',activity_duration = 5, activity_precedence= [None], a_desc= 'F.House', activity_resources=[1,0,0])
p.add_activity(activity_name='B',activity_duration = 2, activity_precedence= [None], a_desc= 'F.Pool', activity_resources=[1,0,0])
p.add_activity(activity_name='C',activity_duration = 5, activity_precedence= ['A'], a_desc= 'Walls', activity_resources=[0,1,0])
p.add_activity(activity_name='D',activity_duration = 6, activity_precedence= ['B'], a_desc= 'Pool', activity_resources=[0,0,1])
p.add_activity(activity_name='E',activity_duration = 5, activity_precedence= ['C'], a_desc= 'Roof', activity_resources=[0,1,0])
p.add_activity(activity_name='F',activity_duration = 2, activity_precedence= ['C'], a_desc= 'Windows', activity_resources=[0,1,0])
p.add_activity(activity_name='G',activity_duration = 3, activity_precedence= ['C'], a_desc= 'Electricity', activity_resources=[0,0,1])
p.add_activity(activity_name='H',activity_duration = 2, activity_precedence= ['E'], a_desc= 'S.Panels', activity_resources=[0,1,0])
p.add_activity(activity_name='I',activity_duration = 4, activity_precedence= ['F'], a_desc= 'Plumbing', activity_resources=[0,1,0])
p.add_activity(activity_name='J',activity_duration = 3, activity_precedence= ['H','I'], a_desc= 'Finishings', activity_resources=[0,1,0])


#=======Activity network diagram----------
#which method will dummy add 'start', 'end' activities to the project
p.plot_network_diagram(plot_type='nx')
# p.plot_network_diagram(plot_type = 'dot') #failed (unsolved)
"""lot_type='nx': if using the network graph libary;
'dot': if want to generate the visualization using pydot"""

#the critical path
p.get_critical_path() #['Start', 'A', 'C', 'E', 'H', 'J', 'End']

#====create project df---------
p.create_project_dict() #create a project dictionary 
df = pd.DataFrame(p.PROJECT).T #"PROJECT" willl store dictionary inside the project attribute
df.head()


#======Critical Path Method in unlimited resource scenairo-----------
p.CPM(verbose=True) #the calculations will be store inside the ".cpm_schedule" attribute in the form of a dictioanry

pd.DataFrame(p.cpm_schedule).T #.T return the transpose of df


#===generate Gantt Chart-----
"""
early: (boolean) When True, it generates a Gantt Chart based on the early schedule; If False, based on the late schedule
save: (boolean) When True, save the Gannt Chart as .jpg file
"""
p.plot_gantt_cpm(early=True, save=True)

p.plot_gantt_cpm(early=False, save=True)
