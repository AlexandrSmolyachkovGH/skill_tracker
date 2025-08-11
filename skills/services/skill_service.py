from uuid import UUID

from django.db import transaction
from django.db.models.query import QuerySet

from skills.models import Skill
from skills.repositories.skill_repo import (
    SkillRepo,
    skill_repo,
)
from skills.repositories.user_skill_repo import (
    UserSkillRepo,
    user_skill_repo,
)
from users.models import UserSkill


class SkillService:
    def __init__(
        self,
    ) -> None:
        self.skill_repo: SkillRepo = skill_repo
        self.user_skill_repo: UserSkillRepo = user_skill_repo
        self.skill_upd_fields: tuple[str, ...] = ("name", "category")
        self.user_skill_upd_fields: tuple[str, ...] = ("level", "xp")

    def parse_skill_and_user_skill_data(self, data: dict) -> tuple:
        skill_data = {
            k: v for k, v in data.items() if k in self.skill_upd_fields
        }

        user_skill_data = {
            k: v for k, v in data.items() if k in self.user_skill_upd_fields
        }
        return skill_data, user_skill_data

    def get_user_skill(
        self,
        user_id: UUID,
        skill_id: UUID,
    ) -> UserSkill:
        """
        Retrieve UserSkull record
        """
        user_skill = self.user_skill_repo.get_user_skill(
            user_id=user_id,
            skill_id=skill_id,
        )
        return user_skill

    def get_user_skills(
        self,
        user_id: UUID,
    ) -> QuerySet[UserSkill]:
        """
        Get multiple UserSkill records
        """
        return self.user_skill_repo.get_user_skills(
            user_id=user_id,
        )

    @transaction.atomic
    def create_skill_and_user_skill(
        self,
        user_id: UUID,
        data: dict,
    ) -> UserSkill:
        """
        Create Skill and UserSkill records
        """
        skill_data, user_skill_data = self.parse_skill_and_user_skill_data(
            data=data,
        )
        skill = self.skill_repo.create_skill(
            skill_data=skill_data,
        )
        user_skill = self.user_skill_repo.create_user_skill(
            user_id=user_id,
            skill=skill,
            user_skill_data=user_skill_data,
        )
        return user_skill

    @transaction.atomic
    def delete_skill_and_user_skill(
        self,
        user_id: UUID,
        skill_id: UUID,
    ) -> Skill:
        """
        Delete Skill and UserSkill records
        """
        deleted_skill = self.skill_repo.delete_skill(
            skill_id=skill_id,
        )
        self.user_skill_repo.delete_user_skill(
            skill_id=skill_id,
            user_id=user_id,
        )
        return deleted_skill

    @transaction.atomic
    def update_skill_and_user_skill(
        self,
        user_id: UUID,
        skill_id: UUID,
        data: dict,
    ) -> UserSkill:
        """
        Update Skill and UserSkill records
        """
        skill_data, user_skill_data = self.parse_skill_and_user_skill_data(
            data=data,
        )
        if skill_data:
            self.skill_repo.update_skill(
                skill_id=skill_id,
                skill_data=skill_data,
            )
        if user_skill_data:
            updated_record = self.user_skill_repo.update_user_skill(
                user_id=user_id,
                skill_id=skill_id,
                user_skill_data=user_skill_data,
            )
        else:
            updated_record = self.user_skill_repo.get_user_skill(
                user_id=user_id,
                skill_id=skill_id,
            )
        return updated_record


skill_service = SkillService()
