# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table(u'orders_customer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
        ))
        db.send_create_signal(u'orders', ['Customer'])

        # Adding model 'Order'
        db.create_table(u'orders_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Customer'])),
            ('customer_po', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('order_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'orders', ['Order'])

        # Adding M2M table for field line_items on 'Order'
        m2m_table_name = db.shorten_name(u'orders_order_line_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm[u'orders.order'], null=False)),
            ('orderlineitem', models.ForeignKey(orm[u'orders.orderlineitem'], null=False))
        ))
        db.create_unique(m2m_table_name, ['order_id', 'orderlineitem_id'])

        # Adding M2M table for field documents on 'Order'
        m2m_table_name = db.shorten_name(u'orders_order_documents')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('order', models.ForeignKey(orm[u'orders.order'], null=False)),
            ('document', models.ForeignKey(orm[u'documents.document'], null=False))
        ))
        db.create_unique(m2m_table_name, ['order_id', 'document_id'])

        # Adding model 'OrderLineItem'
        db.create_table(u'orders_orderlineitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Order'])),
            ('line_number', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reports.Report'], null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
        ))
        db.send_create_signal(u'orders', ['OrderLineItem'])


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table(u'orders_customer')

        # Deleting model 'Order'
        db.delete_table(u'orders_order')

        # Removing M2M table for field line_items on 'Order'
        db.delete_table(db.shorten_name(u'orders_order_line_items'))

        # Removing M2M table for field documents on 'Order'
        db.delete_table(db.shorten_name(u'orders_order_documents'))

        # Deleting model 'OrderLineItem'
        db.delete_table(u'orders_orderlineitem')


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
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'documents.document': {
            'Meta': {'object_name': 'Document'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'document_hash': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pages': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.DocumentType']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'unique': 'True', 'max_length': '32', 'blank': 'True'})
        },
        u'documents.documenttype': {
            'Meta': {'ordering': "('name',)", 'object_name': 'DocumentType'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'orders.customer': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Customer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'orders.order': {
            'Meta': {'object_name': 'Order'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Customer']"}),
            'customer_po': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'documents': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'order_documents'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['documents.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'line_items': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'order_line_items'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['orders.OrderLineItem']"}),
            'order_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'})
        },
        u'orders.orderlineitem': {
            'Meta': {'ordering': "('line_number',)", 'object_name': 'OrderLineItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_number': ('django.db.models.fields.IntegerField', [], {'max_length': '4'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['orders.Order']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Report']", 'null': 'True', 'blank': 'True'})
        },
        u'parts.part': {
            'Meta': {'ordering': "('part_number',)", 'object_name': 'Part'},
            'box_quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'part_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'specification': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['specifications.Specification']", 'null': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'reports.report': {
            'Meta': {'ordering': "('lot_number',)", 'object_name': 'Report'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'documents': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['documents.Document']", 'null': 'True', 'through': u"orm['reports.ReportDocument']", 'blank': 'True'}),
            'heat_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked_reports': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'report_links'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['reports.Report']"}),
            'lot_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'mfg_lot_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'origin_po': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'origin_wo': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'part_number': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parts.Part']"}),
            'raw_material': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'receiving_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 19, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'vendor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vendors.Vendor']"}),
            'vendor_lot_number': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'reports.reportdocument': {
            'Meta': {'object_name': 'ReportDocument'},
            'attachment_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['documents.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_cert': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'primary_document': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['reports.Report']"})
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
        },
        u'vendors.vendor': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Vendor'},
            'city': ('django.db.models.fields.TextField', [], {}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'state': ('django.db.models.fields.TextField', [], {}),
            'street': ('django.db.models.fields.TextField', [], {}),
            'zip': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['orders']