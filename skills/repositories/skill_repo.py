from uuid import UUID

from django.shortcuts import get_object_or_404
from django.utils import timezone

from skills.models import Skill


class SkillRepo:
    def create_skill(
        self,
        skill_data: dict,
    ) -> Skill:
        return Skill.objects.create(**skill_data)

    def delete_skill(
        self,
        skill_id: UUID,
    ) -> Skill:
        skill = get_object_or_404(Skill, id=skill_id)
        skill.deleted_at = timezone.now()
        skill.save(
            update_fields=["deleted_at"],
        )
        return skill

    def update_skill(
        self,
        skill_id: UUID,
        skill_data: dict,
    ) -> Skill:
        skill = get_object_or_404(Skill, id=skill_id)
        for key, value in skill_data.items():
            setattr(skill, key, value)
        skill.save(
            update_fields=list(skill_data.keys()),
        )
        return skill


skill_repo = SkillRepo()
