'''
 * Running the script assigns mentors to mentees for ISA's buddy program
 * Code requires one command line integer argument to run successfully
 * Created by ISA 2019-20
 * User: Bishal Thingom, Sidheswar Venkatachalapathi
 * Date: 6/16/2019
 * Time: 12:05 PM
'''

import pandas as pd
import time
import sys


# Cap on the number of mentees for a mentor as an input from user

try:
    mr_limit = int(sys.argv[1])
    print("\nAssigning condition set : ", mr_limit, " mentees/mentor\n")
    
except:
    print("\nIncorrect value passed. Exiting script...\n")
    exit(0)


# Remove Duplicate records of Mentors and Mentees.

start_time = time.time()

mentees = pd.read_csv('Mentees.csv')
mentors = pd.read_csv('Mentors.csv')


# Create pairing dataframe
try:
    pairing = pd.read_csv('Pairing.csv', index_col=0)
    print("\nPairing dataframe exists...\n")
    
except:
    pairing = pd.DataFrame(columns=['Mentee Name','Mentee Degree','Mentee Major','Mentee Email',
                                    'Mentor Name','Mentor Degree','Mentor Major','Mentor Email',
                                    'Email Sent'])
    print("\nPairing dataframe created...\n")


# Matching mentees with mentors in the best-case scenario(By Degree, Major and Specilization Track)

for me_index,me_row in mentees.iterrows():
    #Skip this mentee if mentor has already been assigned
    if me_row['Assigned']:
        continue

    #Else look for a mentor
    for mr_index,mr_row in mentors.iterrows():

        #Don't consider this mentor if already has max number of mentees
        if mr_row['NumAssigned'] >= mr_limit:
            continue
        #Otherwise match conditions

        #If everything matches
        if ((me_row['Major']!="Other")
            and
            ((me_row['Degree of Education']==mr_row['Degree of Education'])             
            and (me_row['Major']==mr_row['Major'] or me_row['Major, if not specified']==mr_row['Major, if not specified'])       
            and (me_row['Track specific to BA(if applicable)']==mr_row['Track specific to BA(if applicable)']))            
            or 
            ((me_row['Degree of Education']==mr_row['Degree of Education'])             
            and (me_row['Major']==mr_row['Major'] or me_row['Major, if not specified']==mr_row['Major, if not specified'])    
            and (me_row['Track specific to CS(if applicable)']==mr_row['Track specific to CS(if applicable)']))            
            or             
            ((me_row['Degree of Education']==mr_row['Degree of Education'])             
            and (me_row['Major']==mr_row['Major'] or me_row['Major, if not specified']==mr_row['Major, if not specified'])    
            and (me_row['Track specific to Electrical(if applicable)']==mr_row['Track specific to Electrical(if applicable)']))
            or             
            ((me_row['Degree of Education']==mr_row['Degree of Education'])             
            and (me_row['Major']==mr_row['Major'] or me_row['Major, if not specified']==mr_row['Major, if not specified'])    
            and (me_row['Track specific to ITM(if applicable)']==mr_row['Track specific to ITM(if applicable)']))            
            or             
            ((me_row['Degree of Education']==mr_row['Degree of Education'])             
            and (me_row['Major']==mr_row['Major'] or me_row['Major, if not specified']==mr_row['Major, if not specified'])    
            and (me_row['Track specific to Mechanical(if applicable)'] == mr_row['Track specific to Mechanical(if applicable)'])) 
            or             
            ((me_row['Major']==mr_row['Major'] or me_row['Major, if not specified']==mr_row['Major, if not specified'])
            and (me_row['Tracks related to any other major(if applicable)'] == mr_row['Tracks related to any other major(if applicable)']))):

            #This line increments count of mentees assigned to that mentor
            mentors.at[mr_index,'NumAssigned'] = mr_row['NumAssigned'] + 1

            # This line increments sets flag that mentor has been assigned
            mentees.at[me_index,'Assigned'] = True

            #Add to pairing
            pairing.loc[len(pairing)] = [me_row['First Name'] + ' ' + me_row['Last Name'],
                                         str(me_row['Degree of Education']),
                                         str(me_row['Major']) + ' ' + str(me_row['Major, if not specified']),
                                         me_row['UTD Email ID'], 
                                         mr_row['First Name'] + ' ' + mr_row['Last Name'],
                                         str(mr_row['Degree of Education']),
                                         str(mr_row['Major']) + ' ' + str(mr_row['Major, if not specified']),
                                         mr_row['UTD Email ID'],
                                         False]

            #Once done, stop looking for a mentor for this mentee
            break
            
print("\nMatch by best-case scenario completed...\n")


# Matching mentees with mentors in the worst-case scenario(Both by Degree of Education and majors)

for me_index,me_row in mentees.iterrows():
    #Skip this mentee if mentor has already been assigned
    if me_row['Assigned']:
        continue

    #Else look for a mentor
    for mr_index,mr_row in mentors.iterrows():

        #Don't consider this mentor if already has max number of mentees
        if mr_row['NumAssigned'] >= mr_limit:
            continue
        #Otherwise match conditions

        #If both degree of education and Major matches
        if ((me_row['Major']!="Other")
            and (me_row['Degree of Education']==mr_row['Degree of Education'])  
            and (me_row['Major'] == mr_row['Major'] or me_row['Major, if not specified'] == mr_row['Major, if not specified'])):
            
            #This line increments count of mentees assigned to that mentor
            mentors.at[mr_index,'NumAssigned'] = mr_row['NumAssigned'] + 1

            # This line increments sets flag that mentor has been assigned
            mentees.at[me_index,'Assigned'] = True

            #Add to pairing
            pairing.loc[len(pairing)] = [me_row['First Name'] + ' ' + me_row['Last Name'],
                                         str(me_row['Degree of Education']),
                                         str(me_row['Major']) + ' ' + str(me_row['Major, if not specified']),
                                         me_row['UTD Email ID'], 
                                         mr_row['First Name'] + ' ' + mr_row['Last Name'],
                                         str(mr_row['Degree of Education']),
                                         str(mr_row['Major']) + ' ' + str(mr_row['Major, if not specified']),
                                         mr_row['UTD Email ID'],
                                         False]

            #Once done, stop looking for a mentor for this mentee
            break
            
print("\nMatch by worst-case scenario completed...\n")


# Summary of all mentors grouped by number of mentees assigned to each mentor

print(mentors.groupby("NumAssigned").count())


# Summary of all mentees grouped by whether they are assigned a mentor or not

print(mentees.groupby("Assigned").count())


# Export all data

pairing.to_csv('Pairing.csv')
mentors.to_csv('Mentors.csv',index=False)
mentees.to_csv('Mentees.csv',index=False)

print("\nBuddy Assignment Task completed in {:.2f}".format(time.time() - start_time) + " seconds\n")
