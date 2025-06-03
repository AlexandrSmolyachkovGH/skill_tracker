import pytest

from skills.models import (
    Skill,
    SkillCategory,
)


@pytest.mark.django_db
def test_skill_model() -> None:
    skill_model = Skill.objects.create(
        name='TestSkill',
        category=SkillCategory.PROGRAMMING,
    )
    assert Skill.objects.filter(
        name='TestSkill',
        category=SkillCategory.PROGRAMMING,
    ).exists()
    assert skill_model.name == 'TestSkill'
    assert skill_model.category == 'programming'
    assert skill_model.get_category_display() == 'Программирование'
    skill_model.delete()
    assert not Skill.objects.filter(
        name='TestSkill',
        category=SkillCategory.PROGRAMMING,
    ).exists()


def test_skill_model_str_repr() -> None:
    sm = Skill(
        name='TestSkill',
    )
    assert str(sm) == "Skill: TestSkill, category: unspecified"
