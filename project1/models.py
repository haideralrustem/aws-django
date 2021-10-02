from django.db import models

# Create your models here.

class TabularDataSets(models.Model):

    dataset_name = models.TextField(unique=True)
    
    def __str__(self):
        text = '{}'.format(self.dataset_name)
        return text

    def save(self, *args, **kwargs):
        super(TabularDataSets, self).save(*args, **kwargs)



class MyCsvRow(models.Model):

    parent_dataset_table =  models.ForeignKey(TabularDataSets, on_delete=models.CASCADE)
    row_values = models.TextField()   
    row_variables =  models.TextField() 

    def __str__(self):
        text = 'table: {} -> {} '.format(self.parent_dataset_table, self.row_values)
        return text

    def save(self, *args, **kwargs):
        super(MyCsvRow, self).save(*args, **kwargs)