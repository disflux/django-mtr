# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PDFTemplate.length'
        db.add_column(u'pdfgen_pdftemplate', 'length',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Adding field 'PDFTemplate.width'
        db.add_column(u'pdfgen_pdftemplate', 'width',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)


        # Changing field 'PDFTemplate.file'
        db.alter_column(u'pdfgen_pdftemplate', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))

    def backwards(self, orm):
        # Deleting field 'PDFTemplate.length'
        db.delete_column(u'pdfgen_pdftemplate', 'length')

        # Deleting field 'PDFTemplate.width'
        db.delete_column(u'pdfgen_pdftemplate', 'width')


        # Changing field 'PDFTemplate.file'
        db.alter_column(u'pdfgen_pdftemplate', 'file', self.gf('django.db.models.fields.files.FileField')(default='none.pdf', max_length=100))

    models = {
        u'pdfgen.pdftemplate': {
            'Meta': {'object_name': 'PDFTemplate'},
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'template_field'", 'symmetrical': 'False', 'to': u"orm['pdfgen.TemplateField']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'width': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        u'pdfgen.templatefield': {
            'Meta': {'object_name': 'TemplateField'},
            'end_x': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'end_y': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'fill_color': ('django.db.models.fields.CharField', [], {'default': "'black'", 'max_length': '16', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_x': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'start_y': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'text_centered': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'text_size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['pdfgen']