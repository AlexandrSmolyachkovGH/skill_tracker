from uuid import UUID

from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound

from skills.models import Skill
from users.models import (
    User,
    UserSkill,
)


class UserSkillRepo:
    def get_user_skill(
        self,
        user_id: UUID,
        skill_id: UUID,
    ) -> UserSkill:
        user_skill = UserSkill.objects.filter(
            user_id=user_id,
            skill_id=skill_id,
        ).first()
        if not user_skill:
            raise NotFound("UserSkill record not found.")
        return user_skill

    def get_user_skills(
        self,
        user_id: UUID,
    ) -> QuerySet[UserSkill]:
        return UserSkill.objects.filter(
            user_id=user_id,
        )

    def create_user_skill(
        self,
        user_id: UUID,
        skill: Skill,
        user_skill_data: dict,
    ) -> UserSkill:
        user_skill = UserSkill.objects.create(
            skill=skill,
            user_id=user_id,
            **user_skill_data,
        )
        return user_skill

    def delete_user_skill(
        self,
        skill_id: UUID,
        user_id: UUID,
    ) -> None:
        UserSkill.objects.filter(
            skill_id=skill_id,
            user_id=user_id,
        ).delete()

    def update_user_skill(
        self,
        user_id: UUID,
        skill_id: UUID,
        user_skill_data: dict,
    ) -> UserSkill:
        user_skill = get_object_or_404(
            UserSkill,
            skill_id=skill_id,
            user_id=user_id,
        )
        if user_skill_data:
            for key, value in user_skill_data.items():
                setattr(user_skill, key, value)
            user_skill.save(
                update_fields=list(user_skill_data.keys()),
            )
        return user_skill


user_skill_repo = UserSkillRepo()
