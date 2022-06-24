from rest_framework.decorators import api_view
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from serializers import UploadSerializer
import librosa
from django.conf import settings
import random
import pickle
from pydub import AudioSegment
import os
import pandas as pd

model_path = os.path.join(settings.BASE_DIR ,'nootebooks/best_svm_model.sav')
scaller_path = os.path.join(settings.BASE_DIR ,'nootebooks/scaller.sav')
model = pickle.load(open(model_path, 'rb'))
scaller = pickle.load(open(scaller_path, 'rb'))
genre = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz','metal', 'pop', 'reggae', 'rock']
class upload_viewset(ViewSet):
    serializer_class = UploadSerializer
    parser_classes = [MultiPartParser, ]

    def create(self, request, *args, **kwargs):

        file_uploaded = request.FILES.get('file_name')
        file_uploaded_name = file_uploaded.name
        temp = os.path.join(settings.BASE_DIR, 'temp', file_uploaded_name)
        path = f"{temp.split('.')[0]}_{random.randint(0, 1000)}.wav"
        if temp.split('.')[-1] == 'mp3':
            audSeg = AudioSegment.from_mp3(file_uploaded)
            audSeg.export(path, 'wav')
            y, sr = librosa.load(path, duration=3)
        elif temp.split('.')[-1] == 'm4a':
            audSeg = AudioSegment.from_file(file_uploaded)
            audSeg.export(path, 'wav')
            y, sr = librosa.load(path, duration=3)
        elif temp.split('.')[-1] == 'wav':

            y, sr = librosa.load(file_uploaded, duration=3)

        audio_file, _ = librosa.effects.trim(y)
        y_harm, y_perc = librosa.effects.hpss(audio_file)
        tempo, _ = librosa.beat.beat_track(y, sr = sr)

        data = pd.DataFrame(index = [1])
        data["chroma_stft_mean"] = librosa.feature.chroma_stft(audio_file, sr).mean()
        data["chroma_stft_var"] = librosa.feature.chroma_stft(audio_file, sr).var()
        data["rms_mean"] = librosa.feature.rms(audio_file, sr).mean()
        data["rms_var"] = librosa.feature.rms(audio_file, sr).var()
        data["spectral_centroid_mean"] = librosa.feature.spectral_centroid(audio_file, sr).mean()
        data["spectral_centroid_var"] = librosa.feature.spectral_centroid(audio_file, sr).var()
        data["spectral_bandwidth_mean"] = librosa.feature.spectral_bandwidth(audio_file, sr).mean()
        data["spectral_bandwidth_var"] = librosa.feature.spectral_bandwidth(audio_file, sr).var()
        data["rolloff_mean"] = librosa.feature.spectral_rolloff(audio_file, sr)[0].mean()
        data["rolloff_var"] = librosa.feature.spectral_rolloff(audio_file, sr)[0].var()
        data["zero_crossing_rate_mean"] = librosa.feature.zero_crossing_rate(audio_file, pad=False).mean()
        data["zero_crossing_rate_var"] = librosa.feature.zero_crossing_rate(audio_file, pad=False).var()
        data["harmony_mean"] = y_harm.mean()
        data["harmony_var"] = y_harm.var()
        data["perceptr_mean"] = y_perc.mean()
        data["perceptr_var"] = y_perc.var()
        data["tempo"] = tempo
        for i in range(0, 20):
            data[f"mfcc{i+1}_mean"] = librosa.feature.mfcc(y = audio_file, sr = sr, n_mfcc =20)[i].mean()
            data[f"mfcc{i+1}_var"] = librosa.feature.mfcc(y = audio_file, sr = sr, n_mfcc = 20)[i].var()

        X = scaller.transform(data)
        result = genre[model.predict(X)[0]]
        try:
            os.remove(path)
        except:
            pass

        return Response(result)