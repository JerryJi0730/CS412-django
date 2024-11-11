from django.db import models
import csv
from django.conf import settings
class Voter(models.Model):
    # Basic voter information
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    street_number = models.IntegerField()
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10000, blank=True, null=True)
    zip_code = models.IntegerField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.IntegerField()

    # Participation in elections
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)

    # Voter score
    voter_score = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number} -score: {self.voter_score}"

def load_data():
    filename = '/Users/hangji/Desktop/newton_voters.csv'
    f = open(filename)
    headers = f.readline() # discard the first line containing headers # discard headers
    Voter.objects.all().delete()
    for row in f:
        try:
            fields = row.split(',')
            # Create Voter object for each row in the CSV
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9],
                precinct_number=fields[10],
                v20state=fields[11] == "TRUE",
                v21town=fields[12] == "TRUE",
                v21primary=fields[13] == "TRUE",
                v22general=fields[14] == "TRUE",
                v23town=fields[15] == "TRUE",
                voter_score=int(fields[16].strip()),
            )
            print(f'Created voter: {voter}')
            voter.save()
        except:
            print(f"Exception occurred: {fields}.")
    print("Done.")

