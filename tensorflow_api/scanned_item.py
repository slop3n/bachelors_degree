import django_tables2 as tables
from .models import ScannedItem

class ScannedItemsTable(tables.Table):
	class Meta:
		model = ScannedItem
		template = 'django_tables2/bootstrap.html'