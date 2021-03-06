from django.db import models
import uuid

class Section(models.Model):
    title = models.CharField(max_length=100)
    join_id = models.CharField(max_length=100, blank=True, null=True)
    time_table = models.TextField(blank=True, null=True)
    of_class = models.ForeignKey('classes.Class', blank=True, null=True, on_delete=models.SET_NULL, related_name='section_of_class')
    class_teacher = models.ForeignKey('teachers.Teacher', blank=True, null=True, on_delete=models.SET_NULL, related_name='section_class_teacher')
    accepting_req = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        # return self.title
        return str(self.title + " of class " + str(self.of_class))

    def save(self, *args, **kwargs):
        if not self.join_id:
            temp_join_id = str(uuid.uuid4())
            while Section.objects.filter(join_id=temp_join_id):
                temp_join_id = str(uuid.uuid4())
            self.join_id = temp_join_id
        super().save(*args, **kwargs)