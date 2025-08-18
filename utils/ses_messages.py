class SesMessages:
    def get_status_topic(self) -> str:
        return "Task status changed"

    def get_status_message(
        self,
        task_id: str,
        project_id: str,
        new_status: str,
    ) -> str:
        message = (
            f"Status of task: {task_id} "
            f"in project: {project_id} "
            f"was changed to {new_status}"
        )
        return message


ses_messages = SesMessages()
