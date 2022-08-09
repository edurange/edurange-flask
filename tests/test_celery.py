# from edurange_refactored.user.models import StudentGroups, User
# from edurange_refactored.tasks import CreateScenarioTask
#
# class TestCeleryTasks:
#     @app.task(bind=True)
#     def test_CreateScenarioTask(self, name, s_type, owner, group, g_id, s_id):
#
#     try:
#         product.order(self, name, "Ssh_Inception", owner, group, g_id, s_id)
#     except OperationalError as exc:
#         raise self.retry(exc=exc)
# #instructor creates, it goes to database, it's added to student accounts
# #
