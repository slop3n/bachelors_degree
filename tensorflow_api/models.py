from django.db import models

# Create your models here.
class ScannedItem(models.Model):
	label = models.CharField(max_length=200)
	probability = models.DecimalField(default=0, decimal_places=5, max_digits=10)
	scanned_on = models.DateTimeField()

	def __str__(self):
		return 'Item: ' + self.label + ', probability:' + str(self.probability) + ', scanned on: ' + str(self.scanned_on)