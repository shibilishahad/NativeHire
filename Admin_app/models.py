from django.db import models

# class Admin(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
#     worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='Worker')
#     employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='Employer')
    

class TypeOfJobs(models.Model):
    # job_types = models.ForeignKey(Type,on_delete=models.CASCADE)
    type_of_jobs = models.CharField(max_length=20)

    def __str__(self):
        return self.type_of_jobs


