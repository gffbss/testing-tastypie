from django import http
from django.conf import settings
from django.conf.urls import url
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.fields import ToManyField, CharField, ToOneField
from tastypie.resources import ModelResource, Resource
from lecture.api.authorization import UserObjectsOnlyAuthorization
from lecture.models import Student, Class, StudentProject
from uploadbox.models import Media
from _ssl import SSLError

class MediaResource(ModelResource):
    class Meta:
        queryset = Media.objects.all()
        resource_name = "media"
        authorization = UserObjectsOnlyAuthorization()
        authentication = BasicAuthentication()
        always_return_data = True

#     def prepend_urls(self):
#         return [
#             url(r"^(?P<resource_name>%s)/upload_file/(?P<pk>\w[\w/-]*)/$" % self._meta.resource_name, self.wrap_view('upload_file'), name="api_upload_file"),
#         ]
#
#     def upload_file(self, request, **kwargs):
#         self.method_check(request, allowed=['post'])
#         self.is_authenticated(request)
#
#         try:
#             report = self._meta.queryset._clone().get(pk=kwargs['pk'])
#         except self._meta.object_class.DoesNotExist:
#             return http.HttpNotFound()
#
#         bundle = self.build_bundle(obj=report, request=request)
#
#         self.authorized_update_detail(None, bundle)
#
#         file = request.FILES.get('picture', None)
#         if not file:
#             return self.error_response(request, {"error": "No file called picture found"}, response_class=http.HttpBadRequest)
#
#
#         file = request.FILES['file']
#
#         done, tries = False, 0
#         while not done:
#             try:
#                 bundle.obj.original_file.save(file.name, picture)
#                 bundle.obj.save(update_fields=['file_photo'])
#                 done = True
#             except SSLError:
#                 pass
#
#             # Try at max, 10 times before quitting
#             tries += 1
#             if tries > 10:
#                 done = True
#
#         bundle = self.full_dehydrate(bundle)
#
#         return self.create_response(request, bundle, response_class=http.HttpAccepted)




class BareClassResource(ModelResource):
    class Meta:
        queryset = Class.objects.all()
        resource_name = "bare_class"

class BareStudentProjectResource(ModelResource):
    class Meta:
        queryset = StudentProject.objects.all()
        resource_name = "bare_student_project"

class StudentResource(ModelResource):
    klass = ToOneField(BareClassResource, 'klass', full=True)
    project = ToManyField(BareStudentProjectResource, 'projects', full=True)

    class Meta:
        queryset = Student.objects.all()
        resource_name = "student"
        authorization = Authorization()


class StudentProjectResource(ModelResource):
    student = ToOneField(StudentResource, 'student', full=True, null=True)

    class Meta:
        queryset = StudentProject.objects.all()
        resource_name = "project"
        authorization = Authorization()


class ClassResource(ModelResource):
    students = ToManyField(StudentResource, 'students', full=True, null=True)

    class Meta:
        allowed_methods = ['get', 'post']
        always_return_data = True
        queryset = Class.objects.all()
        resource_name = "class"
        authorization = Authorization()
        filtering = {
            'students': ALL_WITH_RELATIONS,
            'title': ['contains', 'icontains'],
            'start_date': ['gt',]
        }


######################
# Non-Model Resource #
######################

class Version(object):
    def __init__(self, identifier=None):
        self.identifier = identifier


class VersionResource(Resource):
    identifier = CharField(attribute='identifier')

    class Meta:
        resource_name = 'version'
        allowed_methods = ['get']
        object_class = Version
        include_resource_uri = False

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.identifier
        else:
            kwargs['pk'] = bundle_or_obj['identifier']

        return kwargs

    def get_object_list(self, bundle, **kwargs):
        return [Version(identifier=settings.VERSION)]

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle, **kwargs)


######################
# Media-Upload Resource #
######################


# class PictureVideoUploadResource(ModelResource):
#
#     def prepend_urls(self):
#         return [
#             url(r"^(?P<resource_name>%s)/upload_picture/(?P<pk>\w[\w/-]*)/$" % self._meta.resource_name, self.wrap_view('upload_picture'), name="api_upload_picture"),
#             url(r"^(?P<resource_name>%s)/upload_video/(?P<pk>\w[\w/-]*)/$" % self._meta.resource_name, self.wrap_view('upload_video'), name="api_upload_video"),
#         ]
#
#     def upload_picture(self, request, **kwargs):
#         self.method_check(request, allowed=['post'])
#         self.is_authenticated(request)
#
#         try:
#             report = self._meta.queryset._clone().get(pk=kwargs['pk'])
#         except self._meta.object_class.DoesNotExist:
#             return http.HttpNotFound()
#
#         bundle = self.build_bundle(obj=report, request=request)
#
#         self.authorized_update_detail(None, bundle)
#
#         picture = request.FILES.get('picture', None)
#         if not picture:
#             return self.error_response(request, {"error": "No file called picture found"}, response_class=http.HttpBadRequest)
#
#         picture = request.FILES['picture']
#
#         done, tries = False, 0
#         while not done:
#             try:
#                 bundle.obj.original_photo.save(picture.name, picture)
#                 bundle.obj.save(update_fields=['original_photo'])
#                 done = True
#             except SSLError:
#                 pass
#
#             # Try at max, 10 times before quitting
#             tries += 1
#             if tries > 10:
#                 done = True
#
#         bundle = self.full_dehydrate(bundle)
#
#         return self.create_response(request, bundle, response_class=http.HttpAccepted)
#
#     def upload_video(self, request, **kwargs):
#         self.method_check(request, allowed=['post'])
#         self.is_authenticated(request)
#
#         try:
#             report = self._meta.queryset._clone().get(pk=kwargs['pk'])
#         except self._meta.object_class.DoesNotExist:
#             return http.HttpNotFound()
#
#         bundle = self.build_bundle(obj=report, request=request)
#
#         self.authorized_update_detail(None, bundle)
#
#         video = request.FILES.get('video', None)
#         if not video:
#             return self.error_response(request, {"error": "No file called video found"}, response_class=http.HttpBadRequest)
#
#         video_thumbnail = request.FILES.get('video_thumbnail', None)
#         if not video_thumbnail:
#             return self.error_response(request, {"error": "No file called video_thumbnail found"}, response_class=http.HttpBadRequest)
#
#         done, tries = False, 0
#         while not done:
#             try:
#                 bundle.obj.video.save(video.name, video)
#                 bundle.obj.video_thumbnail.save(video_thumbnail.name, video_thumbnail)
#                 bundle.obj.save(update_fields=['video', 'video_thumbnail'])
#                 done = True
#             except SSLError:
#                 pass
#
#             # Try at max, 10 times before quitting
#             tries += 1
#             if tries > 10:
#                 done = True
#
#         bundle = self.full_dehydrate(bundle)
#         return self.create_response(request, bundle, response_class=http.HttpAccepted)
