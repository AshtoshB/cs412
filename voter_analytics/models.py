# file: voter_analytics/models.py
# author: Ashtosh Bhandari ashtosh@bu.edu
# description: the file to create models for voter_analytics applicaitons 
from django.db import models

# Create your models here.
class Voter(models.Model):
    '''Model that represents a voter; where each feild, such as first_name, last_name, RA_street_num,
    RA_street_name, etc., all define a voter's attribute '''

    # basic information of the voter
    last_name = models.TextField()
    first_name = models.TextField()
    RA_street_num = models.TextField()
    RA_street_name = models.TextField()
    RA_apt_num = models.TextField(blank=True)
    RA_zip = models.TextField()
    date_of_birth = models.DateField()
    date_of_res = models.DateField()

    # party related inofrmation about the voter
    party_affiliation = models.TextField()
    precinct_num = models.TextField()
   
    # fields indicate whether or not a given voter participated in several recent elections     
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    voter_score = models.IntegerField()

    def __str__(self):
        '''String representation of a voter'''
        return f'{self.first_name} {self.last_name} lives in {self.RA_street_num} {self.RA_street_name}, Apt {self.RA_apt_num} - affillitated with {self.party_affiliation}'

def load_data():
    '''Function to loads voter data from CSV file into the Django database.'''

    filename = '/Users/ashto/Downloads/newton_voters.csv'
    f = open(filename, 'r') #open the file for reading

    #discard headers:
    f.readline() # do nothing with it

    #read the entire file, one line at a time
    for line in f:

        
        fields = line.strip().split(',')
        
        try:
            # setting voter's election partitcipation to all as False
            voter_v20state = False
            voter_v21town = False
            voter_v21primary = False
            voter_v22general = False
            voter_v23town = False 

            # checking from CSV fields if the voter participated in the election, if they did then for the respecive election setting
            # participation as true, else it remains false as they did not participate
            if fields[11] == "TRUE":
                voter_v20state = True
            
            if fields[12] == "TRUE":
                voter_v21town = True
            
            if fields[13] == "TRUE":
                voter_v21primary = True
            
            if fields[14] == "TRUE":
                voter_v22general = True
            
            if fields[15] == "TRUE":
                voter_v23town = True

            # create a new instance of Voter object with this record from CSV
            voter = Voter(
                last_name = fields[1],
                first_name = fields[2],
                RA_street_num = fields[3],
                RA_street_name = fields[4],
                RA_apt_num = fields[5],
                RA_zip = fields[6],
                date_of_birth = fields[7],
                date_of_res = fields[8],
                party_affiliation = fields[9],
                precinct_num = fields[10],
                
                # store the respecitive boolean value for resective election voting participation      
                v20state = voter_v20state,
                v21town = voter_v21town,
                v21primary = voter_v21primary,
                v22general = voter_v22general,
                v23town = voter_v23town,
                
                voter_score = int(fields[16]) 
            )
        
            voter.save() #commit the voter to the database
        
        except Exception as e:
            print(f"Something went wrong: {e}")
            print(f"line = {line}")
            print(f"fields = {fields}")