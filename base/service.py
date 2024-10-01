from logger.models import Log
from base.models import StateRequirements
from django.utils import timezone

class DashboardService():
    def __init__(self, request):
        self.request = request

    def get_dashboard_data(self):
        if not hasattr(self, 'log_objects'):
            self.log_objects = Log.objects.filter(user=self.request.user)

        if not hasattr(self, 'state_requirements'):
            self.state_requirements = StateRequirements.objects.get(state=self.request.user.profile.state)

        dashboard_data = {}

        for student in self.request.user.students.all():
            core_hours_at_home = 0
            core_hours_away = 0
            elective_hours = 0
            
            for log in self.log_objects.filter(student=student):
                if log.hour_type == 'Core' and log.location == 'Home':
                    core_hours_at_home += log.time_spent
                elif log.hour_type == 'Core' and log.location == 'Away':
                    core_hours_away += log.time_spent
                elif log.hour_type == 'Elective':
                    elective_hours += log.time_spent

            total_hours = core_hours_at_home + core_hours_away + elective_hours
            days_left = (timezone.now().date() - self.state_requirements.year_end).days
            average_hours_to_complete = (self.state_requirements.total_hours - total_hours) / days_left
            target_hours = self.state_requirements.total_hours

            dashboard_data[student] = {
                'core_hours_at_home': core_hours_at_home,
                'core_hours_away': core_hours_away,
                'elective_hours': elective_hours,
                'total_hours': total_hours,
                'target_hours': target_hours,
                'days_left': days_left*-1,
                'average_hours_to_complete': round(average_hours_to_complete, 2)*-1
            }

        return dashboard_data
