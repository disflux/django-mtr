from haystack import indexes
from reports.models import Report

class ReportIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)
    part_number = indexes.NgramField(model_attr='part_number')
    created_at = indexes.DateTimeField(model_attr='created_at')
    
    def get_model(self):
        return Report