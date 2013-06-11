from haystack import indexes
from reports.models import Report

class ReportIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created_at = indexes.DateTimeField(model_attr='created_at')
    
    def get_model(self):
        return Report