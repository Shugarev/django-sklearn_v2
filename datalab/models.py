import os

from django.db import models
from django.forms import ModelForm
from django_mysql.models import JSONField

from sklearn_django.settings import BASE_DIR


class ExtraModel(models.Model):
    def is_deletable(self):
        # get all the related object
        for rel in self._meta.get_fields():
            try:
                # check if there is a relationship with at least one related object
                related = rel.related_model.objects.filter(**{rel.field.name: self})
                if related.exists():
                    # if there is return a Tuple of flag = False the related_model object
                    error_text = 'This {} has related to: {} '.format(str(self), str(related[0]))
                    raise IOError(error_text)
            except AttributeError:  # an attribute error for field occurs when checking for AutoField
                pass  # just pass as we dont need to check for AutoField

        return True, None

    class Meta:
        abstract = True


class DataSet(ExtraModel):
    file = models.FileField(upload_to="datasets/")
    upload_date = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        is_deletable, related = self.is_deletable()
        if is_deletable:
            self.file.delete()
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.file.name


# FileUpload form class.
class UploadDataSet(ModelForm):
    class Meta:
        model = DataSet
        fields = ('file',)


class Algorithm(models.Model):
    algorithm_name = models.CharField(max_length=30, blank=False)
    default_algorithm_params = JSONField()
    # для подбора лучших параметров для модели
    algorithm_params_range = JSONField()


class Profile(ExtraModel):
    teach = models.ForeignKey(DataSet, on_delete=models.PROTECT)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    feature_importance = models.CharField(max_length=100, blank=False)
    profile_name = models.CharField(max_length=100, blank=False)
    profile_params = JSONField()
    factors = JSONField()

    def get_drop_columns(self):
        drop_columns = []
        for k, v in self.factors.items():
            if v == 0 or k == 'status':
                drop_columns.append(k)
        return drop_columns

    def get_used_factor_list(self):
        return sorted([k for k, v in self.factors.items() if v == 1 and k != 'status'])

    def get_profile_params(self):
        return self.profile_params

    def delete(self, *args, **kwargs):
        is_deletable, related = self.is_deletable()
        if is_deletable:
            profile_path = "{}/media/{}".format(BASE_DIR, self.profile_name)
            feature_path = "{}/media/{}".format(BASE_DIR, self.feature_importance)
            super().delete(*args, **kwargs)
            if os.path.isfile(profile_path):
                os.remove(profile_path)
            if os.path.isfile(feature_path):
                os.remove(feature_path)

    def __str__(self):
        return ' Model: ' + self.profile_name


class Experiment(ExtraModel):
    test = models.ForeignKey(DataSet, on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    created_date = models.DateTimeField(auto_now_add=True)
    experiment_name = models.CharField(max_length=100, blank=False)
    analyzer_name = models.CharField(max_length=100, blank=False)

    def delete(self, *args, **kwargs):
        is_deletable, related = self.is_deletable()
        if is_deletable:
            experiment_path = "{}/media/{}".format(BASE_DIR, self.experiment_name)
            analyzer_path = "{}/media/{}".format(BASE_DIR, self.analyzer_name)
            super().delete(*args, **kwargs)
            if os.path.isfile(experiment_path):
                os.remove(experiment_path)
            if os.path.isfile(analyzer_path):
                os.remove(analyzer_path)

    def __str__(self):
        return 'Experiment: ' + self.experiment_name
