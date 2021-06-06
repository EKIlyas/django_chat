from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from core.models import Message, Subject, Manager, Student


class SubjectView(LoginRequiredMixin, ListView):
    queryset = Subject.objects.all()
    template_name = 'core/subject_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        managers = Manager.objects.filter(user=self.request.user)
        students = Student.objects.filter(user=self.request.user)
        subjects_manager = queryset.filter(managers__in=managers)
        subjects_student = queryset.filter(students__in=students)
        queryset = subjects_manager.union(subjects_student)
        return queryset


class RoomView(LoginRequiredMixin, ListView):
    queryset = Message.objects.all()
    template_name = 'core/room.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(subject_id=self.kwargs.get('subject_id'))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {
            'subject_id': self.kwargs.get('subject_id')
        }
        context.update(kwargs)
        return super().get_context_data(**context)

    def dispatch(self, request, *args, **kwargs):
        manager_count = Manager.objects.filter(user=request.user, subjects__in=[self.kwargs.get('subject_id')]).count()
        student_count = Student.objects.filter(user=request.user, subjects__in=[self.kwargs.get('subject_id')]).count()
        if manager_count == 0 and student_count == 0:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


