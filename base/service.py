from logger.models import Log
from base.models import StateRequirements
from django.utils import timezone
import pandas as pd

class DashboardService():
    def __init__(self, request):
        self.request = request

    def get_dashboard_data(self):
        if not hasattr(self, 'log_objects'):
            self.log_objects = pd.DataFrame.from_records(
                Log.objects.filter(user=self.request.user).values('student', 'location', 'time_spent', 'hour_type')
            )
            print(self.log_objects)

        if not hasattr(self, 'state_requirements'):
            self.state_requirements = StateRequirements.objects.get(state=self.request.user.profile.state)

        dashboard_data = {}

        for student in self.request.user.students.all():
            core_hours_at_home = 0
            core_hours_away = 0
            elective_hours = 0

            # Filter logs for the current student
            student_logs = self.log_objects[self.log_objects['student'] == student.id]

            # Iterate over filtered logs
            for _, log in student_logs.iterrows():
                if log['hour_type'] == 'Core' and log['location'] == 'Home':
                    core_hours_at_home += log['time_spent']
                elif log['hour_type'] == 'Core' and log['location'] == 'Away':
                    core_hours_away += log['time_spent']
                elif log['hour_type'] == 'Elective':
                    elective_hours += log['time_spent']

            total_hours = core_hours_at_home + core_hours_away + elective_hours
            days_left = (self.state_requirements.year_end - timezone.now().date()).days

            # Avoid division by zero or negative days left
            if days_left > 0:
                average_hours_to_complete = (self.state_requirements.total_hours - total_hours) / days_left
            else:
                average_hours_to_complete = 0  # or None, depending on your business logic

            target_hours = self.state_requirements.total_hours

            dashboard_data[student] = {
                'core_hours_at_home': core_hours_at_home,
                'core_hours_away': core_hours_away,
                'elective_hours': elective_hours,
                'total_hours': total_hours,
                'target_hours': target_hours,
                'days_left': days_left,
                'average_hours_to_complete': round(average_hours_to_complete, 2) if average_hours_to_complete else 0
            }

        return dashboard_data

