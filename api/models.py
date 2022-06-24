from django.db import models
import librosa
# Create your models here.

# class Audio(models.Model):
#     file_name = models.FileField(upload_to='image_file')
#     def processing(self):
#         y, sr = librosa.load(self.file_name, duration=3.0)
#         print(librosa.feature.mfcc(y=y, sr=sr, n_mfcc = 1).mean())

#     def save(self, *args, **kwargs):
#         self.processing()
#         #super().save(*args, **kwargs)
        
