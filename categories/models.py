from django.db import models




class Category(models.Model):

	cName = models.CharField(max_length=200)

	def __str__(self):
		return str(self.id) + ': ' + self.cName



class subCategory (models.Model):
	PCategory =  models.ForeignKey(Category, on_delete=models.CASCADE)
	scName = models.CharField(max_length=200)
	
	def __str__(self):
		return 'self:'+ str(self.id)+ ';' + 'Parent:' + str(self.PCategory) + ';' + self.scName
		

		