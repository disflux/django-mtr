# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TemplateField'
        db.create_table(u'pdfgen_templatefield', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('start_x', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('start_y', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('end_x', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('end_y', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('fill_color', self.gf('django.db.models.fields.CharField')(default='black', max_length=16, null=True)),
            ('text_size', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('text_centered', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
        ))
        db.send_create_signal(u'pdfgen', ['TemplateField'])

        # Adding model 'PDFTemplate'
        db.create_table(u'pdfgen_pdftemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'pdfgen', ['PDFTemplate'])

        # Adding M2M table for field fields on 'PDFTemplate'
        m2m_table_name = db.shorten_name(u'pdfgen_pdftemplate_fields')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pdftemplate', models.ForeignKey(orm[u'pdfgen.pdftemplate'], null=False)),
            ('templatefield', models.ForeignKey(orm[u'pdfgen.templatefield'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pdftemplate_id', 'templatefield_id'])


    def backwards(self, orm):
        # Deleting model 'TemplateField'
        db.delete_table(u'pdfgen_templatefield')

        # Deleting model 'PDFTemplate'
        db.delete_table(u'pdfgen_pdftemplate')

        # Removing M2M table for field fields on 'PDFTemplate'
        db.delete_table(db.shorten_name(u'pdfgen_pdftemplate_fields'))


    models = {
        u'pdfgen.pdftemplate': {
            'Meta': {'object_name': 'PDFTemplate'},
            'fields': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'template_field'", 'symmetrical': 'False', 'to': u"orm['pdfgen.TemplateField']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
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