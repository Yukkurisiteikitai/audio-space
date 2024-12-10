from django.db import models

# Create your models here.


class Post(models.Model):
    #image = 2024.12.10.15:27:42.35532345323422353  .
    timestamp = models.CharField('timeStamp',
                                max_length=40)

    rec_start_time = models.CharField('recStartTime',
                                      max_length=40,
                                      blank=True)

    rec_stop_time = models.CharField('recStopTime',
                                    max_length=40,
                                    blank=True)

    def __str__(self):
        return self.name