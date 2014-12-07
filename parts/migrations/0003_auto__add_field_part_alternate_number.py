# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Part.alternate_number'
        db.add_column(u'parts_part', 'alternate_number',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Part.alternate_number'
        db.delete_column(u'parts_part', 'alternate_number')


    models = {
        u'actstream.action': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'Action'},
            'action_object_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'action_object'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'action_object_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'actor_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'to': u"orm['contenttypes.ContentType']"}),
            'actor_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'target_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'target'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'target_object_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'verb': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'parts.part': {
            'Meta': {'ordering': "('part_number',)", 'object_name': 'Part'},
            'alternate_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'box_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'product_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'}),
            'specification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['specifications.Specification']", 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'specifications.category': {
            'Meta': {'object_name': 'Category'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'overview': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'specifications.specification': {
            'Meta': {'ordering': "('spec',)", 'unique_together': "(('category', 'spec'),)", 'object_name': 'Specification'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['specifications.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_information': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'spec': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        }
    }

    complete_apps = ['parts']