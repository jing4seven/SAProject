"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import json
from StringIO import StringIO

from django.test import TestCase

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from api.secure.models import user

from .models import project, project_status
from .serializers import project_serializer, project_status_serializer

class ModelTest(TestCase):
    test_user = None
    
    def setUp(self):   
        self.test_user = user.objects.create(full_name="test account", email_address="test@test.com",
                                                 username="testaccount", password="testpassword", 
                                                 first_name="test", last_name="test", last_edited_by="szhou")
        return
    
    def tearDown(self):        
        return
    
    def test_project_model(self):
        project.objects.create(name="TST", alias="test project", owner_id=self.test_user.pk,
                                              description="test", is_private=False, last_edited_by="szhou")
        try:
            test_project = project.objects.get(name="TST")
        except project.DoesNotExist:
            test_project = None
        self.assertIsNotNone(test_project, msg="Failed to create and get the project")
        test_project = project.objects.get(name="TST")
        test_project.alias = "test project 1"
        test_project.save()
        test_project = project.objects.get(name="TST")
        self.assertEqual(test_project.alias, "test project 1", msg="Failed to create the project!")
        test_project.delete()
        try:
            test_project = project.objects.get(name="TST")
        except project.DoesNotExist:
            test_project = None
        self.assertIsNone(test_project, msg="Failed to delete the project")
        return
    
    def test_project_status_model(self):
        project.objects.create(name="TST", alias="test project", owner=self.test_user,
                                              description="test", is_private=False, last_edited_by="szhou")
        try:
            test_project = project.objects.get(name="TST")
        except project.DoesNotExist:
            test_project = None
        self.assertIsNotNone(test_project, msg="Failed to create and get the project")
        
        project_status.objects.create(name="open", project=test_project, is_current=True, description="test")
        try:
            test_project_status = project_status.objects.get(project_id=test_project.id)
        except project_status.DoesNotExist:
            test_project_status = None
        self.assertIsNotNone(test_project_status, msg="Failed to create project status")
        
        test_project_status.name = "Close"
        test_project_status.save()
        try:
            test_project_status = project_status.objects.get(project_id=test_project.id)
        except project_status.DoesNotExist:
            test_project_status = None
        self.assertEqual(test_project_status.name, "Close", msg="Failed update the project status")
        
        test_project_status.delete()
        try:
            test_project_status = project_status.objects.get(project_id=test_project.id)
        except project_status.DoesNotExist:
            test_project_status = None
        self.assertIsNone(test_project_status, msg="Failed to delete the project status")
        
        
class SerializerTest(TestCase):
    
    def setUp(self):
        self.test_user = user.objects.create(full_name="test account", email_address="test@test.com",
                                                 username="testaccount", password="testpassword", 
                                                 first_name="test", last_name="test", last_edited_by="szhou")
        self.test_project = project.objects.create(name="TST", alias="test project", owner_id=self.test_user.pk,
                                              description="test", is_private=False, last_edited_by="szhou")
        self.test_project_status = project_status.objects.create(name="Open", project_id=self.test_project.pk, 
                                                                 is_current=False, description="test")
        return
            
    def test_project_serializer(self):
        #test_user_serializer = user_serializer(self.test_user)
        test_serializer = project_serializer(self.test_project)
        test_json_data = JSONRenderer().render(test_serializer.data)
        test_json = json.loads(test_json_data)
        
        self.assertEqual(test_json['name'], 'TST', msg="Failed to parse")
        
        test_input_json_data = '{"name": "TST1", "alias": "test project1", "owner_name": "testaccount", "description": "test", "is_private": "false", "last_edited_by": "szhou"}'
        test_input_stream = StringIO(test_input_json_data)
        test_parse_data = JSONParser().parse(test_input_stream)        

        test_serializer_input = project_serializer(data=test_parse_data)
        if test_serializer_input.is_valid():
            test_serializer_input.save()
        self.assertEqual(project.objects.count(), 2, msg="Failed to insert a project")
        
        try:
            test_created_project = project.objects.get(name="TST1")
        except project.DoesNotExist:
            test_created_project = None
        self.assertIsNotNone(test_created_project, msg="Failed to insert to a project")
        return 
        
    def test_project_status_serializer(self):
        test_serializer = project_status_serializer(self.test_project_status)
        test_json_data = JSONRenderer().render(test_serializer.data)
        test_json = json.loads(test_json_data)
        
        self.assertEqual(test_json['name'], 'Open', msg="Failed to parse a Project Status")
        
        test_input_json_data = '{"name": "Close", "project_id": "'+ str(self.test_project.pk) +'", "is_current": "false", "description": "test"}'
        test_parse_data = JSONParser().parse(StringIO(test_input_json_data))
        
        test_serializer_input = project_status_serializer(data=test_parse_data)
        if test_serializer_input.is_valid():
            test_serializer_input.save()
        
        self.assertEqual(project_status.objects.count(), 2, msg="Failed to insert a project_status")
        
        try:
            test_created_project_status = project_status.objects.get(name="Close")
        except project_status.DoesNotExist:
            test_created_project_status = None
            
        self.assertIsNotNone(test_created_project_status, msg="Falied to instert a project_status")
        return
            
        
